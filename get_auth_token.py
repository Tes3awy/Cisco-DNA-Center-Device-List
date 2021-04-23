#!/usr/bin/env python

import requests
from requests.auth import HTTPBasicAuth
from requests.packages import urllib3
import json
from colorama import init
from termcolor import colored

# Disable SSL warnings. Not needed in production environments with valid certificates
# (REMOVE if you are not sure of its purpose)
urllib3.disable_warnings()

# use Colorama to make Termcolor work on Windows too
init(autoreset=True)

# Get Auth Token
def get_auth_token(ENV: dict) -> str:

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
            verify=bool(ENV["SSL_CERTIFICATE"]),
        )

        response.raise_for_status()
        print(colored("get_auth_token:", "magenta"))
        print(colored("Successful Token Generation.\n", "green"))
        return response.json()["Token"]
    except requests.exceptions.HTTPError as err:
        raise SystemExit(colored(err, "red"))