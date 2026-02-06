#!/bin/bash

# Prefect Docker Workflow Runner Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  dev        - Run in development mode with live reload"
    echo "  prod       - Run in production mode"
    echo "  server     - Start Prefect server only"
    echo "  full       - Start complete stack (server + workflow)"
    echo "  worker     - Start Prefect worker"
    echo "  build      - Build all Docker images"
    echo "  clean      - Clean up containers and volumes"
    echo "  logs       - Show logs from all services"
    echo "  test       - Run the workflow once for testing"
    echo ""
    echo "Examples:"
    echo "  $0 dev                    # Development mode"
    echo "  $0 prod                   # Production mode"
    echo "  $0 server                 # Server only"
    echo "  MATH_X=25 MATH_Y=15 $0 test   # Test with custom values"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to build images
build_images() {
    print_status "Building Docker images..."
    docker-compose build
}

# Function to run in development mode
run_dev() {
    print_status "Starting development environment..."
    docker-compose up prefect-server prefect-dev
}

# Function to run in production mode
run_prod() {
    print_status "Starting production environment..."
    docker-compose up -d prefect-server
    sleep 10  # Wait for server to start
    docker-compose up prefect-workflow
}

# Function to start server only
run_server() {
    print_status "Starting Prefect server..."
    docker-compose up prefect-server
}

# Function to run full stack
run_full() {
    print_status "Starting full Prefect stack..."
    docker-compose up
}

# Function to start worker
run_worker() {
    print_status "Starting Prefect worker..."
    docker-compose up prefect-worker
}

# Function to clean up
clean_up() {
    print_warning "Cleaning up containers and volumes..."
    docker-compose down -v
    docker system prune -f
    print_status "Cleanup completed"
}

# Function to show logs
show_logs() {
    docker-compose logs -f
}

# Function to test workflow
test_workflow() {
    print_status "Testing workflow with values X=${MATH_X:-10}, Y=${MATH_Y:-5}"
    docker-compose run --rm prefect-workflow
}

# Main script logic
check_docker

case "${1:-}" in
    "dev")
        build_images
        run_dev
        ;;
    "prod")
        build_images
        run_prod
        ;;
    "server")
        build_images
        run_server
        ;;
    "full")
        build_images
        run_full
        ;;
    "worker")
        build_images
        run_worker
        ;;
    "build")
        build_images
        ;;
    "clean")
        clean_up
        ;;
    "logs")
        show_logs
        ;;
    "test")
        build_images
        test_workflow
        ;;
    "help"|"-h"|"--help")
        show_usage
        ;;
    *)
        print_error "Unknown command: ${1:-}"
        echo ""
        show_usage
        exit 1
        ;;
esac