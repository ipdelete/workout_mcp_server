# Workout MCP Server

A Model Context Protocol (MCP) server that provides cycling workout analytics tools, enabling LLMs to analyze fitness data, calculate training metrics, and provide insights into athletic performance.

## Features

The Workout MCP Server provides tools for:
- Retrieving workout history (last 50 or last 7 workouts)
- Looking up specific workouts by ID
- Computing fitness metrics:
  - **Fitness (CTL)**: Chronic Training Load - 42-day exponentially weighted moving average
  - **Fatigue (ATL)**: Acute Training Load - 7-day exponentially weighted moving average  
  - **Form (TSB)**: Training Stress Balance - the difference between fitness and fatigue

## Installation

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *workout_mcp_server*.

### Using PIP

Alternatively you can install `workout_mcp_server` via pip:

```bash
pip install workout_mcp_server
```

After installation, you can run it as a module using:

```bash
python -m workout_mcp_server
```

## Configuration

### Configure with Claude Desktop

Add this to your `claude_desktop_config.json`:

<details>
<summary>Using uvx</summary>

```json
"mcpServers": {
  "workout_mcp_server": {
    "command": "uvx",
    "args": ["workout_mcp_server"]
  }
}
```
</details>

<details>
<summary>Using pip installation</summary>

```json
"mcpServers": {
  "workout_mcp_server": {
    "command": "python",
    "args": ["-m", "workout_mcp_server"]
  }
}
```
</details>

### Configure with VSCode MCP Client

Add this to your `settings.json`:

<details>
<summary>Using uvx</summary>

```json
"mcp.servers": {
  "workout_mcp_server": {
    "command": "uvx",
    "args": ["workout_mcp_server"]
  }
}
```
</details>

<details>
<summary>Using pip installation</summary>

```json
"mcp.servers": {
  "workout_mcp_server": {
    "command": "python",
    "args": ["-m", "workout_mcp_server"]
  }
}
```
</details>

## Available Tools

### `get_last_50_workouts`
Retrieves all 50 workouts from the dataset, sorted by date (most recent first).

### `get_last_7_workouts`
Retrieves the 7 most recent workouts, useful for analyzing current training week.

### `get_workout_by_id`
Retrieves a specific workout by its unique ID.

**Input:**
- `workout_id` (string): The unique identifier of the workout

### `compute_fitness`
Calculates current fitness score (Chronic Training Load) based on a 42-day exponentially weighted moving average of Training Stress Score (TSS).

### `compute_fatigue`
Calculates current fatigue score (Acute Training Load) based on a 7-day exponentially weighted moving average of TSS.

### `compute_form`
Calculates current form score (Training Stress Balance) as the difference between fitness and fatigue. Positive values indicate good form, negative values suggest accumulated fatigue.

## Data Structure

Each workout contains:
- `id`: Unique workout identifier
- `date`: Workout date (ISO format)
- `duration_minutes`: Workout duration in minutes
- `distance_km`: Distance covered in kilometers
- `avg_power_watts`: Average power output in watts
- `tss`: Training Stress Score
- `workout_type`: Type of workout (e.g., "endurance", "interval", "recovery")

## Development

### Building from Source

1. Clone the repository
2. Install dependencies: `pip install -e .`
3. Run the server: `python -m workout_mcp_server`

### Testing

Run tests with: `pytest`

## License

MIT License - see LICENSE file for details.
