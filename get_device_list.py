#!/usr/bin/env python3

import requests
from requests.packages import urllib3
import json
from colorama import init
from termcolor import cprint
from distutils.util import strtobool

# Disable SSL warnings. Not needed in production environments with valid certificates
# (REMOVE if you are not sure of its purpose)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# use Colorama to make Termcolor work on Windows too
init(autoreset=True)


def get_device_list(token: str, ENV: dict) -> list:
    """Gets device list of a Cisco DNA Center

    Args:
        token (str): Cisco DNA Center Token
        ENV (dict): Environment Variables

    Raises:
        SystemExit: HTTP Errors

    Returns:
        list: Device list
    """

    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    DEVICE_LIST_URL = "/dna/intent/api/v1/network-device/"

    try:
        response = requests.get(
            f"{ENV['BASE_URL']}{DEVICE_LIST_URL}",
            headers=headers,
            data=None,
            verify=True if strtobool(ENV["SSL_CERTIFICATE"]) else False,
        )
        response.raise_for_status()
        cprint("get_device_list:", "magenta")
        cprint(
            "The request was successful. The result is contained in the response body.\n",
            "green",
        )
        return response.json()["response"]
    except requests.exceptions.HTTPError as err:
        raise SystemExit(cprint(err, "red"))