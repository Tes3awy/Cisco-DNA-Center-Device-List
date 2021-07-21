#!/usr/bin/env python3

# -----------------------------------------------------------------------------------------
#
# Demonstrates how to get Cisco DNA Center device list and save them to an xlsx sheet and
# and device configs and save them to text files.
#
# (C) 2021 Osama Abbas, Cairo, Egypt
# Released under MIT License
#
# Filename: main.py
# Version: Python 3.9.4
# Authors: Osama Abbas (oabbas2512@gmail.com)
# Description:   This program is designed to get Cisco DNA Center device list and
#                save them to an xlsx sheet and device configs and save them to text files.
#
# -----------------------------------------------------------------------------------------

# Import Modules
import platform
import time

from colorama import init
from dotenv import dotenv_values

# Export modules
from export_device_config import export_device_config
from export_device_list import export_device_list
from export_network_health import export_network_health

# Get modules
from get_auth_token import get_auth_token
from get_device_config import get_device_config
from get_device_list import get_device_list
from get_network_health import get_network_health

# Notification module
from notify import notify

# use Colorama to make Termcolor work on Windows too
init(autoreset=True)

# ENV Variables in current project
ENV = {
    **dotenv_values(".env.example"),
    **dotenv_values(".env"),
}


def main():
    # Start time
    start_time = time.perf_counter()

    # Obtain the Cisco DNA Center Auth Token
    token = get_auth_token(ENV=ENV)

    # Obtain devices on Cisco DNA Center
    device_list = get_device_list(token=token, ENV=ENV)

    # Export devices to Excel sheet
    export_device_list(device_list=device_list, ENV=ENV)

    # Obtain device configs
    device_configs = get_device_config(token=token, ENV=ENV)

    # Export device configs to text files
    export_device_config(device_configs=device_configs, ENV=ENV)

    # Obtain network health
    network_health = get_network_health(token=token, ENV=ENV)

    # Export matplotlib bar chart of network health
    export_network_health(network_health=network_health, ENV=ENV)

    # Print Elasped time
    end_time = time.perf_counter()
    print(f"\nElapsed time: {round(end_time-start_time, 2)}")

    # Send notification for Windows users ONLY
    if "Windows" in platform.system():
        notify("Congratulations! Python script ran successfully")


if __name__ == "__main__":
    main()
