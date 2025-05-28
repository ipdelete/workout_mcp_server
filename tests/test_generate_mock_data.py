"""Tests for the mock data generation script."""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.generate_mock_data import (
    calculate_tss,
    generate_workout,
    generate_training_plan,
    generate_mock_workouts
)


class TestCalculateTSS:
    """Test TSS calculation logic."""
    
    def test_recovery_workout_tss(self):
        """Test TSS calculation for recovery workouts."""
        tss = calculate_tss(60, 150, "recovery")
        assert 20 <= tss <= 50
        
    def test_endurance_workout_tss(self):
        """Test TSS calculation for endurance workouts."""
        tss = calculate_tss(120, 180, "endurance")
        assert 40 <= tss <= 80
        
    def test_interval_workout_tss(self):
        """Test TSS calculation for interval workouts."""
        tss = calculate_tss(60, 250, "interval")
        assert 80 <= tss <= 150
        
    def test_tss_bounds(self):
        """Test that TSS is always within valid bounds."""
        tss = calculate_tss(30, 100, "recovery")
        assert tss >= 20
        
        tss = calculate_tss(300, 300, "race")
        assert tss <= 150


class TestGenerateWorkout:
    """Test workout generation."""
    
    def test_rest_day_returns_none(self):
        """Test that rest days return None."""
        workout = generate_workout(datetime.now().date(), "rest")
        assert workout is None
        
    def test_recovery_week_workout(self):
        """Test recovery week workout characteristics."""
        workout = generate_workout(datetime.now().date(), "recovery_week")
        assert workout["workout_type"] in ["recovery", "endurance"]
        assert 30 <= workout["duration_minutes"] <= 90
        assert 100 <= workout["avg_power_watts"] <= 180
        
    def test_intensity_workout(self):
        """Test intensity workout characteristics."""
        workout = generate_workout(datetime.now().date(), "intensity")
        assert workout["workout_type"] in ["threshold", "interval", "race"]
        assert 45 <= workout["duration_minutes"] <= 120
        assert 200 <= workout["avg_power_watts"] <= 300
        
    def test_workout_has_all_fields(self):
        """Test that generated workouts have all required fields."""
        workout = generate_workout(datetime.now().date(), "build")
        assert "id" in workout
        assert "date" in workout
        assert "duration_minutes" in workout
        assert "distance_km" in workout
        assert "avg_power_watts" in workout
        assert "tss" in workout
        assert "workout_type" in workout


class TestGenerateTrainingPlan:
    """Test training plan generation."""
    
    def test_plan_length(self):
        """Test that training plan has correct length."""
        plan = generate_training_plan(datetime.now().date(), 28)
        assert len(plan) == 28
        
    def test_recovery_week_pattern(self):
        """Test that every 4th week is a recovery week."""
        plan = generate_training_plan(datetime.now().date(), 28)
        week4_patterns = plan[21:28]
        recovery_count = sum(1 for p in week4_patterns if p == "recovery_week")
        rest_count = sum(1 for p in week4_patterns if p == "rest")
        assert recovery_count >= 3
        assert rest_count >= 2


class TestGenerateMockWorkouts:
    """Test full mock workout generation."""
    
    def test_generates_correct_number(self):
        """Test that exactly 50 workouts are generated."""
        workouts = generate_mock_workouts(50)
        assert len(workouts) == 50
        
    def test_date_range(self):
        """Test that workouts span approximately 3 months."""
        workouts = generate_mock_workouts(50)
        dates = [datetime.strptime(w["date"], "%Y-%m-%d") for w in workouts]
        date_range = (max(dates) - min(dates)).days
        assert 60 <= date_range <= 120
        
    def test_workout_variety(self):
        """Test that different workout types are represented."""
        workouts = generate_mock_workouts(50)
        workout_types = set(w["workout_type"] for w in workouts)
        assert len(workout_types) >= 4
        
    def test_realistic_tss_values(self):
        """Test that TSS values are realistic."""
        workouts = generate_mock_workouts(50)
        tss_values = [w["tss"] for w in workouts]
        avg_tss = sum(tss_values) / len(tss_values)
        assert 40 <= avg_tss <= 80
        assert all(20 <= tss <= 150 for tss in tss_values)
        
    def test_data_format(self):
        """Test that all workouts have correct data format."""
        workouts = generate_mock_workouts(50)
        for workout in workouts:
            assert isinstance(workout["id"], str)
            assert isinstance(workout["duration_minutes"], int)
            assert isinstance(workout["distance_km"], float)
            assert isinstance(workout["avg_power_watts"], int)
            assert isinstance(workout["tss"], int)
            assert workout["workout_type"] in [
                "recovery", "endurance", "tempo", "threshold", "interval", "race"
            ]
            datetime.strptime(workout["date"], "%Y-%m-%d")


class TestDataFile:
    """Test the generated data file."""
    
    def test_json_file_is_valid(self):
        """Test that the generated JSON file is valid."""
        data_file = Path(__file__).parent.parent / "data_store" / "workouts.json"
        if data_file.exists():
            with open(data_file) as f:
                data = json.load(f)
            assert isinstance(data, list)
            assert len(data) == 50