#!/usr/bin/env python3

import time
from distutils.util import strtobool

import requests
from colorama import init
from requests.exceptions import HTTPError
from requests.packages import urllib3
from termcolor import colored, cprint

# Disable SSL warnings. Not needed in production environments with valid certificates
# (REMOVE if you are not sure of its purpose)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# use Colorama to make Termcolor work on Windows too
init(autoreset=True)


def get_network_health(token: str, ENV: dict) -> dict:
    """Gets network health information

    Args:
        token (str): Cisco DNA Center Toekn
        ENV (dict): Environment Variables

    Raises:
        SystemExit: HTTP Errors
        SystemExit: Keyboard Interrupt

    Returns:
        dict: Network health information
    """

    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    epoch_time = int(time.time()) * 1000  # in milliseconds
    NETWORK_HEALTH_URL = f"/dna/intent/api/v1/network-health?timestamp={epoch_time}"

    try:
        response = requests.get(
            f"{ENV['BASE_URL']}{NETWORK_HEALTH_URL}",
            headers=headers,
            data=None,
            verify=True if strtobool(ENV["SSL_CERTIFICATE"]) else False,
        )
        response.raise_for_status()
        cprint("\nget_network_health:", "magenta")
        cprint(
            "The request was successful. The result is contained in the response body.\n",
            "green",
        )

        return response.json()["healthDistirubution"]

    except HTTPError as err:
        raise SystemExit(colored(err, "red"))
    except KeyboardInterrupt:
        raise SystemExit(colored("Process interrupted by the user", "yellow"))
