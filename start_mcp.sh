#!/bin/bash
# MCP Server Startup Script
cd /Users/purvit/Documents/GitHub/Agent-Testing-MCP
export PYTHONPATH=/Users/purvit/Documents/GitHub/Agent-Testing-MCP
exec /Users/purvit/Documents/GitHub/Agent-Testing-MCP/venv/bin/python -m mcp_server.server
