# Product Requirements Document (PRD)

# Weather-Aware Personal Assistant

**Version:** 1.0
**Date:** June 2026
**Owner:** Francisco Reyes
**Reviewers:** Course Instructor, Peer Reviewers

---

# Table of Contents

1. Executive One-Pager
2. Overview & Context
3. Customer Insights & Evidence
4. Goals & Non-Goals
5. Alternatives Considered
6. User Personas & Use Cases
7. Requirements
8. UX & Design Considerations
9. Technical Notes
10. Metrics & Success Criteria
11. Risks & Mitigations
12. Rollout Plan
13. Decision Log
14. Success Story Narrative
15. Open Questions & Assumptions
16. Glossary

---

# 1. Executive One-Pager

## TL;DR

* Build a CLI-based personal assistant that combines calendar events and weather forecasts.
* Retrieve weather information from a public API.
* Read events from a local JSON calendar file.
* Generate actionable recommendations for the user.
* Demonstrate AI-assisted software orchestration using modular architecture and automated testing.

## Plain Language Summary

Users often check weather and schedules separately before leaving for work, school, or appointments. This project combines both data sources into a single assistant that can provide practical recommendations.

Example:

> "You have a meeting at 2:00 PM in Houston. Rain is expected during your commute. Leave 15 minutes early and bring an umbrella."

The project demonstrates how AI can be directed to build a maintainable software system through structured requirements and architectural guidance.

---

# 2. Overview & Context

## Problem Statement

People frequently make decisions without considering how weather conditions may impact scheduled activities.

This leads to:

* Late arrivals
* Inadequate preparation
* Missed opportunities to plan ahead

## Why Now?

The assignment focuses on orchestration rather than coding. The project showcases how an AI agent can be guided through requirements, documentation, testing, and modular design.

## Strategic Alignment

Supports course objectives:

* AI-assisted development
* Modular software architecture
* Requirements-driven engineering
* Automated testing

---

# 3. Customer Insights & Evidence

## Primary User Feedback

Hypothetical user statement:

> "I always check my calendar and weather separately before leaving."

## Secondary Observation

Many calendar applications do not automatically provide actionable recommendations based on weather conditions.

## Evidence Source

Project assumption based on common user behavior.

No formal survey data available.

---

# 4. Goals & Non-Goals

## Goals

### G1

Provide weather forecasts for scheduled events.

### G2

Provide useful recommendations based on weather conditions.

### G3

Demonstrate modular software architecture.

### G4

Demonstrate AI-assisted software orchestration.

### G5

Provide automated testing coverage.

## Non-Goals

* Calendar synchronization with Google Calendar.
* Real-time GPS tracking.
* Voice assistant integration.
* Multi-user support.
* Mobile application development.

---

# 5. Alternatives Considered

## Alternative A

Weather lookup only.

### Rejected Because

Does not provide contextual recommendations.

## Alternative B

Calendar lookup only.

### Rejected Because

Does not leverage external data.

## Alternative C

LLM-powered recommendations.

### Rejected Because

Introduces additional complexity and API costs.

Current version uses rule-based recommendations.

---

# 6. User Personas & Use Cases

## Persona

### Student Professional

Characteristics:

* Uses a calendar to manage activities.
* Needs quick recommendations.
* Wants minimal setup.

## Use Cases

### UC1

View upcoming events.

### UC2

Check weather associated with an event.

### UC3

Receive recommendations before attending an event.

### UC4

Interact through a command-line interface.

---

# 7. Requirements

## Functional Requirements

### FR-1 Calendar Loading

System shall load events from calendar.json.

### FR-2 Weather Retrieval

System shall retrieve weather forecasts using a public API.

### FR-3 Event Matching

System shall associate forecast data with event dates and times.

### FR-4 Advice Generation

System shall generate recommendations using predefined rules.

Examples:

* Rain -> Bring umbrella
* High temperature -> Bring water
* Severe weather -> Leave earlier

### FR-5 REPL Interface

System shall support an interactive command loop.

Commands:

* show events
* show weather
* advice
* exit

---

## Non-Functional Requirements

### NFR-1 Performance

Responses shall be generated within 3 seconds.

### NFR-2 Maintainability

Each module shall have a single responsibility.

### NFR-3 Reliability

System shall gracefully handle API failures.

### NFR-4 Testability

Core logic shall have automated tests.

---

## Acceptance Criteria

### AC-1

Given a valid calendar file

When the user requests events

Then all events are displayed.

### AC-2

Given weather data is available

When advice is requested

Then weather-aware recommendations are generated.

### AC-3

Given weather API failure

When advice is requested

Then the system displays a meaningful error message.

### AC-4

Given automated tests are executed

When pytest runs

Then all tests pass.

---

# 8. UX & Design Considerations

## Interface

Text-based terminal interface.

Example:

Assistant > advice

Meeting: Engineering Review
Forecast: Rain

Recommendation:
Bring umbrella and leave early.

## Accessibility

* Clear text output
* Simple commands
* Error messages understandable by non-technical users

---

# 9. Technical Notes

## Architecture

main.py

Coordinates execution.

calendar_service.py

Reads calendar data.

weather_service.py

Retrieves weather forecasts.

advice_engine.py

Generates recommendations.

## External Dependency

Open-Meteo API

## Data Format

calendar.json

Example:

[
{
"title": "Engineering Review",
"start": "2026-06-15T14:00",
"end": "2026-06-15T15:00",
"location": "Houston"
}
]

---

# 10. Metrics & Success Criteria

## Technical Metrics

| Metric           | Target     |
| ---------------- | ---------- |
| Test Pass Rate   | 100%       |
| API Success Rate | >95%       |
| Startup Time     | <3 seconds |

## Project Metrics

| Metric          | Target    |
| --------------- | --------- |
| Modular Files   | 4+        |
| Automated Tests | Minimum 3 |
| Documentation   | Complete  |

---

# 11. Risks & Mitigations

| Risk                      | Impact | Mitigation               |
| ------------------------- | ------ | ------------------------ |
| Weather API unavailable   | Medium | Display fallback message |
| Invalid calendar file     | Medium | Validate schema          |
| AI-generated code defects | High   | Automated testing        |
| Scope creep               | Medium | Follow PRD               |
| Timezone mismatch between event time and forecast time | Medium | Treat event times as local to the event location; document the assumption and avoid cross-zone events in v1 |
| Event time has no exact hourly forecast slot (e.g. 2:15 PM) | Medium | Round event time to the nearest forecast hour; define matching tolerance in FR-3 |
| Event falls outside the ~16-day forecast horizon | Low | Detect and return a clear "no forecast available" message rather than failing silently |
| Ambiguous or misspelled location geocodes incorrectly | Medium | Use the top geocoding result; surface the resolved location name to the user for confirmation |

---

# 12. Rollout Plan

## Phase 1

Create project structure.

## Phase 2

Implement calendar reader.

## Phase 3

Implement weather service.

## Phase 4

Implement recommendation engine.

## Phase 5

Create automated tests.

## Phase 6

Final documentation and submission.

---

# 13. Decision Log

| Date      | Decision                     | Owner     |
| --------- | ---------------------------- | --------- |
| June 2026 | Use Open-Meteo API           | Francisco |
| June 2026 | Use rule-based advice engine | Francisco |
| June 2026 | Use Python CLI architecture  | Francisco |

---

# 14. Success Story Narrative

A student launches the assistant before leaving for class.

The assistant detects rain near the event location and recommends leaving early and bringing an umbrella.

The student arrives on time and avoids weather-related disruptions.

The project successfully demonstrates how multiple services can be orchestrated into a useful assistant.

---

# 15. Open Questions & Assumptions

## Assumptions

* Internet connection is available.
* Calendar file follows expected schema.
* Open-Meteo API remains publicly accessible.

## Open Questions

* Should future versions support Google Calendar?
* Should recommendations use an LLM?
* Should location geocoding be automated?
* What timezone are event times expressed in, and how should events spanning multiple timezones be handled?
* What is the acceptable tolerance for matching an event time to a forecast hour (nearest hour, round down, configurable window)?
* How should events beyond the forecast horizon (~16 days out) be presented to the user?
* There is no metric for recommendation *quality* or usefulness, only engineering metrics (test pass rate, uptime, latency). How would advice quality be measured in a future version?
* How should ambiguous location names be disambiguated when geocoding returns multiple candidates?

---

# 16. Glossary

### API

Application Programming Interface.

### CLI

Command Line Interface.

### JSON

JavaScript Object Notation.

### REPL

Read, Evaluate, Print, Loop interactive terminal environment.

### PRD

Product Requirements Document.

### AI Agent

An AI-assisted development tool such as Cursor, Replit Agent, or Windsurf.
