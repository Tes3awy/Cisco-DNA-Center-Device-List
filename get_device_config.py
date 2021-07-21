#!/usr/bin/env python3

from distutils.util import strtobool
from typing import AnyStr, Dict

import requests
from requests.exceptions import ConnectionError, HTTPError
from requests.packages import urllib3
from termcolor import colored, cprint
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings. Not needed in production environments with valid certificates
# (REMOVE if you are not sure of its purpose)
urllib3.disable_warnings(category=InsecureRequestWarning)


# Export device configs to text files
def get_device_config(token: AnyStr, ENV: Dict) -> Dict:
    """Gets device configurations

    Args:
        token (AnyStr): Cisco DNA Center Token
        ENV (Dict): Environment Variables

    Raises:
        SystemExit: HTTP Errors
        SystemExit: Keyboard Interrupt

    Returns:
        dict: Device condgurations
    """

    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    DEVICE_CONFIG_URL = "dna/intent/api/v1/network-device/config"

    try:
        cprint("Getting device configurations", "magenta")
        response = requests.get(
            url=f"{ENV['BASE_URL']}/{DEVICE_CONFIG_URL}",
            headers=headers,
            data=None,
            verify=True if strtobool(val=ENV["SSL_CERTIFICATE"]) else False,
        )
        response.raise_for_status()
    except HTTPError as e:
        raise SystemExit(colored(e, "red"))
    except ConnectionError as e:
        raise SystemExit(colored(e, "red"))
    except KeyboardInterrupt:
        raise SystemExit(colored("Process interrupted by the user", "yellow"))
    else:
        cprint("The request was successful.\n", "green")
        return response.json()["response"]
