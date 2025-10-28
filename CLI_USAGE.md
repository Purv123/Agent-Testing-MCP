# 🖥️ Command-Line Usage Guide

You can use the Agent Testing MCP Server directly from the command line without needing Claude Code or any other MCP client!

## Quick Start

```bash
# List all available test scenarios
./agent-test list

# View details of a specific scenario
./agent-test get basic_001

# Submit a solution for testing
./agent-test submit basic_001 my_solution.py

# Just execute code without full evaluation
./agent-test execute my_code.py
```

---

## Installation

### Option 1: Local Python (Requires Python 3.10+)

```bash
# Clone the repository
git clone https://github.com/Purv123/Agent-Testing-MCP.git
cd Agent-Testing-MCP

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Docker (Works with ANY Python version)

```bash
# Clone the repository
git clone https://github.com/Purv123/Agent-Testing-MCP.git
cd Agent-Testing-MCP

# Build and use Docker
./run_mcp.sh
```

---

## Commands

### 1. List Scenarios

List all available test scenarios:

```bash
./agent-test list
```

**Output:**
```
📋 Available Test Scenarios:

ID                   Title                                              Difficulty   Category
====================================================================================================
basic_001            Implement a Palindrome Checker                     easy         basic
bugfix_001           Fix the Broken Calculator                          easy         bug_fix
intermediate_001     Parse and Analyze JSON Data                        medium       intermediate
advanced_001         Implement Binary Search                            hard         advanced
refactor_001         Refactor Code for Better Readability               medium       refactoring

Total: 5 scenarios
```

### 2. Get Scenario Details

View detailed information about a specific test scenario:

```bash
./agent-test get basic_001
```

**Output:**
```
================================================================================
📝 Implement a Palindrome Checker
================================================================================

ID: basic_001
Category: basic
Difficulty: easy
Language: python

📖 Description:
Write a function that checks if a given string is a palindrome...

✅ Requirements:
  1. Create a function named 'is_palindrome'
  2. Return True if palindrome, False otherwise
  ...

🧪 Test Cases: 5 cases
  1. Simple palindrome
     Input: racecar
     Expected: True
  ...

💡 Starter Code:
def is_palindrome(text):
    # Your code here
    pass
```

### 3. Submit Solution

Submit your solution for automated testing and evaluation:

```bash
./agent-test submit basic_001 solution.py
```

**Example solution.py:**
```python
def is_palindrome(text):
    # Remove non-alphanumeric and convert to lowercase
    cleaned = ''.join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]

def main(text):
    return is_palindrome(text)
```

**Output:**
```
🚀 Submitting solution for: Implement a Palindrome Checker

⏳ Executing code...
🧪 Running test cases...
📊 Evaluating solution...

================================================================================
📊 Test Results Summary
================================================================================

Status: ✅ PASSED
Score: 0.92/1.00
Threshold: 0.70

📈 Metrics:
  Correctness     ████████████████████ 1.00
  Quality         ████████████████░░░░ 0.85
  Completeness    ███████████████████░ 0.95
  Relevance       ████████████████████ 1.00

🧪 Test Cases: 5/5 passed

💾 Results saved:
  • JSON: results/basic_001_20251028_180000.json
  • Report: results/basic_001_20251028_180000.md
```

### 4. Execute Code

Just execute code without full evaluation (useful for testing):

```bash
./agent-test execute test.py
```

**Output:**
```
⚡ Executing python code...

✅ Execution successful

📤 Output:
Hello, World!

Execution time: 0.123s
```

---

## Example Workflow

### Complete Example: Solving the Palindrome Checker

#### Step 1: View the challenge
```bash
./agent-test get basic_001
```

#### Step 2: Write your solution

Create `palindrome_solution.py`:
```python
def is_palindrome(text):
    """Check if text is a palindrome, ignoring case and non-alphanumeric chars"""
    # Remove non-alphanumeric characters and convert to lowercase
    cleaned = ''.join(char.lower() for char in text if char.isalnum())

    # Compare with reverse
    return cleaned == cleaned[::-1]

def main(text):
    """Entry point for testing"""
    return is_palindrome(text)
```

#### Step 3: Test it quickly
```bash
./agent-test execute palindrome_solution.py
```

#### Step 4: Submit for full evaluation
```bash
./agent-test submit basic_001 palindrome_solution.py
```

#### Step 5: View results
```bash
# Results are automatically saved to results/ directory
cat results/basic_001_*.md
```

---

## Advanced Usage

### Custom Test Cases

You can create your own test scenarios in the `test_scenarios/` directory using JSON or YAML format.

Example (`test_scenarios/my_test.json`):
```json
{
  "id": "my_test_001",
  "title": "My Custom Test",
  "description": "Write a function that...",
  "category": "custom",
  "difficulty": "easy",
  "language": "python",
  "test_cases": [
    {
      "input": "test input",
      "expected_output": "expected result",
      "description": "Test case description"
    }
  ],
  "requirements": ["Requirement 1", "Requirement 2"],
  "success_criteria": ["Should do X", "Should handle Y"]
}
```

### Viewing Results

Results are saved in two formats:

1. **JSON** (`results/*.json`) - Machine-readable, complete data
2. **Markdown** (`results/*.md`) - Human-readable report

View a report:
```bash
cat results/basic_001_20251028_180000.md
```

View JSON data:
```bash
cat results/basic_001_20251028_180000.json | jq
```

---

## Using with Docker

If using the Docker version, you can still use the CLI:

```bash
# Create an alias for easier use
alias agent-test='docker run --rm -i \
  -v $(pwd)/test_scenarios:/app/test_scenarios:ro \
  -v $(pwd)/results:/app/results \
  -v $(pwd)/logs:/app/logs \
  agent-testing-mcp python3 mcp_cli.py'

# Then use it normally
agent-test list
agent-test get basic_001
```

Or create a wrapper script for Docker users.

---

## Comparison: CLI vs MCP Server

### Command-Line Interface (CLI)
✅ Simple, direct usage
✅ No setup needed (just run commands)
✅ Great for manual testing
✅ Easy to script and automate
❌ Manual workflow (you run each command)

### MCP Server (with Claude Code/Cline)
✅ AI agent can autonomously test itself
✅ Automated workflow
✅ AI can iterate on solutions
✅ Perfect for evaluating AI coding assistants
❌ Requires MCP client setup

**Use CLI when:** You want to manually test solutions or script automated testing

**Use MCP Server when:** You want AI agents to automatically test and evaluate themselves

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'yaml'"

**Solution:** Activate the virtual environment:
```bash
source venv/bin/activate
```

Or use the wrapper script:
```bash
./agent-test list
```

### "Permission denied"

**Solution:** Make scripts executable:
```bash
chmod +x agent-test mcp_cli.py
```

### Docker not available

If using Docker, make sure it's running:
```bash
docker --version
# Start Docker Desktop if needed
```

---

## Integration with CI/CD

You can integrate the CLI into your CI/CD pipeline:

```yaml
# .github/workflows/test.yml
name: Test Solutions

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: ./agent-test submit basic_001 solutions/basic_001.py
```

---

## Help

Get help anytime:
```bash
./agent-test help
```

---

## Next Steps

- Try solving all 5 scenarios!
- Create your own custom test scenarios
- Integrate into your development workflow
- Use with AI coding assistants via MCP

For MCP server setup, see [CLIENT_INSTRUCTIONS.md](CLIENT_INSTRUCTIONS.md)
