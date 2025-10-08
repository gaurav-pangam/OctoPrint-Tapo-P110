#!/usr/bin/env python3
"""
Debug script for OctoPrint Tapo P110 Plugin connection issues
Run this script to test your P110 connection outside of OctoPrint
"""

import sys
import traceback

# Test configuration - UPDATE THESE VALUES
DEBUG_CONFIG = {
    'device_ip': '192.168.1.100',      # Your P110's IP address
    'username': 'your@email.com',      # Your Tapo account email
    'password': 'your_password'        # Your Tapo account password
}

def test_basic_connectivity():
    """Test basic network connectivity to the device"""
    import subprocess
    import socket
    
    print("🌐 Testing Basic Connectivity...")
    print(f"📍 Target IP: {DEBUG_CONFIG['device_ip']}")
    
    # Test ping
    try:
        result = subprocess.run(['ping', '-c', '3', DEBUG_CONFIG['device_ip']], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Ping successful - Device is reachable")
        else:
            print("❌ Ping failed - Device may be unreachable")
            print(f"   Error: {result.stderr}")
    except Exception as e:
        print(f"❌ Ping test failed: {e}")
    
    # Test port connectivity
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((DEBUG_CONFIG['device_ip'], 9999))
        sock.close()
        
        if result == 0:
            print("✅ Port 9999 is open - Device is listening")
        else:
            print("❌ Port 9999 is not accessible")
    except Exception as e:
        print(f"❌ Port test failed: {e}")

def test_pyp100_import():
    """Test if PyP100 library is available"""
    print("\n📦 Testing PyP100 Library...")
    
    try:
        from PyP100 import PyP110
        print("✅ PyP100 library imported successfully")
        return PyP110
    except ImportError as e:
        print("❌ PyP100 library not found")
        print("   Install with: pip install git+https://github.com/almottier/TapoP100.git@main")
        return None
    except Exception as e:
        print(f"❌ PyP100 import error: {e}")
        return None

def test_device_connection(PyP110):
    """Test actual device connection and authentication"""
    print("\n🔌 Testing Device Connection...")
    
    if not PyP110:
        print("❌ Cannot test - PyP100 library not available")
        return None
    
    try:
        # Create device instance
        device = PyP110.P110(
            DEBUG_CONFIG['device_ip'],
            DEBUG_CONFIG['username'],
            DEBUG_CONFIG['password']
        )
        print("✅ Device instance created")
        
        # Test handshake
        print("🤝 Testing handshake...")
        device.handshake()
        print("✅ Handshake successful")
        
        # Test login
        print("🔐 Testing login...")
        device.login()
        print("✅ Login successful")
        
        return device
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        traceback.print_exc()
        return None

def test_device_operations(device):
    """Test device operations"""
    print("\n📊 Testing Device Operations...")
    
    if not device:
        print("❌ Cannot test - No device connection")
        return
    
    try:
        # Test getting device info
        print("📋 Getting device info...")
        info = device.getDeviceInfo()
        print("✅ Device info retrieved:")
        print(f"   Model: {info.get('model', 'Unknown')}")
        print(f"   Nickname: {info.get('nickname', 'Unknown')}")
        print(f"   Firmware: {info.get('fw_ver', 'Unknown')}")
        print(f"   Status: {'ON' if info.get('device_on') else 'OFF'}")
        print(f"   Signal: {info.get('signal_level', 'Unknown')}")
        
        # Verify it's a P110
        if info.get('model') != 'P110':
            print(f"⚠️  Warning: Expected P110, found {info.get('model')}")
        
    except Exception as e:
        print(f"❌ Failed to get device info: {e}")
        traceback.print_exc()
    
    try:
        # Test energy monitoring (P110 specific)
        print("\n⚡ Testing energy monitoring...")
        energy = device.getEnergyUsage()
        print("✅ Energy data retrieved:")
        print(f"   Current Power: {energy.get('current_power', 0)} mW")
        print(f"   Today Energy: {energy.get('today_energy', 0)} Wh")
        print(f"   Month Energy: {energy.get('month_energy', 0)} Wh")
        
    except Exception as e:
        print(f"❌ Failed to get energy data: {e}")
        print("   This might be normal if energy monitoring is not supported")

def main():
    """Main diagnostic function"""
    print("🔧 OctoPrint Tapo P110 Plugin - Connection Diagnostic")
    print("=" * 60)
    
    # Check if configuration is updated
    if (DEBUG_CONFIG['device_ip'] == '192.168.1.100' and 
        DEBUG_CONFIG['username'] == 'your@email.com'):
        print("❌ Please update DEBUG_CONFIG with your actual device details")
        print("   Edit the values at the top of this script")
        return
    
    print(f"🎯 Testing connection to: {DEBUG_CONFIG['device_ip']}")
    print(f"👤 Using account: {DEBUG_CONFIG['username']}")
    
    # Run tests
    test_basic_connectivity()
    PyP110 = test_pyp100_import()
    device = test_device_connection(PyP110)
    test_device_operations(device)
    
    print("\n" + "=" * 60)
    print("🎉 Diagnostic completed!")
    print("\nIf all tests passed, the issue might be OctoPrint-specific.")
    print("If tests failed, fix the issues above before using the plugin.")
    print("\nFor help, create an issue at:")
    print("https://github.com/gaurav-pangam/OctoPrint-Tapo-P110/issues")

if __name__ == "__main__":
    main()
