# Installation Troubleshooting

## Common Installation Issues

### Issue 1: "Unexpected error while trying to install plugin"

This usually happens due to dependency installation issues. Here are the solutions:

#### Solution A: Manual Dependency Installation

1. **SSH into your OctoPrint server** or access the terminal
2. **Install the PyP100 dependency manually**:
   ```bash
   # Activate OctoPrint's virtual environment (if using one)
   source ~/oprint/bin/activate  # Adjust path as needed
   
   # Install the required dependency
   pip install git+https://github.com/almottier/TapoP100.git@main
   ```
3. **Try installing the plugin again** through the Plugin Manager

#### Solution B: Command Line Installation

```bash
# SSH into your OctoPrint server
# Install dependencies first
pip install requests
pip install git+https://github.com/almottier/TapoP100.git@main

# Then install the plugin
pip install "https://github.com/gaurav-pangam/OctoPrint-Tapo-P110/archive/main.zip"

# Restart OctoPrint
sudo service octoprint restart
```

#### Solution C: Local Installation

1. **Download the plugin**:
   ```bash
   wget https://github.com/gaurav-pangam/OctoPrint-Tapo-P110/archive/main.zip
   unzip main.zip
   cd OctoPrint-Tapo-P110-main
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install git+https://github.com/almottier/TapoP100.git@main
   ```

3. **Install the plugin**:
   ```bash
   pip install .
   ```

### Issue 2: "PyP100 library not available" in logs

If you see this error in OctoPrint logs after installation:

1. **Install PyP100 manually**:
   ```bash
   pip install git+https://github.com/almottier/TapoP100.git@main
   ```

2. **Restart OctoPrint**:
   ```bash
   sudo service octoprint restart
   ```

### Issue 3: Plugin appears but doesn't work

1. **Check OctoPrint logs** for specific error messages
2. **Verify your Python version** (requires Python 3.7+):
   ```bash
   python3 --version
   ```
3. **Test the connection** using the included test script:
   ```bash
   cd /path/to/plugin
   python test_plugin.py
   ```

## Environment-Specific Instructions

### OctoPi (Raspberry Pi)

```bash
# SSH into your Pi
ssh pi@octopi.local

# Activate OctoPrint environment
source ~/oprint/bin/activate

# Install dependencies
pip install git+https://github.com/almottier/TapoP100.git@main

# Install plugin
pip install "https://github.com/gaurav-pangam/OctoPrint-Tapo-P110/archive/main.zip"

# Restart OctoPrint
sudo service octoprint restart
```

### Docker Installations

For Docker-based OctoPrint installations, you may need to:

1. **Access the container**:
   ```bash
   docker exec -it octoprint_container_name bash
   ```

2. **Install dependencies inside the container**:
   ```bash
   pip install git+https://github.com/almottier/TapoP100.git@main
   pip install "https://github.com/gaurav-pangam/OctoPrint-Tapo-P110/archive/main.zip"
   ```

3. **Restart the container**

### Virtual Environment Installations

If OctoPrint is running in a virtual environment:

```bash
# Find and activate the virtual environment
source /path/to/venv/bin/activate

# Install dependencies
pip install git+https://github.com/almottier/TapoP100.git@main

# Install plugin
pip install "https://github.com/gaurav-pangam/OctoPrint-Tapo-P110/archive/main.zip"
```

## Verification Steps

After installation, verify the plugin works:

1. **Check Plugin Manager**: Plugin should appear in the installed plugins list
2. **Check Settings**: Go to Settings → Tapo P110 (should be available)
3. **Check Logs**: Look for "Tapo P110 Plugin started" in OctoPrint logs
4. **Test Connection**: Use the "Test Connection" button in settings

## Getting Help

If you're still having issues:

1. **Check the logs**: Settings → Logs → Look for "tapo_p110" entries
2. **Create an issue**: [GitHub Issues](https://github.com/gaurav-pangam/OctoPrint-Tapo-P110/issues)
3. **Include information**:
   - OctoPrint version
   - Python version
   - Operating system
   - Full error message from logs
   - Installation method attempted

## Alternative Installation Methods

### Method 1: Download and Extract
1. Download: https://github.com/gaurav-pangam/OctoPrint-Tapo-P110/archive/main.zip
2. Extract the ZIP file
3. Upload the extracted folder via Plugin Manager → "Upload"

### Method 2: Git Clone
```bash
git clone https://github.com/gaurav-pangam/OctoPrint-Tapo-P110.git
cd OctoPrint-Tapo-P110
pip install .
```

## Success Indicators

You'll know the installation worked when:
- ✅ Plugin appears in Plugin Manager
- ✅ "Tapo P110" tab appears in OctoPrint interface
- ✅ Settings page is accessible
- ✅ No error messages in logs
- ✅ Test connection succeeds
