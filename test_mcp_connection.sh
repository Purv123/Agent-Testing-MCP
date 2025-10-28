#!/bin/bash
# Test script to verify MCP server responds correctly

echo "Testing MCP Server Connection..."
echo ""

# Send a valid initialize message
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test-client","version":"1.0.0"}}}' | ./run_mcp.sh 2>&1 | head -20

echo ""
echo "If you see a JSON response above with 'result' field, the server is working!"
