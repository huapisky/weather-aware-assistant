"""weather_service.py

Retrieves weather forecasts from the Open-Meteo public API (FR-2).
Handles API failures gracefully (NFR-3).
"""

import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT_SECONDS = 3  # supports NFR-1 (respond within 3 seconds)

# WMO weather interpretation codes used by Open-Meteo, grouped by condition.
RAIN_CODES = {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82}
SEVERE_CODES = {95, 96, 99}  # thunderstorms
SNOW_CODES = {71, 73, 75, 77, 85, 86}


class WeatherError(Exception):
    """Raised when weather data cannot be retrieved."""


def geocode(location):
    """Convert a location name (e.g. 'Houston') to (latitude, longitude)."""
    try:
        resp = requests.get(
            GEOCODE_URL,
            params={"name": location, "count": 1},
            timeout=TIMEOUT_SECONDS,
        )
        resp.raise_for_status()
        results = resp.json().get("results")
    except requests.RequestException as exc:
        raise WeatherError(f"Could not reach geocoding service: {exc}") from exc

    if not results:
        raise WeatherError(f"Location not found: {location}")
    top = results[0]
    return top["latitude"], top["longitude"]


def get_forecast(location, event_dt):
    """Return forecast dict for a location at a specific datetime.

    Output: {"temp_f": float, "precip_prob": int, "code": int,
             "condition": str}
    Raises WeatherError if the API is unreachable or data is missing.
    """
    lat, lon = geocode(location)
    try:
        resp = requests.get(
            FORECAST_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "hourly": "temperature_2m,precipitation_probability,weather_code",
                "temperature_unit": "fahrenheit",
                "timezone": "auto",
            },
            timeout=TIMEOUT_SECONDS,
        )
        resp.raise_for_status()
        hourly = resp.json()["hourly"]
    except (requests.RequestException, KeyError) as exc:
        raise WeatherError(f"Could not retrieve forecast: {exc}") from exc

    # Find the hourly entry closest to the event start time.
    target = event_dt.strftime("%Y-%m-%dT%H:00")
    times = hourly["time"]
    if target not in times:
        raise WeatherError(
            f"No forecast available for {target} (Open-Meteo covers ~16 days ahead)."
        )
    idx = times.index(target)

    code = hourly["weather_code"][idx]
    return {
        "temp_f": hourly["temperature_2m"][idx],
        "precip_prob": hourly["precipitation_probability"][idx],
        "code": code,
        "condition": describe_code(code),
    }


def describe_code(code):
    """Translate a WMO weather code into a plain-English condition."""
    if code in SEVERE_CODES:
        return "Thunderstorm"
    if code in RAIN_CODES:
        return "Rain"
    if code in SNOW_CODES:
        return "Snow"
    if code == 0:
        return "Clear"
    if code in (1, 2, 3):
        return "Partly cloudy"
    if code in (45, 48):
        return "Fog"
    return "Unknown"
