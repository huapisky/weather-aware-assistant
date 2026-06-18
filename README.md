# Weather-Aware Personal Assistant

EDS 6397 course project. A CLI assistant that combines local calendar events with Open-Meteo weather forecasts to generate actionable recommendations.

## Setup

```bash
pip install requests pytest
```

## Run

```bash
python main.py
```

Commands: `show events`, `show weather`, `advice`, `help`, `exit`

## Run Tests

```bash
pytest tests/ -v
```

16 tests covering calendar loading (AC-1), advice generation (AC-2), API failure handling (AC-3), and full pass rate (AC-4). All weather API calls are mocked, so tests run offline.

## Coverage

```bash
pip install pytest-cov
pytest tests/ --cov=. --cov-report=term
```

Core logic coverage: advice_engine 100%, calendar_service 90%, weather_service 83% (89% overall). `main.py` is excluded via `.coveragerc` as thin CLI presentation glue; all business logic lives in the tested modules.

## Architecture Diagram

See `architecture.svg` for the module and data-flow diagram.

## Architecture

| File | Responsibility |
|---|---|
| `main.py` | REPL loop; wires modules together |
| `calendar_service.py` | Loads and validates `calendar.json` |
| `weather_service.py` | Geocodes locations, fetches Open-Meteo hourly forecasts |
| `advice_engine.py` | Pure rule-based recommendations (no I/O) |
| `calendar.json` | Sample event data |
| `tests/test_assistant.py` | Automated test suite |

## Notes

- Open-Meteo requires no API key and forecasts ~16 days ahead.
- Forecast lookup matches the hourly slot of each event's start time.
- All network calls use a 3-second timeout (NFR-1) and raise a catchable `WeatherError` on failure (NFR-3).

## Vibe Report

A reflection on directing an AI agent through this build.

### Where did the AI's "vibe" drift?

The clearest drift was premature victory. After the first build, the agent reported 10 passing tests and a complete project. A coverage report told a different story: `weather_service.py` sat at 56% because the tests exercised every failure path but never the happy path. The forecast parsing logic, the core of the module, had executed zero times under test. The suite looked thorough because it had good error-handling tests, which created a green-checkmark vibe that did not match reality. The fix was adding a full mocked-pipeline test (fake geocode response, fake forecast response, assert on parsed output), which brought core logic to 89% with the advice engine at 100%. Lesson: passing tests measure what you wrote tests for, not what the code does.

### When did I use the "Builder Hammer"?

I never swung it. Every line of code in this project came from the AI; I steered entirely through prompts and constraints, and I did not hand-edit a single module. I want to be honest about that rather than invent a rescue story, but I also do not think "no manual fixes" means I got lucky. Three things made the hammer unnecessary:

1. **Tight scope.** Thanks to ChatGPT's PRD Builder, the PRD's non-goals kept the surface area small. There was less room for the AI to go wrong because there was less to build.
2. **Constraints up front, not corrections after.** `docs/rules.md` set the architecture rules before any code was written: pure advice engine, typed exceptions, no logic in main.py. Steering at the design level meant I rarely had to correct at the code level.
3. **Tests caught the one real defect before I did.** The coverage gap in `weather_service.py` (described above) was a genuine logic blind spot. But the fix was another prompt ("add a happy-path test for the forecast parser"), not a manual edit. The guardrail surfaced the problem and re-prompting closed it.

Where I *would* have reached for the hammer: if re-prompting had failed to fix the coverage gap after two or three tries, or if the AI had introduced a subtle parsing bug that a prompt kept misunderstanding. The skill the assignment is really testing is knowing the difference between a problem a better prompt solves and a problem only manual code solves. On a project this size, everything fell in the first bucket. On a larger system with tangled state, it would not.

### Most successful steering prompt

"Make the advice engine pure logic with no I/O: forecast dict in, list of strings out." This single constraint shaped the entire architecture. It forced all network and file access to the edges of the system, made the advice module testable with plain dictionaries and zero mocks, and is the reason it reached 100% coverage trivially. The general pattern: constraints steer better than requests. "Make it testable" produced vague results; naming the exact structural property that creates testability produced the right design on the first pass.
