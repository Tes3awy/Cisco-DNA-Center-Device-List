#!/usr/bin/env python3

import os
from datetime import datetime

from colorama import init
from requests.packages import urllib3
from termcolor import cprint

# Disable SSL warnings. Not needed in production environments with valid certificates
# (REMOVE if you are not sure of its purpose)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# use Colorama to make Termcolor work on Windows too
init(autoreset=True)

# Export device configs to text files
def export_device_config(device_configs: dict, ENV: dict) -> None:
    """Exports device configurations into text files

    Args:
        device_configs (dict): Device configurations
        ENV (dict): Environment variables
    """

    # Today's date
    today = datetime.today().strftime("%Y-%m-%d")

    # Create configs directory if not created
    DIR = "configs"
    os.makedirs(DIR, exist_ok=True)

    CONFIGS_DIR = f'{DIR}/{ENV["DOMAIN"]}/{today}'
    os.makedirs(f"{CONFIGS_DIR}", exist_ok=True)

    cprint("export_device_config:", "magenta")

    for config in device_configs:
        cfg = config["runningConfig"].lstrip()
        config_id = config["id"]
        cfg_file_name = f"{config_id}_{today}.txt"
        # Create a config file
        with open(os.path.join(CONFIGS_DIR, cfg_file_name), "w") as config_file:
            config_file.write(cfg)
        cprint(
            f"'{cfg_file_name}' config file is created successfully!",
            "cyan",
        )
