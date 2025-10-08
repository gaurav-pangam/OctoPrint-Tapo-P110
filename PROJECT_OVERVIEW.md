# OctoPrint Tapo P110 Plugin - Project Overview

## 🎯 Project Purpose

This is a **standalone OctoPrint plugin** that provides direct control of Tapo P110 smart plugs with a modern web interface, energy monitoring, and print automation features.

## 🔑 Key Features

### Core Functionality
- **Direct Device Control**: Turn P110 on/off/toggle from OctoPrint interface
- **Real-time Status**: Live device status updates with connection monitoring
- **Energy Monitoring**: Track power consumption, daily/monthly usage statistics
- **Print Automation**: Auto power control based on print start/stop events

### Technical Features
- **Modern Web UI**: Responsive design with real-time updates
- **REST API**: Complete API for external integrations
- **Error Handling**: Robust connection management with auto-reconnection
- **Logging**: Comprehensive logging for troubleshooting

## 📁 Project Structure

```
octoprint-tapo-p110/
├── setup.py                           # Package configuration
├── requirements.txt                   # Dependencies
├── MANIFEST.in                        # Package manifest
├── README.md                          # User documentation
├── LICENSE                            # AGPLv3 license
├── PROJECT_OVERVIEW.md               # This file
├── install.sh                        # Installation script
├── test_plugin.py                    # Test script
└── octoprint_tapo_p110/              # Main plugin package
    ├── __init__.py                   # Core plugin class
    ├── templates/                    # Jinja2 templates
    │   ├── tapo_p110_settings.jinja2 # Settings page
    │   └── tapo_p110_tab.jinja2      # Main control tab
    └── static/                       # Web assets
        ├── js/
        │   └── tapo_p110.js          # Frontend JavaScript
        └── css/
            └── tapo_p110.css         # Styling
```

## 🔧 Technical Architecture

### Plugin Class Structure
- **StartupPlugin**: Initialize on OctoPrint startup
- **TemplatePlugin**: Provide web interface templates
- **SettingsPlugin**: Handle configuration management
- **AssetPlugin**: Serve CSS/JS assets
- **SimpleApiPlugin**: Expose REST API endpoints
- **EventHandlerPlugin**: React to print events

### API Endpoints
- `POST /api/plugin/tapo_p110` with commands:
  - `turn_on` - Turn device ON
  - `turn_off` - Turn device OFF
  - `toggle` - Toggle device state
  - `get_status` - Get device status
  - `get_energy` - Get energy usage data
  - `test_connection` - Test device connection

### Web Interface
- **Settings Tab**: Device configuration and automation settings
- **Main Tab**: Device control, status monitoring, energy display
- **Real-time Updates**: Auto-refresh capabilities with manual controls

## 🚀 Installation Methods

### 1. Plugin Manager (Recommended)
```
https://github.com/gaurav-pangam/OctoPrint-Tapo-P110/archive/main.zip
```

### 2. Command Line
```bash
pip install "https://github.com/gaurav-pangam/OctoPrint-Tapo-P110/archive/main.zip"
```

### 3. Development Installation
```bash
git clone https://github.com/gaurav-pangam/OctoPrint-Tapo-P110.git
cd OctoPrint-Tapo-P110
./install.sh
```

## ⚙️ Configuration Requirements

### Device Settings
- **Device IP**: Static IP address of P110 (e.g., 192.168.1.100)
- **Username**: Tapo account email address
- **Password**: Tapo account password

### Automation Options
- **Auto ON at Print Start**: Turn on P110 when print begins
- **Auto OFF at Print End**: Turn off P110 when print completes
- **Auto-off Delay**: Configurable delay (0-3600 seconds)

### Energy Monitoring
- **Enable Monitoring**: Track power consumption
- **Update Interval**: Data refresh rate (10-300 seconds)

## 🔍 Testing

### Pre-installation Test
```bash
python test_plugin.py
```

### Manual Testing Checklist
- [ ] Device connection and authentication
- [ ] Power control (on/off/toggle)
- [ ] Status monitoring and updates
- [ ] Energy data retrieval
- [ ] Web interface functionality
- [ ] Print event automation
- [ ] Error handling and reconnection

## 🛠️ Development

### Dependencies
- **PyP100**: Tapo device communication (almottier fork)
- **requests**: HTTP communication
- **OctoPrint**: Plugin framework

### Code Quality
- Comprehensive error handling
- Threaded operations for non-blocking UI
- Connection pooling and auto-reconnection
- Responsive web design
- Extensive logging for debugging

## 📊 Compatibility

### Supported Devices
- ✅ Tapo P110 (Energy monitoring smart plug)
- ✅ Firmware 1.1.3+ (Build 240523 Rel.175054 and newer)

### System Requirements
- ✅ OctoPrint 1.4.0+
- ✅ Python 3.7+
- ✅ Network connectivity between OctoPrint and P110

### Browser Compatibility
- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers (responsive design)

## 🔄 Future Enhancements

### Planned Features
- Multiple device support
- Energy usage graphs and charts
- Scheduled power control
- Integration with other OctoPrint plugins
- MQTT support for home automation
- Power consumption alerts

### Community Contributions
- Bug reports and feature requests welcome
- Pull requests accepted with proper testing
- Documentation improvements encouraged

## 📄 License

AGPLv3 - See LICENSE file for details

## 🙏 Acknowledgments

- [almottier/TapoP100](https://github.com/almottier/TapoP100) for the excellent Tapo library
- OctoPrint community for the amazing platform
- Beta testers and contributors
