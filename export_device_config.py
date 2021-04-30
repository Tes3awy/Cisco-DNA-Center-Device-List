#!/usr/bin/env python3

import os
import requests
from requests.packages import urllib3
import json
from colorama import init
from termcolor import cprint
from datetime import datetime
from distutils.util import strtobool

# Disable SSL warnings. Not needed in production environments with valid certificates
# (REMOVE if you are not sure of its purpose)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# use Colorama to make Termcolor work on Windows too
init(autoreset=True)

# Export device configs to text files
def export_device_config(token: str, ENV: dict):
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    DEVICE_CONFIG_URL = "/dna/intent/api/v1/network-device/config"

    try:
        response = requests.get(
            f"{ENV['BASE_URL']}{DEVICE_CONFIG_URL}",
            headers=headers,
            data=None,
            verify=True if strtobool(ENV["SSL_CERTIFICATE"]) else False,
        )
        response.raise_for_status()
        cprint("export_device_config:", "magenta")
        cprint(
            "The request was successful. The result is contained in the response body.\n",
            "green",
        )

        device_configs = response.json()["response"]

        DIR = "configs"

        # Create configs directory if not created
        if not os.path.exists(DIR):
            os.makedirs(DIR)

        # Today's date
        today = datetime.today().strftime("%Y-%m-%d")
        for config in device_configs:
            cfg = config["runningConfig"].strip()
            config_id = config["id"]
            cfg_file_name = f"{config_id}_{today}.txt"
            # Create a config file
            with open(os.path.join(DIR, cfg_file_name), "w") as config_file:
                config_file.write(cfg)
                cprint(
                    f"'{cfg_file_name}' config file is created successfully!",
                    "cyan",
                )

        print("\n")

    except requests.exceptions.HTTPError as err:
        raise SystemExit(cprint(err, "red"))
