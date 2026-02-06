#!/bin/bash

# Local Python Workflow Runner (for dev containers without Docker)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_header() {
    echo -e "${BLUE}[PREFECT]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  run        - Run the workflow with default values"
    echo "  test       - Run workflow with test values"
    echo "  server     - Start Prefect server (background)"
    echo "  ui         - Open Prefect UI (if server running)"
    echo "  install    - Install requirements"
    echo "  clean      - Stop any running Prefect processes"
    echo ""
    echo "Examples:"
    echo "  $0 install              # Install dependencies"
    echo "  $0 run                  # Run with default values"
    echo "  $0 test                 # Run with test values"
    echo "  MATH_X=25 MATH_Y=15 $0 run  # Custom values"
}

# Function to install requirements
install_deps() {
    print_status "Installing Python requirements..."
    pip install -r requirements.txt
    print_status "Requirements installed successfully"
}

# Function to check requirements
check_requirements() {
    if ! python -c "import prefect" 2>/dev/null; then
        print_warning "Prefect not found. Installing requirements..."
        install_deps
    fi
}

# Function to run workflow
run_workflow() {
    print_header "Running Mathematical Operations Workflow"
    echo "Parameters: X=${MATH_X:-10}, Y=${MATH_Y:-5}"
    echo "=" * 50
    
    # Set environment variables if not set
    export MATH_X=${MATH_X:-10}
    export MATH_Y=${MATH_Y:-5}
    
    # Run the workflow
    python task.py
}

# Function to run with test values
run_test() {
    print_header "Running Test Workflow"
    export MATH_X=25
    export MATH_Y=15
    run_workflow
}

# Function to start Prefect server
start_server() {
    print_status "Starting Prefect server on http://localhost:4200..."
    print_warning "Server will run in background. Use './run_local.sh clean' to stop."
    
    # Start server in background
    nohup prefect server start --host 0.0.0.0 --port 4200 > prefect_server.log 2>&1 &
    echo $! > prefect_server.pid
    
    # Wait a moment and check if it started
    sleep 3
    if ps -p $(cat prefect_server.pid) > /dev/null 2>&1; then
        print_status "Prefect server started successfully!"
        print_status "UI available at: http://localhost:4200"
        print_status "Logs: tail -f prefect_server.log"
    else
        print_error "Failed to start Prefect server. Check prefect_server.log"
    fi
}

# Function to open UI
open_ui() {
    if [[ -f prefect_server.pid ]] && ps -p $(cat prefect_server.pid) > /dev/null 2>&1; then
        print_status "Prefect UI should be available at: http://localhost:4200"
        print_status "Open this URL in your browser"
    else
        print_error "Prefect server doesn't seem to be running"
        print_status "Start it with: $0 server"
    fi
}

# Function to clean up
clean_up() {
    print_status "Stopping Prefect processes..."
    
    # Stop server if running
    if [[ -f prefect_server.pid ]]; then
        local pid=$(cat prefect_server.pid)
        if ps -p $pid > /dev/null 2>&1; then
            kill $pid
            print_status "Stopped Prefect server (PID: $pid)"
        fi
        rm -f prefect_server.pid
    fi
    
    # Clean up log files
    rm -f prefect_server.log
    
    # Kill any remaining prefect processes
    pkill -f "prefect server" 2>/dev/null || true
    
    print_status "Cleanup completed"
}

# Main script logic
case "${1:-}" in
    "install")
        install_deps
        ;;
    "run")
        check_requirements
        run_workflow
        ;;
    "test")
        check_requirements
        run_test
        ;;
    "server")
        check_requirements
        start_server
        ;;
    "ui")
        open_ui
        ;;
    "clean")
        clean_up
        ;;
    "help"|"-h"|"--help")
        show_usage
        ;;
    *)
        if [[ -z "${1:-}" ]]; then
            print_status "No command specified. Running workflow with default values..."
            check_requirements
            run_workflow
        else
            print_error "Unknown command: ${1}"
            echo ""
            show_usage
            exit 1
        fi
        ;;
esac