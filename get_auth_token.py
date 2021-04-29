#!/usr/bin/env python3

import requests
from requests.auth import HTTPBasicAuth
from requests.packages import urllib3
import json
from colorama import init
from termcolor import colored
from distutils.util import strtobool

# Disable SSL warnings. Not needed in production environments with valid certificates
# (REMOVE if you are not sure of its purpose)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# use Colorama to make Termcolor work on Windows too
init(autoreset=True)


def get_auth_token(ENV: dict) -> str:
    """Gets Cisco DNA Center Auth Token

    Args:
        ENV (dict): Environment Variables

    Raises:
        SystemExit: HTTP Errors

    Returns:
        str: Generated Token
    """

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    try:
        response = requests.post(
            url=f"{ENV['BASE_URL']}/dna/system/api/v1/auth/token",
            auth=HTTPBasicAuth(ENV["USERNAME"], ENV["PASSWORD"]),
            headers=headers,
            data=None,
            verify=True if strtobool(ENV["SSL_CERTIFICATE"]) else False,
        )

        response.raise_for_status()
        print(colored("get_auth_token:", "magenta"))
        print(colored("Successful Token Generation.\n", "green"))
        return response.json()["Token"]
    except requests.exceptions.HTTPError as err:
        raise SystemExit(colored(err, "red"))