# Get Auth Token
import requests
from requests.auth import HTTPBasicAuth
import json
import urllib3

from credentials import BASE_URL, USERNAME, PASSWORD, SSL_CERTIFICATE

# Disable SSL warnings. Not needed in production environments with valid certificates
# (DON'T if you are not sure of its purpose)
urllib3.disable_warnings()


def get_auth_token():
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    try:
        response = requests.post(
            f"{BASE_URL}/dna/system/api/v1/auth/token/",
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            headers=headers,
            data=None,
            verify=SSL_CERTIFICATE,
        )
        response.raise_for_status()
        print("Successful Token Generation.\n")
        return response.json()["Token"]
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)