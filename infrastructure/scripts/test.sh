#!/bin/bash

# Test execution script for Simple To-Do List CLI application
# Version: 1.0
# Requires: Docker, Docker Compose, Bash 4.0+

# Enable strict error handling
set -euo pipefail

# Global variables
SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
PROJECT_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)
COMPOSE_FILE="$PROJECT_ROOT/infrastructure/templates/docker-compose.test.yml"
TEST_RESULTS_DIR="$PROJECT_ROOT/test-results"
LOG_FILE="$TEST_RESULTS_DIR/test-execution.log"
CONTAINER_NAME="todo-app-test"
MAX_RETRIES=3
TEST_TIMEOUT=600

# Color definitions for console output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log_message() {
    local message="$1"
    local level="${2:-INFO}"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Format the message
    local formatted_message="[$timestamp] [$level] $message"
    
    # Console output with color
    case "$level" in
        "ERROR")
            echo -e "${RED}${formatted_message}${NC}" >&2
            ;;
        "WARNING")
            echo -e "${YELLOW}${formatted_message}${NC}" >&2
            ;;
        "SUCCESS")
            echo -e "${GREEN}${formatted_message}${NC}"
            ;;
        *)
            echo -e "${formatted_message}"
            ;;
    esac
    
    # Log file output
    echo "$formatted_message" >> "$LOG_FILE"
}

# Dependency check function
check_dependencies() {
    log_message "Checking dependencies..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_message "Docker is not installed" "ERROR"
        return 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_message "Docker Compose is not installed" "ERROR"
        return 1
    }
    
    # Check configuration files
    if [ ! -f "$COMPOSE_FILE" ]; then
        log_message "Docker Compose file not found: $COMPOSE_FILE" "ERROR"
        return 1
    }
    
    log_message "All dependencies satisfied" "SUCCESS"
    return 0
}

# Cleanup function
cleanup() {
    local exit_code=$?
    log_message "Starting cleanup process..."
    
    # Stop and remove test container
    if docker ps -a | grep -q "$CONTAINER_NAME"; then
        log_message "Stopping test container..."
        docker-compose -f "$COMPOSE_FILE" down --volumes --remove-orphans || true
    fi
    
    # Clean up test results if empty
    if [ -d "$TEST_RESULTS_DIR" ] && [ -z "$(ls -A "$TEST_RESULTS_DIR")" ]; then
        rm -rf "$TEST_RESULTS_DIR"
    fi
    
    log_message "Cleanup completed" "SUCCESS"
    exit "$exit_code"
}

# Set up trap for cleanup
trap cleanup EXIT SIGINT SIGTERM SIGQUIT

# Test environment setup function
setup_test_environment() {
    log_message "Setting up test environment..."
    
    # Create test results directory
    mkdir -p "$TEST_RESULTS_DIR"
    chmod 755 "$TEST_RESULTS_DIR"
    
    # Initialize log file
    touch "$LOG_FILE"
    chmod 644 "$LOG_FILE"
    
    # Build/pull test container
    log_message "Building test container..."
    if ! docker-compose -f "$COMPOSE_FILE" build; then
        log_message "Failed to build test container" "ERROR"
        return 1
    fi
    
    log_message "Test environment setup completed" "SUCCESS"
    return 0
}

# Test execution function
run_tests() {
    local retry_count=0
    local test_status=1
    
    while [ $retry_count -lt $MAX_RETRIES ] && [ $test_status -ne 0 ]; do
        if [ $retry_count -gt 0 ]; then
            log_message "Retrying test execution (Attempt $((retry_count + 1)))" "WARNING"
        fi
        
        log_message "Starting test execution..."
        
        # Run tests with timeout
        if timeout "$TEST_TIMEOUT" docker-compose -f "$COMPOSE_FILE" run \
            --rm \
            -v "$TEST_RESULTS_DIR:/app/test-results" \
            "$CONTAINER_NAME" pytest \
            --junitxml=/app/test-results/junit.xml \
            --cov=/app/src \
            --cov-report=xml:/app/test-results/coverage.xml \
            --cov-report=html:/app/test-results/htmlcov; then
            
            test_status=0
            log_message "Tests completed successfully" "SUCCESS"
        else
            test_status=$?
            log_message "Test execution failed with status $test_status" "ERROR"
            ((retry_count++))
        fi
    done
    
    # Check if we exceeded retries
    if [ $test_status -ne 0 ]; then
        log_message "Tests failed after $MAX_RETRIES attempts" "ERROR"
    fi
    
    return $test_status
}

# Main execution function
main() {
    log_message "Starting test execution script..."
    
    # Check dependencies
    if ! check_dependencies; then
        log_message "Dependency check failed" "ERROR"
        exit 1
    fi
    
    # Set up test environment
    if ! setup_test_environment; then
        log_message "Test environment setup failed" "ERROR"
        exit 1
    fi
    
    # Run tests
    if ! run_tests; then
        log_message "Test execution failed" "ERROR"
        exit 1
    fi
    
    log_message "Test execution completed successfully" "SUCCESS"
    exit 0
}

# Execute main function
main