#!/bin/bash
# MCP Server Docker Startup Script
# This script runs the MCP server in a Docker container

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run Docker container with stdio for MCP communication
docker run -i --rm \
  --name "agent-testing-mcp-$$" \
  -v "${SCRIPT_DIR}/test_scenarios:/app/test_scenarios:ro" \
  -v "${SCRIPT_DIR}/results:/app/results" \
  -v "${SCRIPT_DIR}/logs:/app/logs" \
  agent-testing-mcp
