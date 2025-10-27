# Installation Guide

This guide will help you set up the Agent Testing MCP Server on a new machine.

## Prerequisites

- **Python**: 3.9 or higher (3.11 recommended)
- **pip**: Latest version (upgrade with `pip install --upgrade pip`)
- **Git**: For cloning the repository
- **Docker** (Optional): For enhanced security in code execution

## Installation Steps

### 1. Check Python Version

```bash
python3 --version
# Should show Python 3.9.x or higher
```

If you don't have Python 3.9+, install it:
- **macOS**: `brew install python@3.11`
- **Ubuntu/Debian**: `sudo apt install python3.11 python3.11-venv`
- **Windows**: Download from [python.org](https://www.python.org/downloads/)

### 2. Clone the Repository

```bash
git clone https://github.com/Purv123/Agent-Testing-MCP.git
cd Agent-Testing-MCP
```

### 3. Create Virtual Environment

```bash
python3 -m venv venv
```

### 4. Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```cmd
venv\Scripts\activate
```

### 5. Upgrade pip

```bash
pip install --upgrade pip setuptools wheel
```

### 6. Install Dependencies

```bash
pip install -r requirements.txt
```

### Troubleshooting Installation Issues

#### Issue: "No matching distribution found for mcp>=1.0.0"

**Solutions:**

1. **Upgrade pip first:**
   ```bash
   pip install --upgrade pip
   ```

2. **Check Python version:**
   ```bash
   python --version
   # Must be 3.9 or higher
   ```

3. **Install mcp separately:**
   ```bash
   pip install mcp
   pip install -r requirements.txt
   ```

4. **Use specific version:**
   ```bash
   pip install mcp==1.18.0
   pip install -r requirements.txt
   ```

5. **Clear pip cache:**
   ```bash
   pip cache purge
   pip install -r requirements.txt
   ```

6. **Check network/proxy settings:**
   ```bash
   pip install --index-url https://pypi.org/simple/ mcp
   ```

#### Issue: "Command 'python3' not found"

**Solution:** Use `python` instead of `python3`:
```bash
python -m venv venv
```

#### Issue: DeepEval installation fails

DeepEval has many dependencies. If it fails:

1. **Skip DeepEval (use basic evaluation only):**
   ```bash
   # Remove deepeval from requirements.txt temporarily
   grep -v deepeval requirements.txt > requirements-minimal.txt
   pip install -r requirements-minimal.txt
   ```

2. **Install DeepEval separately later:**
   ```bash
   pip install deepeval
   ```

### 7. Verify Installation

```bash
python -c "import mcp; print('MCP version:', mcp.__version__)"
```

Should output something like:
```
MCP version: 1.18.0
```

### 8. Test the Server

```bash
python -m mcp_server.server
```

You should see:
```
INFO - Loaded 5 test scenarios
INFO - Code executor initialized
INFO - Test evaluator initialized
INFO - Starting Agent Testing MCP Server...
```

Press `Ctrl+C` to stop.

## Configuring for Claude Code

### Option 1: Using CLI (Recommended)

```bash
# Make sure start_mcp.sh is executable
chmod +x start_mcp.sh

# Add to Claude Code
claude mcp add --scope user --transport stdio agent-testing -- /full/path/to/Agent-Testing-MCP/start_mcp.sh
```

Replace `/full/path/to/` with your actual path. To get it:
```bash
pwd
# Copy the output
```

### Option 2: Manual Configuration

Edit `~/.claude.json` and add:

```json
{
  "mcpServers": {
    "agent-testing": {
      "type": "stdio",
      "command": "/full/path/to/Agent-Testing-MCP/start_mcp.sh",
      "args": [],
      "env": {}
    }
  }
}
```

### For Windows Users

Create `start_mcp.bat`:
```batch
@echo off
cd /d %~dp0
set PYTHONPATH=%~dp0
venv\Scripts\python.exe -m mcp_server.server
```

Then configure:
```json
{
  "mcpServers": {
    "agent-testing": {
      "type": "stdio",
      "command": "C:\\path\\to\\Agent-Testing-MCP\\start_mcp.bat",
      "args": [],
      "env": {}
    }
  }
}
```

## Verify MCP Connection

```bash
claude mcp list
```

Should show:
```
agent-testing: /path/to/start_mcp.sh - ✓ Connected
```

## Optional: Docker Setup

For enhanced security, install Docker:

**macOS:**
```bash
brew install --cask docker
# Open Docker Desktop once to complete setup
```

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Log out and back in
```

**Verify Docker:**
```bash
docker --version
docker pull python:3.11-slim
```

The server will auto-detect Docker and use it if available.

## Environment Variables (Optional)

Create `.env` file in the project root:

```bash
# DeepEval (for advanced AI evaluation)
OPENAI_API_KEY=your-openai-api-key-here

# Execution timeouts
DEFAULT_TIMEOUT=30
BASH_DEFAULT_TIMEOUT_MS=120000

# Force Docker usage
FORCE_DOCKER=true
```

## Updating

To update to the latest version:

```bash
git pull
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt --upgrade
```

## Uninstalling

```bash
# Remove MCP server
claude mcp remove agent-testing -s user

# Delete the directory
cd ..
rm -rf Agent-Testing-MCP
```

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/Purv123/Agent-Testing-MCP/issues)
- **Documentation**: See [README.md](README.md)
- **MCP Docs**: [Model Context Protocol](https://modelcontextprotocol.io/)

## Common Installation Errors

### SSL Certificate Errors

```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Permission Denied Errors

**macOS/Linux:**
```bash
sudo chown -R $USER:$USER venv
chmod +x start_mcp.sh
```

**Windows:**
Run terminal as Administrator

### Module Not Found After Installation

Make sure virtual environment is activated:
```bash
which python  # Should show path to venv/bin/python
```

If not, activate it again:
```bash
source venv/bin/activate  # macOS/Linux
```

---

**Successfully installed?** Check out [QUICKSTART.md](QUICKSTART.md) to start testing!
