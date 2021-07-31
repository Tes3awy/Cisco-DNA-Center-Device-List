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


def get_device_list(token: AnyStr, ENV: Dict[AnyStr, Any]) -> List[Dict[AnyStr, Any]]:
    """Gets device list of a Cisco DNA Center

    Parameters
    ----------
    token : AnyStr
        Auth token
    ENV : Dict[AnyStr, Any]
        Environment variables

    Returns
    -------
    List[Dict[AnyStr, Any]]
        List of network devices

    Raises
    ------
    SystemExit
        ConnectionError, HTTPError
    SystemExit
        KeyboardInterrupt
    """

    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    DEVICE_LIST_URL = "dna/intent/api/v1/network-device/"

    try:
        cprint(text="Getting device list", color="magenta")
        response = requests.get(
            url=f"{ENV['BASE_URL']}/{DEVICE_LIST_URL}",
            headers=headers,
            data=None,
            verify=bool(strtobool(val=ENV["SSL_CERTIFICATE"])),
        )

        response.raise_for_status()
    except (ConnectionError, HTTPError) as e:
        raise SystemExit(colored(text=e, color="red"))
    except KeyboardInterrupt:
        raise SystemExit(
            colored(text="Process interrupted by the user", color="yellow")
        )
    else:
        cprint(text="The request was successful.\n", color="green")
        return response.json()["response"]
