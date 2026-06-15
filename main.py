"""main.py

Coordinates the assistant: REPL loop wiring calendar, weather, and advice
modules together (FR-5). Run with:  python main.py
"""

import calendar_service
import weather_service
import advice_engine

HELP_TEXT = """Commands:
  show events   List upcoming calendar events
  show weather  Show forecast for each event
  advice        Get weather-aware recommendations
  help          Show this message
  exit          Quit the assistant"""


def cmd_show_events(events):
    for i, event in enumerate(events, 1):
        print(f"  {i}. {calendar_service.format_event(event)}")


def cmd_show_weather(events):
    for event in events:
        print(f"\n  {event['title']} ({event['location']})")
        try:
            fc = weather_service.get_forecast(event["location"], event["start_dt"])
            print(f"    Forecast: {fc['condition']}, {fc['temp_f']:.0f}°F, "
                  f"{fc['precip_prob']}% chance of precipitation")
        except weather_service.WeatherError as exc:
            print(f"    Weather unavailable: {exc}")


def cmd_advice(events):
    for event in events:
        print(f"\n  {event['title']} | {event['start_dt'].strftime('%a %I:%M %p')} | {event['location']}")
        try:
            fc = weather_service.get_forecast(event["location"], event["start_dt"])
            print(f"    Forecast: {fc['condition']}, {fc['temp_f']:.0f}°F")
            for tip in advice_engine.generate_advice(fc):
                print(f"    -> {tip}")
        except weather_service.WeatherError as exc:
            print(f"    Weather unavailable: {exc}")
            print("    -> Check a local forecast manually before leaving.")


def main():
    print("Weather-Aware Personal Assistant")
    print("=" * 40)

    try:
        events = calendar_service.load_events("calendar.json")
    except calendar_service.CalendarError as exc:
        print(f"Error loading calendar: {exc}")
        return

    print(f"Loaded {len(events)} event(s).")
    print(HELP_TEXT)

    while True:
        try:
            command = input("\nAssistant > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if command == "exit":
            print("Goodbye!")
            break
        elif command == "show events":
            cmd_show_events(events)
        elif command == "show weather":
            cmd_show_weather(events)
        elif command == "advice":
            cmd_advice(events)
        elif command == "help":
            print(HELP_TEXT)
        elif command == "":
            continue
        else:
            print(f"  Unknown command: '{command}'. Type 'help' for options.")


if __name__ == "__main__":
    main()
