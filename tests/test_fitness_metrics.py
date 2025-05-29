"""Tests for fitness metrics calculations."""

import math
from datetime import datetime, timedelta

from workout_mcp_server.data_loader import Workout
from workout_mcp_server.tools.fitness_metrics import (
    calculate_ewma,
    get_workouts_for_ctl_calculation,
)


class TestCalculateEWMA:
    """Test exponentially weighted moving average calculation."""

    def test_empty_tss_values(self):
        """Test EWMA with empty TSS values."""
        result = calculate_ewma([], time_constant=42)
        assert result == 0.0

    def test_single_tss_value(self):
        """Test EWMA with single TSS value."""
        result = calculate_ewma([100], time_constant=42)
        assert result == 100.0

    def test_two_tss_values(self):
        """Test EWMA with two TSS values."""
        # alpha = 1 - exp(-1/42) ≈ 0.02353
        alpha = 1 - math.exp(-1 / 42)
        expected = alpha * 80 + (1 - alpha) * 100

        result = calculate_ewma([100, 80], time_constant=42)
        assert abs(result - expected) < 0.001

    def test_multiple_tss_values_ctl(self):
        """Test EWMA with multiple TSS values for CTL (42-day)."""
        tss_values = [100, 90, 110, 85, 95]
        result = calculate_ewma(tss_values, time_constant=42)

        # Result should be reasonable fitness value
        assert 80 <= result <= 120
        assert isinstance(result, float)

    def test_multiple_tss_values_atl(self):
        """Test EWMA with multiple TSS values for ATL (7-day)."""
        tss_values = [100, 90, 110, 85, 95]
        result = calculate_ewma(tss_values, time_constant=7)

        # ATL should be more responsive to recent values
        assert 80 <= result <= 120
        assert isinstance(result, float)

    def test_ewma_responsiveness(self):
        """Test that shorter time constants are more responsive."""
        tss_values = [50, 50, 50, 50, 100]  # Big jump at end

        ctl = calculate_ewma(tss_values, time_constant=42)
        atl = calculate_ewma(tss_values, time_constant=7)

        # ATL (7-day) should be closer to the recent high value than CTL (42-day)
        assert atl > ctl
        assert atl > 50  # Should be pulled up by the 100
        assert ctl < atl  # CTL should be less responsive

    def test_increasing_trend(self):
        """Test EWMA with increasing TSS trend."""
        tss_values = [50, 60, 70, 80, 90]
        result = calculate_ewma(tss_values, time_constant=42)

        # Should be somewhere between start and end values
        assert 50 < result < 90
        # Should be closer to start value due to long time constant (42 days)
        assert result < 60  # With 42-day constant, change is very gradual

    def test_decreasing_trend(self):
        """Test EWMA with decreasing TSS trend."""
        tss_values = [90, 80, 70, 60, 50]
        result = calculate_ewma(tss_values, time_constant=42)

        # Should be somewhere between start and end values
        assert 50 < result < 90
        # Should be closer to start value due to long time constant (42 days)
        assert result > 80  # With 42-day constant, change is very gradual


class TestGetWorkoutsForCtlCalculation:
    """Test workout filtering for CTL calculation."""

    def create_workout(self, date_str: str, tss: int = 75) -> Workout:
        """Helper to create workout for testing."""
        return Workout(
            id=f"test-{date_str}",
            date=datetime.fromisoformat(date_str),
            duration_minutes=60,
            distance_km=30.0,
            avg_power_watts=200,
            tss=tss,
            workout_type="endurance",
        )

    def test_empty_workouts(self):
        """Test with no workouts available."""
        workouts = []
        target_date = datetime(2024, 2, 15)

        result = get_workouts_for_ctl_calculation(workouts, target_date)
        assert result == []

    def test_workouts_before_target_date(self):
        """Test filtering workouts before target date."""
        workouts = [
            self.create_workout("2024-02-10"),
            self.create_workout("2024-02-12"),
            self.create_workout("2024-02-15"),
            self.create_workout("2024-02-20"),  # After target date
        ]
        target_date = datetime(2024, 2, 15)

        result = get_workouts_for_ctl_calculation(workouts, target_date)

        # Should include workouts up to and including target date
        assert len(result) == 3
        assert result[0].date.date() == datetime(2024, 2, 10).date()
        assert result[1].date.date() == datetime(2024, 2, 12).date()
        assert result[2].date.date() == datetime(2024, 2, 15).date()

    def test_workouts_sorted_chronologically(self):
        """Test that returned workouts are sorted chronologically."""
        workouts = [
            self.create_workout("2024-02-15"),
            self.create_workout("2024-02-10"),
            self.create_workout("2024-02-12"),
        ]
        target_date = datetime(2024, 2, 16)

        result = get_workouts_for_ctl_calculation(workouts, target_date)

        # Should be sorted oldest first
        assert len(result) == 3
        assert result[0].date.date() == datetime(2024, 2, 10).date()
        assert result[1].date.date() == datetime(2024, 2, 12).date()
        assert result[2].date.date() == datetime(2024, 2, 15).date()

    def test_workout_on_target_date_included(self):
        """Test that workout on target date is included."""
        workouts = [
            self.create_workout("2024-02-15"),
        ]
        target_date = datetime(2024, 2, 15)

        result = get_workouts_for_ctl_calculation(workouts, target_date)

        assert len(result) == 1
        assert result[0].date.date() == datetime(2024, 2, 15).date()

    def test_many_workouts_within_window(self):
        """Test with many workouts within calculation window."""
        # Create 60 days of workouts (more than 42-day CTL window)
        workouts = []
        base_date = datetime(2024, 1, 1)
        for i in range(60):
            workout_date = base_date + timedelta(days=i)
            workouts.append(self.create_workout(workout_date.strftime("%Y-%m-%d")))

        target_date = datetime(2024, 2, 29)  # February 29, 2024 (day 59, 0-indexed)

        result = get_workouts_for_ctl_calculation(workouts, target_date)

        # Should return all workouts up to and including target date
        # Days 0-59 (inclusive) = 60 workouts
        assert len(result) == 60
        assert result[0].date.date() == datetime(2024, 1, 1).date()
        assert result[-1].date.date() == datetime(2024, 2, 29).date()

    def test_different_time_constants(self):
        """Test that function works for different time constants."""
        workouts = [
            self.create_workout("2024-02-10"),
            self.create_workout("2024-02-12"),
            self.create_workout("2024-02-15"),
        ]
        target_date = datetime(2024, 2, 16)

        # Test with 7-day window (for ATL)
        result_7day = get_workouts_for_ctl_calculation(workouts, target_date, days=7)
        # Test with 42-day window (for CTL)
        result_42day = get_workouts_for_ctl_calculation(workouts, target_date, days=42)

        # Both should return same workouts since all are within 7 days
        assert len(result_7day) == len(result_42day) == 3
        assert result_7day == result_42day
