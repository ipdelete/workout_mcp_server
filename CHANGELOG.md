# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-05-30

### Added
- **compute_form** tool ([#16](https://github.com/ianphil/workout_mcp_server/issues/16), [PR #29](https://github.com/ianphil/workout_mcp_server/pull/29))
  - Calculates Training Stress Balance (TSB) as CTL minus ATL
  - Provides interpretation of athlete's form/freshness state
  - TSB > 5: Fresh, TSB -5 to 5: Neutral, TSB < -5: Fatigued

## [0.1.5] - 2025-05-29

### Added
- **compute_fatigue** tool ([#15](https://github.com/ianphil/workout_mcp_server/issues/15), [PR #28](https://github.com/ianphil/workout_mcp_server/pull/28))
  - Calculates Acute Training Load (ATL) using 7-day EWMA of TSS
  - Represents short-term training stress and fatigue
  
- **compute_fitness** tool ([#14](https://github.com/ianphil/workout_mcp_server/issues/14), [PR #27](https://github.com/ianphil/workout_mcp_server/pull/27))
  - Calculates Chronic Training Load (CTL) using 42-day EWMA of TSS
  - Represents long-term fitness adaptation
  - Created reusable EWMA utility function in `tools/fitness_metrics.py`

- **get_last_50_workouts** tool ([#13](https://github.com/ianphil/workout_mcp_server/issues/13), [PR #26](https://github.com/ianphil/workout_mcp_server/pull/26))
  - Returns all 50 workouts sorted by date (newest first)
  - Provides complete training history for analysis

- **get_last_7_workouts** tool ([#12](https://github.com/ianphil/workout_mcp_server/issues/12), [PR #25](https://github.com/ianphil/workout_mcp_server/pull/25))
  - Returns the 7 most recent workouts
  - Useful for current training week analysis

## [0.1.0] - 2025-05-28

### Added
- **Initial Release** - Complete foundation for Workout MCP Server
  
- **MCP Tools**
  - `get_workout_by_id` tool ([#10](https://github.com/ianphil/workout_mcp_server/issues/10), [PR #24](https://github.com/ianphil/workout_mcp_server/pull/24))
    - Retrieves specific workout by ID
    - Returns complete workout details

- **Data Infrastructure**
  - Data loading functionality ([#9](https://github.com/ianphil/workout_mcp_server/issues/9), [PR #23](https://github.com/ianphil/workout_mcp_server/pull/23))
    - Pydantic-based `Workout` model
    - `WorkoutDataLoader` class with caching
    - Date parsing and validation
  - Mock data generation ([#8](https://github.com/ianphil/workout_mcp_server/issues/8), [PR #22](https://github.com/ianphil/workout_mcp_server/pull/22))
    - 50 realistic cycling workouts
    - Training patterns with build/recovery weeks

- **Server Foundation**
  - MCP server skeleton ([#7](https://github.com/ianphil/workout_mcp_server/issues/7), [PR #21](https://github.com/ianphil/workout_mcp_server/pull/21))
    - FastMCP framework integration
    - Logging configuration
    - Tools directory structure
  - Python environment setup ([#6](https://github.com/ianphil/workout_mcp_server/issues/6), [PR #20](https://github.com/ianphil/workout_mcp_server/pull/20))
    - Development dependencies (pytest, black, mypy, ruff)
    - Modern pyproject.toml configuration
  - Project structure ([#5](https://github.com/ianphil/workout_mcp_server/issues/5), [PR #1](https://github.com/ianphil/workout_mcp_server/pull/1))
    - Initial documentation (README, PRD, ADRs)
    - Standard Python package layout

### Technical Details
- Python 3.10+ requirement (FastMCP dependency)
- Full test coverage with 60+ unit tests
- Type hints and mypy strict compliance
- Async/await patterns for all MCP tools