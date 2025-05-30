# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Workout MCP Server is a Model Context Protocol server that provides cycling workout analytics tools for LLMs. It enables AI assistants to retrieve workout history, calculate fitness metrics (CTL, ATL, TSB), and analyze athletic performance trends.

## Development Commands

```bash
# Install dependencies (using uv - recommended)
uv sync

# Install dependencies (using pip)
pip install -e .

# Run the MCP server
python -m workout_mcp_server
# or
uvx workout_mcp_server

# Run tests
pytest

# Run a specific test
pytest tests/test_main.py::test_name

# Format code
black .

# Lint code
ruff check .
ruff check --fix .

# Type check
mypy src/

# Run all checks (format, lint, type check, tests)
black . && ruff check . && mypy src/ && pytest
```

## Architecture & Key Design Decisions

### MCP Framework
The project uses FastMCP for rapid development and type safety (ADR-002). FastMCP provides decorators for creating MCP tools and handles the protocol implementation.

### Testing Philosophy
Follow behavior-driven testing (ADR-001):
- Test what the code does, not how it does it
- Write tests from the user's perspective
- Avoid testing implementation details

### Data Model
- Single JSON file (`data_store/workouts.json`) stores 50 mock cycling workouts
- Each workout contains:
  - `id`: UUID string
  - `date`: ISO format date (YYYY-MM-DD)
  - `duration_minutes`: Integer
  - `distance_km`: Float
  - `avg_power_watts`: Integer
  - `tss`: Training Stress Score (Integer)
  - `workout_type`: String ("endurance", "interval", "recovery", "threshold")

### Fitness Metrics Calculations
- **Fitness (CTL)**: 42-day exponentially weighted moving average of TSS
- **Fatigue (ATL)**: 7-day exponentially weighted moving average of TSS  
- **Form (TSB)**: Fitness minus Fatigue (positive = fresh, negative = fatigued)

## Implementation Status

All MCP tools have been implemented:
1. `get_last_50_workouts` - ✓ Retrieves all 50 workouts, sorted by date (most recent first)
2. `get_last_7_workouts` - ✓ Retrieves the 7 most recent workouts
3. `get_workout_by_id` - ✓ Retrieves specific workout by ID
4. `compute_fitness` - ✓ Calculates CTL (42-day EWMA of TSS)
5. `compute_fatigue` - ✓ Calculates ATL (7-day EWMA of TSS)
6. `compute_form` - ✓ Calculates TSB (CTL - ATL)

## Key Files
- `src/workout_mcp_server/main.py` - Main MCP server implementation
- `src/workout_mcp_server/tools/` - Directory for tool implementations
- `data_store/workouts.json` - Mock workout data
- `tests/` - Test files following pytest conventions
- `docs/project-prd.md` - Detailed product requirements
- `docs/adr/` - Architecture decision records

## Code Style
- Python 3.10+ with type hints
- Black formatting (88 char line length)
- Ruff linting with E, F, I, UP rules
- MyPy for type checking with strict settings
- Async/await patterns for MCP tools