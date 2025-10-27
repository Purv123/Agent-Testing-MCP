@echo off
REM MCP Server Startup Script for Windows
cd /d %~dp0
set PYTHONPATH=%~dp0
%~dp0venv\Scripts\python.exe -m mcp_server.server
