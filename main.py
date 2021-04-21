#!/usr/bin/env python

# ---------------------------------------------------------------------------------------
#
# Demonstrates how to get Cisco DNA Center AO Labs devices and save them to an xlsx sheet
#
# (C) 2021 Osama Abbas, Cairo, Egypt
# Released under MIT License
#
# Filename: main.py
# Version: Python 3.9.4
# Authors: Osama Abbas (oabbas2512@gmail.com)
# Description:   This program is designed to get Cisco DNA Center AO Labs devices and
#                save them to an xlsx sheet.
#
# ---------------------------------------------------------------------------------------

# Import Modules
from get_auth_token import get_auth_token
from get_device_list import get_device_list
from export_device_list import export_device_list
from export_device_config import export_device_config


def main():
    # Obtain the Cisco DNA Center Auth Token
    token = get_auth_token()

    # Obtain devices on Cisco DNA Center
    devices = get_device_list(token)

    # Export devices to Excel sheet
    export_device_list(devices)

    # Export device configs
    export_device_config(token)


if __name__ == "__main__":
    main()
