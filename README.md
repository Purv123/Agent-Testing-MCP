# Agent Testing MCP Server

A universal testing framework for AI coding agents using the Model Context Protocol (MCP). This server enables automated evaluation of AI agents like Claude Code, Cursor, GitHub Copilot, and similar tools through declarative test scenarios.

## Features

- **Universal Testing Framework**: Test any MCP-compatible AI coding agent
- **Declarative Test Scenarios**: Define tests using JSON/YAML files
- **Safe Code Execution**: Docker-based sandboxing with subprocess fallback
- **Intelligent Evaluation**: DeepEval integration for comprehensive assessment
- **Multiple Metrics**: Correctness, code quality, completeness, and relevance
- **Rich Reporting**: JSON results and Markdown reports with full interaction logs
- **Extensible**: Easy to add custom test scenarios and evaluation metrics

## Architecture

```
┌─────────────────┐
│   AI Agent      │ (Claude Code, Cursor, etc.)
│  (MCP Client)   │
└────────┬────────┘
         │ MCP Protocol
         │
┌────────▼────────────────────────────────────┐
│         Agent Testing MCP Server            │
│  ┌──────────────────────────────────────┐  │
│  │  MCP Tools (list, get, submit, etc.) │  │
│  └──────────────┬───────────────────────┘  │
│                 │                           │
│  ┌──────────────▼───────────────────────┐  │
│  │      Test Scenario Manager           │  │
│  │  (Load & manage test definitions)    │  │
│  └──────────────┬───────────────────────┘  │
│                 │                           │
│  ┌──────────────▼───────────────────────┐  │
│  │       Code Executor                  │  │
│  │  (Docker/Subprocess sandboxing)      │  │
│  └──────────────┬───────────────────────┘  │
│                 │                           │
│  ┌──────────────▼───────────────────────┐  │
│  │      Test Evaluator                  │  │
│  │  (DeepEval + Custom metrics)         │  │
│  └──────────────┬───────────────────────┘  │
│                 │                           │
│  ┌──────────────▼───────────────────────┐  │
│  │      Result Reporter                 │  │
│  │  (JSON/Markdown reports)             │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Docker (optional, for enhanced security)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd Agent-Testing-MCP
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up DeepEval** (optional, for advanced evaluation):
   ```bash
   # DeepEval requires an API key for LLM-based metrics
   export OPENAI_API_KEY="your-api-key"  # Or use other supported providers
   ```

5. **Verify Docker** (optional but recommended):
   ```bash
   docker --version
   # If not installed, the server will fall back to subprocess execution
   ```

## Quick Start

### Running the MCP Server

Start the server using stdio transport (standard for MCP):

```bash
python -m mcp_server.server
```

The server will:
- Load all test scenarios from `test_scenarios/`
- Start listening for MCP client connections
- Log activity to `logs/mcp_server.log`

### Connecting with Claude Code

Add to your Claude Code MCP configuration:

```json
{
  "mcpServers": {
    "agent-testing": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/path/to/Agent-Testing-MCP"
    }
  }
}
```

Restart Claude Code, and the server tools will be available.

## Usage

### Available MCP Tools

The server exposes the following tools to AI agents:

#### 1. `list_test_scenarios`
List all available test scenarios.

```json
{
  "category": "basic"  // optional filter
}
```

#### 2. `get_test_scenario`
Get detailed information about a specific test.

```json
{
  "scenario_id": "basic_001"
}
```

#### 3. `submit_solution`
Submit your solution for evaluation.

```json
{
  "scenario_id": "basic_001",
  "code": "def is_palindrome(text):\n    return text == text[::-1]",
  "language": "python",
  "explanation": "Using string slicing to reverse and compare"
}
```

#### 4. `execute_code`
Execute code in a sandbox without full evaluation.

```json
{
  "code": "print('Hello, World!')",
  "language": "python",
  "timeout": 30
}
```

#### 5. `get_test_results`
Get detailed results for a test run.

```json
{
  "run_id": "basic_001_20250121_143022"
}
```

#### 6. `list_test_runs`
List all test runs with optional filtering.

```json
{
  "scenario_id": "basic_001",  // optional
  "status": "passed"           // optional: passed, failed, error
}
```

### Example Workflow

As an AI agent using the MCP server:

```
1. Agent: list_test_scenarios()
   → Receives list of available tests

2. Agent: get_test_scenario(scenario_id="basic_001")
   → Receives detailed requirements and test cases

3. Agent: Writes solution code

4. Agent: submit_solution(scenario_id="basic_001", code="...", language="python")
   → Receives evaluation results immediately

5. Agent: get_test_results(run_id="...")
   → Receives detailed report with feedback
```

## Creating Custom Test Scenarios

Test scenarios are defined in JSON or YAML format in the `test_scenarios/` directory.

### Scenario Structure

```json
{
  "id": "unique_scenario_id",
  "title": "Human-readable title",
  "description": "What the agent should build",
  "category": "basic|intermediate|advanced|bug_fix|refactoring",
  "difficulty": "easy|medium|hard",
  "context": "Background information and constraints",

  "requirements": [
    "Specific requirement 1",
    "Specific requirement 2"
  ],

  "success_criteria": [
    "What defines success for this test"
  ],

  "language": "python|javascript|typescript",
  "timeout": 30,

  "test_cases": [
    {
      "input": "input data (can be any JSON type)",
      "expected_output": "expected result",
      "description": "What this test validates"
    }
  ],

  "starter_code": "Optional template code",
  "hints": ["Optional hints for the agent"],

  "evaluation_metrics": {
    "weights": {
      "correctness": 0.4,
      "quality": 0.3,
      "completeness": 0.2,
      "relevance": 0.1
    },
    "pass_threshold": 0.7
  }
}
```

### Example: Simple Test Scenario

```json
{
  "id": "hello_world",
  "title": "Hello World Function",
  "description": "Write a function that returns 'Hello, {name}!'",
  "category": "basic",
  "difficulty": "easy",
  "language": "python",

  "requirements": [
    "Create a function named 'greet'",
    "Take a name parameter",
    "Return greeting string"
  ],

  "test_cases": [
    {
      "input": "Alice",
      "expected_output": "Hello, Alice!",
      "description": "Basic greeting"
    },
    {
      "input": "World",
      "expected_output": "Hello, World!",
      "description": "Classic hello world"
    }
  ],

  "starter_code": "def greet(name):\n    pass\n\ndef main(name):\n    return greet(name)"
}
```

## Evaluation System

### Metrics

The evaluator assesses solutions across multiple dimensions:

1. **Correctness (40%)**: Do test cases pass?
2. **Code Quality (20%)**: Is code clean, documented, and well-structured?
3. **Completeness (20%)**: Are all requirements addressed?
4. **Relevance (20%)**: Does it solve the right problem?

*Weights can be customized per scenario*

### DeepEval Integration

When available, DeepEval provides additional LLM-based metrics:
- Answer relevancy
- Faithfulness to requirements
- Contextual understanding

### Pass/Fail Determination

- Each metric produces a score from 0.0 to 1.0
- Weighted average creates overall score
- Default pass threshold: 0.7 (70%)
- Customizable per scenario

## Results and Reporting

### Output Locations

- **JSON Results**: `results/{run_id}.json`
- **Markdown Reports**: `results/{run_id}.md`
- **Code Snapshots**: `results/{run_id}_code.{ext}`
- **Logs**: `logs/mcp_server.log`

### Report Contents

Each test run generates:
- Complete scenario details
- Submitted code and explanation
- Execution output and errors
- Test case results
- Evaluation metrics and scores
- Detailed feedback
- Pass/fail determination

### Example Report Structure

```markdown
# Test Report: Implement a Palindrome Checker

**Status:** ✓ PASSED
**Score:** 0.85/1.00

## Execution Results
- All 5 test cases passed
- No errors
- Clean output

## Evaluation
- Correctness: 1.00/1.00
- Quality: 0.75/1.00
- Completeness: 0.85/1.00
- Relevance: 0.90/1.00

## Feedback
- ✓ All test cases passed successfully
- ✓ Solution appears complete
- Code quality issues: No comments or documentation
```

## Configuration

### Environment Variables

```bash
# DeepEval (optional)
export OPENAI_API_KEY="your-key"

# Execution timeout (optional, default: 30s)
export DEFAULT_TIMEOUT=60

# Docker usage (optional, default: auto-detect)
export FORCE_DOCKER=true
```

### Server Configuration

Create `config.json` for advanced settings:

```json
{
  "scenarios_dir": "test_scenarios",
  "results_dir": "results",
  "logs_dir": "logs",
  "executor": {
    "use_docker": true,
    "default_timeout": 30,
    "docker_image": "python:3.11-slim"
  },
  "evaluator": {
    "enable_deepeval": true,
    "default_pass_threshold": 0.7
  }
}
```

## Development

### Project Structure

```
Agent-Testing-MCP/
├── mcp_server/           # Core server implementation
│   ├── server.py         # MCP server with tool definitions
│   ├── test_manager.py   # Test scenario management
│   ├── executor.py       # Safe code execution
│   ├── evaluator.py      # DeepEval integration
│   └── reporter.py       # Results and reporting
├── test_scenarios/       # Test definitions (JSON/YAML)
├── results/              # Test results and reports
├── logs/                 # Server logs
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Code formatting
black mcp_server/

# Linting
ruff check mcp_server/
```

### Adding New Features

1. **New Evaluation Metrics**: Extend `evaluator.py`
2. **New Languages**: Update `executor.py` with language support
3. **Custom Tools**: Add to `server.py` tool definitions
4. **New Report Formats**: Extend `reporter.py`

## Troubleshooting

### Common Issues

**Docker not available**
```
WARNING: Docker not available, falling back to subprocess execution
```
→ Install Docker or continue with subprocess (less isolated)

**DeepEval import errors**
```
WARNING: DeepEval not available. Using basic evaluation only.
```
→ Install DeepEval: `pip install deepeval` and configure API keys

**Test scenarios not loading**
```
WARNING: Scenarios directory not found
```
→ Ensure `test_scenarios/` exists with valid JSON/YAML files

**Permission errors on Docker**
```
Error: permission denied while trying to connect to Docker
```
→ Add user to docker group: `sudo usermod -aG docker $USER`

## Examples

See the `test_scenarios/` directory for complete examples:

- `001_basic_function.json` - Simple palindrome checker
- `002_data_processing.json` - JSON parsing and analysis
- `003_bug_fix.json` - Debugging exercise
- `004_refactoring.json` - Code improvement task
- `005_algorithm.json` - Binary search implementation

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure code passes linting
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built on the [Model Context Protocol](https://modelcontextprotocol.io/)
- Evaluation powered by [DeepEval](https://docs.confident-ai.com/)
- Inspired by the need for systematic AI agent testing

## Support

- Issues: [GitHub Issues](https://github.com/yourusername/Agent-Testing-MCP/issues)
- Documentation: [Full Docs](./docs/)
- MCP Specification: [MCP Docs](https://spec.modelcontextprotocol.io/)

---

**Built with Model Context Protocol for universal AI agent testing**
