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


def test_compute_fatigue_tool_exists():
    """Test that compute_fatigue tool is registered."""
    from workout_mcp_server.main import compute_fatigue

    assert callable(compute_fatigue)
    assert hasattr(compute_fatigue, "__doc__")
    assert "Acute Training Load" in compute_fatigue.__doc__
    assert "ATL" in compute_fatigue.__doc__


async def test_compute_fatigue_success():
    """Test successful ATL calculation."""
    from datetime import datetime, timedelta
    from unittest.mock import patch

    from workout_mcp_server.data_loader import Workout
    from workout_mcp_server.main import compute_fatigue

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

        result = await compute_fatigue("2024-01-30")

        assert isinstance(result, dict)
        assert "error" not in result
        assert result["target_date"] == "2024-01-30"
        assert "atl" in result
        assert isinstance(result["atl"], float)
        assert result["atl"] > 0  # Should have positive ATL with workouts
        assert result["workouts_count"] == 30
        assert "date_range" in result
        assert result["date_range"]["earliest_workout"] == "2024-01-01"
        assert result["date_range"]["latest_workout"] == "2024-01-30"

        mock_loader.get_all_workouts.assert_called_once_with(sort_by_date=False)


async def test_compute_fatigue_no_workouts():
    """Test ATL calculation with no workout data."""
    from unittest.mock import patch

    from workout_mcp_server.main import compute_fatigue

    with patch("workout_mcp_server.main.data_loader") as mock_loader:
        mock_loader.get_all_workouts.return_value = []

        result = await compute_fatigue("2024-01-15")

        assert isinstance(result, dict)
        assert "error" not in result
        assert result["target_date"] == "2024-01-15"
        assert result["atl"] == 0.0
        assert result["workouts_count"] == 0
        assert "message" in result
        assert "No workout data available" in result["message"]


async def test_compute_fatigue_invalid_date():
    """Test ATL calculation with invalid date format."""
    from workout_mcp_server.main import compute_fatigue

    result = await compute_fatigue("invalid-date")

    assert isinstance(result, dict)
    assert "error" in result
    assert "Invalid date format" in result["error"]
    assert "invalid-date" in result["error"]
    assert "YYYY-MM-DD" in result["error"]


async def test_compute_fatigue_realistic_values():
    """Test ATL calculation produces realistic fatigue values."""
    from datetime import datetime, timedelta
    from unittest.mock import patch

    from workout_mcp_server.data_loader import Workout
    from workout_mcp_server.main import compute_fatigue

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

        result = await compute_fatigue("2024-02-20")

        assert isinstance(result, dict)
        assert "error" not in result

        # ATL should be in realistic range for cycling fatigue
        assert 60 <= result["atl"] <= 120
        assert result["workouts_count"] > 30  # Should have many workouts
        assert result["atl"] > 0


async def test_compute_fatigue_exception():
    """Test handling of exceptions during ATL calculation."""
    from unittest.mock import patch

    from workout_mcp_server.main import compute_fatigue

    with patch("workout_mcp_server.main.data_loader") as mock_loader:
        mock_loader.get_all_workouts.side_effect = Exception("Database error")

        result = await compute_fatigue("2024-01-15")

        assert isinstance(result, dict)
        assert "error" in result
        assert "Failed to calculate ATL" in result["error"]
        assert "Database error" in result["error"]


async def test_compute_fatigue_vs_fitness_responsiveness():
    """Test that ATL (7-day) is more responsive than CTL (42-day)."""
    from datetime import datetime, timedelta
    from unittest.mock import patch

    from workout_mcp_server.data_loader import Workout
    from workout_mcp_server.main import compute_fatigue, compute_fitness

    # Create workouts with a big spike in recent TSS
    mock_workouts = []
    base_date = datetime(2024, 1, 1)

    # 40 days of moderate TSS, then 5 days of high TSS
    for i in range(45):
        workout_date = base_date + timedelta(days=i)
        tss = 70 if i < 40 else 150  # Big jump in last 5 days
        mock_workouts.append(
            Workout(
                id=f"test-{i:02d}",
                date=workout_date,
                duration_minutes=60,
                distance_km=30.0,
                avg_power_watts=200,
                tss=tss,
                workout_type="endurance",
            )
        )

    with patch("workout_mcp_server.main.data_loader") as mock_loader:
        mock_loader.get_all_workouts.return_value = mock_workouts

        target_date = "2024-02-14"  # Day 44
        atl_result = await compute_fatigue(target_date)
        ctl_result = await compute_fitness(target_date)

        assert isinstance(atl_result, dict)
        assert isinstance(ctl_result, dict)
        assert "error" not in atl_result
        assert "error" not in ctl_result

        # ATL should be more responsive to recent high TSS values
        assert atl_result["atl"] > ctl_result["ctl"]
        assert atl_result["atl"] > 100  # Should be pulled up by recent high values
        assert ctl_result["ctl"] < atl_result["atl"]  # CTL should be less responsive


# Tests for compute_form tool


def test_compute_form_tool_exists():
    """Test that compute_form tool is registered."""
    from workout_mcp_server.main import compute_form

    assert callable(compute_form)
    assert hasattr(compute_form, "__doc__")
    assert "Training Stress Balance" in compute_form.__doc__
    assert "TSB" in compute_form.__doc__


async def test_compute_form_success():
    """Test successful TSB calculation."""
    from unittest.mock import AsyncMock, patch

    from workout_mcp_server.main import compute_form

    # Mock successful responses from compute_fitness and compute_fatigue
    mock_ctl_result = {
        "target_date": "2024-02-14",
        "ctl": 75.5,
        "workouts_count": 42,
        "date_range": {
            "earliest_workout": "2024-01-04",
            "latest_workout": "2024-02-14",
        },
    }

    mock_atl_result = {
        "target_date": "2024-02-14",
        "atl": 82.3,
        "workouts_count": 7,
        "date_range": {
            "earliest_workout": "2024-02-08",
            "latest_workout": "2024-02-14",
        },
    }

    with patch(
        "workout_mcp_server.main.compute_fitness", new_callable=AsyncMock
    ) as mock_fitness:
        with patch(
            "workout_mcp_server.main.compute_fatigue", new_callable=AsyncMock
        ) as mock_fatigue:
            mock_fitness.return_value = mock_ctl_result
            mock_fatigue.return_value = mock_atl_result

            result = await compute_form("2024-02-14")

            # Verify the functions were called with correct parameters
            mock_fitness.assert_called_once_with("2024-02-14")
            mock_fatigue.assert_called_once_with("2024-02-14")

            # Check result structure
            assert isinstance(result, dict)
            assert "error" not in result
            assert result["target_date"] == "2024-02-14"
            assert result["tsb"] == -6.8  # 75.5 - 82.3
            assert result["ctl"] == 75.5
            assert result["atl"] == 82.3
            assert "interpretation" in result
            assert "Fatigued" in result["interpretation"]
            assert result["workouts_count"] == 42  # max of both counts


async def test_compute_form_fresh_athlete():
    """Test TSB calculation for a fresh athlete (positive TSB)."""
    from unittest.mock import AsyncMock, patch

    from workout_mcp_server.main import compute_form

    # Mock responses showing low fatigue, higher fitness
    mock_ctl_result = {"target_date": "2024-02-14", "ctl": 85.0, "workouts_count": 42}
    mock_atl_result = {"target_date": "2024-02-14", "atl": 70.0, "workouts_count": 7}

    with patch(
        "workout_mcp_server.main.compute_fitness", new_callable=AsyncMock
    ) as mock_fitness:
        with patch(
            "workout_mcp_server.main.compute_fatigue", new_callable=AsyncMock
        ) as mock_fatigue:
            mock_fitness.return_value = mock_ctl_result
            mock_fatigue.return_value = mock_atl_result

            result = await compute_form("2024-02-14")

            assert result["tsb"] == 15.0  # 85.0 - 70.0
            assert "Fresh" in result["interpretation"]


async def test_compute_form_neutral_athlete():
    """Test TSB calculation for neutral form (TSB near zero)."""
    from unittest.mock import AsyncMock, patch

    from workout_mcp_server.main import compute_form

    # Mock responses showing balanced CTL and ATL
    mock_ctl_result = {"target_date": "2024-02-14", "ctl": 80.0, "workouts_count": 42}
    mock_atl_result = {"target_date": "2024-02-14", "atl": 77.5, "workouts_count": 7}

    with patch(
        "workout_mcp_server.main.compute_fitness", new_callable=AsyncMock
    ) as mock_fitness:
        with patch(
            "workout_mcp_server.main.compute_fatigue", new_callable=AsyncMock
        ) as mock_fatigue:
            mock_fitness.return_value = mock_ctl_result
            mock_fatigue.return_value = mock_atl_result

            result = await compute_form("2024-02-14")

            assert result["tsb"] == 2.5  # 80.0 - 77.5
            assert "Neutral" in result["interpretation"]


async def test_compute_form_invalid_date():
    """Test compute_form with invalid date format."""
    from unittest.mock import AsyncMock, patch

    from workout_mcp_server.main import compute_form

    # Mock compute_fitness to return an error
    mock_error_result = {
        "error": "Invalid date format 'bad-date'. Use YYYY-MM-DD format."
    }

    with patch(
        "workout_mcp_server.main.compute_fitness", new_callable=AsyncMock
    ) as mock_fitness:
        mock_fitness.return_value = mock_error_result

        result = await compute_form("bad-date")

        # Should propagate the error from compute_fitness
        assert "error" in result
        assert "Invalid date format" in result["error"]


async def test_compute_form_fitness_error():
    """Test compute_form when compute_fitness returns an error."""
    from unittest.mock import AsyncMock, patch

    from workout_mcp_server.main import compute_form

    mock_error_result = {"error": "Failed to calculate CTL: Database error"}

    with patch(
        "workout_mcp_server.main.compute_fitness", new_callable=AsyncMock
    ) as mock_fitness:
        mock_fitness.return_value = mock_error_result

        result = await compute_form("2024-02-14")

        assert "error" in result
        assert "Failed to calculate CTL" in result["error"]


async def test_compute_form_fatigue_error():
    """Test compute_form when compute_fatigue returns an error."""
    from unittest.mock import AsyncMock, patch

    from workout_mcp_server.main import compute_form

    mock_ctl_result = {"target_date": "2024-02-14", "ctl": 75.0, "workouts_count": 42}
    mock_error_result = {"error": "Failed to calculate ATL: Database error"}

    with patch(
        "workout_mcp_server.main.compute_fitness", new_callable=AsyncMock
    ) as mock_fitness:
        with patch(
            "workout_mcp_server.main.compute_fatigue", new_callable=AsyncMock
        ) as mock_fatigue:
            mock_fitness.return_value = mock_ctl_result
            mock_fatigue.return_value = mock_error_result

            result = await compute_form("2024-02-14")

            assert "error" in result
            assert "Failed to calculate ATL" in result["error"]


async def test_compute_form_no_workouts():
    """Test compute_form with no workout data."""
    from unittest.mock import AsyncMock, patch

    from workout_mcp_server.main import compute_form

    # Mock responses with zero values
    mock_ctl_result = {"target_date": "2024-02-14", "ctl": 0.0, "workouts_count": 0}
    mock_atl_result = {"target_date": "2024-02-14", "atl": 0.0, "workouts_count": 0}

    with patch(
        "workout_mcp_server.main.compute_fitness", new_callable=AsyncMock
    ) as mock_fitness:
        with patch(
            "workout_mcp_server.main.compute_fatigue", new_callable=AsyncMock
        ) as mock_fatigue:
            mock_fitness.return_value = mock_ctl_result
            mock_fatigue.return_value = mock_atl_result

            result = await compute_form("2024-02-14")

            assert result["tsb"] == 0.0
            assert result["ctl"] == 0.0
            assert result["atl"] == 0.0
            assert result["workouts_count"] == 0


async def test_compute_form_exception_handling():
    """Test compute_form handles unexpected exceptions."""
    from unittest.mock import AsyncMock, patch

    from workout_mcp_server.main import compute_form

    with patch(
        "workout_mcp_server.main.compute_fitness", new_callable=AsyncMock
    ) as mock_fitness:
        mock_fitness.side_effect = Exception("Unexpected error")

        result = await compute_form("2024-02-14")

        assert "error" in result
        assert "Failed to calculate TSB" in result["error"]
