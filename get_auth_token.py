#!/usr/bin/env python3

from distutils.util import strtobool
from typing import AnyStr, Dict

import requests
from requests.auth import HTTPBasicAuth as BasicAuth
from requests.exceptions import ConnectionError, HTTPError
from requests.packages import urllib3
from termcolor import colored, cprint
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings. Not needed in production environments with valid certificates
# (REMOVE if you are not sure of its purpose)
urllib3.disable_warnings(category=InsecureRequestWarning)


def get_auth_token(ENV: Dict) -> AnyStr:
    """Gets Cisco DNA Center Auth Token

    Args:
        ENV (Dict): Environment Variables

    Raises:
        SystemExit: HTTP Errors

    Returns:
        AnyStr: Generated Token
    """

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    try:
        cprint("Generating auth token", "magenta")
        response = requests.post(
            url=f"{ENV['BASE_URL']}/dna/system/api/v1/auth/token",
            auth=BasicAuth(username=ENV["USERNAME"], password=ENV["PASSWORD"]),
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
        cprint("Successful Token Generation.\n", "green")
        return response.json()["Token"]
