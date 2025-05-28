# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Python development environment configuration with FastMCP framework
- Project structure with proper Python package layout in `src/workout_mcp_server/`
- Development dependencies: pytest, black, mypy, ruff for code quality
- Basic test suite to verify environment setup
- Package entry points for running with `python -m workout_mcp_server`
- MCP server skeleton implementation using FastMCP
- Basic server initialization with logging configuration
- Tools directory structure for future tool implementations
- Server responds to MCP protocol handshake
- Tests for server instance creation and configuration

### Changed
- Python version requirement updated to 3.10+ (required by FastMCP)
- Project configuration moved to modern pyproject.toml format with hatchling build backend

## [0.1.0] - 2025-05-28

### Added
- Initial project structure and documentation
- Architecture Decision Records (ADRs) for testing philosophy and MCP framework selection
- Project requirements documentation (PRD)
- Basic README with project overview