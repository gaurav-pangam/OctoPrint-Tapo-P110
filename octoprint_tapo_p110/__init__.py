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
        """Connect to the P110 device"""
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

            try:
                self._logger.info(f"Connecting to P110 at {device_ip}")
                self.device = PyP110.P110(device_ip, username, password)
                
                self.device.handshake()
                self.device.login()
                
                # Get device info to verify it's a P110
                self.device_info = self.device.getDeviceInfo()
                device_model = self.device_info.get('model', 'Unknown')
                firmware_version = self.device_info.get('fw_ver', 'Unknown')
                
                self._logger.info(f"Connected to {device_model} with firmware {firmware_version}")
                
                if device_model != 'P110':
                    self._logger.warning(f"Expected P110, but connected to {device_model}")
                
                return True
                
            except Exception as e:
                self._logger.error(f"Failed to connect to P110: {e}")
                self.device = None
                return False

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
            self.last_status = info.get('device_on', False)
            return info
        except Exception as e:
            self._logger.error(f"Failed to get status: {e}")
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
        """Test connection to device"""
        self._disconnect()  # Force reconnection
        return self._connect()

    ##~~ Startup

    def on_after_startup(self):
        self._logger.info("Tapo P110 Plugin started")
        
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
