#!/usr/bin/env python

import os
import re
import requests
import urllib3
import json

from credentials import BASE_URL, SSL_CERTIFICATE

# Disable SSL warnings. Not needed in production environments with valid certificates
# (REMOVE if you are not sure of its purpose)
urllib3.disable_warnings()

# Export device configs to text files
def export_device_config(token):
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    DEVICE_CONFIG_URL = "/dna/intent/api/v1/network-device/config"

    try:
        response = requests.get(
            f"{BASE_URL}{DEVICE_CONFIG_URL}",
            headers=headers,
            data=None,
            verify=SSL_CERTIFICATE,
        )
        response.raise_for_status()
        print(
            "The request was successful. The result is contained in the response body.\n"
        )

        device_configs = response.json()["response"]

        DIR = "configs"

        # Create configs directory if not created
        if not os.path.exists(DIR):
            os.makedirs(DIR)

        # Export a config file for each device
        for config in device_configs:
            conf = config["runningConfig"].strip()
            # Find the string after hostname by index
            regex = re.findall(r"\w+", conf)
            index = regex.index("hostname")
            hostname = regex[index + 1]
            # Create a config file
            with open(os.path.join(DIR, f"{hostname}.txt"), "w") as config_file:
                config_file.write(config["runningConfig"])
                print(f"'{hostname}.txt' config file was created successfully!")

    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
