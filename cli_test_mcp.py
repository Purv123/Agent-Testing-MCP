#!/usr/bin/env python3
"""
Simple CLI client to interact with the MCP server directly
"""
import json
import subprocess
import sys

def send_mcp_request(method, params=None):
    """Send a JSON-RPC request to the MCP server"""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {}
    }

    # Start the MCP server
    process = subprocess.Popen(
        ["./run_mcp.sh"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Send request
    request_str = json.dumps(request) + "\n"
    stdout, stderr = process.communicate(input=request_str, timeout=10)

    # Parse response
    lines = stdout.strip().split("\n")
    for line in lines:
        if line.strip() and line.startswith("{"):
            try:
                response = json.loads(line)
                return response
            except json.JSONDecodeError:
                continue

    return {"error": "No valid JSON response", "stdout": stdout, "stderr": stderr}

def main():
    print("🚀 MCP Server CLI Test\n")

    # Initialize
    print("1. Initializing MCP server...")
    response = send_mcp_request("initialize", {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "cli-test", "version": "1.0"}
    })
    print(f"   Response: {json.dumps(response, indent=2)}\n")

    # List tools
    print("2. Listing available tools...")
    response = send_mcp_request("tools/list")
    if "result" in response:
        tools = response["result"].get("tools", [])
        print(f"   Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool.get('name')}: {tool.get('description', 'No description')[:60]}...")
    print()

if __name__ == "__main__":
    main()
