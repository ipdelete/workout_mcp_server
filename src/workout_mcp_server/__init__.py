"""Workout MCP Server - MCP server for cycling workout analytics."""

from .data_loader import Workout, WorkoutDataError, WorkoutDataLoader

__version__ = "0.1.0"
__all__ = ["Workout", "WorkoutDataError", "WorkoutDataLoader", "__version__"]
