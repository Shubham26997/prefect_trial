#!/bin/bash

# Prefect Deployment Management Script

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[DEPLOY]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  create       - Create all deployments"
    echo "  list         - List all deployments"
    echo "  delete       - Delete all deployments"
    echo "  worker       - Start worker to execute deployments"
    echo "  trigger      - Trigger a specific deployment"
    echo "  schedules    - Show deployment schedules"
    echo "  logs         - Show recent flow run logs"
    echo ""
    echo "Examples:"
    echo "  $0 create                    # Create all deployments"
    echo "  $0 worker                    # Start worker"
    echo "  $0 trigger manual-math-operations  # Trigger specific deployment"
}

create_deployments() {
    print_header "Creating Prefect deployments..."
    python deploy.py
}

list_deployments() {
    print_header "Listing deployments..."
    prefect deployment ls
}

delete_deployments() {
    print_warning "Deleting all deployments..."
    
    # Get deployment names and delete them
    deployments=$(prefect deployment ls --format json | python -c "
import json, sys
data = json.load(sys.stdin)
for dep in data:
    print(dep['name'])
" 2>/dev/null || echo "")

    if [[ -z "$deployments" ]]; then
        print_warning "No deployments found to delete"
        return
    fi

    echo "$deployments" | while read -r dep_name; do
        if [[ -n "$dep_name" ]]; then
            print_status "Deleting deployment: $dep_name"
            prefect deployment delete "$dep_name" --yes 2>/dev/null || true
        fi
    done
    
    print_status "Deployment deletion completed"
}

start_worker() {
    print_header "Starting Prefect worker..."
    print_status "Worker will execute flows from deployments"
    print_status "Press Ctrl+C to stop the worker"
    print_warning "Keep this running to execute scheduled flows"
    
    # Create work pool if it doesn't exist
    prefect work-pool create --type process default-agent-pool 2>/dev/null || true
    prefect work-pool create --type process test 2>/dev/null || true
    
    # Start worker
    prefect worker start --pool default-agent-pool
}

trigger_deployment() {
    local deployment_name="$1"
    
    if [[ -z "$deployment_name" ]]; then
        print_error "Please specify deployment name"
        echo "Available deployments:"
        prefect deployment ls
        return 1
    fi
    
    print_header "Triggering deployment: $deployment_name"
    
    # Trigger the deployment
    flow_run_id=$(prefect deployment run "$deployment_name")
    print_status "Flow run started with ID: $flow_run_id"
    print_status "Check progress in UI or use: prefect flow-run logs $flow_run_id"
}

show_schedules() {
    print_header "Deployment schedules:"
    prefect deployment ls --format json | python -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for dep in data:
        schedule = dep.get('schedule', {})
        if schedule:
            print(f\"📅 {dep['name']}: {schedule.get('type', 'No schedule')} - {schedule.get('interval', schedule.get('cron', 'N/A'))}\")
        else:
            print(f\"📅 {dep['name']}: Manual trigger only\")
except:
    print('Error parsing deployment data')
"
}

show_logs() {
    print_header "Recent flow run logs..."
    prefect flow-run ls --limit 5
}

# Check if prefect server is running
check_server() {
    if ! curl -s http://localhost:4200/api/health > /dev/null 2>&1; then
        print_warning "Prefect server not detected on port 4200"
        print_status "Starting server in background..."
        nohup prefect server start --host 0.0.0.0 --port 4200 > prefect_server.log 2>&1 &
        echo $! > prefect_server.pid
        sleep 5
    fi
}

# Main script
case "${1:-}" in
    "create")
        check_server
        create_deployments
        ;;
    "list")
        list_deployments
        ;;
    "delete")
        delete_deployments
        ;;
    "worker")
        check_server
        start_worker
        ;;
    "trigger")
        trigger_deployment "$2"
        ;;
    "schedules")
        show_schedules
        ;;
    "logs")
        show_logs
        ;;
    "help"|"-h"|"--help")
        show_usage
        ;;
    *)
        if [[ -z "${1:-}" ]]; then
            print_status "No command specified. Creating deployments by default..."
            check_server
            create_deployments
        else
            print_error "Unknown command: $1"
            show_usage
            exit 1
        fi
        ;;
esac