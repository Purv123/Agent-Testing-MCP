# Docker Setup Guide

Run the Agent Testing MCP Server in Docker - **no Python installation required!**

## Prerequisites

- **Docker**: Install from [docker.com](https://docs.docker.com/get-docker/)
- **Docker Compose** (optional but recommended): Usually included with Docker Desktop

## Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/Purv123/Agent-Testing-MCP.git
cd Agent-Testing-MCP

# 2. Build and run
docker-compose up -d

# 3. Check logs
docker-compose logs -f

# 4. Stop
docker-compose down
```

### Option 2: Using Docker Directly

```bash
# 1. Build the image
docker build -t agent-testing-mcp .

# 2. Run the container
docker run -it --rm \
  --name agent-testing-mcp \
  -v $(pwd)/test_scenarios:/app/test_scenarios:ro \
  -v $(pwd)/results:/app/results \
  -v $(pwd)/logs:/app/logs \
  agent-testing-mcp

# 3. Stop (Ctrl+C)
```

## Integration with Claude Code

### Using Docker Container as MCP Server

You can configure Claude Code to use the Docker container as an MCP server.

#### Method 1: Using docker run command

```bash
claude mcp add --scope user --transport stdio agent-testing \
  -- docker run -i --rm \
  -v $(pwd)/test_scenarios:/app/test_scenarios:ro \
  -v $(pwd)/results:/app/results \
  -v $(pwd)/logs:/app/logs \
  agent-testing-mcp
```

#### Method 2: Create a startup script

Create `start_mcp_docker.sh`:

```bash
#!/bin/bash
cd /path/to/Agent-Testing-MCP
docker run -i --rm \
  --name agent-testing-mcp-$(date +%s) \
  -v $(pwd)/test_scenarios:/app/test_scenarios:ro \
  -v $(pwd)/results:/app/results \
  -v $(pwd)/logs:/app/logs \
  agent-testing-mcp
```

Make it executable:
```bash
chmod +x start_mcp_docker.sh
```

Add to Claude Code:
```bash
claude mcp add --scope user --transport stdio agent-testing \
  -- /path/to/Agent-Testing-MCP/start_mcp_docker.sh
```

#### Method 3: Manual configuration

Edit `~/.claude.json`:

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
      ],
      "env": {}
    }
  }
}
```

**Important:** Replace `/full/path/to/Agent-Testing-MCP` with your actual path.

## Building the Image

### Standard Build

```bash
docker build -t agent-testing-mcp:latest .
```

### Build with specific version tag

```bash
docker build -t agent-testing-mcp:v1.0 .
```

### Build without cache (clean build)

```bash
docker build --no-cache -t agent-testing-mcp .
```

## Running Options

### Interactive Mode (Default)

```bash
docker run -it --rm agent-testing-mcp
```

### Background Mode (Daemon)

```bash
docker run -d --name agent-testing-mcp agent-testing-mcp
```

### With Environment Variables

```bash
docker run -it --rm \
  -e OPENAI_API_KEY="your-key" \
  -e DEFAULT_TIMEOUT=60 \
  agent-testing-mcp
```

### With Custom Test Scenarios

```bash
docker run -it --rm \
  -v /path/to/custom-tests:/app/test_scenarios:ro \
  agent-testing-mcp
```

## Volume Mounts Explained

- **test_scenarios** (read-only): Your test scenario definitions
- **results**: Test execution results and reports
- **logs**: Server logs for debugging

## Docker Compose Configuration

The `docker-compose.yml` includes:

- **Automatic restart**: Server restarts if it crashes
- **Resource limits**: CPU and memory constraints
- **Volume persistence**: Results and logs are saved
- **Environment variables**: Easy configuration

### Customize docker-compose.yml

Edit `docker-compose.yml` to add your OpenAI key:

```yaml
environment:
  - OPENAI_API_KEY=sk-your-actual-key-here
```

## Verify Installation

### Check if image was built

```bash
docker images | grep agent-testing-mcp
```

Should show:
```
agent-testing-mcp   latest   xxxxx   X minutes ago   XXX MB
```

### Test the container

```bash
docker run --rm agent-testing-mcp python -c "import mcp; print('MCP version:', mcp.__version__)"
```

Should output:
```
MCP version: 1.18.0
```

### Verify MCP server starts

```bash
docker run --rm agent-testing-mcp python -m mcp_server.server &
sleep 2
docker logs agent-testing-mcp
```

Should show:
```
INFO - Loaded 5 test scenarios
INFO - Agent Testing Server initialized
INFO - Starting Agent Testing MCP Server...
```

## Troubleshooting

### Issue: "Cannot connect to Docker daemon"

**Solution:**
```bash
# Start Docker Desktop (macOS/Windows)
# OR on Linux:
sudo systemctl start docker
```

### Issue: "permission denied while trying to connect"

**Solution (Linux):**
```bash
sudo usermod -aG docker $USER
# Log out and back in
```

### Issue: Volume mount not working

**Make sure paths are absolute:**
```bash
docker run -it --rm \
  -v $(pwd)/test_scenarios:/app/test_scenarios:ro \
  agent-testing-mcp
```

Use `$(pwd)` for current directory or provide full path.

### Issue: Container exits immediately

**Check logs:**
```bash
docker logs agent-testing-mcp
```

Or run interactively to see errors:
```bash
docker run -it --rm agent-testing-mcp /bin/bash
# Then inside container:
python -m mcp_server.server
```

## Updating the Image

```bash
# Pull latest code
git pull

# Rebuild image
docker-compose build
# OR
docker build -t agent-testing-mcp .

# Restart
docker-compose up -d
```

## Cleanup

### Remove stopped containers

```bash
docker rm agent-testing-mcp
```

### Remove image

```bash
docker rmi agent-testing-mcp
```

### Remove all (containers, image, volumes)

```bash
docker-compose down -v
docker rmi agent-testing-mcp
```

### Clean Docker system (free space)

```bash
docker system prune -a
```

## Publishing the Image (Optional)

### To Docker Hub

```bash
# Tag for Docker Hub
docker tag agent-testing-mcp:latest yourusername/agent-testing-mcp:latest

# Login
docker login

# Push
docker push yourusername/agent-testing-mcp:latest
```

### To GitHub Container Registry

```bash
# Tag for GHCR
docker tag agent-testing-mcp:latest ghcr.io/yourusername/agent-testing-mcp:latest

# Login
echo $GITHUB_TOKEN | docker login ghcr.io -u yourusername --password-stdin

# Push
docker push ghcr.io/yourusername/agent-testing-mcp:latest
```

Then users can pull with:
```bash
docker pull yourusername/agent-testing-mcp:latest
```

## Production Recommendations

1. **Use specific version tags** instead of `latest`
2. **Set resource limits** in docker-compose.yml
3. **Mount logs** to host for monitoring
4. **Use secrets management** for API keys
5. **Enable health checks**
6. **Use multi-stage builds** for smaller images (advanced)

## Benefits of Docker Deployment

✅ **No Python installation needed** - Works on any machine with Docker
✅ **Consistent environment** - Same Python/dependencies everywhere
✅ **Isolated** - Doesn't affect host system
✅ **Easy updates** - Just rebuild and restart
✅ **Portable** - Works on macOS, Linux, Windows
✅ **Scalable** - Can run multiple instances

---

**Need help?** See [README.md](README.md) or [INSTALLATION.md](INSTALLATION.md)
