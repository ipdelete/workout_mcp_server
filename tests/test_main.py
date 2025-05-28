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
