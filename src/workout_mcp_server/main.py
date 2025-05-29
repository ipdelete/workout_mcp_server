"""Workout MCP Server - Main entry point."""

import logging
from pathlib import Path

from fastmcp import FastMCP

from .data_loader import WorkoutDataLoader

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp: FastMCP = FastMCP("workout-mcp-server")

# Initialize data loader
DATA_PATH = Path(__file__).parent.parent.parent / "data_store" / "workouts.json"
data_loader = WorkoutDataLoader(DATA_PATH)


@mcp.tool()
async def get_workout_by_id(workout_id: str) -> dict:
    """Get details of a specific workout by ID.

    Args:
        workout_id: The unique identifier of the workout

    Returns:
        Dictionary containing workout details including date, duration, TSS, and type
    """
    try:
        workout = data_loader.get_workout_by_id(workout_id)
        if workout is None:
            return {"error": f"Workout with ID '{workout_id}' not found"}

        # Convert Pydantic model to dict and format date as string
        workout_dict = workout.model_dump()
        workout_dict["date"] = workout.date.strftime("%Y-%m-%d")
        return workout_dict
    except Exception as e:
        logger.error(f"Error retrieving workout {workout_id}: {e}")
        return {"error": f"Failed to retrieve workout: {str(e)}"}


@mcp.tool()
async def get_last_7_workouts() -> list[dict] | dict:
    """Get the 7 most recent workouts for analyzing current training week.

    Returns:
        List of up to 7 workout dictionaries sorted by date (newest first),
        or error dictionary if retrieval fails
    """
    try:
        # Get all workouts sorted by date (newest first)
        workouts = data_loader.get_all_workouts(sort_by_date=True)
        
        # Take first 7 workouts (or fewer if less than 7 exist)
        recent_workouts = workouts[:7]
        
        # Convert each workout to dict format with date as string
        result = []
        for workout in recent_workouts:
            workout_dict = workout.model_dump()
            workout_dict["date"] = workout.date.strftime("%Y-%m-%d")
            result.append(workout_dict)
        
        return result
    except Exception as e:
        logger.error(f"Error retrieving last 7 workouts: {e}")
        return {"error": f"Failed to retrieve workouts: {str(e)}"}


def configure_logging() -> None:
    """Configure logging for the MCP server."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


def main() -> None:
    """Main entry point for the workout MCP server."""
    configure_logging()

    try:
        logger.info("Initializing workout-mcp-server")
        # FastMCP handles the server lifecycle
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
