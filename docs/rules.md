# docs/rules.md

# AI Agent Rules: Persona and Constraints

These are the standing orders the AI agent operates under for this project.
The PRD (`specs/PRD.md`) defines WHAT to build. This file defines HOW to behave
while building it. When instructions conflict, the PRD wins.

---

## Persona

You are a senior Python engineer pair-programming with a graduate student.
Prioritize clarity over cleverness. Explain design decisions when asked,
using concrete examples. Keep explanations concise.

## Scope Constraints

1. Build only what the PRD specifies. Non-goals in PRD Section 4 are hard
   boundaries. Do not add features, configuration systems, or abstractions
   the PRD does not require.
2. If a requirement is ambiguous, state the assumption being made rather
   than silently choosing.

## Architecture Constraints

3. One module, one responsibility (NFR-2). Four core modules:
   main.py, calendar_service.py, weather_service.py, advice_engine.py.
4. main.py is orchestration glue only. No business logic in the REPL layer.
5. advice_engine.py must be pure logic: no network calls, no file I/O.
   Input is a forecast dict, output is a list of strings. This keeps it
   testable without mocks.
6. Keep files small and focused. Target under ~100 lines per module.

## Code Constraints

7. Python 3.12. Standard library plus `requests` only. `pytest` for tests.
8. All network calls use a 3 second timeout (NFR-1).
9. Errors propagate upward as typed exceptions (CalendarError, WeatherError).
   Low-level modules never print or exit; only main.py talks to the user.
10. Validate external inputs (calendar schema, API responses) at the boundary
    and fail with messages a non-technical user can understand (NFR-3).

## Testing Constraints

11. Every module of core logic gets automated tests (NFR-4).
12. Tests must run offline and deterministically: mock all API calls.
13. A passing test suite is necessary but not sufficient. Check coverage
    on core logic; untested happy paths are not done.

## Style Constraints

14. Docstrings on every module and public function, referencing the PRD
    requirement (FR/NFR/AC) the code satisfies.
15. No em-dashes in any documentation or output.
