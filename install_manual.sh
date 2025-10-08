#!/bin/bash

# Manual Installation Script for OctoPrint Tapo P110 Plugin
# This bypasses OctoPrint's Plugin Manager for direct installation

set -e

echo "🔧 OctoPrint Tapo P110 Plugin - Manual Installation"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Find OctoPrint installation
print_status "Looking for OctoPrint installation..."

# Common OctoPrint locations
OCTOPRINT_PATHS=(
    "$HOME/oprint"
    "$HOME/.local"
    "/opt/octoprint"
    "$(which octoprint 2>/dev/null | xargs dirname 2>/dev/null | xargs dirname 2>/dev/null)"
)

OCTOPRINT_PYTHON=""
OCTOPRINT_PIP=""

for path in "${OCTOPRINT_PATHS[@]}"; do
    if [[ -n "$path" && -d "$path" ]]; then
        if [[ -f "$path/bin/python" ]]; then
            OCTOPRINT_PYTHON="$path/bin/python"
            OCTOPRINT_PIP="$path/bin/pip"
            print_success "Found OctoPrint at: $path"
            break
        elif [[ -f "$path/bin/python3" ]]; then
            OCTOPRINT_PYTHON="$path/bin/python3"
            OCTOPRINT_PIP="$path/bin/pip3"
            print_success "Found OctoPrint at: $path"
            break
        fi
    fi
done

# Fallback to system Python if OctoPrint venv not found
if [[ -z "$OCTOPRINT_PYTHON" ]]; then
    print_warning "OctoPrint virtual environment not found, using system Python"
    OCTOPRINT_PYTHON="python3"
    OCTOPRINT_PIP="pip3"
fi

print_status "Using Python: $OCTOPRINT_PYTHON"
print_status "Using pip: $OCTOPRINT_PIP"

# Check Python version
print_status "Checking Python version..."
PYTHON_VERSION=$($OCTOPRINT_PYTHON --version 2>&1 | cut -d' ' -f2)
print_status "Python version: $PYTHON_VERSION"

# Install PyP100 dependency
print_status "Installing PyP100 dependency..."
$OCTOPRINT_PIP install git+https://github.com/almottier/TapoP100.git@main

if [[ $? -eq 0 ]]; then
    print_success "PyP100 installed successfully"
else
    print_error "Failed to install PyP100"
    exit 1
fi

# Install requests if not present
print_status "Installing requests dependency..."
$OCTOPRINT_PIP install "requests>=2.24.0"

# Install the plugin
print_status "Installing OctoPrint Tapo P110 Plugin..."

# Try different installation methods
INSTALL_SUCCESS=false

# Method 1: Direct from GitHub
print_status "Trying installation from GitHub..."
if $OCTOPRINT_PIP install "https://github.com/gaurav-pangam/OctoPrint-Tapo-P110/archive/main.zip"; then
    INSTALL_SUCCESS=true
    print_success "Plugin installed from GitHub"
fi

# Method 2: Local wheel if available
if [[ "$INSTALL_SUCCESS" = false && -f "dist/octoprint_tapo_p110-1.0.1-py3-none-any.whl" ]]; then
    print_status "Trying installation from local wheel..."
    if $OCTOPRINT_PIP install "dist/octoprint_tapo_p110-1.0.1-py3-none-any.whl"; then
        INSTALL_SUCCESS=true
        print_success "Plugin installed from local wheel"
    fi
fi

# Method 3: Local setup.py
if [[ "$INSTALL_SUCCESS" = false ]]; then
    print_status "Trying installation from local setup.py..."
    if $OCTOPRINT_PIP install .; then
        INSTALL_SUCCESS=true
        print_success "Plugin installed from local setup.py"
    fi
fi

if [[ "$INSTALL_SUCCESS" = false ]]; then
    print_error "All installation methods failed"
    exit 1
fi

# Verify installation
print_status "Verifying installation..."
if $OCTOPRINT_PYTHON -c "import octoprint_tapo_p110; print('Plugin imported successfully')"; then
    print_success "Plugin verification successful"
else
    print_error "Plugin verification failed"
    exit 1
fi

# Check PyP100 availability
print_status "Verifying PyP100 dependency..."
if $OCTOPRINT_PYTHON -c "from PyP100 import PyP110; print('PyP100 available')"; then
    print_success "PyP100 verification successful"
else
    print_error "PyP100 verification failed"
    exit 1
fi

echo ""
print_success "🎉 Installation completed successfully!"
echo ""
echo "Next steps:"
echo "1. Restart OctoPrint"
echo "2. Go to Settings → Plugins to verify the plugin is listed"
echo "3. Go to Settings → Tapo P110 to configure your device"
echo "4. Use the 'Test Connection' button to verify connectivity"
echo ""
echo "If you encounter issues:"
echo "- Check OctoPrint logs for error messages"
echo "- Run the debug script: python3 debug_connection.py"
echo "- Create an issue: https://github.com/gaurav-pangam/OctoPrint-Tapo-P110/issues"
echo ""
print_status "Installation log completed"
