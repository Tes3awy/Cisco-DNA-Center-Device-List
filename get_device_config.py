#!/usr/bin/env python3

from distutils.util import strtobool

import requests
from colorama import init
from requests.packages import urllib3
from termcolor import cprint

# Disable SSL warnings. Not needed in production environments with valid certificates
# (REMOVE if you are not sure of its purpose)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# use Colorama to make Termcolor work on Windows too
init(autoreset=True)

# Export device configs to text files
def get_device_config(token: str, ENV: dict) -> dict:
    """Gets device configurations

    Args:
        token (str): Cisco DNA Center Token
        ENV (dict): Environment Variables

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

    DEVICE_CONFIG_URL = "/dna/intent/api/v1/network-device/config"

    try:
        response = requests.get(
            f"{ENV['BASE_URL']}{DEVICE_CONFIG_URL}",
            headers=headers,
            data=None,
            verify=True if strtobool(ENV["SSL_CERTIFICATE"]) else False,
        )
        response.raise_for_status()
        cprint("get_device_config:", "magenta")
        cprint(
            "The request was successful. The result is contained in the response body.\n",
            "green",
        )

        return response.json()["response"]

    except requests.exceptions.HTTPError as err:
        raise SystemExit(cprint(err, "red"))
    except KeyboardInterrupt:
        raise SystemExit(cprint("Process interrupted by the user", "yellow"))