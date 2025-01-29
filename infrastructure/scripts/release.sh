#!/bin/bash

# Release script for Simple To-Do List CLI application
# Version: 1.0.0
# Dependencies: Python 3.6+, pip, twine (4.0.2), semver (3.0.1), keyring (24.2.0)

# Strict error handling
set -euo pipefail

# Directory setup
SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
PROJECT_ROOT=$(realpath "$SCRIPT_DIR/../..")
CLI_DIR="$PROJECT_ROOT/src/cli"
DIST_DIR="$CLI_DIR/dist"
BACKUP_DIR="$CLI_DIR/.backup"
LOG_DIR="$PROJECT_ROOT/logs/release"
VERSION=$(python3 -c 'from src.cli import __version__; print(__version__)')
RELEASE_TIMESTAMP=$(date +%Y%m%d_%H%M%S)
MAX_RETRIES=3
RETRY_DELAY=5

# Logging setup
mkdir -p "$LOG_DIR"
exec 1> >(tee -a "${LOG_DIR}/release_${RELEASE_TIMESTAMP}.log")
exec 2>&1

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Utility functions
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
}

warn() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        error "Release process failed with exit code $exit_code"
        # Restore from backup if exists
        if [ -d "${BACKUP_DIR}/${RELEASE_TIMESTAMP}" ]; then
            warn "Restoring from backup..."
            rsync -av "${BACKUP_DIR}/${RELEASE_TIMESTAMP}/" "$CLI_DIR/"
        fi
    fi
    exit $exit_code
}

trap cleanup EXIT

check_dependencies() {
    log "Checking dependencies..."
    
    # Check Python version
    if ! command -v python3 >/dev/null 2>&1; then
        error "Python 3 is not installed"
        return 1
    fi
    
    local python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if ! python3 -c 'import sys; assert sys.version_info >= (3,6)' 2>/dev/null; then
        error "Python 3.6+ is required, found version $python_version"
        return 1
    }
    
    # Check pip and required packages
    if ! command -v pip3 >/dev/null 2>&1; then
        error "pip3 is not installed"
        return 1
    }
    
    local required_packages=("twine==4.0.2" "semver==3.0.1" "keyring==24.2.0")
    for package in "${required_packages[@]}"; do
        if ! pip3 show $(echo "$package" | cut -d= -f1) >/dev/null 2>&1; then
            error "Required package $package is not installed"
            return 1
        fi
    done
    
    # Check git
    if ! command -v git >/dev/null 2>&1; then
        error "git is not installed"
        return 1
    }
    
    success "All dependencies are satisfied"
    return 0
}

validate_version() {
    local version=$1
    log "Validating version $version..."
    
    # Check semantic versioning format
    if ! python3 -c "import semver; semver.VersionInfo.parse('$version')" 2>/dev/null; then
        error "Invalid semantic version format: $version"
        return 1
    }
    
    # Check if version exists in git tags
    if git rev-parse "v$version" >/dev/null 2>&1; then
        error "Version $version already exists as a git tag"
        return 1
    }
    
    # Check if version exists on PyPI
    if python3 -m twine check "$DIST_DIR/*" >/dev/null 2>&1; then
        if curl -s "https://pypi.org/pypi/simple-todo-cli/$version/json" >/dev/null 2>&1; then
            error "Version $version already exists on PyPI"
            return 1
        fi
    fi
    
    success "Version $version is valid"
    return 0
}

create_release() {
    log "Creating release for version $VERSION..."
    
    # Create backup
    mkdir -p "${BACKUP_DIR}/${RELEASE_TIMESTAMP}"
    rsync -av "$CLI_DIR/" "${BACKUP_DIR}/${RELEASE_TIMESTAMP}/"
    
    # Run tests
    log "Running test suite..."
    if ! source "$SCRIPT_DIR/test.sh" run_tests; then
        error "Tests failed"
        return 1
    fi
    
    # Build package
    log "Building package..."
    if ! source "$SCRIPT_DIR/build.sh" build_python_package; then
        error "Package build failed"
        return 1
    fi
    
    # Create git tag
    log "Creating git tag..."
    git tag -s "v$VERSION" -m "Release version $VERSION"
    git push origin "v$VERSION"
    
    success "Release v$VERSION created successfully"
    return 0
}

publish_to_pypi() {
    log "Publishing version $VERSION to PyPI..."
    
    local attempt=1
    while [ $attempt -le $MAX_RETRIES ]; do
        log "Attempt $attempt of $MAX_RETRIES..."
        
        # Verify PyPI credentials
        if ! python3 -c "import keyring; assert keyring.get_password('pypi', 'simple-todo-cli')" 2>/dev/null; then
            error "PyPI credentials not found in keyring"
            return 1
        fi
        
        # Check package and upload
        if python3 -m twine check "$DIST_DIR/*" && \
           python3 -m twine upload --skip-existing "$DIST_DIR/*"; then
            success "Package published successfully to PyPI"
            return 0
        fi
        
        warn "Upload attempt $attempt failed. Retrying in $RETRY_DELAY seconds..."
        sleep $RETRY_DELAY
        ((attempt++))
    done
    
    error "Failed to publish package after $MAX_RETRIES attempts"
    return 1
}

main() {
    log "Starting release process..."
    
    # Check dependencies
    if ! check_dependencies; then
        error "Dependency check failed"
        exit 1
    fi
    
    # Validate version
    if ! validate_version "$VERSION"; then
        error "Version validation failed"
        exit 1
    fi
    
    # Create release
    if ! create_release; then
        error "Release creation failed"
        exit 1
    fi
    
    # Publish to PyPI
    if ! publish_to_pypi; then
        error "PyPI publication failed"
        exit 1
    }
    
    success "Release process completed successfully"
    return 0
}

# Execute main function
main