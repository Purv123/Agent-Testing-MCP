# 🐳 Docker Quick Start - EASIEST METHOD!

**No Python installation needed. No version conflicts. Just Docker.**

## For Your Other Machine (ANY Python Version!)

### Step 1: Install Docker

- **macOS/Windows**: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Linux**:
  ```bash
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  ```

### Step 2: Clone and Build

```bash
git clone https://github.com/Purv123/Agent-Testing-MCP.git
cd Agent-Testing-MCP
docker build -t agent-testing-mcp .
```

### Step 3: Run

```bash
docker-compose up -d
```

That's it! ✅

## Configure with Claude Code

### Option 1: Using startup script

```bash
# Make script executable
chmod +x start_mcp_docker.sh

# Add to Claude Code
claude mcp add --scope user --transport stdio agent-testing \
  -- /full/path/to/Agent-Testing-MCP/start_mcp_docker.sh
```

### Option 2: Direct docker command

Add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "agent-testing": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "/full/path/to/Agent-Testing-MCP/test_scenarios:/app/test_scenarios:ro",
        "-v", "/full/path/to/Agent-Testing-MCP/results:/app/results",
        "-v", "/full/path/to/Agent-Testing-MCP/logs:/app/logs",
        "agent-testing-mcp"
      ]
    }
  }
}
```

**Replace `/full/path/to/Agent-Testing-MCP` with actual path.**

To get full path:
```bash
cd Agent-Testing-MCP && pwd
```

## Verify

```bash
docker images | grep agent-testing-mcp
```

Should show:
```
agent-testing-mcp   latest   ...   ...   ...
```

Test run:
```bash
docker run --rm agent-testing-mcp python -c "import mcp; print('Success!')"
```

## Why Docker?

✅ **Works on ANY Python version** (even 3.6, 3.7, 3.8, 3.9)
✅ **One command setup** - No dependency hell
✅ **Same environment everywhere** - No "works on my machine"
✅ **Isolated** - Won't break your system
✅ **Easy to update** - Just rebuild
✅ **Cross-platform** - macOS, Linux, Windows

## Common Commands

```bash
# Build
docker build -t agent-testing-mcp .

# Run (interactive)
docker run -it --rm agent-testing-mcp

# Run (background)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild after updates
git pull
docker-compose build
docker-compose up -d
```

## Troubleshooting

**Can't connect to Docker daemon?**
```bash
# Start Docker Desktop (macOS/Windows)
# OR on Linux:
sudo systemctl start docker
```

**Permission denied (Linux)?**
```bash
sudo usermod -aG docker $USER
# Log out and back in
```

**Need to update?**
```bash
git pull
docker build -t agent-testing-mcp .
```

---

**This is THE solution for "No matching distribution found for mcp" error!** 🎯

Full details: [DOCKER.md](DOCKER.md)
