"""Workout MCP Server - Main entry point."""

import logging
from datetime import datetime
from pathlib import Path

from fastmcp import FastMCP

from .data_loader import WorkoutDataLoader
from .tools.fitness_metrics import calculate_ewma, get_workouts_for_ctl_calculation

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


@mcp.tool()
async def get_last_50_workouts() -> list[dict] | dict:
    """Get all 50 workouts providing complete training history.

    Returns:
        List of all 50 workout dictionaries sorted by date (newest first),
        or error dictionary if retrieval fails
    """
    try:
        # Get all workouts sorted by date (newest first)
        workouts = data_loader.get_all_workouts(sort_by_date=True)

        # Convert each workout to dict format with date as string
        result = []
        for workout in workouts:
            workout_dict = workout.model_dump()
            workout_dict["date"] = workout.date.strftime("%Y-%m-%d")
            result.append(workout_dict)

        return result
    except Exception as e:
        logger.error(f"Error retrieving all workouts: {e}")
        return {"error": f"Failed to retrieve workouts: {str(e)}"}


@mcp.tool()
async def compute_fitness(target_date: str) -> dict:
    """Calculate Chronic Training Load (CTL) for a given date.

    CTL represents fitness and is calculated as a 42-day exponentially
    weighted moving average of Training Stress Score (TSS).

    Args:
        target_date: Date in ISO format (YYYY-MM-DD) for CTL calculation

    Returns:
        Dictionary containing CTL value and metadata, or error dictionary
    """
    try:
        # Parse target date
        try:
            target_dt = datetime.fromisoformat(target_date)
        except ValueError:
            return {
                "error": f"Invalid date format '{target_date}'. Use YYYY-MM-DD format."
            }

        # Get all workouts
        all_workouts = data_loader.get_all_workouts(sort_by_date=False)

        # Get relevant workouts for CTL calculation (42-day window)
        relevant_workouts = get_workouts_for_ctl_calculation(
            all_workouts, target_dt, days=42
        )

        if not relevant_workouts:
            return {
                "target_date": target_date,
                "ctl": 0.0,
                "workouts_count": 0,
                "message": "No workout data available for CTL calculation",
            }

        # Extract TSS values in chronological order
        tss_values = [workout.tss for workout in relevant_workouts]

        # Calculate CTL using 42-day EWMA
        ctl = calculate_ewma(tss_values, time_constant=42)

        return {
            "target_date": target_date,
            "ctl": round(ctl, 1),
            "workouts_count": len(relevant_workouts),
            "date_range": {
                "earliest_workout": relevant_workouts[0].date.strftime("%Y-%m-%d"),
                "latest_workout": relevant_workouts[-1].date.strftime("%Y-%m-%d"),
            },
        }

    except Exception as e:
        logger.error(f"Error calculating CTL for {target_date}: {e}")
        return {"error": f"Failed to calculate CTL: {str(e)}"}


@mcp.tool()
async def compute_fatigue(target_date: str) -> dict:
    """Calculate Acute Training Load (ATL) for a given date.

    ATL represents fatigue and is calculated as a 7-day exponentially
    weighted moving average of Training Stress Score (TSS).

    Args:
        target_date: Date in ISO format (YYYY-MM-DD) for ATL calculation

    Returns:
        Dictionary containing ATL value and metadata, or error dictionary
    """
    try:
        # Parse target date
        try:
            target_dt = datetime.fromisoformat(target_date)
        except ValueError:
            return {
                "error": f"Invalid date format '{target_date}'. Use YYYY-MM-DD format."
            }

        # Get all workouts
        all_workouts = data_loader.get_all_workouts(sort_by_date=False)

        # Get relevant workouts for ATL calculation (7-day window)
        relevant_workouts = get_workouts_for_ctl_calculation(
            all_workouts, target_dt, days=7
        )

        if not relevant_workouts:
            return {
                "target_date": target_date,
                "atl": 0.0,
                "workouts_count": 0,
                "message": "No workout data available for ATL calculation",
            }

        # Extract TSS values in chronological order
        tss_values = [workout.tss for workout in relevant_workouts]

        # Calculate ATL using 7-day EWMA
        atl = calculate_ewma(tss_values, time_constant=7)

        return {
            "target_date": target_date,
            "atl": round(atl, 1),
            "workouts_count": len(relevant_workouts),
            "date_range": {
                "earliest_workout": relevant_workouts[0].date.strftime("%Y-%m-%d"),
                "latest_workout": relevant_workouts[-1].date.strftime("%Y-%m-%d"),
            },
        }

    except Exception as e:
        logger.error(f"Error calculating ATL for {target_date}: {e}")
        return {"error": f"Failed to calculate ATL: {str(e)}"}


@mcp.tool()
async def compute_form(target_date: str) -> dict:
    """Calculate Training Stress Balance (TSB) for a given date.

    TSB represents form/freshness and is calculated as the difference
    between CTL (fitness) and ATL (fatigue). Positive values indicate
    freshness, negative values indicate fatigue.

    Args:
        target_date: Date in ISO format (YYYY-MM-DD) for TSB calculation

    Returns:
        Dictionary containing TSB value, interpretation, and metadata,
        or error dictionary
    """
    try:
        # Calculate CTL (fitness)
        ctl_result = await compute_fitness(target_date)
        if "error" in ctl_result:
            return {"error": ctl_result["error"]}

        # Calculate ATL (fatigue)
        atl_result = await compute_fatigue(target_date)
        if "error" in atl_result:
            return {"error": atl_result["error"]}

        # Calculate TSB (form)
        ctl = ctl_result.get("ctl", 0.0)
        atl = atl_result.get("atl", 0.0)
        tsb = ctl - atl

        # Interpret TSB value
        if tsb > 5:
            interpretation = "Fresh - Good readiness for hard training or competition"
        elif tsb > -5:
            interpretation = "Neutral - Balanced training load"
        else:
            interpretation = "Fatigued - Consider recovery or lighter training"

        return {
            "target_date": target_date,
            "tsb": round(tsb, 1),
            "ctl": ctl,
            "atl": atl,
            "interpretation": interpretation,
            "workouts_count": max(
                ctl_result.get("workouts_count", 0), atl_result.get("workouts_count", 0)
            ),
        }

    except Exception as e:
        logger.error(f"Error calculating TSB for {target_date}: {e}")
        return {"error": f"Failed to calculate TSB: {str(e)}"}


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
