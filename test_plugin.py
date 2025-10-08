#!/usr/bin/env python3
"""
Test script for OctoPrint Tapo P110 Plugin
Tests basic functionality without OctoPrint
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'octoprint_tapo_p110'))

from PyP100 import PyP110
import time

# Test configuration - update these values
TEST_CONFIG = {
    'device_ip': '192.168.1.100',  # Update with your P110 IP
    'username': 'your@email.com',   # Update with your Tapo username
    'password': 'your_password'     # Update with your Tapo password
}

def test_connection():
    """Test basic connection to P110"""
    print("🔌 Testing P110 Connection...")
    print(f"📍 Device IP: {TEST_CONFIG['device_ip']}")
    print(f"👤 Username: {TEST_CONFIG['username']}")
    
    try:
        device = PyP110.P110(
            TEST_CONFIG['device_ip'], 
            TEST_CONFIG['username'], 
            TEST_CONFIG['password']
        )
        
        print("🤝 Performing handshake...")
        device.handshake()
        
        print("🔐 Logging in...")
        device.login()
        
        print("✅ Connection successful!")
        return device
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None

def test_device_info(device):
    """Test getting device information"""
    print("\n📊 Testing Device Info...")
    
    try:
        info = device.getDeviceInfo()
        
        print("✅ Device info retrieved:")
        print(f"  • Model: {info.get('model', 'N/A')}")
        print(f"  • Nickname: {info.get('nickname', 'N/A')}")
        print(f"  • Firmware: {info.get('fw_ver', 'N/A')}")
        print(f"  • Hardware: {info.get('hw_ver', 'N/A')}")
        print(f"  • Device On: {info.get('device_on', 'N/A')}")
        print(f"  • Signal Level: {info.get('signal_level', 'N/A')}")
        
        # Verify it's a P110
        if info.get('model') != 'P110':
            print(f"⚠️  Warning: Expected P110, but found {info.get('model')}")
        
        return info
        
    except Exception as e:
        print(f"❌ Failed to get device info: {e}")
        return None

def test_energy_monitoring(device):
    """Test energy monitoring functionality"""
    print("\n⚡ Testing Energy Monitoring...")
    
    try:
        energy = device.getEnergyUsage()
        
        print("✅ Energy data retrieved:")
        print(f"  • Current Power: {energy.get('current_power', 'N/A')} mW")
        print(f"  • Today's Energy: {energy.get('today_energy', 'N/A')} Wh")
        print(f"  • Month's Energy: {energy.get('month_energy', 'N/A')} Wh")
        print(f"  • Today's Runtime: {energy.get('today_runtime', 'N/A')} minutes")
        print(f"  • Month's Runtime: {energy.get('month_runtime', 'N/A')} minutes")
        
        return energy
        
    except Exception as e:
        print(f"❌ Failed to get energy data: {e}")
        return None

def test_power_control(device):
    """Test power control functionality"""
    print("\n🔄 Testing Power Control...")
    
    try:
        # Get current status
        info = device.getDeviceInfo()
        current_state = info.get('device_on', False)
        print(f"📊 Current state: {'ON' if current_state else 'OFF'}")
        
        # Test toggle
        if current_state:
            print("🔴 Testing turn OFF...")
            device.turnOff()
            time.sleep(2)
            
            info = device.getDeviceInfo()
            new_state = info.get('device_on', True)
            if not new_state:
                print("✅ Turn OFF successful")
            else:
                print("❌ Turn OFF failed")
                
            # Turn back on
            print("🟢 Turning back ON...")
            device.turnOn()
            time.sleep(2)
            
        else:
            print("🟢 Testing turn ON...")
            device.turnOn()
            time.sleep(2)
            
            info = device.getDeviceInfo()
            new_state = info.get('device_on', False)
            if new_state:
                print("✅ Turn ON successful")
            else:
                print("❌ Turn ON failed")
                
            # Turn back off
            print("🔴 Turning back OFF...")
            device.turnOff()
            time.sleep(2)
        
        print("✅ Power control test completed")
        
    except Exception as e:
        print(f"❌ Power control test failed: {e}")

def main():
    """Main test function"""
    print("🚀 OctoPrint Tapo P110 Plugin Test")
    print("=" * 50)
    
    # Check configuration
    if (TEST_CONFIG['device_ip'] == '192.168.1.100' or 
        TEST_CONFIG['username'] == 'your@email.com'):
        print("❌ Please update TEST_CONFIG with your actual device details")
        print("   Edit the values at the top of this script")
        return
    
    # Test connection
    device = test_connection()
    if not device:
        print("\n❌ Cannot proceed without connection")
        return
    
    # Test device info
    device_info = test_device_info(device)
    if not device_info:
        print("\n❌ Device info test failed")
        return
    
    # Test energy monitoring
    energy_data = test_energy_monitoring(device)
    if not energy_data:
        print("\n⚠️  Energy monitoring test failed (may not be supported)")
    
    # Test power control (optional - will change device state)
    response = input("\n🔄 Test power control? This will turn your device on/off (y/N): ")
    if response.lower() in ['y', 'yes']:
        test_power_control(device)
    else:
        print("⏭️  Skipping power control test")
    
    print("\n🎉 Test completed!")
    print("\nIf all tests passed, your P110 is ready for the OctoPrint plugin!")

if __name__ == "__main__":
    main()
