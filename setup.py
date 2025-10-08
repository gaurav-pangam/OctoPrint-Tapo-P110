# coding=utf-8
from setuptools import setup
import os

########################################################################################################################

plugin_identifier = "tapo_p110"
plugin_package = "octoprint_%s" % plugin_identifier
plugin_name = "OctoPrint-Tapo-P110"
plugin_version = "1.0.1"
plugin_description = "Direct Tapo P110 Smart Plug control for OctoPrint with energy monitoring and power management"
plugin_author = "Gaurav Pangam"
plugin_author_email = "pangamgaurav20@gmail.com"
plugin_url = "https://github.com/gaurav-pangam/OctoPrint-Tapo-P110"
plugin_license = "AGPLv3"

def package_data_dirs(source, sub_folders):
    dirs = []
    for d in sub_folders:
        folder = os.path.join(source, d)
        if not os.path.exists(folder):
            continue
        for dirname, _, files in os.walk(folder):
            dirname = os.path.relpath(dirname, source)
            for f in files:
                dirs.append(os.path.join(dirname, f))
    return dirs

def params():
    name = plugin_name
    version = plugin_version
    description = plugin_description
    author = plugin_author
    author_email = plugin_author_email
    url = plugin_url
    license = plugin_license

    packages = [plugin_package]
    package_data = {plugin_package: package_data_dirs(plugin_package, ['static', 'templates', 'translations'])}
    include_package_data = True
    zip_safe = False

    install_requires = [
        "requests>=2.24.0"
    ]

    python_requires = ">=3.7"

    entry_points = {
        "octoprint.plugin": ["%s = %s" % (plugin_identifier, plugin_package)]
    }

    return locals()

setup(**params())
