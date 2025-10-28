# 🎯 Setting Up Agent Testing MCP with Cline in VS Code

Cline (formerly Claude Dev) **fully supports MCP servers**! Here's how to connect this testing framework to Cline.

---

## 📋 Prerequisites

✅ VS Code installed
✅ Cline extension installed
✅ Agent Testing MCP repository cloned

---

## 🚀 Setup Instructions

### Step 1: Prepare the MCP Server

First, ensure the MCP server is ready:

```bash
cd Agent-Testing-MCP

# Option A: Local Python (requires Python 3.10+)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Option B: Docker (works with any Python version)
./run_mcp.sh
# Press Ctrl+C after it starts successfully
```

Get the full path to the startup script:

```bash
# For local Python setup
cd Agent-Testing-MCP && pwd
# Copy this path, you'll need it: /full/path/to/Agent-Testing-MCP

# For Docker setup
cd Agent-Testing-MCP && pwd
# Same - copy this path
```

---

### Step 2: Configure MCP in Cline

#### Method 1: Using Cline Settings UI (Easiest)

1. **Open VS Code**

2. **Open Cline** (click Cline icon in sidebar or `Cmd+Shift+P` → "Cline: Open")

3. **Click the Settings/Gear icon** in Cline panel (top right)

4. **Scroll to "MCP Servers" section**

5. **Click "Add MCP Server" or "Edit MCP Settings"**

6. **Add the following configuration:**

   **For Local Python:**
   ```json
   {
     "mcpServers": {
       "agent-testing": {
         "command": "/full/path/to/Agent-Testing-MCP/start_mcp.sh",
         "args": [],
         "env": {}
       }
     }
   }
   ```

   **For Docker:**
   ```json
   {
     "mcpServers": {
       "agent-testing": {
         "command": "/full/path/to/Agent-Testing-MCP/run_mcp.sh",
         "args": [],
         "env": {}
       }
     }
   }
   ```

7. **Save the settings**

8. **Reload VS Code** (`Cmd+Shift+P` → "Developer: Reload Window")

#### Method 2: Edit Config File Directly

1. **Find Cline's MCP config file:**

   The file location varies by OS:
   - **macOS**: `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
   - **Linux**: `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
   - **Windows**: `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`

2. **Create/Edit the file:**

   ```json
   {
     "mcpServers": {
       "agent-testing": {
         "command": "/full/path/to/Agent-Testing-MCP/start_mcp.sh",
         "args": [],
         "env": {}
       }
     }
   }
   ```

   **Important:** Replace `/full/path/to/Agent-Testing-MCP` with your actual path!

3. **Save the file**

4. **Reload VS Code**

---

### Step 3: Verify Connection

1. **Open Cline in VS Code**

2. **Look for MCP indicator** - You should see:
   - A "Tools" or "MCP" section in Cline
   - Or an indicator showing MCP servers are connected

3. **Test by asking Cline:**
   ```
   List all available test scenarios from the MCP server
   ```

   You should get a response showing the 5 test scenarios!

---

## 🎯 Using Cline with MCP Tools

Once configured, you can ask Cline to use the MCP tools:

### Example 1: Browse Scenarios
**You ask Cline:**
```
What test scenarios are available?
```

**Cline will:**
- Call `list_test_scenarios` MCP tool
- Show you all 5 scenarios with details

### Example 2: Get Scenario Details
**You ask Cline:**
```
Show me the details for test scenario basic_001
```

**Cline will:**
- Call `get_test_scenario` with ID "basic_001"
- Display requirements, test cases, hints

### Example 3: Write and Submit Solution
**You ask Cline:**
```
Write a solution for the basic_001 palindrome checker test and submit it for evaluation
```

**Cline will:**
1. Call `get_test_scenario` to see requirements
2. Write the Python code
3. Call `submit_solution` with the code
4. Show you the test results
5. If tests fail, iterate and improve!

### Example 4: Execute Code
**You ask Cline:**
```
Execute this code and show me the output: [paste code]
```

**Cline will:**
- Call `execute_code` MCP tool
- Show execution results

---

## 🔧 Troubleshooting

### Issue 1: "MCP Server Failed to Start"

**Check 1:** Verify the path is correct
```bash
# Test manually
/full/path/to/Agent-Testing-MCP/start_mcp.sh
# Should start and wait (press Ctrl+C to stop)
```

**Check 2:** Make script executable
```bash
chmod +x /full/path/to/Agent-Testing-MCP/start_mcp.sh
```

**Check 3:** Check logs
```bash
cat /full/path/to/Agent-Testing-MCP/logs/mcp_server.log
```

### Issue 2: "No MCP Tools Visible"

**Solution 1:** Reload VS Code
- `Cmd+Shift+P` → "Developer: Reload Window"

**Solution 2:** Restart Cline
- Close Cline panel
- Reopen Cline

**Solution 3:** Check Cline version
- Update Cline to latest version
- Cline added MCP support in recent versions

### Issue 3: "ModuleNotFoundError"

This means the virtual environment isn't activated properly.

**Fix the start_mcp.sh script:**
```bash
#!/bin/bash
cd /full/path/to/Agent-Testing-MCP
source /full/path/to/Agent-Testing-MCP/venv/bin/activate
export PYTHONPATH=/full/path/to/Agent-Testing-MCP
exec python -m mcp_server.server
```

### Issue 4: Docker Version Not Working

**Make sure Docker is running:**
```bash
docker info
# Should show Docker daemon info
```

**Test the script:**
```bash
./run_mcp.sh status
```

---

## 📋 Available MCP Tools

Once connected, Cline can use these tools:

1. **`list_test_scenarios`**
   - Lists all available test scenarios
   - Optional: filter by category

2. **`get_test_scenario`**
   - Get detailed info about a specific test
   - Requires: scenario_id

3. **`submit_solution`**
   - Submit code for evaluation
   - Requires: scenario_id, code, language
   - Optional: explanation

4. **`execute_code`**
   - Run code in sandbox
   - Requires: code, language
   - Optional: timeout

5. **`get_test_results`**
   - Retrieve detailed test results
   - Requires: run_id

6. **`list_test_runs`**
   - List all past test runs
   - Optional: filter by scenario_id or status

---

## 🎨 Example Workflows

### Workflow 1: Complete a Challenge

**Step 1: Ask Cline**
```
I want to work on the palindrome checker challenge. Show me the requirements.
```

**Step 2: Let Cline Write Code**
```
Write a solution for basic_001 that passes all test cases
```

**Step 3: Submit and Review**
```
Submit this solution for evaluation
```

**Step 4: Iterate if Needed**
```
The test failed on case 3. Fix the code to handle spaces and punctuation correctly.
```

### Workflow 2: Debug Failing Tests

**You:**
```
I have this code [paste code]. Test it against scenario basic_001 and tell me what's wrong.
```

**Cline will:**
1. Submit the code
2. Analyze failures
3. Suggest fixes
4. Resubmit until passing

### Workflow 3: Explore All Scenarios

**You:**
```
Show me all available test scenarios and let me choose one to work on
```

**Cline will:**
1. List all scenarios
2. Wait for your choice
3. Show details of chosen scenario
4. Help you solve it

---

## 💡 Pro Tips

### Tip 1: Let Cline Drive
Instead of using CLI commands, just talk to Cline:
```
"List test scenarios"
"Solve the palindrome challenge"
"Submit my solution and show results"
```

### Tip 2: Iterate Automatically
```
Keep improving the solution until all tests pass with a score above 0.9
```

Cline will automatically submit, review results, and iterate!

### Tip 3: Learn from Results
```
Explain why my solution failed test case 3 and teach me the correct approach
```

### Tip 4: Batch Processing
```
Complete all 5 test scenarios one by one, showing results for each
```

---

## 📊 Configuration Examples

### Minimal Configuration
```json
{
  "mcpServers": {
    "agent-testing": {
      "command": "/Users/yourname/Agent-Testing-MCP/start_mcp.sh"
    }
  }
}
```

### With Environment Variables
```json
{
  "mcpServers": {
    "agent-testing": {
      "command": "/Users/yourname/Agent-Testing-MCP/start_mcp.sh",
      "args": [],
      "env": {
        "PYTHONPATH": "/Users/yourname/Agent-Testing-MCP",
        "DEFAULT_TIMEOUT": "60"
      }
    }
  }
}
```

### Docker Configuration
```json
{
  "mcpServers": {
    "agent-testing": {
      "command": "/Users/yourname/Agent-Testing-MCP/run_mcp.sh",
      "args": [],
      "env": {}
    }
  }
}
```

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Cline shows MCP server connected
- [ ] Ask Cline: "List test scenarios" - shows 5 scenarios
- [ ] Ask Cline: "Show basic_001 details" - shows requirements
- [ ] Ask Cline: "Write a hello world function and execute it" - runs code
- [ ] Check logs folder - `logs/mcp_server.log` has entries

---

## 🆚 Cline vs CLI vs Cursor

### Use Cline (MCP) when:
✅ You want AI to autonomously solve challenges
✅ You want conversational interaction
✅ You want AI to iterate until tests pass
✅ You prefer VS Code integrated experience

### Use CLI when:
✅ You're writing code manually
✅ You want quick testing
✅ You're scripting/automating
✅ You don't need AI assistance

### Use Cursor when:
✅ You have Cursor subscription
✅ You want Cursor's AI features for coding
✅ Then use CLI for testing (Cursor doesn't support MCP)

### Use All Three Together!
- **Cline** - For autonomous AI problem solving
- **Cursor** - For AI-assisted manual coding
- **CLI** - For quick testing and automation

---

## 🎓 Next Steps

1. ✅ Complete the setup above
2. ✅ Test connection with Cline
3. ✅ Try solving basic_001 with Cline's help
4. ✅ Explore all 5 scenarios
5. ✅ Create your own test scenarios

---

## 📚 Additional Resources

- **CURSOR_GUIDE.md** - Using with Cursor
- **CLI_USAGE.md** - Command-line interface
- **CLIENT_INSTRUCTIONS.md** - Installation guide
- **TEST_RESULTS.md** - Example results

---

## 🎉 You're All Set!

Cline + MCP = Powerful AI-assisted coding practice!

Ask Cline anything about the test scenarios and watch it:
- Understand requirements
- Write solutions
- Submit for testing
- Iterate until perfect

Happy coding! 🚀
