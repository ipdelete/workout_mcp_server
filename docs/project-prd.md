# MCP Fitness Analytics Server - Product Requirements Document

## Overview
Build a Model Context Protocol (MCP) server in Python that provides cycling workout analytics tools using mock data from a JSON file.

## Core Requirements

### Tools to Implement
1. **get_last_50_workouts** - Return all 50 workouts from the dataset
2. **get_last_7_workouts** - Return the 7 most recent workouts 
3. **get_workout_by_id** - Return a specific workout by its ID
4. **compute_fitness** - Calculate current fitness score based on recent training load
5. **compute_fatigue** - Calculate current fatigue score based on recent training stress
6. **compute_form** - Calculate current form score (fitness minus fatigue)

### Data Structure
**JSON file containing 50 mock cycling workouts with fields:**
- `id` (string) - Unique workout identifier
- `date` (ISO string) - Workout date
- `duration_minutes` (number) - Workout duration
- `distance_km` (number) - Distance covered
- `avg_power_watts` (number) - Average power output
- `tss` (number) - Training Stress Score
- `workout_type` (string) - Type of workout (e.g., "endurance", "interval", "recovery")

### Analytics Calculations
- **Fitness (CTL)**: 42-day exponentially weighted moving average of TSS
- **Fatigue (ATL)**: 7-day exponentially weighted moving average of TSS  
- **Form (TSB)**: Fitness minus Fatigue

## Technical Implementation
- **Language**: Python
- **Framework**: MCP SDK for Python
- **Data Storage**: Single JSON file with mock workout data
- **Response Format**: JSON responses for all tools

## Deliverables
1. Python MCP server implementation
2. JSON file with 50 mock cycling workouts
3. All 6 tools implemented and functional
4. Basic error handling for invalid IDs or missing data

## Success Criteria
- All tools return properly formatted JSON responses
- Analytics calculations produce reasonable fitness/fatigue/form scores
- Server can be started and responds to MCP tool calls
- Mock data covers a realistic 50-workout timespan (approximately 3-4 months of training)