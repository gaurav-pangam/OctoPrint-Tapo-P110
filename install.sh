#!/bin/bash
# OctoPrint Tapo P110 Plugin Installation Script

echo "🚀 Installing OctoPrint Tapo P110 Plugin..."
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo "❌ Error: setup.py not found. Please run this script from the plugin directory."
    exit 1
fi

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ Error: pip is not installed or not in PATH."
    exit 1
fi

echo "✅ Found setup.py and pip"

# Install the plugin
echo "📦 Installing plugin and dependencies..."
pip install -e .

if [ $? -eq 0 ]; then
    echo "✅ Plugin installed successfully!"
    echo ""
    echo "🎯 Next steps:"
    echo "1. Restart OctoPrint:"
    echo "   sudo service octoprint restart"
    echo ""
    echo "2. Configure the plugin:"
    echo "   - Go to OctoPrint Settings → Tapo P110"
    echo "   - Enter your P110 IP address"
    echo "   - Enter your Tapo account credentials"
    echo "   - Test the connection"
    echo ""
    echo "3. Optional: Test before installing:"
    echo "   python test_plugin.py"
    echo ""
    echo "📚 See README.md for detailed setup instructions"
else
    echo "❌ Installation failed. Check the error messages above."
    exit 1
fi
