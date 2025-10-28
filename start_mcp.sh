#!/bin/bash
# MCP Server Startup Script for Cline/MCP Clients
set -e

cd /Users/purvit/Documents/GitHub/Agent-Testing-MCP
export PYTHONPATH=/Users/purvit/Documents/GitHub/Agent-Testing-MCP

# Start MCP server (Python will handle stdio)
exec /Users/purvit/Documents/GitHub/Agent-Testing-MCP/venv/bin/python -u -m mcp_server.server
