import os
from datetime import date
from typing import Any, AnyStr, Dict, List

from termcolor import cprint


# Export device configs to text files
def export_device_config(
    device_configs: List[Dict[AnyStr, AnyStr]], ENV: Dict[AnyStr, Any]
) -> None:
    """Exports device configurations to text files

    Parameters
    ----------
    device_configs : List[Dict[AnyStr, AnyStr]]
        List of network device configurations
    ENV : Dict[AnyStr, Any]
        Environment variables
    """

    today = date.today()

    # Create configs directory if not created
    os.makedirs(name="configs", exist_ok=True)

    CONFIGS_DIR = f'configs/{ENV["DOMAIN"]}/{today}'
    os.makedirs(name=f"{CONFIGS_DIR}", exist_ok=True)

    cprint(text="Exporting device configurations...", color="magenta")

    for config in device_configs:
        cfg: AnyStr = config["runningConfig"]
        cfg_id = config["id"]
        cfg_fname = f"{cfg_id}_{today}.txt"
        # Create a config file
        with open(file=os.path.join(CONFIGS_DIR, cfg_fname), mode="w") as cfg_file:
            cfg_file.write(cfg.lstrip())
        cprint(text=f"Created '{cfg_fname}' config file", color="cyan")
