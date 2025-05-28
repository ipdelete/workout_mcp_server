"""Tests for the workout data loader module."""

import json
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from workout_mcp_server.data_loader import (
    Workout,
    WorkoutDataError,
    WorkoutDataLoader,
    filter_workouts_by_date_range,
    load_workouts,
    sort_workouts_by_date,
)


class TestWorkoutModel:
    """Tests for the Workout Pydantic model."""

    def test_valid_workout_from_dict(self):
        """Test creating a valid workout from dictionary."""
        data = {
            "id": "123",
            "date": "2024-01-15",
            "duration_minutes": 60,
            "distance_km": 30.5,
            "avg_power_watts": 200,
            "tss": 75,
            "workout_type": "endurance",
        }
        workout = Workout(**data)

        assert workout.id == "123"
        assert workout.date == datetime(2024, 1, 15)
        assert workout.duration_minutes == 60
        assert workout.distance_km == 30.5
        assert workout.avg_power_watts == 200
        assert workout.tss == 75
        assert workout.workout_type == "endurance"

    def test_workout_with_datetime_object(self):
        """Test creating a workout with a datetime object instead of string."""
        data = {
            "id": "123",
            "date": datetime(2024, 1, 15),
            "duration_minutes": 60,
            "distance_km": 30.5,
            "avg_power_watts": 200,
            "tss": 75,
            "workout_type": "endurance",
        }
        workout = Workout(**data)
        assert workout.date == datetime(2024, 1, 15)

    def test_invalid_date_format(self):
        """Test validation fails with invalid date format."""
        data = {
            "id": "123",
            "date": "01/15/2024",  # Invalid format
            "duration_minutes": 60,
            "distance_km": 30.5,
            "avg_power_watts": 200,
            "tss": 75,
            "workout_type": "endurance",
        }
        with pytest.raises(ValidationError, match="Invalid date format"):
            Workout(**data)

    def test_negative_duration(self):
        """Test validation fails with negative duration."""
        data = {
            "id": "123",
            "date": "2024-01-15",
            "duration_minutes": -10,
            "distance_km": 30.5,
            "avg_power_watts": 200,
            "tss": 75,
            "workout_type": "endurance",
        }
        with pytest.raises(ValidationError, match="greater than 0"):
            Workout(**data)

    def test_negative_distance(self):
        """Test validation fails with negative distance."""
        data = {
            "id": "123",
            "date": "2024-01-15",
            "duration_minutes": 60,
            "distance_km": -5.0,
            "avg_power_watts": 200,
            "tss": 75,
            "workout_type": "endurance",
        }
        with pytest.raises(ValidationError, match="greater than or equal to 0"):
            Workout(**data)

    def test_negative_power(self):
        """Test validation fails with negative power."""
        data = {
            "id": "123",
            "date": "2024-01-15",
            "duration_minutes": 60,
            "distance_km": 30.5,
            "avg_power_watts": -100,
            "tss": 75,
            "workout_type": "endurance",
        }
        with pytest.raises(ValidationError, match="greater than or equal to 0"):
            Workout(**data)

    def test_negative_tss(self):
        """Test validation fails with negative TSS."""
        data = {
            "id": "123",
            "date": "2024-01-15",
            "duration_minutes": 60,
            "distance_km": 30.5,
            "avg_power_watts": 200,
            "tss": -10,
            "workout_type": "endurance",
        }
        with pytest.raises(ValidationError, match="greater than or equal to 0"):
            Workout(**data)

    def test_missing_required_field(self):
        """Test validation fails when required field is missing."""
        data = {
            "id": "123",
            "date": "2024-01-15",
            "duration_minutes": 60,
            # Missing other required fields
        }
        with pytest.raises(ValidationError):
            Workout(**data)


class TestLoadWorkouts:
    """Tests for the load_workouts function."""

    def test_load_valid_json_file(self, tmp_path):
        """Test loading a valid JSON file."""
        test_data = [
            {
                "id": "1",
                "date": "2024-01-15",
                "duration_minutes": 60,
                "distance_km": 30.5,
                "avg_power_watts": 200,
                "tss": 75,
                "workout_type": "endurance",
            }
        ]
        file_path = tmp_path / "test.json"
        file_path.write_text(json.dumps(test_data))

        result = load_workouts(file_path)
        assert len(result) == 1
        assert isinstance(result[0], Workout)
        assert result[0].id == "1"

    def test_file_not_found(self):
        """Test error handling when file doesn't exist."""
        with pytest.raises(WorkoutDataError, match="Workout data file not found"):
            load_workouts(Path("/nonexistent/file.json"))

    def test_invalid_json(self, tmp_path):
        """Test error handling for invalid JSON."""
        file_path = tmp_path / "invalid.json"
        file_path.write_text("{invalid json")

        with pytest.raises(WorkoutDataError, match="Invalid JSON"):
            load_workouts(file_path)

    def test_non_list_data(self, tmp_path):
        """Test error when JSON root is not a list."""
        file_path = tmp_path / "not_list.json"
        file_path.write_text('{"not": "a list"}')

        with pytest.raises(WorkoutDataError, match="Workout data must be a list"):
            load_workouts(file_path)

    def test_invalid_workout_data(self, tmp_path):
        """Test error handling for invalid workout data."""
        test_data = [
            {
                "id": "1",
                "date": "2024-01-15",
                # Missing required fields
            }
        ]
        file_path = tmp_path / "invalid_workout.json"
        file_path.write_text(json.dumps(test_data))

        with pytest.raises(WorkoutDataError, match="Invalid workout at index 0"):
            load_workouts(file_path)


class TestSortWorkoutsByDate:
    """Tests for the sort_workouts_by_date function."""

    @pytest.fixture
    def sample_workouts(self):
        """Create sample workout objects for testing."""
        return [
            Workout(
                id="1",
                date="2024-01-15",
                duration_minutes=60,
                distance_km=30.5,
                avg_power_watts=200,
                tss=75,
                workout_type="endurance",
            ),
            Workout(
                id="2",
                date="2024-01-17",
                duration_minutes=45,
                distance_km=25.0,
                avg_power_watts=250,
                tss=85,
                workout_type="interval",
            ),
            Workout(
                id="3",
                date="2024-01-16",
                duration_minutes=30,
                distance_km=15.0,
                avg_power_watts=150,
                tss=40,
                workout_type="recovery",
            ),
        ]

    def test_sort_descending(self, sample_workouts):
        """Test sorting workouts by date in descending order."""
        result = sort_workouts_by_date(sample_workouts, descending=True)

        assert result[0].id == "2"  # Jan 17
        assert result[1].id == "3"  # Jan 16
        assert result[2].id == "1"  # Jan 15

    def test_sort_ascending(self, sample_workouts):
        """Test sorting workouts by date in ascending order."""
        result = sort_workouts_by_date(sample_workouts, descending=False)

        assert result[0].id == "1"  # Jan 15
        assert result[1].id == "3"  # Jan 16
        assert result[2].id == "2"  # Jan 17


class TestFilterWorkoutsByDateRange:
    """Tests for the filter_workouts_by_date_range function."""

    @pytest.fixture
    def sample_workouts(self):
        """Create sample workout objects for testing."""
        return [
            Workout(
                id="1",
                date="2024-01-10",
                duration_minutes=60,
                distance_km=30.5,
                avg_power_watts=200,
                tss=75,
                workout_type="endurance",
            ),
            Workout(
                id="2",
                date="2024-01-15",
                duration_minutes=45,
                distance_km=25.0,
                avg_power_watts=250,
                tss=85,
                workout_type="interval",
            ),
            Workout(
                id="3",
                date="2024-01-20",
                duration_minutes=30,
                distance_km=15.0,
                avg_power_watts=150,
                tss=40,
                workout_type="recovery",
            ),
            Workout(
                id="4",
                date="2024-01-25",
                duration_minutes=90,
                distance_km=45.0,
                avg_power_watts=180,
                tss=100,
                workout_type="endurance",
            ),
        ]

    def test_filter_with_both_dates(self, sample_workouts):
        """Test filtering with both start and end dates."""
        start = datetime(2024, 1, 12)
        end = datetime(2024, 1, 22)

        result = filter_workouts_by_date_range(sample_workouts, start, end)

        assert len(result) == 2
        assert result[0].id == "2"
        assert result[1].id == "3"

    def test_filter_with_start_date_only(self, sample_workouts):
        """Test filtering with only start date."""
        start = datetime(2024, 1, 15)

        result = filter_workouts_by_date_range(sample_workouts, start_date=start)

        assert len(result) == 3
        assert result[0].id == "2"
        assert result[1].id == "3"
        assert result[2].id == "4"

    def test_filter_with_end_date_only(self, sample_workouts):
        """Test filtering with only end date."""
        end = datetime(2024, 1, 15)

        result = filter_workouts_by_date_range(sample_workouts, end_date=end)

        assert len(result) == 2
        assert result[0].id == "1"
        assert result[1].id == "2"

    def test_filter_with_no_dates(self, sample_workouts):
        """Test filtering with no date constraints returns all workouts."""
        result = filter_workouts_by_date_range(sample_workouts)
        assert len(result) == 4


class TestWorkoutDataLoader:
    """Tests for the WorkoutDataLoader class."""

    @pytest.fixture
    def sample_workouts_data(self):
        """Sample workout data for testing."""
        return [
            {
                "id": "1",
                "date": "2024-01-15",
                "duration_minutes": 60,
                "distance_km": 30.5,
                "avg_power_watts": 200,
                "tss": 75,
                "workout_type": "endurance",
            },
            {
                "id": "2",
                "date": "2024-01-17",
                "duration_minutes": 45,
                "distance_km": 25.0,
                "avg_power_watts": 250,
                "tss": 85,
                "workout_type": "interval",
            },
            {
                "id": "3",
                "date": "2024-01-16",
                "duration_minutes": 30,
                "distance_km": 15.0,
                "avg_power_watts": 150,
                "tss": 40,
                "workout_type": "recovery",
            },
        ]

    def test_load_and_cache(self, tmp_path, sample_workouts_data):
        """Test loading data and caching behavior."""
        file_path = tmp_path / "workouts.json"
        file_path.write_text(json.dumps(sample_workouts_data))

        loader = WorkoutDataLoader(file_path)

        # First load
        result1 = loader.load()
        assert len(result1) == 3
        assert all(isinstance(w, Workout) for w in result1)
        assert all(isinstance(w.date, datetime) for w in result1)

        # Second load should use cache
        with patch("builtins.open", side_effect=Exception("Should not open file")):
            result2 = loader.load()
            assert result2 == result1

    def test_get_all_workouts_sorted(self, tmp_path, sample_workouts_data):
        """Test getting all workouts sorted by date."""
        file_path = tmp_path / "workouts.json"
        file_path.write_text(json.dumps(sample_workouts_data))

        loader = WorkoutDataLoader(file_path)
        result = loader.get_all_workouts(sort_by_date=True)

        assert len(result) == 3
        assert result[0].id == "2"  # Jan 17
        assert result[1].id == "3"  # Jan 16
        assert result[2].id == "1"  # Jan 15

    def test_get_workouts_by_date_range(self, tmp_path, sample_workouts_data):
        """Test getting workouts within a date range."""
        file_path = tmp_path / "workouts.json"
        file_path.write_text(json.dumps(sample_workouts_data))

        loader = WorkoutDataLoader(file_path)
        start = datetime(2024, 1, 16)
        end = datetime(2024, 1, 17)

        result = loader.get_workouts_by_date_range(start, end)

        assert len(result) == 2
        assert result[0].id == "2"  # Jan 17
        assert result[1].id == "3"  # Jan 16

    def test_get_workout_by_id(self, tmp_path, sample_workouts_data):
        """Test getting a specific workout by ID."""
        file_path = tmp_path / "workouts.json"
        file_path.write_text(json.dumps(sample_workouts_data))

        loader = WorkoutDataLoader(file_path)

        result = loader.get_workout_by_id("2")
        assert result is not None
        assert result.id == "2"
        assert result.workout_type == "interval"

        # Test non-existent ID
        result = loader.get_workout_by_id("999")
        assert result is None

    def test_clear_cache(self, tmp_path, sample_workouts_data):
        """Test clearing the cache."""
        file_path = tmp_path / "workouts.json"
        file_path.write_text(json.dumps(sample_workouts_data))

        loader = WorkoutDataLoader(file_path)

        # Load data
        loader.load()
        assert loader._cached_data is not None

        # Clear cache
        loader.clear_cache()
        assert loader._cached_data is None

    def test_validation_error_propagation(self, tmp_path):
        """Test that validation errors are properly propagated."""
        invalid_data = [
            {
                "id": "1",
                "date": "2024-01-15",
                # Missing required fields
            }
        ]
        file_path = tmp_path / "invalid.json"
        file_path.write_text(json.dumps(invalid_data))

        loader = WorkoutDataLoader(file_path)

        with pytest.raises(WorkoutDataError, match="Invalid workout at index 0"):
            loader.load()

    def test_get_all_workouts_unsorted(self, tmp_path, sample_workouts_data):
        """Test getting all workouts without sorting."""
        file_path = tmp_path / "workouts.json"
        file_path.write_text(json.dumps(sample_workouts_data))

        loader = WorkoutDataLoader(file_path)
        result = loader.get_all_workouts(sort_by_date=False)

        assert len(result) == 3
        # Order should match the original file order
        assert result[0].id == "1"
        assert result[1].id == "2"
        assert result[2].id == "3"
