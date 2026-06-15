"""advice_engine.py

Generates recommendations from forecast data using predefined rules (FR-4).
Pure logic, no I/O, which makes it trivially testable (NFR-4).
"""

HOT_THRESHOLD_F = 90
COLD_THRESHOLD_F = 40
RAIN_PROBABILITY_THRESHOLD = 40  # percent


def generate_advice(forecast):
    """Return a list of recommendation strings for a forecast dict.

    Expected keys: temp_f, precip_prob, condition.
    """
    tips = []
    condition = forecast.get("condition", "Unknown")
    temp = forecast.get("temp_f")
    precip = forecast.get("precip_prob", 0)

    if condition == "Thunderstorm":
        tips.append("Severe weather expected. Leave 20+ minutes early and drive carefully.")
    elif condition in ("Rain", "Snow") or precip >= RAIN_PROBABILITY_THRESHOLD:
        tips.append("Precipitation likely. Bring an umbrella and leave 15 minutes early.")

    if condition == "Fog":
        tips.append("Low visibility. Allow extra commute time.")

    if temp is not None:
        if temp >= HOT_THRESHOLD_F:
            tips.append(f"High temperature ({temp:.0f}°F). Bring water and dress light.")
        elif temp <= COLD_THRESHOLD_F:
            tips.append(f"Cold conditions ({temp:.0f}°F). Bring a jacket.")

    if not tips:
        tips.append("Conditions look good. No special preparation needed.")

    return tips
