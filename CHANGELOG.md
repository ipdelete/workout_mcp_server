# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### Phase 4: compute_fitness Tool Implementation (Issue #14)
- Implemented `compute_fitness` MCP tool for Chronic Training Load (CTL) calculation
- CTL calculated as 42-day exponentially weighted moving average of TSS values
- Reusable EWMA utility function in `src/workout_mcp_server/tools/fitness_metrics.py`
- Tool accepts target_date parameter and returns CTL with metadata (workouts count, date range)
- Comprehensive error handling for invalid dates, missing data, and exceptions
- Edge case handling for insufficient workout data with appropriate messaging
- Full test coverage with 20 new unit tests for EWMA calculations and tool functionality
- Mathematical formula: alpha = 1 - exp(-1/42) for 42-day time constant
- FastMCP decorator pattern with proper type hints and documentation
- Fitness metrics module designed for reuse by future ATL and TSB tools

#### Phase 3: get_last_50_workouts Tool Implementation (Issue #13)
- Implemented `get_last_50_workouts` MCP tool in `src/workout_mcp_server/main.py`
- Tool returns all 50 workouts from the dataset providing complete training history
- Workouts are automatically sorted by date (newest first) using existing data loader
- Includes all workout fields (id, date, duration_minutes, distance_km, avg_power_watts, tss, workout_type)
- Comprehensive error handling with appropriate logging for failures
- Leverages existing `WorkoutDataLoader.get_all_workouts()` method from Phase 2
- Full test coverage with 4 new unit tests covering success cases, edge cases, and error handling
- FastMCP decorator pattern for tool definition with proper type hints and documentation

#### Phase 3: get_workout_by_id Tool Implementation (Issue #10)
- Implemented `get_workout_by_id` MCP tool in `src/workout_mcp_server/main.py`
- Tool accepts a workout_id parameter and returns complete workout details
- Returns appropriate error message if workout not found or on exceptions
- Leverages existing `WorkoutDataLoader.get_workout_by_id()` method from Phase 2
- Includes proper error handling and logging
- Full test coverage with unit tests for success and error cases
- FastMCP decorator pattern for tool definition with type hints

#### Phase 2: Data Loading Functionality (Issue #9)
- Comprehensive data loading module in `src/workout_mcp_server/data_loader.py`
- Pydantic-based `Workout` model for data validation and parsing
- `WorkoutDataLoader` class with caching support for efficient data access
- Functions to load, validate, sort, and filter workout data by date range
- Automatic date parsing from ISO format strings to datetime objects
- Robust error handling with custom `WorkoutDataError` exception
- Full test coverage with 26 unit tests for all data loading functionality
- Type hints and mypy compliance for all functions and methods

#### Phase 2: Mock Workout Data Generation
- Python script to generate 50 mock cycling workout entries in `scripts/generate_mock_data.py`
- Mock data stored in JSON format at `data_store/workouts.json`
- Realistic workout data with proper TSS calculations based on duration, power, and workout type
- Training plan generator that creates realistic patterns (build weeks, recovery weeks, rest days)
- Comprehensive test suite for data generation logic
- Data model includes: id, date, duration_minutes, distance_km, avg_power_watts, tss, workout_type

#### Phase 1: MCP Server Skeleton
- MCP server skeleton implementation using FastMCP framework
- Basic server initialization with logging configuration  
- Tools directory structure for future tool implementations
- Server responds to MCP protocol handshake
- Tests for server instance creation and configuration

#### Development Environment Setup
- Python development environment configuration with FastMCP framework
- Project structure with proper Python package layout in `src/workout_mcp_server/`
- Development dependencies: pytest, black, mypy, ruff for code quality
- Basic test suite to verify environment setup
- Package entry points for running with `python -m workout_mcp_server`

### Changed
- Python version requirement updated to 3.10+ (required by FastMCP)
- Project configuration moved to modern pyproject.toml format with hatchling build backend

## [0.1.0] - 2025-05-28

### Added
- Initial project structure and documentation
- Architecture Decision Records (ADRs) for testing philosophy and MCP framework selection
- Project requirements documentation (PRD)
- Basic README with project overview