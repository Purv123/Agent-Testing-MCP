#!/bin/bash
# Agent Testing MCP Server - One-Click Launcher
# This script handles everything: build, run, and manage the MCP server in Docker

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="agent-testing-mcp"
CONTAINER_NAME="agent-testing-mcp-server"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Functions
print_info() {
    echo -e "${BLUE}ℹ ${NC}$1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_header() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Agent Testing MCP Server - Docker${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo ""
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed!"
        echo ""
        echo "Please install Docker:"
        echo "  - macOS/Windows: https://www.docker.com/products/docker-desktop/"
        echo "  - Linux: curl -fsSL https://get.docker.com | sh"
        exit 1
    fi
    print_success "Docker is installed"
}

# Check if Docker daemon is running
check_docker_daemon() {
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running!"
        echo ""
        echo "Please start Docker:"
        echo "  - macOS/Windows: Open Docker Desktop"
        echo "  - Linux: sudo systemctl start docker"
        exit 1
    fi
    print_success "Docker daemon is running"
}

# Check if image exists
check_image_exists() {
    if docker images "$IMAGE_NAME" | grep -q "$IMAGE_NAME"; then
        return 0
    else
        return 1
    fi
}

# Build Docker image
build_image() {
    print_info "Building Docker image..."
    cd "$SCRIPT_DIR"

    if docker build -t "$IMAGE_NAME" .; then
        print_success "Docker image built successfully"
        return 0
    else
        print_error "Failed to build Docker image"
        return 1
    fi
}

# Stop existing container
stop_existing_container() {
    if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        print_info "Stopping existing container..."
        docker stop "$CONTAINER_NAME" &> /dev/null || true
        docker rm "$CONTAINER_NAME" &> /dev/null || true
        print_success "Existing container stopped"
    fi
}

# Create necessary directories
create_directories() {
    cd "$SCRIPT_DIR"
    mkdir -p results logs
    print_success "Directories ready"
}

# Run container
run_container() {
    print_info "Starting MCP server container..."

    # Check if running in stdio mode (for MCP) or standalone
    if [ -t 0 ]; then
        # Interactive mode (standalone)
        print_info "Running in standalone mode (press Ctrl+C to stop)"
        docker run -it --rm \
            --name "$CONTAINER_NAME" \
            -v "${SCRIPT_DIR}/test_scenarios:/app/test_scenarios:ro" \
            -v "${SCRIPT_DIR}/results:/app/results" \
            -v "${SCRIPT_DIR}/logs:/app/logs" \
            "$IMAGE_NAME"
    else
        # stdio mode (for MCP communication)
        print_info "Running in stdio mode (for MCP)"
        docker run -i --rm \
            --name "${CONTAINER_NAME}-$$" \
            -v "${SCRIPT_DIR}/test_scenarios:/app/test_scenarios:ro" \
            -v "${SCRIPT_DIR}/results:/app/results" \
            -v "${SCRIPT_DIR}/logs:/app/logs" \
            "$IMAGE_NAME"
    fi
}

# Show status
show_status() {
    echo ""
    print_success "MCP Server is ready!"
    echo ""
    echo "Container: $CONTAINER_NAME"
    echo "Image: $IMAGE_NAME"
    echo ""
    echo "Volumes:"
    echo "  • test_scenarios: ${SCRIPT_DIR}/test_scenarios (read-only)"
    echo "  • results: ${SCRIPT_DIR}/results"
    echo "  • logs: ${SCRIPT_DIR}/logs"
    echo ""
}

# Main execution
main() {
    print_header

    # Checks
    check_docker
    check_docker_daemon

    # Check if image exists, build if not
    if ! check_image_exists; then
        print_warning "Image not found. Building..."
        if ! build_image; then
            print_error "Build failed. Exiting."
            exit 1
        fi
    else
        print_success "Docker image found"

        # Ask if user wants to rebuild
        if [ -t 0 ]; then  # Only ask if interactive
            echo ""
            read -p "Rebuild image? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                build_image
            fi
        fi
    fi

    # Prepare
    stop_existing_container
    create_directories

    # Show status
    show_status

    # Run
    run_container
}

# Handle script arguments
case "${1:-}" in
    build)
        print_header
        check_docker
        check_docker_daemon
        build_image
        print_success "Build complete!"
        ;;
    stop)
        print_header
        stop_existing_container
        print_success "Container stopped"
        ;;
    rebuild)
        print_header
        check_docker
        check_docker_daemon
        print_info "Rebuilding image..."
        docker rmi "$IMAGE_NAME" 2>/dev/null || true
        build_image
        print_success "Rebuild complete!"
        ;;
    logs)
        docker logs -f "$CONTAINER_NAME" 2>/dev/null || print_error "Container not running"
        ;;
    shell)
        print_info "Opening shell in container..."
        docker run -it --rm \
            -v "${SCRIPT_DIR}/test_scenarios:/app/test_scenarios:ro" \
            -v "${SCRIPT_DIR}/results:/app/results" \
            -v "${SCRIPT_DIR}/logs:/app/logs" \
            "$IMAGE_NAME" /bin/bash
        ;;
    status)
        print_header
        if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}"; then
            print_success "Container is running"
            docker ps --filter "name=${CONTAINER_NAME}" --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
        else
            print_warning "Container is not running"
        fi
        ;;
    help|--help|-h)
        print_header
        echo "Usage: $0 [COMMAND]"
        echo ""
        echo "Commands:"
        echo "  (none)    Run the MCP server (default)"
        echo "  build     Build the Docker image"
        echo "  rebuild   Rebuild the Docker image from scratch"
        echo "  stop      Stop the running container"
        echo "  logs      Show container logs"
        echo "  shell     Open a shell in the container"
        echo "  status    Show container status"
        echo "  help      Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0                  # Run the server"
        echo "  $0 build            # Build image"
        echo "  $0 rebuild          # Rebuild from scratch"
        echo "  $0 stop             # Stop server"
        echo "  $0 logs             # View logs"
        echo ""
        ;;
    *)
        main
        ;;
esac
