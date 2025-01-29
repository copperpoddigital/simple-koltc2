#!/bin/bash
set -euo pipefail

# Script version 1.0.0
# Linting and code quality check script for Simple To-Do List CLI application

# Global configuration
PYLINT_CONFIG="infrastructure/config/pylintrc"
BLACK_CONFIG="infrastructure/config/black.toml"
SOURCE_DIR="src/cli"
EXIT_CODE=0
VERBOSE=false
MIN_PYLINT_SCORE=9.0
PYTHON_VERSION=3.6
TIMEOUT=300

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Error handling
trap 'handle_error $? $LINENO $BASH_LINENO "$BASH_COMMAND" $(printf "::%s" ${FUNCNAME[@]:-})' ERR

handle_error() {
    local exit_code=$1
    local line_no=$2
    local bash_lineno=$3
    local last_command=$4
    local func_trace=$5
    log_error "Error occurred in script at line $line_no"
    log_error "Last command: $last_command"
    log_error "Exit code: $exit_code"
    if [ "$VERBOSE" = true ]; then
        log_error "Function trace: $func_trace"
    fi
    exit "$exit_code"
}

# Check dependencies and configurations
check_dependencies() {
    log_info "Checking dependencies..."
    
    # Check Python version
    local python_version
    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if (( $(echo "$python_version < $PYTHON_VERSION" | bc -l) )); then
        log_error "Python version $PYTHON_VERSION or higher required (found $python_version)"
        return 1
    }

    # Check pylint
    if ! command -v pylint &> /dev/null; then
        log_error "pylint is not installed"
        return 1
    fi
    
    # Check black
    if ! command -v black &> /dev/null; then
        log_error "black is not installed"
        return 1
    }
    
    # Check configuration files
    if [ ! -f "$PYLINT_CONFIG" ]; then
        log_error "Pylint config not found at $PYLINT_CONFIG"
        return 1
    fi
    
    if [ ! -f "$BLACK_CONFIG" ]; then
        log_error "Black config not found at $BLACK_CONFIG"
        return 1
    }
    
    # Check source directory
    if [ ! -d "$SOURCE_DIR" ]; then
        log_error "Source directory not found at $SOURCE_DIR"
        return 1
    }
    
    log_info "All dependencies satisfied"
    return 0
}

# Run Black formatter
run_black() {
    log_info "Running Black formatter..."
    local black_output
    local black_exit_code=0
    
    # Create temporary file for black output
    local black_tmp
    black_tmp=$(mktemp)
    
    # Run black with timeout
    if ! timeout "$TIMEOUT" black --config "$BLACK_CONFIG" "$SOURCE_DIR" > "$black_tmp" 2>&1; then
        black_exit_code=$?
        log_error "Black formatting failed"
        cat "$black_tmp"
        rm "$black_tmp"
        return $black_exit_code
    fi
    
    if [ "$VERBOSE" = true ]; then
        cat "$black_tmp"
    fi
    
    rm "$black_tmp"
    log_info "Black formatting completed successfully"
    return 0
}

# Run Pylint analyzer
run_pylint() {
    log_info "Running Pylint analysis..."
    local pylint_output
    local pylint_exit_code=0
    
    # Create temporary file for pylint output
    local pylint_tmp
    pylint_tmp=$(mktemp)
    
    # Run pylint with timeout
    if ! timeout "$TIMEOUT" pylint --rcfile="$PYLINT_CONFIG" "$SOURCE_DIR" > "$pylint_tmp" 2>&1; then
        pylint_exit_code=$?
        # Check if it's just a quality score failure
        if [ $pylint_exit_code -eq 32 ]; then
            log_warn "Pylint score below threshold"
        else
            log_error "Pylint analysis failed"
            cat "$pylint_tmp"
            rm "$pylint_tmp"
            return $pylint_exit_code
        fi
    fi
    
    # Extract score from pylint output
    local score
    score=$(grep "Your code has been rated at" "$pylint_tmp" | grep -o '[0-9.]*' | head -1)
    
    if [ "$VERBOSE" = true ]; then
        cat "$pylint_tmp"
    fi
    
    if (( $(echo "$score < $MIN_PYLINT_SCORE" | bc -l) )); then
        log_error "Pylint score ($score) below minimum threshold ($MIN_PYLINT_SCORE)"
        rm "$pylint_tmp"
        return 1
    fi
    
    rm "$pylint_tmp"
    log_info "Pylint analysis completed successfully (score: $score)"
    return 0
}

# Generate quality report
generate_report() {
    local report_file="quality_report.txt"
    log_info "Generating quality report..."
    
    {
        echo "=== Code Quality Report ==="
        echo "Date: $(date)"
        echo "Source Directory: $SOURCE_DIR"
        echo
        echo "=== Black Formatting ==="
        black --config "$BLACK_CONFIG" --check "$SOURCE_DIR" 2>&1 || true
        echo
        echo "=== Pylint Analysis ==="
        pylint --rcfile="$PYLINT_CONFIG" "$SOURCE_DIR" || true
    } > "$report_file"
    
    log_info "Report generated: $report_file"
}

# Parse command line arguments
while getopts "vc:t:h" opt; do
    case $opt in
        v)
            VERBOSE=true
            ;;
        c)
            SOURCE_DIR="$OPTARG"
            ;;
        t)
            TIMEOUT="$OPTARG"
            ;;
        h)
            echo "Usage: $0 [-v] [-c source_dir] [-t timeout] [-h]"
            echo "  -v: Verbose output"
            echo "  -c: Source directory (default: $SOURCE_DIR)"
            echo "  -t: Timeout in seconds (default: $TIMEOUT)"
            echo "  -h: Show this help"
            exit 0
            ;;
        \?)
            log_error "Invalid option: -$OPTARG"
            exit 1
            ;;
    esac
done

# Main execution
main() {
    log_info "Starting code quality checks..."
    
    # Check dependencies
    if ! check_dependencies; then
        EXIT_CODE=1
        return $EXIT_CODE
    fi
    
    # Run Black formatter
    if ! run_black; then
        EXIT_CODE=1
    fi
    
    # Run Pylint analyzer
    if ! run_pylint; then
        EXIT_CODE=1
    fi
    
    # Generate report if any checks failed or verbose mode is enabled
    if [ $EXIT_CODE -ne 0 ] || [ "$VERBOSE" = true ]; then
        generate_report
    fi
    
    if [ $EXIT_CODE -eq 0 ]; then
        log_info "All quality checks passed successfully"
    else
        log_error "Quality checks failed"
    fi
    
    return $EXIT_CODE
}

# Execute main function
main
exit $EXIT_CODE