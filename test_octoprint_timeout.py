#!/usr/bin/env python3
"""
Test script to verify timeout fixes work in OctoPrint environment
Run this on your OctoPrint server to test the connection
"""

import sys
import time

# Configuration - UPDATE THESE VALUES
CONFIG = {
    'device_ip': '192.168.0.105',
    'username': 'pangamgaurav20@gmail.com',
    'password': 'Test@1234'
}

def test_progressive_timeouts():
    """Test the same progressive timeout logic as the plugin"""
    print("🔧 Testing Progressive Timeout Logic")
    print("=" * 50)
    
    try:
        from PyP100 import PyP110
    except ImportError:
        print("❌ PyP100 not available. Install with:")
        print("   pip install git+https://github.com/almottier/TapoP100.git@main")
        return False
    
    timeout_attempts = [5, 10, 15, 30]  # Same as plugin
    
    for attempt, timeout_seconds in enumerate(timeout_attempts, 1):
        print(f"\n🔄 Attempt {attempt}/{len(timeout_attempts)} with {timeout_seconds}s timeout")
        
        try:
            print(f"   Creating device instance...")
            device = PyP110.P110(CONFIG['device_ip'], CONFIG['username'], CONFIG['password'])
            
            # Try to configure timeout (same as plugin)
            configure_timeout(device, timeout_seconds)
            
            start_time = time.time()
            
            print(f"   Performing handshake...")
            device.handshake()
            handshake_time = time.time() - start_time
            
            print(f"   Performing login...")
            device.login()
            login_time = time.time() - start_time
            
            print(f"   Getting device info...")
            info = device.getDeviceInfo()
            total_time = time.time() - start_time
            
            print(f"   ✅ SUCCESS in {total_time:.2f}s!")
            print(f"      Handshake: {handshake_time:.2f}s")
            print(f"      Login: {login_time:.2f}s")
            print(f"      Total: {total_time:.2f}s")
            
            if isinstance(info, dict):
                print(f"      Model: {info.get('model', 'Unknown')}")
                print(f"      Firmware: {info.get('fw_ver', 'Unknown')}")
                print(f"      Status: {'ON' if info.get('device_on') else 'OFF'}")
            
            return True
            
        except Exception as e:
            elapsed = time.time() - start_time
            error_type = type(e).__name__
            
            if 'timeout' in str(e).lower() or 'read timed out' in str(e).lower():
                print(f"   ⏱️  Timeout after {elapsed:.2f}s: {e}")
                if attempt < len(timeout_attempts):
                    print(f"   🔄 Retrying with longer timeout...")
                    continue
                else:
                    print(f"   ❌ All timeout attempts failed")
                    return False
            else:
                print(f"   ❌ Non-timeout error: {error_type}: {e}")
                return False
    
    return False

def configure_timeout(device, timeout_seconds):
    """Configure timeout for device (same logic as plugin)"""
    try:
        if hasattr(device, 'timeout'):
            device.timeout = timeout_seconds
            print(f"      Set device.timeout = {timeout_seconds}")
        elif hasattr(device, '_timeout'):
            device._timeout = timeout_seconds
            print(f"      Set device._timeout = {timeout_seconds}")
        elif hasattr(device, 'session'):
            if hasattr(device.session, 'timeout'):
                device.session.timeout = timeout_seconds
                print(f"      Set session.timeout = {timeout_seconds}")
    except Exception as e:
        print(f"      Could not configure timeout: {e}")

def test_environment_info():
    """Test environment information"""
    print("🔍 Environment Information")
    print("=" * 50)
    
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    # Test PyP100 availability
    try:
        import PyP100
        print(f"PyP100 location: {PyP100.__file__}")
        
        # Check for version info
        if hasattr(PyP100, '__version__'):
            print(f"PyP100 version: {PyP100.__version__}")
        else:
            print("PyP100 version: Unknown")
            
    except ImportError:
        print("❌ PyP100 not available")
        return False
    
    # Test requests library
    try:
        import requests
        print(f"Requests version: {requests.__version__}")
    except ImportError:
        print("❌ Requests not available")
    
    return True

def test_basic_connectivity():
    """Test basic connectivity"""
    print("\n🌐 Basic Connectivity Test")
    print("=" * 50)
    
    import subprocess
    import socket
    
    # Test ping
    try:
        result = subprocess.run(['ping', '-c', '3', CONFIG['device_ip']], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Ping successful")
        else:
            print("❌ Ping failed")
            print(f"   Error: {result.stderr}")
    except Exception as e:
        print(f"❌ Ping test failed: {e}")
    
    # Test port 80
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        start_time = time.time()
        result = sock.connect_ex((CONFIG['device_ip'], 80))
        elapsed = time.time() - start_time
        sock.close()
        
        if result == 0:
            print(f"✅ Port 80 accessible in {elapsed:.2f}s")
        else:
            print(f"❌ Port 80 not accessible")
    except Exception as e:
        print(f"❌ Port test failed: {e}")

def main():
    """Main test function"""
    print("🧪 OctoPrint Timeout Fix Verification")
    print("=" * 60)
    print(f"Testing: {CONFIG['device_ip']}")
    print(f"Account: {CONFIG['username']}")
    
    # Check if config is updated
    if CONFIG['device_ip'] == '192.168.0.105' and CONFIG['username'] == 'pangamgaurav20@gmail.com':
        print("\n⚠️  Using default config - update CONFIG values at top of script if needed")
    
    # Test environment
    if not test_environment_info():
        print("\n❌ Environment test failed")
        return
    
    # Test connectivity
    test_basic_connectivity()
    
    # Test progressive timeouts
    print("\n" + "=" * 60)
    success = test_progressive_timeouts()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 SUCCESS! The timeout fix should work in OctoPrint")
        print("\nNext steps:")
        print("1. Update your OctoPrint plugin to the latest version")
        print("2. Restart OctoPrint")
        print("3. Try the connection again")
        print("4. Check logs for 'attempt X/4' messages showing progressive timeouts")
    else:
        print("❌ FAILED! There may be deeper network issues")
        print("\nTroubleshooting:")
        print("1. Check if device IP is correct")
        print("2. Verify credentials are correct")
        print("3. Check network connectivity")
        print("4. Try running this script with different timeout values")

if __name__ == "__main__":
    main()
