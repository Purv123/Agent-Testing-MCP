# Quick Start Guide

Get up and running with the Agent Testing MCP Server in 5 minutes!

## Installation (2 minutes)

```bash
# 1. Navigate to the project
cd Agent-Testing-MCP

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Test the Server (1 minute)

```bash
# Start the server
python -m mcp_server.server
```

You should see:
```
INFO - Agent Testing Server initialized
INFO - Loaded 5 test scenarios
INFO - Starting Agent Testing MCP Server...
```

Press Ctrl+C to stop.

## Connect with Claude Code (2 minutes)

### Option 1: Manual MCP Configuration

1. Open Claude Code settings
2. Add MCP server configuration:

```json
{
  "mcpServers": {
    "agent-testing": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/full/path/to/Agent-Testing-MCP",
      "env": {
        "PYTHONPATH": "/full/path/to/Agent-Testing-MCP"
      }
    }
  }
}
```

3. Restart Claude Code

### Option 2: Using the MCP Inspector (for testing)

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run with your server
mcp-inspector python -m mcp_server.server
```

## Your First Test

Once connected, try this with your AI agent:

### Step 1: List Available Tests
```
List available test scenarios
```

The server will show you all available tests.

### Step 2: Get a Test Scenario
```
Get details for test scenario "basic_001"
```

You'll receive the full test specification.

### Step 3: Solve and Submit
```
I'll solve the palindrome checker test (basic_001)
```

Let the agent write the solution and submit it.

### Step 4: View Results
```
Show me the detailed test results
```

You'll get a full report with scores and feedback.

## What's Next?

### Create Your Own Test

1. Create a new file in `test_scenarios/`:

```json
{
  "id": "my_test_001",
  "title": "My First Test",
  "description": "Write a function that adds two numbers",
  "category": "basic",
  "difficulty": "easy",
  "language": "python",
  "requirements": [
    "Create an 'add' function",
    "Take two parameters",
    "Return their sum"
  ],
  "test_cases": [
    {
      "input": {"a": 2, "b": 3},
      "expected_output": 5,
      "description": "Basic addition"
    }
  ],
  "starter_code": "def add(a, b):\n    pass\n\ndef main(a, b):\n    return add(a, b)"
}
```

2. Restart the server
3. Your test is now available!

### Enable Docker (Optional)

For better isolation:

```bash
# Install Docker
# https://docs.docker.com/get-docker/

# Pull Python image
docker pull python:3.11-slim

# Restart server - it will auto-detect Docker
```

### Enable DeepEval (Optional)

For advanced AI-based evaluation:

```bash
# Install DeepEval
pip install deepeval

# Set API key
export OPENAI_API_KEY="your-api-key"

# Restart server
```

## Common Commands

```bash
# Start server
python -m mcp_server.server

# View logs
tail -f logs/mcp_server.log

# Check results
ls -l results/

# View a specific result
cat results/basic_001_*.json
```

## Troubleshooting

**"Module not found" error**
```bash
# Ensure you're in the right directory and venv is activated
pwd  # Should show Agent-Testing-MCP
which python  # Should show venv/bin/python
```

**No test scenarios loaded**
```bash
# Verify test files exist
ls test_scenarios/
# Should show .json files
```

**Docker not working**
```bash
# Check Docker status
docker ps
# If error, server will fall back to subprocess (that's okay!)
```

## Next Steps

- Read the full [README.md](README.md) for details
- Explore example scenarios in `test_scenarios/`
- Check generated reports in `results/`
- Create custom test scenarios for your use case

## Need Help?

- Check `logs/mcp_server.log` for errors
- Review example scenarios in `test_scenarios/`
- See [README.md](README.md) for full documentation

Happy testing! 🚀
