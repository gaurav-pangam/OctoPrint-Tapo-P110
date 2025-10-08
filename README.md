# OctoPrint Tapo P110 Plugin

A comprehensive OctoPrint plugin for controlling Tapo P110 smart plugs with energy monitoring, automation, and a modern web interface.

## 🌟 Features

- **🔌 Direct Device Control**: Turn your P110 on/off/toggle from OctoPrint
- **📊 Real-time Energy Monitoring**: Track power consumption, daily/monthly usage
- **🤖 Print Automation**: Auto power control based on print events
- **📱 Modern Web Interface**: Responsive design with live status updates
- **⚡ Energy Logging**: Monitor power consumption during prints
- **🔧 Easy Configuration**: Simple setup through OctoPrint settings
- **🔄 Auto-reconnection**: Handles network interruptions gracefully

## 📋 Requirements

- **OctoPrint**: 1.4.0 or newer
- **Python**: 3.7 or newer
- **Device**: Tapo P110 Smart Plug (firmware 1.1.3+)
- **Network**: P110 and OctoPrint on same network

## 🚀 Installation

### Method 1: Plugin Manager (Recommended)

1. Open OctoPrint Settings
2. Go to **Plugin Manager**
3. Click **"Get More..."**
4. Enter this URL:
   ```
   https://github.com/gaurav-pangam/OctoPrint-Tapo-P110/archive/main.zip
   ```
5. Click **"Install"**
6. Restart OctoPrint when prompted

### Method 2: Command Line

```bash
# SSH into your OctoPrint server
pip install "https://github.com/gaurav-pangam/OctoPrint-Tapo-P110/archive/main.zip"

# Restart OctoPrint
sudo service octoprint restart
```

### Method 3: Manual Installation

```bash
# Clone the repository
git clone https://github.com/gaurav-pangam/OctoPrint-Tapo-P110.git
cd OctoPrint-Tapo-P110

# Install in development mode
pip install -e .
```

## ⚙️ Configuration

### 1. Basic Setup

1. Go to **Settings** → **Tapo P110**
2. Enter your device details:
   - **Device IP**: Your P110's IP address (e.g., `192.168.1.100`)
   - **Username**: Your Tapo account email
   - **Password**: Your Tapo account password

### 2. Find Your P110 IP Address

**Option A: Router Admin Panel**
- Log into your router
- Look for "Connected Devices" or "DHCP Clients"
- Find device named "Tapo_Plug" or similar

**Option B: Network Scanner**
```bash
# Linux/Mac
nmap -sn 192.168.1.0/24 | grep -B2 "Tapo"

# Or use a mobile app like "Fing"
```

**Option C: Tapo App**
- Open Tapo app → Device Settings → Device Info

### 3. Automation Settings

- **Auto ON at Print Start**: Turn on P110 when print begins
- **Auto OFF at Print End**: Turn off P110 when print completes
- **Auto-off Delay**: Wait time before turning off (0-3600 seconds)

### 4. Energy Monitoring

- **Enable Monitoring**: Track power consumption
- **Update Interval**: How often to check energy data (10-300 seconds)

## 🎯 Usage

### Web Interface

1. **Main Tab**: Go to **"Tapo P110"** tab in OctoPrint
2. **Device Control**: Use ON/OFF/Toggle buttons
3. **Status Monitoring**: View real-time device status
4. **Energy Data**: Monitor power consumption and usage

### Manual Control

- **Turn ON**: Click green "Turn ON" button
- **Turn OFF**: Click red "Turn OFF" button  
- **Toggle**: Click orange "Toggle" button
- **Refresh**: Update status and energy data

### Automation

Once configured, the plugin will automatically:
- Turn ON your P110 when a print starts (if enabled)
- Turn OFF your P110 when a print completes (if enabled)
- Log energy consumption during prints
- Reconnect if connection is lost

## 📊 Energy Monitoring

The plugin displays:
- **Current Power**: Real-time power consumption in watts
- **Today's Energy**: Total energy used today in Wh/kWh
- **Monthly Energy**: Total energy used this month
- **Runtime**: How long the device has been on

## 🔧 Troubleshooting

### Connection Issues

**Problem**: "Failed to connect to P110"
- ✅ Verify IP address is correct
- ✅ Check P110 is powered and connected to WiFi
- ✅ Ensure OctoPrint and P110 are on same network
- ✅ Test credentials in Tapo mobile app

**Problem**: "Authentication failed"
- ✅ Use exact same email/password as Tapo app
- ✅ Check for typos in credentials
- ✅ Try logging out and back into Tapo app

### Plugin Not Appearing

**Problem**: Plugin not visible in OctoPrint
- ✅ Check installation completed successfully
- ✅ Restart OctoPrint service
- ✅ Check OctoPrint logs for errors
- ✅ Verify Python version compatibility

### Energy Data Not Updating

**Problem**: Energy monitoring not working
- ✅ Enable energy monitoring in settings
- ✅ Check update interval setting
- ✅ Verify P110 model (not P100)
- ✅ Check OctoPrint logs for errors

## 📝 Logs

Check OctoPrint logs for detailed information:
- Go to **Settings** → **Logs**
- Look for entries containing "tapo_p110"
- Common log messages:
  - `Connected to P110 with firmware X.X.X`
  - `P110 turned ON/OFF successfully`
  - `Current power: XXX mW`

## 🔄 Updates

The plugin supports automatic updates through OctoPrint's Software Update plugin:
1. Go to **Settings** → **Software Update**
2. Check for updates
3. Install when available

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/gaurav-pangam/OctoPrint-Tapo-P110/issues)
- **Discussions**: [GitHub Discussions](https://github.com/gaurav-pangam/OctoPrint-Tapo-P110/discussions)
- **Email**: pangamgaurav20@gmail.com

## 📄 License

This project is licensed under the AGPLv3 License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [almottier/TapoP100](https://github.com/almottier/TapoP100) - Tapo device communication library
- [OctoPrint](https://octoprint.org/) - The amazing 3D printer management platform
- Tapo P110 community for testing and feedback
