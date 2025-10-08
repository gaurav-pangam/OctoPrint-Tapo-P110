# coding=utf-8
from setuptools import setup, find_packages

########################################################################################################################

plugin_identifier = "tapo_p110"
plugin_package = "octoprint_%s" % plugin_identifier
plugin_name = "OctoPrint-Tapo-P110"
plugin_version = "1.0.0"
plugin_description = "Direct Tapo P110 Smart Plug control for OctoPrint with energy monitoring and power management"
plugin_author = "Gaurav Pangam"
plugin_author_email = "pangamgaurav20@gmail.com"
plugin_url = "https://github.com/gaurav-pangam/OctoPrint-Tapo-P110"
plugin_license = "AGPLv3"
plugin_additional_data = []

def package_data_dirs(source, sub_folders):
    import os
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

setup(
    name=plugin_name,
    version=plugin_version,
    description=plugin_description,
    author=plugin_author,
    author_email=plugin_author_email,
    url=plugin_url,
    license=plugin_license,

    packages=[plugin_package],
    package_data={
        plugin_package: package_data_dirs(plugin_package, ['static', 'templates', 'translations'] + plugin_additional_data)
    },
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        "requests>=2.24.0",
        "PyP100"  # Will be installed separately
    ],

    python_requires=">=3.7",

    entry_points={
        "octoprint.plugin": [
            "%s = %s" % (plugin_identifier, plugin_package)
        ]
    },

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Hardware"
    ],

    keywords="octoprint plugin tapo p110 smart plug 3d printing automation energy monitoring"
)
