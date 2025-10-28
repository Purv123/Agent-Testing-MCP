# ⚡ Quick Setup: Cline + MCP (5 Minutes)

## Step 1: Get the Path
```bash
cd Agent-Testing-MCP
pwd
# Copy this path!
```

## Step 2: Configure Cline

### Option A: Cline UI (Easiest)

1. Open **Cline** in VS Code (sidebar icon)
2. Click **Settings/Gear** icon (top right)
3. Find **"MCP Servers"** section
4. Click **"Edit MCP Settings"**
5. Add this (replace the path):

```json
{
  "mcpServers": {
    "agent-testing": {
      "command": "/PASTE/YOUR/PATH/HERE/start_mcp.sh"
    }
  }
}
```

6. **Save** and **Reload VS Code**

### Option B: Config File

Edit `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "agent-testing": {
      "command": "/full/path/to/Agent-Testing-MCP/start_mcp.sh"
    }
  }
}
```

## Step 3: Test It!

In Cline chat, type:
```
List all test scenarios
```

Should show 5 scenarios! ✅

## Step 4: Start Coding!

```
Show me the palindrome checker challenge and help me solve it
```

Cline will:
1. Get requirements
2. Write solution
3. Submit for testing
4. Iterate until perfect!

---

## 🎯 Common Commands for Cline

Just talk naturally:

- `"List test scenarios"`
- `"Show me basic_001 details"`
- `"Write a solution for basic_001"`
- `"Submit my solution for testing"`
- `"Fix the failing tests"`
- `"Solve all 5 scenarios"`

---

## 🔧 Troubleshooting

**MCP not connecting?**
```bash
# Make script executable
chmod +x /path/to/start_mcp.sh

# Test manually
/path/to/start_mcp.sh
# Should start (Ctrl+C to stop)
```

**Still not working?**
- Check `logs/mcp_server.log`
- Reload VS Code completely
- See CLINE_SETUP.md for detailed troubleshooting

---

## 📚 Full Documentation

- **CLINE_SETUP.md** ← Detailed setup guide
- **CLI_USAGE.md** ← Command-line usage
- **CURSOR_GUIDE.md** ← Using with Cursor

---

**That's it! Enjoy AI-powered coding practice! 🚀**
