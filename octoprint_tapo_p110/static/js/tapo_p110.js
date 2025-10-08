/*
 * View model for OctoPrint-Tapo-P110
 *
 * Author: Gaurav Pangam
 * License: AGPLv3
 */
$(function() {
    function TapoP110ViewModel(parameters) {
        var self = this;

        // Dependencies
        self.settings = parameters[0];

        // Observable properties
        self.deviceStatus = ko.observable(null);
        self.energyData = ko.observable(null);
        self.isConnecting = ko.observable(false);
        self.lastError = ko.observable("");
        self.lastSuccess = ko.observable("");
        self.autoRefreshEnergy = ko.observable(false);

        // Auto-refresh timer
        self.refreshTimer = null;

        // Clear messages after delay
        self.clearMessages = function() {
            setTimeout(function() {
                self.lastError("");
                self.lastSuccess("");
            }, 5000);
        };

        // Show success message
        self.showSuccess = function(message) {
            self.lastError("");
            self.lastSuccess(message);
            self.clearMessages();
        };

        // Show error message
        self.showError = function(message) {
            self.lastSuccess("");
            self.lastError(message);
            self.clearMessages();
        };

        // API call wrapper
        self.apiCall = function(command, data, successCallback, errorCallback) {
            self.isConnecting(true);
            
            $.ajax({
                url: API_BASEURL + "plugin/tapo_p110",
                type: "POST",
                dataType: "json",
                data: JSON.stringify({
                    command: command,
                    ...data
                }),
                contentType: "application/json; charset=UTF-8",
                success: function(response) {
                    self.isConnecting(false);
                    if (successCallback) {
                        successCallback(response);
                    }
                },
                error: function(xhr, status, error) {
                    self.isConnecting(false);
                    var message = "Request failed: " + error;
                    if (xhr.responseJSON && xhr.responseJSON.error) {
                        message = xhr.responseJSON.error;
                    }
                    if (errorCallback) {
                        errorCallback(message);
                    } else {
                        self.showError(message);
                    }
                }
            });
        };

        // Device control functions
        self.turnOn = function() {
            self.apiCall("turn_on", {}, function(response) {
                if (response.success) {
                    self.showSuccess("Device turned ON");
                    self.refreshStatus();
                } else {
                    self.showError("Failed to turn ON device");
                }
            });
        };

        self.turnOff = function() {
            self.apiCall("turn_off", {}, function(response) {
                if (response.success) {
                    self.showSuccess("Device turned OFF");
                    self.refreshStatus();
                } else {
                    self.showError("Failed to turn OFF device");
                }
            });
        };

        self.toggle = function() {
            self.apiCall("toggle", {}, function(response) {
                if (response.success) {
                    self.showSuccess("Device state toggled");
                    self.refreshStatus();
                } else {
                    self.showError("Failed to toggle device");
                }
            });
        };

        // Status and monitoring functions
        self.refreshStatus = function() {
            self.apiCall("get_status", {}, function(response) {
                if (response.status) {
                    self.deviceStatus(response.status);
                } else {
                    self.showError("Failed to get device status");
                }
            });
        };

        self.refreshEnergy = function() {
            self.apiCall("get_energy", {}, function(response) {
                if (response.energy) {
                    self.energyData(response.energy);
                } else {
                    self.showError("Failed to get energy data");
                }
            });
        };

        self.testConnection = function() {
            self.apiCall("test_connection", {}, function(response) {
                if (response.success) {
                    self.showSuccess("Connection test successful");
                    self.refreshStatus();
                } else {
                    self.showError("Connection test failed");
                }
            });
        };

        // Auto-refresh functionality
        self.autoRefreshEnergy.subscribe(function(enabled) {
            if (enabled) {
                self.startAutoRefresh();
            } else {
                self.stopAutoRefresh();
            }
        });

        self.startAutoRefresh = function() {
            if (self.refreshTimer) {
                clearInterval(self.refreshTimer);
            }
            
            self.refreshTimer = setInterval(function() {
                if (self.autoRefreshEnergy()) {
                    self.refreshEnergy();
                }
            }, 30000); // 30 seconds
        };

        self.stopAutoRefresh = function() {
            if (self.refreshTimer) {
                clearInterval(self.refreshTimer);
                self.refreshTimer = null;
            }
        };

        // Formatting functions
        self.formatPower = function(milliwatts) {
            if (!milliwatts) return "0 W";
            var watts = milliwatts / 1000;
            return watts.toFixed(2) + " W";
        };

        self.formatEnergy = function(watthours) {
            if (!watthours) return "0 Wh";
            if (watthours >= 1000) {
                return (watthours / 1000).toFixed(2) + " kWh";
            }
            return watthours.toFixed(1) + " Wh";
        };

        self.formatRuntime = function(minutes) {
            if (!minutes) return "0 min";
            if (minutes >= 60) {
                var hours = Math.floor(minutes / 60);
                var mins = minutes % 60;
                return hours + "h " + mins + "m";
            }
            return minutes + " min";
        };

        self.formatOnTime = function(seconds) {
            if (!seconds) return "0s";
            if (seconds >= 3600) {
                var hours = Math.floor(seconds / 3600);
                var mins = Math.floor((seconds % 3600) / 60);
                var secs = seconds % 60;
                return hours + "h " + mins + "m " + secs + "s";
            } else if (seconds >= 60) {
                var mins = Math.floor(seconds / 60);
                var secs = seconds % 60;
                return mins + "m " + secs + "s";
            }
            return seconds + "s";
        };

        // Initialize
        self.onBeforeBinding = function() {
            // Initial status refresh
            setTimeout(function() {
                self.refreshStatus();
                self.refreshEnergy();
            }, 1000);
        };

        // Cleanup
        self.onTabChange = function(current, previous) {
            if (previous === "#tab_plugin_tapo_p110") {
                self.stopAutoRefresh();
            }
        };
    }

    // Register the view model
    OCTOPRINT_VIEWMODELS.push({
        construct: TapoP110ViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#tab_plugin_tapo_p110", "#settings_plugin_tapo_p110"]
    });
});
