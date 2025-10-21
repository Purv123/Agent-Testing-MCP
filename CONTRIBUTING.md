# Contributing to Agent Testing MCP Server

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/Agent-Testing-MCP.git
   cd Agent-Testing-MCP
   ```

3. **Set up development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

- Write clean, documented code
- Follow existing code style (PEP 8 for Python)
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run tests
pytest tests/

# Format code
black mcp_server/

# Lint
ruff check mcp_server/

# Type checking
mypy mcp_server/
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: add new evaluation metric"
# or
git commit -m "fix: resolve Docker execution timeout"
```

Use conventional commit messages:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## What to Contribute

### High Priority

- Additional test scenarios
- Support for more programming languages
- New evaluation metrics
- Performance improvements
- Bug fixes

### Ideas Welcome

- Better error handling
- Enhanced reporting formats
- Integration with other testing frameworks
- UI for test management
- Additional safety features for code execution

## Code Style

### Python

- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Keep functions focused and small
- Write tests for new code

Example:
```python
def evaluate_solution(
    code: str,
    test_cases: List[TestCase],
    timeout: int = 30
) -> EvaluationResult:
    """
    Evaluate a code solution against test cases.

    Args:
        code: The solution code to evaluate
        test_cases: List of test cases to run
        timeout: Maximum execution time in seconds

    Returns:
        EvaluationResult with scores and feedback

    Raises:
        ExecutionError: If code execution fails
    """
    # Implementation
```

### Test Scenarios (JSON)

- Use clear, descriptive IDs
- Provide comprehensive test cases
- Include helpful hints
- Document expected behavior

## Testing

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_evaluator.py

# With coverage
pytest --cov=mcp_server
```

### Writing Tests

```python
import pytest
from mcp_server.evaluator import TestEvaluator

def test_correctness_evaluation():
    """Test that correctness is properly evaluated"""
    evaluator = TestEvaluator()

    execution_result = {
        "success": True,
        "test_results": [
            {"passed": True},
            {"passed": True},
            {"passed": False}
        ]
    }

    result = evaluator._evaluate_correctness(execution_result)

    assert result["score"] == 2/3
    assert result["passed_tests"] == 2
    assert result["total_tests"] == 3
```

## Documentation

### Code Documentation

- Add docstrings to all public functions and classes
- Use clear variable names
- Comment complex logic
- Update README.md for user-facing changes

### Test Scenario Documentation

- Provide clear descriptions
- Explain requirements thoroughly
- Include helpful hints
- Document edge cases

## Adding New Features

### New Evaluation Metric

1. Add metric to `evaluator.py`:
```python
def _evaluate_new_metric(self, code: str, scenario: TestScenario) -> Dict[str, Any]:
    """Evaluate using new metric"""
    # Implementation
    return {
        "score": 0.85,
        "details": "Metric description",
        "insights": ["Finding 1", "Finding 2"]
    }
```

2. Integrate into main evaluation flow
3. Add tests
4. Document in README

### New Programming Language

1. Add executor support in `executor.py`:
```python
async def _execute_rust(self, code: str, test_cases: List, timeout: int):
    """Execute Rust code"""
    # Implementation
```

2. Update test runner generation
3. Add example scenario
4. Document supported languages

## Pull Request Guidelines

### Before Submitting

- [ ] Tests pass
- [ ] Code is formatted (black)
- [ ] No linting errors (ruff)
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### PR Description

Include:
- What changes were made
- Why the changes are needed
- How to test the changes
- Any breaking changes
- Related issues

Example:
```markdown
## Description
Adds support for JavaScript test execution using Node.js

## Motivation
Users requested ability to test JavaScript code

## Changes
- Added `_execute_javascript` method to CodeExecutor
- Created JS test runner template
- Added example JS scenario
- Updated documentation

## Testing
- Added unit tests for JS execution
- Tested with sample scenarios
- Verified Docker and subprocess modes

## Breaking Changes
None

## Related Issues
Closes #42
```

## Community Guidelines

- Be respectful and inclusive
- Help others learn
- Give constructive feedback
- Follow the code of conduct

## Questions?

- Open an issue for bugs
- Start a discussion for ideas
- Comment on existing issues
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Agent Testing MCP Server! 🚀
