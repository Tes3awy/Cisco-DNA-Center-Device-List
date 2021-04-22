#!/usr/bin/env python

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
from get_auth_token import get_auth_token
from get_device_list import get_device_list
from export_device_list import export_device_list
from export_device_config import export_device_config
from get_network_health import get_network_health


def main():
    # Obtain the Cisco DNA Center Auth Token
    token = get_auth_token()

    # Obtain devices on Cisco DNA Center
    devices = get_device_list(token)

    # Export devices to Excel sheet
    export_device_list(devices)

    # Export device configs to .txt files
    export_device_config(token)

    # Obtain network health
    get_network_health(token)


if __name__ == "__main__":
    main()
