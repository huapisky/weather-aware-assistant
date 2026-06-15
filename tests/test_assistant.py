"""Automated tests (NFR-4, AC-1 through AC-4).

Weather API calls are mocked so tests run offline and deterministically.
Run with:  pytest -v
"""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import calendar_service
import weather_service
from advice_engine import generate_advice


# ---------- Calendar tests (AC-1) ----------

def test_load_valid_calendar(tmp_path):
    """AC-1: a valid calendar file loads and returns all events."""
    cal = tmp_path / "calendar.json"
    cal.write_text(json.dumps([
        {"title": "B", "start": "2026-06-15T14:00", "end": "2026-06-15T15:00", "location": "Houston"},
        {"title": "A", "start": "2026-06-14T09:00", "end": "2026-06-14T10:00", "location": "Austin"},
    ]))
    events = calendar_service.load_events(cal)
    assert len(events) == 2
    assert events[0]["title"] == "A"  # sorted by start time


def test_missing_calendar_raises():
    with pytest.raises(calendar_service.CalendarError):
        calendar_service.load_events("does_not_exist.json")


def test_invalid_schema_raises(tmp_path):
    cal = tmp_path / "calendar.json"
    cal.write_text(json.dumps([{"title": "No dates"}]))
    with pytest.raises(calendar_service.CalendarError):
        calendar_service.load_events(cal)


# ---------- Advice engine tests (AC-2) ----------

def test_rain_advice():
    """AC-2: rain forecast produces umbrella recommendation."""
    tips = generate_advice({"condition": "Rain", "temp_f": 75, "precip_prob": 80})
    assert any("umbrella" in t.lower() for t in tips)


def test_heat_advice():
    tips = generate_advice({"condition": "Clear", "temp_f": 98, "precip_prob": 0})
    assert any("water" in t.lower() for t in tips)


def test_severe_weather_advice():
    tips = generate_advice({"condition": "Thunderstorm", "temp_f": 70, "precip_prob": 90})
    assert any("early" in t.lower() for t in tips)


def test_clear_weather_advice():
    tips = generate_advice({"condition": "Clear", "temp_f": 72, "precip_prob": 5})
    assert tips == ["Conditions look good. No special preparation needed."]


# ---------- Weather service tests (AC-3) ----------

def test_api_failure_raises_weather_error():
    """AC-3: API failure surfaces as a catchable, meaningful error."""
    import requests
    from datetime import datetime
    with patch("weather_service.requests.get", side_effect=requests.ConnectionError("down")):
        with pytest.raises(weather_service.WeatherError):
            weather_service.get_forecast("Houston", datetime(2026, 6, 15, 14))


def test_unknown_location_raises():
    class FakeResp:
        def raise_for_status(self): pass
        def json(self): return {"results": None}
    with patch("weather_service.requests.get", return_value=FakeResp()):
        with pytest.raises(weather_service.WeatherError, match="not found"):
            weather_service.geocode("Atlantis")


def test_weather_code_translation():
    assert weather_service.describe_code(95) == "Thunderstorm"
    assert weather_service.describe_code(61) == "Rain"
    assert weather_service.describe_code(0) == "Clear"


# ---------- Coverage additions: happy paths and remaining rules ----------

def test_get_forecast_happy_path():
    """Full pipeline with mocked API: geocode then hourly forecast parse."""
    from datetime import datetime

    class GeoResp:
        def raise_for_status(self): pass
        def json(self):
            return {"results": [{"latitude": 29.76, "longitude": -95.36}]}

    class ForecastResp:
        def raise_for_status(self): pass
        def json(self):
            return {"hourly": {
                "time": ["2026-06-15T13:00", "2026-06-15T14:00"],
                "temperature_2m": [88.0, 91.5],
                "precipitation_probability": [10, 65],
                "weather_code": [1, 61],
            }}

    with patch("weather_service.requests.get", side_effect=[GeoResp(), ForecastResp()]):
        fc = weather_service.get_forecast("Houston", datetime(2026, 6, 15, 14))
    assert fc["condition"] == "Rain"
    assert fc["temp_f"] == 91.5
    assert fc["precip_prob"] == 65


def test_forecast_out_of_range_raises():
    """Event beyond the 16-day forecast window raises a clear error."""
    from datetime import datetime

    class GeoResp:
        def raise_for_status(self): pass
        def json(self):
            return {"results": [{"latitude": 29.76, "longitude": -95.36}]}

    class ForecastResp:
        def raise_for_status(self): pass
        def json(self):
            return {"hourly": {"time": ["2026-06-15T13:00"],
                               "temperature_2m": [88.0],
                               "precipitation_probability": [10],
                               "weather_code": [1]}}

    with patch("weather_service.requests.get", side_effect=[GeoResp(), ForecastResp()]):
        with pytest.raises(weather_service.WeatherError, match="No forecast"):
            weather_service.get_forecast("Houston", datetime(2026, 12, 25, 14))


def test_fog_advice():
    tips = generate_advice({"condition": "Fog", "temp_f": 60, "precip_prob": 10})
    assert any("visibility" in t.lower() for t in tips)


def test_cold_advice():
    tips = generate_advice({"condition": "Clear", "temp_f": 35, "precip_prob": 0})
    assert any("jacket" in t.lower() for t in tips)


def test_format_event():
    events = calendar_service.load_events.__module__  # keep import used
    from datetime import datetime
    event = {"title": "Demo", "location": "Houston",
             "start_dt": datetime(2026, 6, 15, 14, 0)}
    line = calendar_service.format_event(event)
    assert "Demo" in line and "Houston" in line and "02:00 PM" in line


def test_invalid_date_raises(tmp_path):
    cal = tmp_path / "calendar.json"
    cal.write_text(json.dumps([{"title": "Bad", "start": "not-a-date",
                                "end": "2026-06-15T15:00", "location": "Houston"}]))
    with pytest.raises(calendar_service.CalendarError, match="invalid date"):
        calendar_service.load_events(cal)
