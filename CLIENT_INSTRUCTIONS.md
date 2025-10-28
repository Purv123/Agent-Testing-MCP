# 📋 Instructions for Client Setup

## Quick Setup Checklist

### ✅ Step 1: Choose Your Installation Method

**Option A: Docker (Recommended - Works on ANY Python version)**
- Requires: Docker only
- Setup time: 5 minutes
- Difficulty: ⭐ (Easiest)

**Option B: Local Python (Only if you have Python 3.10+)**
- Requires: Python 3.10 or higher
- Setup time: 3 minutes
- Difficulty: ⭐⭐

---

## Option A: Docker Installation (Recommended)

### Prerequisites
- [ ] Docker installed
  - macOS/Windows: [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
  - Linux: `curl -fsSL https://get.docker.com | sudo sh`

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/Purv123/Agent-Testing-MCP.git
cd Agent-Testing-MCP

# 2. Run the one-command setup
./run_mcp.sh
```

**That's it!** The script will automatically:
- Check Docker installation
- Build the image (first time only, takes 2-3 minutes)
- Start the MCP server

### Expected Output
```
═══════════════════════════════════════════
  Agent Testing MCP Server - Docker
═══════════════════════════════════════════

✓ Docker is installed
✓ Docker daemon is running
⚠ Image not found. Building...
ℹ Building Docker image...
✓ Docker image built successfully
✓ Directories ready

✓ MCP Server is ready!
```

---

## Option B: Local Python Installation

### Prerequisites
- [ ] Python 3.10 or higher installed
  - Check: `python3 --version`
  - If 3.9 or lower, you **must** use Option A (Docker)

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/Purv123/Agent-Testing-MCP.git
cd Agent-Testing-MCP

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the server
./start_mcp.sh
```

### Expected Output
```
INFO - Loaded 5 test scenarios
INFO - Code executor initialized
INFO - Test evaluator initialized
INFO - Agent Testing Server initialized
INFO - Starting Agent Testing MCP Server...
```

---

## Configure with Claude Code

### For Docker Setup
```bash
# Get the full path
cd Agent-Testing-MCP && pwd
# Copy the output

# Add to Claude Code
claude mcp add --scope user --transport stdio agent-testing \
  -- /full/path/from/above/run_mcp.sh
```

### For Python Setup
```bash
# Get the full path
cd Agent-Testing-MCP && pwd
# Copy the output

# Add to Claude Code
claude mcp add --scope user --transport stdio agent-testing \
  -- /full/path/from/above/start_mcp.sh
```

### Verify Connection
```bash
claude mcp list
```

Should show:
```
agent-testing: /path/to/script - ✓ Connected
```

---

## Useful Commands (Docker)

```bash
./run_mcp.sh           # Start server
./run_mcp.sh stop      # Stop server
./run_mcp.sh logs      # View logs
./run_mcp.sh status    # Check status
./run_mcp.sh rebuild   # Rebuild image
./run_mcp.sh help      # Show all commands
```

---

## Troubleshooting

### Problem: "Docker not installed"
**Solution:** Install Docker (see Prerequisites above)

### Problem: "Docker daemon not running"
**Solution:**
- macOS/Windows: Open Docker Desktop
- Linux: `sudo systemctl start docker`

### Problem: "No matching distribution found for mcp"
**Cause:** You have Python 3.9 or lower
**Solution:** Use Docker installation (Option A)

### Problem: "Permission denied" (Linux)
**Solution:**
```bash
sudo usermod -aG docker $USER
# Log out and log back in
```

### Problem: Script not executable
**Solution:**
```bash
chmod +x run_mcp.sh
chmod +x start_mcp.sh
```

### Problem: "Module 'mcp' not found"
**Cause:** Virtual environment not activated
**Solution:**
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

---

## Verification Steps

After installation, verify everything works:

### 1. Check Server Starts
```bash
# Docker:
./run_mcp.sh status

# Python:
ps aux | grep mcp_server
```

### 2. Check Logs
```bash
# Docker:
./run_mcp.sh logs

# Python:
cat logs/mcp_server.log
```

### 3. Test with Claude Code
In Claude Code, ask:
```
List all available test scenarios
```

Should return 5 test scenarios.

---

## What You Get

- ✅ 5 pre-built test scenarios
- ✅ Automated code execution and testing
- ✅ Intelligent evaluation with scoring
- ✅ Detailed test reports
- ✅ Safe sandboxed execution
- ✅ Full MCP integration

---

## Support & Documentation

- **Quick Start:** [EASY_SETUP.md](EASY_SETUP.md)
- **Docker Guide:** [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)
- **Full Docs:** [README.md](README.md)
- **Installation Help:** [INSTALLATION.md](INSTALLATION.md)
- **Test Results:** [TEST_RESULTS.md](TEST_RESULTS.md)

---

## Need Help?

1. Check [INSTALLATION.md](INSTALLATION.md) for detailed troubleshooting
2. Review [TEST_RESULTS.md](TEST_RESULTS.md) for expected behavior
3. Open an issue on GitHub

---

## Summary

**Easiest Path:**
1. Install Docker
2. Run `./run_mcp.sh`
3. Done! ✅

**Total Time:** 5 minutes (plus Docker download if needed)

---

**Questions?** Check the documentation files or contact support.
