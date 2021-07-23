#!/usr/bin/env python3

from distutils.util import strtobool
from typing import Any, AnyStr, Dict, List

import requests
from requests.exceptions import ConnectionError, HTTPError
from requests.packages import urllib3
from termcolor import colored, cprint
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings. Not needed in production environments with valid certificates
# (REMOVE if you are not sure of its purpose)
urllib3.disable_warnings(category=InsecureRequestWarning)


# Export device configs to text files
def get_device_config(
    token: AnyStr, ENV: Dict[AnyStr, Any]
) -> List[Dict[AnyStr, AnyStr]]:
    """Gets running configuration of network devices

    Parameters
    ----------
    token : AnyStr
        Auth token
    ENV : Dict[AnyStr, Any]
        Environment variables

    Returns
    -------
    List[Dict[AnyStr, AnyStr]]
        Configuration of network devices

    Raises
    ------
    SystemExit
        HTTPError
    SystemExit
        ConnectionError
    SystemExit
        KeyboardInterrupt
    """
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    DEVICE_CONFIG_URL = "dna/intent/api/v1/network-device/config"

    try:
        cprint(text="Getting device configurations", color="magenta")
        response = requests.get(
            url=f"{ENV['BASE_URL']}/{DEVICE_CONFIG_URL}",
            headers=headers,
            data=None,
            verify=True if strtobool(val=ENV["SSL_CERTIFICATE"]) else False,
        )
        response.raise_for_status()
    except HTTPError as e:
        raise SystemExit(colored(text=e, color="red"))
    except ConnectionError as e:
        raise SystemExit(colored(text=e, color="red"))
    except KeyboardInterrupt:
        raise SystemExit(
            colored(text="Process interrupted by the user", color="yellow")
        )
    else:
        cprint(text="The request was successful.\n", color="green")
        return response.json()["response"]
