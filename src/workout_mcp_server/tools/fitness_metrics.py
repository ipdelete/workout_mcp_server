"""Fitness metrics calculation utilities."""

import math
from collections.abc import Sequence
from datetime import datetime

from ..data_loader import Workout


def calculate_ewma(tss_values: Sequence[int], time_constant: int) -> float:
    """Calculate exponentially weighted moving average for TSS values.

    Args:
        tss_values: Sequence of TSS values in chronological order (oldest first)
        time_constant: Time constant in days (e.g., 42 for CTL, 7 for ATL)

    Returns:
        EWMA value as float

    Notes:
        - Uses alpha = 1 - exp(-1/time_constant) decay factor
        - Returns 0.0 if no TSS values provided
        - Assumes TSS values are in chronological order
    """
    if not tss_values:
        return 0.0

    # Calculate decay factor (alpha)
    alpha = 1 - math.exp(-1 / time_constant)

    # Initialize EWMA with first TSS value
    ewma = float(tss_values[0])

    # Calculate EWMA for remaining values
    for tss in tss_values[1:]:
        ewma = alpha * tss + (1 - alpha) * ewma

    return ewma


def get_workouts_for_ctl_calculation(
    workouts: list[Workout], target_date: datetime, days: int = 42
) -> list[Workout]:
    """Get workouts for CTL/ATL calculation up to target date.

    Args:
        workouts: All available workouts (should be sorted by date)
        target_date: Target date for calculation
        days: Number of days to look back (42 for CTL, 7 for ATL)

    Returns:
        List of workouts within the specified time window, sorted chronologically
    """
    # Filter workouts up to and including target date
    relevant_workouts = [
        workout for workout in workouts if workout.date.date() <= target_date.date()
    ]

    # Sort by date (oldest first) for EWMA calculation
    relevant_workouts.sort(key=lambda w: w.date)

    # Return all workouts if we have fewer than the desired window
    # This allows gradual buildup of fitness metrics for new athletes
    return relevant_workouts
