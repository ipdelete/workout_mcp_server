"""Tests for workout_mcp_server."""

from workout_mcp_server import __version__


def test_version():
    """Test that the version is defined."""
    assert __version__ == "0.1.0"


def test_import():
    """Test that we can import the main module."""
    from workout_mcp_server import main

    assert hasattr(main, "main")


def test_mcp_instance():
    """Test that the MCP server instance is created."""
    from workout_mcp_server.main import mcp

    assert mcp is not None
    assert mcp.name == "workout-mcp-server"


def test_configure_logging():
    """Test that logging can be configured."""
    from workout_mcp_server.main import configure_logging

    # Should not raise any exceptions
    configure_logging()


def test_main_function_exists():
    """Test that main function exists and is callable."""
    from workout_mcp_server.main import main

    assert callable(main)


def test_get_workout_by_id_tool_exists():
    """Test that get_workout_by_id tool is registered."""
    from workout_mcp_server.main import get_workout_by_id

    assert callable(get_workout_by_id)
    assert hasattr(get_workout_by_id, "__doc__")
    assert "Get details of a specific workout by ID" in get_workout_by_id.__doc__


async def test_get_workout_by_id_success():
    """Test successful retrieval of a workout by ID."""
    from datetime import datetime
    from unittest.mock import patch

    from workout_mcp_server.data_loader import Workout
    from workout_mcp_server.main import get_workout_by_id

    # Create a mock workout
    mock_workout = Workout(
        id="test-123",
        date=datetime(2024, 1, 15),
        duration_minutes=90,
        distance_km=45.0,
        avg_power_watts=200,
        tss=85,
        workout_type="threshold",
    )

    # Mock the data_loader
    with patch("workout_mcp_server.main.data_loader") as mock_loader:
        mock_loader.get_workout_by_id.return_value = mock_workout

        result = await get_workout_by_id("test-123")

        assert result["id"] == "test-123"
        assert result["date"] == "2024-01-15"
        assert result["duration_minutes"] == 90
        assert result["distance_km"] == 45.0
        assert result["avg_power_watts"] == 200
        assert result["tss"] == 85
        assert result["workout_type"] == "threshold"
        assert "error" not in result

        mock_loader.get_workout_by_id.assert_called_once_with("test-123")


async def test_get_workout_by_id_not_found():
    """Test retrieval of non-existent workout."""
    from unittest.mock import patch

    from workout_mcp_server.main import get_workout_by_id

    with patch("workout_mcp_server.main.data_loader") as mock_loader:
        mock_loader.get_workout_by_id.return_value = None

        result = await get_workout_by_id("non-existent-id")

        assert "error" in result
        assert result["error"] == "Workout with ID 'non-existent-id' not found"

        mock_loader.get_workout_by_id.assert_called_once_with("non-existent-id")


async def test_get_workout_by_id_exception():
    """Test handling of exceptions during workout retrieval."""
    from unittest.mock import patch

    from workout_mcp_server.main import get_workout_by_id

    with patch("workout_mcp_server.main.data_loader") as mock_loader:
        mock_loader.get_workout_by_id.side_effect = Exception("Database error")

        result = await get_workout_by_id("test-123")

        assert "error" in result
        assert "Failed to retrieve workout" in result["error"]
        assert "Database error" in result["error"]


def test_get_last_7_workouts_tool_exists():
    """Test that get_last_7_workouts tool is registered."""
    from workout_mcp_server.main import get_last_7_workouts

    assert callable(get_last_7_workouts)
    assert hasattr(get_last_7_workouts, "__doc__")
    assert "7 most recent workouts" in get_last_7_workouts.__doc__


async def test_get_last_7_workouts_success():
    """Test successful retrieval of 7 most recent workouts."""
    from datetime import datetime
    from unittest.mock import patch

    from workout_mcp_server.data_loader import Workout
    from workout_mcp_server.main import get_last_7_workouts

    # Create mock workouts (already sorted by date, newest first)
    mock_workouts = [
        Workout(
            id=f"test-{i}",
            date=datetime(2024, 1, 20 - i),
            duration_minutes=60 + i,
            distance_km=30.0 + i,
            avg_power_watts=200 + i,
            tss=75 + i,
            workout_type="endurance",
        )
        for i in range(10)
    ]

    with patch("workout_mcp_server.main.data_loader") as mock_loader:
        mock_loader.get_all_workouts.return_value = mock_workouts

        result = await get_last_7_workouts()

        # Should return exactly 7 workouts
        assert isinstance(result, list)
        assert len(result) == 7

        # Should be ordered by date (newest first)
        assert result[0]["id"] == "test-0"
        assert result[0]["date"] == "2024-01-20"
        assert result[6]["id"] == "test-6"
        assert result[6]["date"] == "2024-01-14"

        # Check that each workout has all required fields
        for workout_dict in result:
            assert "id" in workout_dict
            assert "date" in workout_dict
            assert "duration_minutes" in workout_dict
            assert "distance_km" in workout_dict
            assert "avg_power_watts" in workout_dict
            assert "tss" in workout_dict
            assert "workout_type" in workout_dict
            assert "error" not in workout_dict

        mock_loader.get_all_workouts.assert_called_once_with(sort_by_date=True)


async def test_get_last_7_workouts_fewer_than_7():
    """Test retrieval when fewer than 7 workouts exist."""
    from datetime import datetime
    from unittest.mock import patch

    from workout_mcp_server.data_loader import Workout
    from workout_mcp_server.main import get_last_7_workouts

    # Create only 3 mock workouts
    mock_workouts = [
        Workout(
            id=f"test-{i}",
            date=datetime(2024, 1, 20 - i),
            duration_minutes=60,
            distance_km=30.0,
            avg_power_watts=200,
            tss=75,
            workout_type="endurance",
        )
        for i in range(3)
    ]

    with patch("workout_mcp_server.main.data_loader") as mock_loader:
        mock_loader.get_all_workouts.return_value = mock_workouts

        result = await get_last_7_workouts()

        # Should return all 3 workouts (not 7)
        assert isinstance(result, list)
        assert len(result) == 3

        # Verify each workout has required fields
        for workout_dict in result:
            assert "id" in workout_dict
            assert "date" in workout_dict
            assert "error" not in workout_dict

        mock_loader.get_all_workouts.assert_called_once_with(sort_by_date=True)


async def test_get_last_7_workouts_exception():
    """Test handling of exceptions during workout retrieval."""
    from unittest.mock import patch

    from workout_mcp_server.main import get_last_7_workouts

    with patch("workout_mcp_server.main.data_loader") as mock_loader:
        mock_loader.get_all_workouts.side_effect = Exception("Database error")

        result = await get_last_7_workouts()

        assert isinstance(result, dict)
        assert "error" in result
        assert "Failed to retrieve workouts" in result["error"]
        assert "Database error" in result["error"]


def test_get_last_50_workouts_tool_exists():
    """Test that get_last_50_workouts tool is registered."""
    from workout_mcp_server.main import get_last_50_workouts

    assert callable(get_last_50_workouts)
    assert hasattr(get_last_50_workouts, "__doc__")
    assert "all 50 workouts" in get_last_50_workouts.__doc__
    assert "complete training history" in get_last_50_workouts.__doc__


async def test_get_last_50_workouts_success():
    """Test successful retrieval of all 50 workouts."""
    from datetime import datetime, timedelta
    from unittest.mock import patch

    from workout_mcp_server.data_loader import Workout
    from workout_mcp_server.main import get_last_50_workouts

    # Create mock workouts (50 workouts)
    mock_workouts = [
        Workout(
            id=f"test-{i:02d}",
            date=datetime(2024, 1, 1) + timedelta(days=i),
            duration_minutes=60 + i,
            distance_km=30.0 + i,
            avg_power_watts=200 + i,
            tss=75 + i,
            workout_type="endurance",
        )
        for i in range(50)
    ]

    with patch("workout_mcp_server.main.data_loader") as mock_loader:
        mock_loader.get_all_workouts.return_value = mock_workouts

        result = await get_last_50_workouts()

        # Should return exactly 50 workouts
        assert isinstance(result, list)
        assert len(result) == 50

        # Should be ordered by date (already sorted by data_loader)
        assert result[0]["id"] == "test-00"
        assert result[49]["id"] == "test-49"

        # Check that each workout has all required fields
        for workout_dict in result:
            assert "id" in workout_dict
            assert "date" in workout_dict
            assert "duration_minutes" in workout_dict
            assert "distance_km" in workout_dict
            assert "avg_power_watts" in workout_dict
            assert "tss" in workout_dict
            assert "workout_type" in workout_dict
            assert "error" not in workout_dict

        mock_loader.get_all_workouts.assert_called_once_with(sort_by_date=True)


async def test_get_last_50_workouts_fewer_than_50():
    """Test retrieval when fewer than 50 workouts exist."""
    from datetime import datetime, timedelta
    from unittest.mock import patch

    from workout_mcp_server.data_loader import Workout
    from workout_mcp_server.main import get_last_50_workouts

    # Create only 30 mock workouts
    mock_workouts = [
        Workout(
            id=f"test-{i:02d}",
            date=datetime(2024, 1, 1) + timedelta(days=i),
            duration_minutes=60,
            distance_km=30.0,
            avg_power_watts=200,
            tss=75,
            workout_type="endurance",
        )
        for i in range(30)
    ]

    with patch("workout_mcp_server.main.data_loader") as mock_loader:
        mock_loader.get_all_workouts.return_value = mock_workouts

        result = await get_last_50_workouts()

        # Should return all 30 workouts (not 50)
        assert isinstance(result, list)
        assert len(result) == 30

        # Verify each workout has required fields
        for workout_dict in result:
            assert "id" in workout_dict
            assert "date" in workout_dict
            assert "error" not in workout_dict

        mock_loader.get_all_workouts.assert_called_once_with(sort_by_date=True)


async def test_get_last_50_workouts_exception():
    """Test handling of exceptions during workout retrieval."""
    from unittest.mock import patch

    from workout_mcp_server.main import get_last_50_workouts

    with patch("workout_mcp_server.main.data_loader") as mock_loader:
        mock_loader.get_all_workouts.side_effect = Exception("Database error")

        result = await get_last_50_workouts()

        assert isinstance(result, dict)
        assert "error" in result
        assert "Failed to retrieve workouts" in result["error"]
        assert "Database error" in result["error"]


def test_compute_fitness_tool_exists():
    """Test that compute_fitness tool is registered."""
    from workout_mcp_server.main import compute_fitness

    assert callable(compute_fitness)
    assert hasattr(compute_fitness, "__doc__")
    assert "Chronic Training Load" in compute_fitness.__doc__
    assert "CTL" in compute_fitness.__doc__


async def test_compute_fitness_success():
    """Test successful CTL calculation."""
    from datetime import datetime, timedelta
    from unittest.mock import patch

    from workout_mcp_server.data_loader import Workout
    from workout_mcp_server.main import compute_fitness

    # Create mock workouts over several weeks
    mock_workouts = []
    base_date = datetime(2024, 1, 1)
    for i in range(30):  # 30 days of workouts
        workout_date = base_date + timedelta(days=i)
        mock_workouts.append(
            Workout(
                id=f"test-{i:02d}",
                date=workout_date,
                duration_minutes=60 + (i % 10),
                distance_km=30.0 + (i % 5),
                avg_power_watts=200 + (i % 20),
                tss=75 + (i % 25),  # TSS varies from 75-99
                workout_type="endurance",
            )
        )

    with patch("workout_mcp_server.main.data_loader") as mock_loader:
        mock_loader.get_all_workouts.return_value = mock_workouts

        result = await compute_fitness("2024-01-30")

        assert isinstance(result, dict)
        assert "error" not in result
        assert result["target_date"] == "2024-01-30"
        assert "ctl" in result
        assert isinstance(result["ctl"], float)
        assert result["ctl"] > 0  # Should have positive CTL with workouts
        assert result["workouts_count"] == 30
        assert "date_range" in result
        assert result["date_range"]["earliest_workout"] == "2024-01-01"
        assert result["date_range"]["latest_workout"] == "2024-01-30"

        mock_loader.get_all_workouts.assert_called_once_with(sort_by_date=False)


async def test_compute_fitness_no_workouts():
    """Test CTL calculation with no workout data."""
    from unittest.mock import patch

    from workout_mcp_server.main import compute_fitness

    with patch("workout_mcp_server.main.data_loader") as mock_loader:
        mock_loader.get_all_workouts.return_value = []

        result = await compute_fitness("2024-01-15")

        assert isinstance(result, dict)
        assert "error" not in result
        assert result["target_date"] == "2024-01-15"
        assert result["ctl"] == 0.0
        assert result["workouts_count"] == 0
        assert "message" in result
        assert "No workout data available" in result["message"]


async def test_compute_fitness_invalid_date():
    """Test CTL calculation with invalid date format."""
    from workout_mcp_server.main import compute_fitness

    result = await compute_fitness("invalid-date")

    assert isinstance(result, dict)
    assert "error" in result
    assert "Invalid date format" in result["error"]
    assert "invalid-date" in result["error"]
    assert "YYYY-MM-DD" in result["error"]


async def test_compute_fitness_realistic_values():
    """Test CTL calculation produces realistic fitness values."""
    from datetime import datetime, timedelta
    from unittest.mock import patch

    from workout_mcp_server.data_loader import Workout
    from workout_mcp_server.main import compute_fitness

    # Create workouts with realistic TSS progression
    mock_workouts = []
    base_date = datetime(2024, 1, 1)
    tss_values = [
        85,
        95,
        60,
        110,
        0,
        0,
        125,
        90,
        80,
        105,
    ]  # Week pattern with rest days

    for i in range(50):  # 50 days of workouts
        workout_date = base_date + timedelta(days=i)
        tss = tss_values[i % len(tss_values)]

        if tss > 0:  # Only create workout if TSS > 0 (no rest days)
            mock_workouts.append(
                Workout(
                    id=f"test-{i:02d}",
                    date=workout_date,
                    duration_minutes=int(tss * 0.8),  # Approximate duration
                    distance_km=30.0,
                    avg_power_watts=200,
                    tss=tss,
                    workout_type="endurance",
                )
            )

    with patch("workout_mcp_server.main.data_loader") as mock_loader:
        mock_loader.get_all_workouts.return_value = mock_workouts

        result = await compute_fitness("2024-02-20")

        assert isinstance(result, dict)
        assert "error" not in result

        # CTL should be in realistic range for cycling fitness
        assert 60 <= result["ctl"] <= 120
        assert result["workouts_count"] > 30  # Should have many workouts
        assert result["ctl"] > 0


async def test_compute_fitness_exception():
    """Test handling of exceptions during CTL calculation."""
    from unittest.mock import patch

    from workout_mcp_server.main import compute_fitness

    with patch("workout_mcp_server.main.data_loader") as mock_loader:
        mock_loader.get_all_workouts.side_effect = Exception("Database error")

        result = await compute_fitness("2024-01-15")

        assert isinstance(result, dict)
        assert "error" in result
        assert "Failed to calculate CTL" in result["error"]
        assert "Database error" in result["error"]
