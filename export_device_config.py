#!/usr/bin/env python3

import os
from datetime import date
from typing import AnyStr, Dict

from termcolor import cprint


# Export device configs to text files
def export_device_config(device_configs: Dict, ENV: Dict) -> None:
    """Exports device configurations into text files

    Args:
        device_configs (Dict): Device configurations
        ENV (Dict): Environment variables
    """

    # Today's date
    today = date.today()

    # Create configs directory if not created
    os.makedirs("configs", exist_ok=True)

    CONFIGS_DIR = f'configs/{ENV["DOMAIN"]}/{today}'
    os.makedirs(f"{CONFIGS_DIR}", exist_ok=True)

    cprint("Exporting device configurations", "magenta")

    for config in device_configs:
        cfg: AnyStr = config["runningConfig"]
        cfg_id = config["id"]
        cfg_fname = f"{cfg_id}_{today}.txt"
        # Create a config file
        with open(file=os.path.join(CONFIGS_DIR, cfg_fname), mode="w") as cfg_file:
            cfg_file.write(cfg.lstrip())
        cprint(f"'{cfg_fname}' config file was created successfully", "cyan")
