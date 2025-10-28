# 🎯 Using Agent Testing MCP with Cursor

Since Cursor doesn't support MCP natively, here's how to use this testing framework effectively with your Cursor subscription.

---

## 🚀 Quick Start

### Setup (One Time)

```bash
# Clone the repository
git clone https://github.com/Purv123/Agent-Testing-MCP.git
cd Agent-Testing-MCP

# Install dependencies
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Open in Cursor

```bash
# Open the project in Cursor
cursor .
# or just: Open Cursor and drag the folder
```

---

## 💡 Workflow: Cursor + CLI Testing

### Step 1: Browse Available Challenges

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
```

### Step 2: Get Test Requirements

```bash
./agent-test get basic_001
```

This shows:
- ✅ Requirements
- 🧪 Test cases
- 💡 Hints
- 📝 Starter code

### Step 3: Ask Cursor to Write the Solution

In Cursor Chat (Cmd+L or Ctrl+L):

```
I need to solve this coding challenge. Here are the requirements:

[Paste the requirements from terminal]

Please write a Python solution that:
1. Implements the is_palindrome function
2. Includes a main(text) function as entry point
3. Handles all the test cases
4. Includes proper error handling and documentation
```

### Step 4: Save and Test

Save Cursor's solution as `solution.py` in the project root, then:

```bash
./agent-test submit basic_001 solution.py
```

### Step 5: Iterate if Needed

If tests fail, copy the test results and paste into Cursor:

```
The solution failed with these test results:

[Paste test results]

Please fix the code to pass all tests.
```

Cursor will suggest improvements. Save and test again!

---

## 📋 Complete Example

### Example 1: Palindrome Checker

**Terminal:**
```bash
./agent-test get basic_001
```

**Cursor Chat:**
```
Write a Python function to check if a string is a palindrome. Requirements:
- Function name: is_palindrome(text)
- Return True/False
- Ignore case and non-alphanumeric characters
- Include main(text) entry point for testing
```

**Cursor writes:** (saves as `palindrome.py`)
```python
def is_palindrome(text):
    """Check if text is a palindrome, ignoring case and non-alphanumeric chars"""
    cleaned = ''.join(char.lower() for char in text if char.isalnum())
    return cleaned == cleaned[::-1]

def main(text):
    """Entry point for testing"""
    return is_palindrome(text)
```

**Terminal:**
```bash
./agent-test submit basic_001 palindrome.py
```

**Result:**
```
✅ PASSED
Score: 0.92/1.00
🧪 Test Cases: 5/5 passed
```

---

## 🎨 Advanced Tips

### Tip 1: Use Cursor Rules

The `.cursorrules` file in this project provides context to Cursor about:
- Available test scenarios
- Code requirements
- Testing commands
- Evaluation metrics

Cursor will automatically use this context!

### Tip 2: Quick Code Review

Before submitting, ask Cursor to review:

```
Review this code for:
- Correctness
- Code quality
- Edge cases
- Documentation
```

### Tip 3: Batch Processing

Create solutions for multiple scenarios:

```bash
# In Cursor, create files:
# - basic_001_solution.py
# - bugfix_001_solution.py
# - intermediate_001_solution.py

# Then test all:
./agent-test submit basic_001 basic_001_solution.py
./agent-test submit bugfix_001 bugfix_001_solution.py
./agent-test submit intermediate_001 intermediate_001_solution.py
```

### Tip 4: Use Cursor Composer

For complex challenges, use Cursor Composer (Cmd+I):
1. Select the starter code
2. Press Cmd+I
3. Describe the implementation
4. Cursor edits inline

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError"

**Solution:** Activate virtual environment:
```bash
source venv/bin/activate
./agent-test list
```

### Issue: Test failures

**Solution:** Copy exact error to Cursor:
```
My code failed this test case:
Input: "A man a plan a canal Panama"
Expected: True
Got: False

Please fix the is_palindrome function.
```

### Issue: Code structure

**Solution:** Always include both functions:
```python
def your_logic_function(param):
    # Your implementation
    pass

def main(input_data):
    # Entry point - required for testing!
    return your_logic_function(input_data)
```

---

## 📊 Understanding Test Results

When you run `./agent-test submit`, you get:

### 1. Execution Status
```
✅ Execution successful
or
❌ Execution Error: [error details]
```

### 2. Test Results
```
🧪 Test Cases: 5/5 passed
or
🧪 Test Cases: 3/5 passed

❌ Failed Tests:
  • Test case 3: Palindrome with spaces
    Expected: True
    Got: False
```

### 3. Evaluation Scores
```
📈 Metrics:
  Correctness     ████████████████████ 1.00
  Quality         ████████████████░░░░ 0.85
  Completeness    ███████████████████░ 0.95
  Relevance       ████████████████████ 1.00
```

### 4. Overall Result
```
Status: ✅ PASSED
Score: 0.92/1.00
Threshold: 0.70
```

### 5. Saved Files
```
💾 Results saved:
  • JSON: results/basic_001_20251028_180000.json
  • Report: results/basic_001_20251028_180000.md
```

---

## 🎯 Best Practices

### DO:
✅ Start with easier scenarios (basic_001)
✅ Read all requirements carefully
✅ Test frequently (after each change)
✅ Use Cursor for code, CLI for testing
✅ Review detailed reports in `results/`
✅ Ask Cursor to explain failures

### DON'T:
❌ Skip the `main()` function
❌ Ignore edge cases mentioned in requirements
❌ Submit without testing locally first
❌ Forget to activate virtual environment

---

## 🔄 Integration with Cursor Workflow

### Method 1: Side-by-Side

```
┌─────────────────────┬─────────────────────┐
│                     │                     │
│   Cursor Editor     │   Terminal          │
│                     │                     │
│   Write code here   │   Test here         │
│                     │   ./agent-test ...  │
│                     │                     │
└─────────────────────┴─────────────────────┘
```

### Method 2: Integrated Terminal

In Cursor:
1. Open integrated terminal (Ctrl+`)
2. Run `./agent-test` commands directly
3. Copy/paste results into Cursor chat
4. Iterate quickly

### Method 3: Cursor Tasks

Create Cursor tasks in `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Test Solution",
      "type": "shell",
      "command": "./agent-test submit ${input:scenarioId} ${file}",
      "problemMatcher": []
    }
  ],
  "inputs": [
    {
      "id": "scenarioId",
      "type": "promptString",
      "description": "Scenario ID (e.g., basic_001)"
    }
  ]
}
```

Then: `Cmd+Shift+P` → "Run Task" → "Test Solution"

---

## 🎓 Learning Path

### Beginner (Start Here)
1. `basic_001` - Palindrome Checker
2. `bugfix_001` - Fix Calculator

### Intermediate
3. `intermediate_001` - JSON Parser
4. `refactor_001` - Code Refactoring

### Advanced
5. `advanced_001` - Binary Search

---

## 📚 Additional Resources

- **CLI_USAGE.md** - Full CLI command reference
- **CLIENT_INSTRUCTIONS.md** - Installation guide
- **TEST_RESULTS.md** - Expected behavior examples
- **Results folder** - Your test reports

---

## 🤝 Combining Cursor + Claude Code

**Pro Tip:** Use both tools together!

- **Cursor (Paid)**: For writing code with AI assistance
- **Claude Code (Free)**: For MCP server testing

```bash
# Terminal 1: Cursor for coding
cursor .

# Terminal 2: Claude Code for MCP testing
claude mcp add --scope user --transport stdio agent-testing \
  -- /full/path/to/Agent-Testing-MCP/run_mcp.sh

# Now you can ask Claude Code to run tests via MCP!
```

---

## 💬 Example Conversations with Cursor

### Getting Started
**You:** "List the available test scenarios in this project"
**Cursor:** *Reads .cursorrules and lists scenarios*

### Writing Code
**You:** "Write a solution for basic_001 palindrome checker"
**Cursor:** *Generates solution with main() function*

### Debugging
**You:** "This test failed: [paste error]. Fix the code."
**Cursor:** *Analyzes error and suggests fix*

### Optimization
**You:** "Make this code more efficient and add better comments"
**Cursor:** *Refactors and documents*

---

## ✨ Summary

**Cursor** ➡️ Write code with AI assistance
**CLI** ➡️ Test and evaluate solutions
**Together** ➡️ Perfect AI-assisted coding practice!

**Workflow:**
1. `./agent-test get <id>` - See requirements
2. Ask Cursor to write solution
3. `./agent-test submit <id> <file>` - Test it
4. Share results with Cursor - Iterate
5. Repeat until ✅ PASSED!

Enjoy coding with Cursor! 🚀
