# Task Breakdown for MCP Fitness Analytics Server

## Phase 1: Project Setup & Structure
1. **Create project directory structure**
   - Initialize Python project folder
   - Set up basic file organization

2. **Set up Python environment & dependencies**
   - Create virtual environment
   - Install MCP SDK and required packages
   - Create requirements.txt

3. **Create basic MCP server skeleton**
   - Initialize MCP server with proper imports
   - Set up server configuration and entry point

## Phase 2: Data Foundation
4. **Generate mock workout data**
   - Create JSON file with 50 realistic cycling workouts
   - Ensure data spans 3-4 months with varied workout types
   - Include all required fields (id, date, duration, distance, power, TSS, type)

5. **Implement data loading functionality**
   - Create utility functions to read JSON file
   - Add basic data validation and error handling

## Phase 3: Basic Tool Implementation
6. **Implement get_workout_by_id tool**
   - Create tool handler function
   - Add ID validation and error handling for missing workouts

7. **Implement get_last_7_workouts tool**
   - Sort workouts by date
   - Return 7 most recent workouts

8. **Implement get_last_50_workouts tool**
   - Return all workouts (simplest implementation)

## Phase 4: Analytics Implementation
9. **Implement fitness calculation (CTL)**
   - Create exponentially weighted moving average function
   - Calculate 42-day fitness score based on TSS

10. **Implement fatigue calculation (ATL)**
    - Create 7-day exponentially weighted moving average
    - Calculate current fatigue score

11. **Implement form calculation (TSB)**
    - Combine fitness and fatigue calculations
    - Return fitness minus fatigue score

## Phase 5: Integration & Testing
12. **Register all tools with MCP server**
    - Add tool definitions to server
    - Ensure proper tool routing

13. **Test server functionality**
    - Start server and verify it accepts connections
    - Test each tool individually
    - Verify JSON responses are properly formatted

14. **Add error handling and edge cases**
    - Handle missing data gracefully
    - Add appropriate error messages
    - Validate input parameters
