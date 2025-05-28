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
