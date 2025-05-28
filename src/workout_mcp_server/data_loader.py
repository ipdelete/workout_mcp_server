"""Data loading module for workout MCP server.

This module provides functionality to load, parse, and manipulate workout data
from JSON files using Pydantic for validation.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)


class WorkoutDataError(Exception):
    """Exception raised for errors in workout data loading or validation."""

    pass


class Workout(BaseModel):
    """Pydantic model for workout data validation and parsing."""

    id: str
    date: datetime
    duration_minutes: int = Field(
        gt=0, description="Duration in minutes must be positive"
    )
    distance_km: float = Field(
        ge=0, description="Distance in kilometers must be non-negative"
    )
    avg_power_watts: int = Field(
        ge=0, description="Average power in watts must be non-negative"
    )
    tss: int = Field(ge=0, description="Training Stress Score must be non-negative")
    workout_type: str

    @field_validator("date", mode="before")
    @classmethod
    def parse_date(cls, v: str | datetime) -> datetime:
        """Parse date string to datetime object."""
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                raise ValueError(f"Invalid date format: {v}")
        raise ValueError(f"Date must be string or datetime, got {type(v)}")


def load_workouts(file_path: Path) -> list[Workout]:
    """Load workout data from a JSON file.

    Args:
        file_path: Path to the JSON file containing workout data.

    Returns:
        List of validated Workout objects.

    Raises:
        WorkoutDataError: If file cannot be read or contains invalid data.
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise WorkoutDataError(f"Workout data file not found: {file_path}")
    except json.JSONDecodeError as e:
        raise WorkoutDataError(f"Invalid JSON in workout data file: {e}")
    except Exception as e:
        raise WorkoutDataError(f"Error reading workout data file: {e}")

    if not isinstance(data, list):
        raise WorkoutDataError("Workout data must be a list")

    # Validate and parse each workout
    workouts = []
    for i, workout_data in enumerate(data):
        try:
            workout = Workout(**workout_data)
            workouts.append(workout)
        except Exception as e:
            raise WorkoutDataError(f"Invalid workout at index {i}: {e}")

    return workouts


def sort_workouts_by_date(
    workouts: list[Workout], descending: bool = True
) -> list[Workout]:
    """Sort workouts by date.

    Args:
        workouts: List of Workout objects.
        descending: If True, sort from newest to oldest.

    Returns:
        Sorted list of Workout objects.
    """
    return sorted(workouts, key=lambda w: w.date, reverse=descending)


def filter_workouts_by_date_range(
    workouts: list[Workout],
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> list[Workout]:
    """Filter workouts by date range.

    Args:
        workouts: List of Workout objects.
        start_date: Minimum date (inclusive). If None, no lower bound.
        end_date: Maximum date (inclusive). If None, no upper bound.

    Returns:
        Filtered list of Workout objects.
    """
    filtered = []
    for workout in workouts:
        if start_date and workout.date < start_date:
            continue
        if end_date and workout.date > end_date:
            continue
        filtered.append(workout)

    return filtered


class WorkoutDataLoader:
    """Main class for loading and managing workout data."""

    def __init__(self, file_path: Path) -> None:
        """Initialize the workout data loader.

        Args:
            file_path: Path to the JSON file containing workout data.
        """
        self.file_path = file_path
        self._cached_data: list[Workout] | None = None

    def load(self) -> list[Workout]:
        """Load and validate workout data, with caching.

        Returns:
            List of validated Workout objects.

        Raises:
            WorkoutDataError: If data cannot be loaded or is invalid.
        """
        if self._cached_data is not None:
            return self._cached_data

        logger.info(f"Loading workout data from {self.file_path}")
        self._cached_data = load_workouts(self.file_path)
        logger.info(f"Successfully loaded {len(self._cached_data)} workouts")

        return self._cached_data

    def get_all_workouts(self, sort_by_date: bool = True) -> list[Workout]:
        """Get all workouts, optionally sorted by date.

        Args:
            sort_by_date: If True, sort workouts by date (newest first).

        Returns:
            List of Workout objects.
        """
        workouts = self.load()
        if sort_by_date:
            return sort_workouts_by_date(workouts, descending=True)
        return workouts

    def get_workouts_by_date_range(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        sort_by_date: bool = True,
    ) -> list[Workout]:
        """Get workouts within a date range.

        Args:
            start_date: Minimum date (inclusive).
            end_date: Maximum date (inclusive).
            sort_by_date: If True, sort results by date (newest first).

        Returns:
            Filtered list of Workout objects.
        """
        workouts = self.load()
        filtered = filter_workouts_by_date_range(workouts, start_date, end_date)
        if sort_by_date:
            return sort_workouts_by_date(filtered, descending=True)
        return filtered

    def get_workout_by_id(self, workout_id: str) -> Workout | None:
        """Get a specific workout by ID.

        Args:
            workout_id: The ID of the workout to retrieve.

        Returns:
            Workout object if found, None otherwise.
        """
        workouts = self.load()
        for workout in workouts:
            if workout.id == workout_id:
                return workout
        return None

    def clear_cache(self) -> None:
        """Clear the cached workout data."""
        self._cached_data = None
