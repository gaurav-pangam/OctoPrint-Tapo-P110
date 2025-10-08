# coding=utf-8
from __future__ import absolute_import
import threading
import time

__author__ = "Gaurav Pangam <pangamgaurav20@gmail.com>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2025 Gaurav Pangam - Released under terms of the AGPLv3 License"

import octoprint.plugin
import flask
import subprocess
import sys

# Try to import PyP100, install if not available
try:
    from PyP100 import PyP110
except ImportError:
    try:
        # Try to install PyP100 if not available
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "git+https://github.com/almottier/TapoP100.git@main"
        ])
        from PyP100 import PyP110
    except Exception as e:
        # If installation fails, we'll handle it in the plugin
        PyP110 = None


class TapoP110Plugin(octoprint.plugin.StartupPlugin,
                     octoprint.plugin.TemplatePlugin,
                     octoprint.plugin.SettingsPlugin,
                     octoprint.plugin.AssetPlugin,
                     octoprint.plugin.SimpleApiPlugin,
                     octoprint.plugin.EventHandlerPlugin):

    def __init__(self):
        self.device = None
        self.device_info = None
        self.last_status = None
        self.last_energy_data = None
        self.connection_lock = threading.Lock()

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(
            device_ip='',
            username='',
            password='',
            auto_on_print_start=False,
            auto_off_print_end=False,
            auto_off_delay=300,  # 5 minutes
            enable_energy_monitoring=True,
            energy_update_interval=30  # 30 seconds
        )

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        # Reconnect with new settings
        self._disconnect()

    ##~~ AssetPlugin mixin

    def get_assets(self):
        return dict(
            js=["js/tapo_p110.js"],
            css=["css/tapo_p110.css"]
        )

    ##~~ TemplatePlugin mixin

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False),
            dict(type="tab", custom_bindings=False)
        ]

    ##~~ SimpleApiPlugin mixin

    def get_api_commands(self):
        return dict(
            turn_on=[],
            turn_off=[],
            toggle=[],
            get_status=[],
            get_energy=[],
            test_connection=[]
        )

    def on_api_command(self, command, data):
        if command == "turn_on":
            return flask.jsonify(success=self._turn_on())
        elif command == "turn_off":
            return flask.jsonify(success=self._turn_off())
        elif command == "toggle":
            return flask.jsonify(success=self._toggle())
        elif command == "get_status":
            status = self._get_status()
            return flask.jsonify(status=status)
        elif command == "get_energy":
            energy = self._get_energy_usage()
            return flask.jsonify(energy=energy)
        elif command == "test_connection":
            return flask.jsonify(success=self._test_connection())

    ##~~ EventHandlerPlugin mixin

    def on_event(self, event, payload):
        if event == "PrintStarted" and self._settings.get_boolean(["auto_on_print_start"]):
            self._logger.info("Print started - turning on P110")
            self._turn_on()
        elif event == "PrintDone" and self._settings.get_boolean(["auto_off_print_end"]):
            delay = self._settings.get_int(["auto_off_delay"])
            self._logger.info(f"Print done - turning off P110 in {delay} seconds")
            threading.Timer(delay, self._turn_off).start()

    ##~~ Device Control Methods

    def _connect(self):
        """Connect to the P110 device with timeout handling"""
        with self.connection_lock:
            if self.device:
                return True

            # Check if PyP110 is available
            if PyP110 is None:
                self._logger.error("PyP100 library not available. Please install manually: pip install git+https://github.com/almottier/TapoP100.git@main")
                return False

            device_ip = self._settings.get(["device_ip"])
            username = self._settings.get(["username"])
            password = self._settings.get(["password"])

            if not all([device_ip, username, password]):
                self._logger.error("Device configuration incomplete")
                return False

            # Try connection with increasing timeouts to handle OctoPrint environment issues
            timeout_attempts = [5, 10, 15, 30]  # Progressive timeout values

            for attempt, timeout_seconds in enumerate(timeout_attempts, 1):
                try:
                    self._logger.info(f"Connecting to P110 at {device_ip} (attempt {attempt}/{len(timeout_attempts)}, timeout: {timeout_seconds}s)")

                    # Create device instance
                    self.device = PyP110.P110(device_ip, username, password)

                    # Try to configure timeout if possible
                    self._configure_device_timeout(self.device, timeout_seconds)

                    self._logger.debug("Performing handshake...")
                    self.device.handshake()

                    self._logger.debug("Performing login...")
                    self.device.login()

                    # Get device info to verify it's a P110
                    self._logger.debug("Getting device info...")
                    self.device_info = self.device.getDeviceInfo()

                    # Handle different response formats
                    if isinstance(self.device_info, dict):
                        device_model = self.device_info.get('model', 'Unknown')
                        firmware_version = self.device_info.get('fw_ver', 'Unknown')
                    else:
                        # Some firmware versions return different formats
                        self._logger.warning(f"Unexpected device info format: {type(self.device_info)}")
                        device_model = 'Unknown'
                        firmware_version = 'Unknown'

                    self._logger.info(f"Connected to {device_model} with firmware {firmware_version} (timeout: {timeout_seconds}s)")

                    if device_model != 'P110' and device_model != 'Unknown':
                        self._logger.warning(f"Expected P110, but connected to {device_model}")

                    return True

                except (TimeoutError, ConnectionError) as e:
                    self._logger.warning(f"Timeout/Connection error on attempt {attempt} ({timeout_seconds}s): {e}")
                    self.device = None
                    if attempt < len(timeout_attempts):
                        self._logger.info(f"Retrying with longer timeout...")
                        continue
                    else:
                        self._logger.error("All timeout attempts failed")
                        return False

                except KeyError as e:
                    self._logger.error(f"Failed to connect to P110 - Response format error: {e}")
                    self._logger.error("This might be a firmware compatibility issue. Try updating your P110 firmware.")
                    self.device = None
                    return False

                except Exception as e:
                    error_type = type(e).__name__

                    # Handle specific timeout-related errors
                    if 'timeout' in str(e).lower() or 'read timed out' in str(e).lower():
                        self._logger.warning(f"Timeout error on attempt {attempt} ({timeout_seconds}s): {e}")
                        self.device = None
                        if attempt < len(timeout_attempts):
                            self._logger.info(f"Retrying with longer timeout...")
                            continue
                        else:
                            self._logger.error("All timeout attempts failed")
                            return False
                    else:
                        # Non-timeout error, don't retry
                        self._logger.error(f"Failed to connect to P110: {e}")
                        self._logger.error(f"Error type: {error_type}")
                        # Log more details for debugging
                        import traceback
                        self._logger.debug(f"Full traceback: {traceback.format_exc()}")
                        self.device = None
                        return False

            return False

    def _configure_device_timeout(self, device, timeout_seconds):
        """Configure timeout for PyP100 device to handle OctoPrint environment issues"""
        try:
            # Try different ways to set timeout based on PyP100 implementation
            if hasattr(device, 'timeout'):
                device.timeout = timeout_seconds
                self._logger.debug(f"Set device.timeout = {timeout_seconds}")
            elif hasattr(device, '_timeout'):
                device._timeout = timeout_seconds
                self._logger.debug(f"Set device._timeout = {timeout_seconds}")
            elif hasattr(device, 'session'):
                if hasattr(device.session, 'timeout'):
                    device.session.timeout = timeout_seconds
                    self._logger.debug(f"Set session.timeout = {timeout_seconds}")

            # Try to configure requests session if available
            if hasattr(device, 'session'):
                import requests.adapters
                # Configure adapter with timeout
                adapter = requests.adapters.HTTPAdapter()
                device.session.mount('http://', adapter)
                device.session.mount('https://', adapter)
                self._logger.debug(f"Configured session adapters")

        except Exception as e:
            self._logger.debug(f"Could not configure timeout: {e}")

    def _disconnect(self):
        """Disconnect from the device"""
        with self.connection_lock:
            self.device = None
            self.device_info = None

    def _turn_on(self):
        """Turn the device ON"""
        if not self._connect():
            return False
        
        try:
            self.device.turnOn()
            self.last_status = True
            self._logger.info("P110 turned ON")
            return True
        except Exception as e:
            self._logger.error(f"Failed to turn ON: {e}")
            self._disconnect()
            return False

    def _turn_off(self):
        """Turn the device OFF"""
        if not self._connect():
            return False
        
        try:
            self.device.turnOff()
            self.last_status = False
            self._logger.info("P110 turned OFF")
            return True
        except Exception as e:
            self._logger.error(f"Failed to turn OFF: {e}")
            self._disconnect()
            return False

    def _toggle(self):
        """Toggle the device state"""
        status = self._get_status()
        if status is None:
            return False
        
        if status.get('device_on', False):
            return self._turn_off()
        else:
            return self._turn_on()

    def _get_status(self):
        """Get device status"""
        if not self._connect():
            return None

        try:
            info = self.device.getDeviceInfo()

            # Handle different response formats
            if isinstance(info, dict):
                self.last_status = info.get('device_on', False)
                return info
            else:
                self._logger.error(f"Unexpected status response format: {type(info)}")
                return None

        except KeyError as e:
            self._logger.error(f"Failed to get status - Response format error: {e}")
            self._logger.error("This might be a firmware compatibility issue.")
            self._disconnect()
            return None
        except Exception as e:
            self._logger.error(f"Failed to get status: {e}")
            self._logger.error(f"Error type: {type(e).__name__}")
            self._disconnect()
            return None

    def _get_energy_usage(self):
        """Get energy usage data"""
        if not self._connect():
            return None
        
        try:
            energy = self.device.getEnergyUsage()
            self.last_energy_data = energy
            return energy
        except Exception as e:
            self._logger.error(f"Failed to get energy usage: {e}")
            return None

    def _test_connection(self):
        """Test connection to device with detailed debugging and timeout handling"""
        self._disconnect()  # Force reconnection

        # Debug information
        device_ip = self._settings.get(["device_ip"])
        username = self._settings.get(["username"])
        password = self._settings.get(["password"])

        self._logger.info(f"Testing connection to {device_ip} with user {username}")

        # Check PyP100 availability
        if PyP110 is None:
            self._logger.error("PyP100 library not available for testing")
            return False

        # Test with progressive timeouts like the main connection method
        timeout_attempts = [5, 10, 15, 30]

        for attempt, timeout_seconds in enumerate(timeout_attempts, 1):
            try:
                self._logger.info(f"Test attempt {attempt}/{len(timeout_attempts)} with {timeout_seconds}s timeout")

                self._logger.info("Creating device instance...")
                device = PyP110.P110(device_ip, username, password)

                # Configure timeout
                self._configure_device_timeout(device, timeout_seconds)

                self._logger.info("Testing handshake...")
                device.handshake()

                self._logger.info("Testing login...")
                device.login()

                self._logger.info("Testing device info...")
                info = device.getDeviceInfo()
                self._logger.info(f"Device info received: type={type(info)}")

                if isinstance(info, dict):
                    self._logger.info(f"Model: {info.get('model', 'Unknown')}")
                    self._logger.info(f"Firmware: {info.get('fw_ver', 'Unknown')}")
                    self._logger.info(f"Device On: {info.get('device_on', 'Unknown')}")

                self._logger.info(f"✅ Test connection successful with {timeout_seconds}s timeout!")
                return True

            except Exception as e:
                error_type = type(e).__name__

                if 'timeout' in str(e).lower() or 'read timed out' in str(e).lower():
                    self._logger.warning(f"Test timeout on attempt {attempt} ({timeout_seconds}s): {e}")
                    if attempt < len(timeout_attempts):
                        self._logger.info(f"Retrying test with longer timeout...")
                        continue
                    else:
                        self._logger.error("All test timeout attempts failed")
                        return False
                else:
                    self._logger.error(f"Test connection failed: {e}")
                    self._logger.error(f"Error type: {error_type}")
                    import traceback
                    self._logger.error(f"Full traceback: {traceback.format_exc()}")
                    return False

        return False

    ##~~ Startup

    def on_after_startup(self):
        self._logger.info("Tapo P110 Plugin started")

        # Debug PyP100 availability
        if PyP110 is None:
            self._logger.error("PyP100 library is not available!")
        else:
            try:
                # Try to get PyP100 version info
                import PyP100
                self._logger.info(f"PyP100 library loaded successfully from: {PyP100.__file__}")
            except Exception as e:
                self._logger.error(f"PyP100 import issue: {e}")

        # Start energy monitoring if enabled
        if self._settings.get_boolean(["enable_energy_monitoring"]):
            self._start_energy_monitoring()

    def _start_energy_monitoring(self):
        """Start periodic energy monitoring"""
        def monitor():
            while True:
                try:
                    if self._settings.get_boolean(["enable_energy_monitoring"]):
                        energy = self._get_energy_usage()
                        if energy:
                            current_power = energy.get('current_power', 0)
                            self._logger.debug(f"Current power: {current_power} mW")

                    interval = self._settings.get_int(["energy_update_interval"])
                    time.sleep(interval)
                except Exception as e:
                    self._logger.error(f"Energy monitoring error: {e}")
                    time.sleep(60)  # Wait before retrying

        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()

    ##~~ Software Update Hook

    def get_update_information(self):
        return dict(
            tapo_p110=dict(
                displayName="Tapo P110",
                displayVersion=self._plugin_version,
                type="github_release",
                user="gaurav-pangam",
                repo="OctoPrint-Tapo-P110",
                current=self._plugin_version,
                pip="https://github.com/gaurav-pangam/OctoPrint-Tapo-P110/archive/{target_version}.zip"
            )
        )


__plugin_name__ = "Tapo P110"
__plugin_pythoncompat__ = ">=3.7,<4"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = TapoP110Plugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
