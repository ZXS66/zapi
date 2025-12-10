
#!/bin/bash

# Simple zapi Docker build and run script
# Usage:
#   ./run.sh [dev|prod|help]
#
# dev  - Development mode (hot reload)
# prod - Production mode
# help - Show usage

set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

show_usage() {
    echo "Usage: $0 [dev|prod|help]"
    echo "  dev   - Development mode (hot reload)"
    echo "  prod  - Production mode"
    echo "  help  - Show this help message"
    echo
    echo "Examples:"
    echo "  $0 dev"
    echo "  $0 prod"
}

main() {
    local mode="${1:-help}"
    if [ "$mode" = "help" ] || [ "$mode" = "-h" ] || [ "$mode" = "--help" ]; then
        show_usage
        exit 0
    fi

    if [ "$mode" != "dev" ] && [ "$mode" != "prod" ]; then
        print_error "Invalid mode: $mode"
        show_usage
        exit 1
    fi

    # Detect Podman or Docker
    if command -v podman &> /dev/null; then
        CT_TOOL="podman"
        print_success "Podman detected. Using Podman."
    elif command -v docker &> /dev/null; then
        CT_TOOL="docker"
        print_warning "Podman not found. Using Docker."
    else
        print_error "Neither Podman nor Docker is installed."
        exit 1
    fi

    print_status "Building image with $CT_TOOL..."
    $CT_TOOL build -t zapi .
    print_success "Image built: zapi"

    print_status "Stopping any running zapi container..."
    $CT_TOOL stop zapi_app 2>/dev/null || true
    $CT_TOOL rm zapi_app 2>/dev/null || true

    if [ "$mode" = "dev" ]; then
        print_status "Starting zapi in development mode (hot reload)..."
        $CT_TOOL run -it --name zapi_app -p 8000:8000 --env-file .env.dev zapi uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    else
        print_status "Starting zapi in production mode..."
        $CT_TOOL run -it --name zapi_app -p 8000:8000 --env-file .env zapi uvicorn app.main:app --host 0.0.0.0 --port 8000
    fi
}

main "$@"
