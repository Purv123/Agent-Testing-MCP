# Example Usage

This document shows real-world examples of using the Agent Testing MCP Server.

## Example 1: Testing an AI Agent on Basic Tasks

### Scenario
Test if an AI agent can correctly implement a palindrome checker.

### Agent Interaction

**Agent calls:**
```json
list_test_scenarios({"category": "basic"})
```

**Server responds:**
```json
{
  "scenarios": [
    {
      "id": "basic_001",
      "title": "Implement a Palindrome Checker",
      "category": "basic",
      "difficulty": "easy",
      "description": "Write a function that checks if a given string is a palindrome"
    }
  ],
  "total": 1
}
```

**Agent calls:**
```json
get_test_scenario({"scenario_id": "basic_001"})
```

**Server responds with full details including:**
- Requirements
- Test cases
- Starter code
- Hints

**Agent submits solution:**
```json
submit_solution({
  "scenario_id": "basic_001",
  "code": "def is_palindrome(text):\n    cleaned = ''.join(c.lower() for c in text if c.isalnum())\n    return cleaned == cleaned[::-1]\n\ndef main(text):\n    return is_palindrome(text)",
  "language": "python",
  "explanation": "I'm using list comprehension to filter alphanumeric characters and convert to lowercase, then comparing with the reversed string."
})
```

**Server evaluates and responds:**
```json
{
  "run_id": "basic_001_20250121_143022",
  "status": "passed",
  "passed": true,
  "score": 0.92,
  "summary": "✓ Solution PASSED with score 0.92. Well done!",
  "execution": {
    "success": true,
    "output": "===TEST_RESULTS===\n[...all tests passed...]"
  },
  "message": "Solution evaluated successfully. Use get_test_results for detailed report."
}
```

## Example 2: Debugging a Broken Solution

### Agent submits buggy code:

```python
def is_palindrome(text):
    return text == text[::-1]  # BUG: doesn't handle case/spaces

def main(text):
    return is_palindrome(text)
```

### Server evaluation:
```json
{
  "status": "failed",
  "passed": false,
  "score": 0.40,
  "execution": {
    "success": true,
    "test_results": [
      {"test_case": 1, "passed": true},   // "racecar" works
      {"test_case": 2, "passed": true},   // "hello" correctly false
      {"test_case": 3, "passed": false},  // "A man a plan..." fails
      {"test_case": 4, "passed": true},   // empty string works
      {"test_case": 5, "passed": false}   // "Was it a car..." fails
    ]
  },
  "evaluation": {
    "metrics": {
      "correctness": {
        "score": 0.60,
        "passed_tests": 3,
        "total_tests": 5
      }
    },
    "feedback": [
      "⚠ Partial success: Passed 3/5 test cases",
      "Code quality issues: No comments or documentation"
    ]
  }
}
```

### Agent iterates and fixes:

```python
def is_palindrome(text):
    """Check if text is a palindrome, ignoring case and non-alphanumeric characters."""
    cleaned = ''.join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]

def main(text):
    return is_palindrome(text)
```

### New evaluation:
```json
{
  "status": "passed",
  "passed": true,
  "score": 0.92
}
```

## Example 3: Benchmark Multiple Agents

Test the same scenario with different AI agents to compare performance.

### Test Run Results:

```
Agent A (Claude Code):
  - basic_001: PASSED (0.92)
  - intermediate_001: PASSED (0.85)
  - advanced_001: FAILED (0.65)

Agent B (Cursor):
  - basic_001: PASSED (0.88)
  - intermediate_001: PASSED (0.78)
  - advanced_001: PASSED (0.82)

Agent C (Copilot):
  - basic_001: PASSED (0.90)
  - intermediate_001: FAILED (0.62)
  - advanced_001: FAILED (0.58)
```

### Summary Statistics:

```bash
# Get summary across all runs
python -c "
from mcp_server.reporter import ResultReporter
reporter = ResultReporter()
summary = reporter.generate_summary_report()
print(summary)
"
```

Output:
```json
{
  "total_runs": 9,
  "passed": 6,
  "failed": 3,
  "pass_rate": 66.7,
  "average_score": 0.78,
  "by_scenario": [
    {
      "scenario_id": "basic_001",
      "total": 3,
      "passed": 3,
      "avg_score": 0.90
    },
    ...
  ]
}
```

## Example 4: Custom Test Scenario

### Use Case: Test if agent can work with your API

Create `test_scenarios/api_endpoint.json`:

```json
{
  "id": "api_001",
  "title": "Create REST API Endpoint",
  "description": "Create a Flask endpoint that accepts JSON and returns processed data",
  "category": "intermediate",
  "difficulty": "medium",
  "language": "python",

  "context": "Build a /process endpoint that takes {numbers: []} and returns {sum, average, count}",

  "requirements": [
    "Use Flask framework",
    "Create POST endpoint at /process",
    "Accept JSON with 'numbers' array",
    "Return JSON with sum, average, count",
    "Handle empty arrays gracefully"
  ],

  "test_cases": [
    {
      "input": {"numbers": [1, 2, 3, 4, 5]},
      "expected_output": {"sum": 15, "average": 3.0, "count": 5},
      "description": "Basic calculation"
    },
    {
      "input": {"numbers": []},
      "expected_output": {"sum": 0, "average": 0, "count": 0},
      "description": "Empty array"
    }
  ],

  "starter_code": "from flask import Flask, request, jsonify\n\napp = Flask(__name__)\n\n# Your code here\n\ndef main(data):\n    # Simulate POST request\n    return process_numbers(data)",

  "evaluation_metrics": {
    "weights": {
      "correctness": 0.5,
      "quality": 0.3,
      "completeness": 0.2
    },
    "pass_threshold": 0.75
  }
}
```

## Example 5: Regression Testing

Use the server to detect if agent improvements break existing functionality.

### Baseline Run (v1.0):
```bash
python scripts/run_all_tests.py --agent "agent_v1" --output baseline.json
```

Results:
```json
{
  "version": "agent_v1",
  "date": "2025-01-21",
  "total_scenarios": 10,
  "passed": 8,
  "failed": 2,
  "average_score": 0.82
}
```

### After Update (v1.1):
```bash
python scripts/run_all_tests.py --agent "agent_v1.1" --output new_version.json
```

Results:
```json
{
  "version": "agent_v1.1",
  "date": "2025-01-28",
  "total_scenarios": 10,
  "passed": 9,
  "failed": 1,
  "average_score": 0.87
}
```

### Compare:
```bash
python scripts/compare_results.py baseline.json new_version.json
```

Output:
```
Improvements:
  ✓ advanced_001: 0.65 → 0.82 (+0.17)
  ✓ intermediate_003: FAILED → PASSED

Regressions:
  (none)

Overall: +5% pass rate, +0.05 average score
```

## Example 6: Using execute_code for Quick Tests

Test code snippets without full scenario submission:

```json
execute_code({
  "code": "import math\nprint(math.pi)",
  "language": "python",
  "timeout": 5
})
```

Response:
```json
{
  "success": true,
  "output": "3.141592653589793\n",
  "errors": "",
  "return_code": 0
}
```

## Example 7: Filtering Test Runs

```json
// Get all failed runs
list_test_runs({"status": "failed"})

// Get all runs for a specific scenario
list_test_runs({"scenario_id": "basic_001"})

// Combine filters
list_test_runs({
  "scenario_id": "advanced_001",
  "status": "passed"
})
```

## Best Practices

1. **Start Simple**: Begin with basic scenarios to validate agent setup
2. **Iterate**: Use feedback to improve solutions
3. **Track Progress**: Use list_test_runs to monitor improvements
4. **Custom Scenarios**: Create scenarios matching your real-world needs
5. **Regression Testing**: Run periodically to catch degradations
6. **Compare Agents**: Use same scenarios across different agents

## Advanced Usage

### Programmatic Access

```python
from mcp_server.test_manager import TestManager
from mcp_server.executor import CodeExecutor
from mcp_server.evaluator import TestEvaluator

# Load scenarios
manager = TestManager()
scenario = manager.get_scenario("basic_001")

# Execute code
executor = CodeExecutor()
result = await executor.execute(
    code="your code here",
    language="python",
    test_cases=scenario.test_cases,
    timeout=30
)

# Evaluate
evaluator = TestEvaluator()
evaluation = await evaluator.evaluate(
    scenario=scenario,
    code="your code",
    execution_result=result
)

print(f"Score: {evaluation['overall_score']}")
print(f"Passed: {evaluation['passed']}")
```

### Batch Testing

```python
# Test all scenarios
for scenario in manager.list_scenarios():
    print(f"Testing {scenario.id}...")
    # Submit solution
    # Collect results

# Generate summary
summary = reporter.generate_summary_report()
print(f"Pass rate: {summary['pass_rate']}%")
```

---

These examples demonstrate the flexibility and power of the Agent Testing MCP Server for comprehensive AI agent evaluation!
