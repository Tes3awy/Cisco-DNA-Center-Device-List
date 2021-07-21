#!/usr/bin/env python3

import time
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


def get_network_health(token: AnyStr, ENV: Dict) -> Dict:
    """Gets network health information

    Args:
        token (AnyStr): Cisco DNA Center Toekn
        ENV (Dict): Environment Variables

    Raises:
        SystemExit: HTTP Errors
        SystemExit: Keyboard Interrupt

    Returns:
        Dict: Network health information
    """

    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    epoch_time = int(time.time()) * 1000  # in milliseconds
    NETWORK_HEALTH_URL = f"dna/intent/api/v1/network-health?timestamp={epoch_time}"

    try:
        cprint("\nGetting network health", "magenta")
        response = requests.get(
            url=f"{ENV['BASE_URL']}/{NETWORK_HEALTH_URL}",
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
        return response.json()["healthDistirubution"]
