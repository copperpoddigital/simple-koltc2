#!/bin/bash

# Production-grade build script for Simple To-Do List CLI application
# Version: 1.0
# Requires: docker, docker-compose, python3 (>=3.6), pip

# Enable strict error handling
set -euo pipefail

# Global variables and paths
SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
PROJECT_ROOT=$(realpath "$SCRIPT_DIR/../..")
CLI_DIR="$PROJECT_ROOT/src/cli"
DOCKER_CONTEXT="$PROJECT_ROOT"
LOG_FILE="$SCRIPT_DIR/build.log"
BUILD_VERSION=$(python3 -c "import sys; sys.path.append('$CLI_DIR'); import setup; print(setup.version)")

# ANSI color codes for logging
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function with timestamp and level
log_message() {
    local message="$1"
    local level="${2:-INFO}"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Format the log message
    local log_entry="[$timestamp] [$level] $message"
    
    # Console output with colors
    case "$level" in
        "ERROR")
            echo -e "${RED}$log_entry${NC}" >&2
            ;;
        "WARNING")
            echo -e "${YELLOW}$log_entry${NC}"
            ;;
        "SUCCESS")
            echo -e "${GREEN}$log_entry${NC}"
            ;;
        *)
            echo "$log_entry"
            ;;
    esac
    
    # File output
    echo "$log_entry" >> "$LOG_FILE"
}

# Check if required build dependencies are installed
check_dependencies() {
    log_message "Checking build dependencies..."
    
    # Check Docker
    if ! docker --version > /dev/null 2>&1; then
        log_message "Docker is not installed or not in PATH" "ERROR"
        return 1
    fi
    
    # Check Docker Compose
    if ! docker-compose --version > /dev/null 2>&1; then
        log_message "Docker Compose is not installed or not in PATH" "ERROR"
        return 1
    fi
    
    # Check Python version
    if ! python3 -c "import sys; assert sys.version_info >= (3,6)" > /dev/null 2>&1; then
        log_message "Python 3.6 or higher is required" "ERROR"
        return 1
    fi
    
    # Check pip
    if ! pip --version > /dev/null 2>&1; then
        log_message "pip is not installed or not in PATH" "ERROR"
        return 1
    }
    
    # Log versions for debugging
    log_message "Docker: $(docker --version)"
    log_message "Docker Compose: $(docker-compose --version)"
    log_message "Python: $(python3 --version)"
    log_message "pip: $(pip --version)"
    
    return 0
}

# Build Docker image
build_docker_image() {
    log_message "Building Docker image version $BUILD_VERSION..."
    
    # Change to project root for Docker context
    cd "$DOCKER_CONTEXT"
    
    # Build the image with build args and cache optimization
    if ! docker build \
        --build-arg VERSION="$BUILD_VERSION" \
        --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
        --cache-from "todo-cli:latest" \
        -t "todo-cli:$BUILD_VERSION" \
        -t "todo-cli:latest" \
        -f infrastructure/Dockerfile .; then
        log_message "Docker build failed" "ERROR"
        return 1
    fi
    
    # Verify image creation
    if ! docker image inspect "todo-cli:$BUILD_VERSION" > /dev/null 2>&1; then
        log_message "Docker image verification failed" "ERROR"
        return 1
    fi
    
    # Log image details
    local image_size=$(docker image inspect "todo-cli:$BUILD_VERSION" --format='{{.Size}}')
    log_message "Docker image built successfully (size: $image_size bytes)" "SUCCESS"
    
    return 0
}

# Build Python package
build_python_package() {
    log_message "Building Python package version $BUILD_VERSION..."
    
    # Change to CLI directory
    cd "$CLI_DIR"
    
    # Clean previous builds
    rm -rf build/ dist/ *.egg-info/
    
    # Build source distribution and wheel
    if ! python3 setup.py sdist bdist_wheel; then
        log_message "Python package build failed" "ERROR"
        return 1
    fi
    
    # Verify package contents
    if ! pip install --dry-run dist/*.whl; then
        log_message "Package verification failed" "ERROR"
        return 1
    fi
    
    log_message "Python package built successfully" "SUCCESS"
    return 0
}

# Cleanup build artifacts
cleanup_builds() {
    log_message "Cleaning up build artifacts..."
    
    # Clean Python build directories
    cd "$CLI_DIR"
    rm -rf build/
    
    # Clean Docker build cache if specified
    if [ "${CLEAN_DOCKER_CACHE:-false}" = "true" ]; then
        docker builder prune -f
    fi
    
    log_message "Cleanup completed" "SUCCESS"
    return 0
}

# Main execution function
main() {
    # Initialize log file
    : > "$LOG_FILE"
    log_message "Starting build process for version $BUILD_VERSION..."
    
    # Check dependencies
    if ! check_dependencies; then
        log_message "Dependency check failed" "ERROR"
        exit 1
    fi
    
    # Build Docker image with retry
    local retries=3
    while [ $retries -gt 0 ]; do
        if build_docker_image; then
            break
        fi
        retries=$((retries-1))
        if [ $retries -gt 0 ]; then
            log_message "Retrying Docker build ($retries attempts remaining)" "WARNING"
        fi
    done
    
    if [ $retries -eq 0 ]; then
        log_message "Docker build failed after all retry attempts" "ERROR"
        exit 1
    fi
    
    # Build Python package
    if ! build_python_package; then
        log_message "Python package build failed" "ERROR"
        exit 1
    fi
    
    # Cleanup if successful
    cleanup_builds
    
    log_message "Build process completed successfully" "SUCCESS"
    return 0
}

# Execute main function
main "$@"