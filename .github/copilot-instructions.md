# GitHub Copilot Instructions

This file provides guidance to GitHub Copilot when working with code in this repository.

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
- Single JSON file stores 50 mock cycling workouts
- Each workout contains: date, duration, TSS (Training Stress Score), description

### Fitness Metrics Calculations
- **Fitness (CTL)**: 42-day exponentially weighted moving average of TSS
- **Fatigue (ATL)**: 7-day exponentially weighted moving average of TSS  
- **Form (TSB)**: Fitness minus Fatigue (positive = fresh, negative = fatigued)

## Implementation Status

Currently skeleton only - `src/main.py` needs to be replaced with actual MCP server implementation using FastMCP. The following tools need to be implemented:
1. `get_workouts` - Retrieve workout history with optional date filtering
2. `calculate_fitness_metrics` - Calculate CTL, ATL, and TSB for a given date
3. `analyze_performance` - Provide insights based on training patterns

## Key Files
- `src/main.py` - Main MCP server implementation (needs to be written)
- `tests/` - Test files following pytest conventions
- `docs/project-prd.md` - Detailed product requirements
- `docs/adr/` - Architecture decision records

## Coding Guidelines

When generating code for this project:
- Use Python 3.11+ features and type hints
- Follow PEP 8 style guidelines
- Use black for code formatting
- Write tests for all new functionality using pytest
- Use FastMCP decorators for MCP tool implementations
- Handle errors gracefully and return meaningful error messages
- Keep functions focused and single-purpose