#!/usr/bin/env python3

from distutils.util import strtobool
from typing import AnyStr, Dict, List

import requests
from requests.exceptions import ConnectionError, HTTPError
from requests.packages import urllib3
from termcolor import colored, cprint
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings. Not needed in production environments with valid certificates
# (REMOVE if you are not sure of its purpose)
urllib3.disable_warnings(category=InsecureRequestWarning)


def get_device_list(token: AnyStr, ENV: Dict) -> List:
    """Gets device list of a Cisco DNA Center

    Args:
        token (AnyStr): Cisco DNA Center Token
        ENV (Dict): Environment Variables

    Raises:
        SystemExit: HTTP Errors

    Returns:
        List: Device list
    """

    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    DEVICE_LIST_URL = "dna/intent/api/v1/network-device/"

    try:
        cprint("Getting device list", "magenta")
        response = requests.get(
            url=f"{ENV['BASE_URL']}/{DEVICE_LIST_URL}",
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
