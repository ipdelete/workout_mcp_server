"""Workout MCP Server - Main entry point."""

import logging

from fastmcp import FastMCP

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp: FastMCP = FastMCP("workout-mcp-server")


def configure_logging() -> None:
    """Configure logging for the MCP server."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


def main() -> None:
    """Main entry point for the workout MCP server."""
    configure_logging()

    try:
        logger.info("Initializing workout-mcp-server")
        # FastMCP handles the server lifecycle
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
