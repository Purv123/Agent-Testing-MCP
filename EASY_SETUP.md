# 🚀 Easiest Setup Ever - 2 Commands!

## For Your Other Machine

No matter what Python version you have (even none!), this will work:

### Step 1: Install Docker (One Time)

**macOS/Windows:** Download [Docker Desktop](https://www.docker.com/products/docker-desktop/)

**Linux:**
```bash
curl -fsSL https://get.docker.com | sudo sh
```

### Step 2: Run It!

```bash
git clone https://github.com/Purv123/Agent-Testing-MCP.git
cd Agent-Testing-MCP
./run_mcp.sh
```

**Done!** 🎉

---

## What Just Happened?

The script automatically:
1. ✅ Checked Docker is installed
2. ✅ Built the Docker image (Python 3.11 + all dependencies)
3. ✅ Created necessary directories
4. ✅ Started the MCP server

No Python installation. No pip. No version conflicts. Just works.

---

## Use with Claude Code

```bash
claude mcp add --scope user --transport stdio agent-testing \
  -- /full/path/to/Agent-Testing-MCP/run_mcp.sh
```

Get full path:
```bash
cd Agent-Testing-MCP && pwd
```

---

## Useful Commands

```bash
./run_mcp.sh           # Start server
./run_mcp.sh stop      # Stop server
./run_mcp.sh logs      # View logs
./run_mcp.sh status    # Check status
./run_mcp.sh rebuild   # Rebuild image
./run_mcp.sh shell     # Debug shell
./run_mcp.sh help      # Show all commands
```

---

## Why This Works When pip install Failed

Your machine has Python 3.9 (or lower), but `mcp` requires Python 3.10+.

**Solution:** Docker containers have their own Python 3.11 inside!
- Your host: Python 3.9 ❌
- Docker container: Python 3.11 ✅

Your host Python doesn't matter at all!

---

## File Structure After Setup

```
Agent-Testing-MCP/
├── run_mcp.sh          ← The magic script!
├── test_scenarios/     ← Test definitions
├── results/            ← Test results (auto-created)
├── logs/               ← Server logs (auto-created)
├── Dockerfile          ← Docker image definition
└── docker-compose.yml  ← Alternative runner
```

---

## Troubleshooting

### "Docker command not found"
Install Docker first (see Step 1 above)

### "Cannot connect to Docker daemon"
**macOS/Windows:** Start Docker Desktop
**Linux:** `sudo systemctl start docker`

### "Permission denied" (Linux only)
```bash
sudo usermod -aG docker $USER
# Log out and back in
```

### "Image build failed"
```bash
./run_mcp.sh rebuild
```

---

## Update to Latest Version

```bash
cd Agent-Testing-MCP
git pull
./run_mcp.sh rebuild
```

---

## Alternative Methods (if you prefer)

### Using docker-compose
```bash
docker-compose up -d
```

### Using docker directly
```bash
docker build -t agent-testing-mcp .
docker run -it --rm agent-testing-mcp
```

---

## That's It!

**2 commands. Any Python version. Any OS. Just works.** 🎯

For more details:
- Quick guide: [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)
- Full guide: [DOCKER.md](DOCKER.md)
- Python install: [INSTALLATION.md](INSTALLATION.md)
