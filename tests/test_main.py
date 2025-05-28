"""Tests for workout_mcp_server."""


from workout_mcp_server import __version__


def test_version():
    """Test that the version is defined."""
    assert __version__ == "0.1.0"


def test_import():
    """Test that we can import the main module."""
    from workout_mcp_server import main

    assert hasattr(main, "main")
