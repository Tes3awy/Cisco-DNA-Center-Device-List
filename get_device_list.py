import requests
import urllib3
import json

from credentials import BASE_URL, SSL_CERTIFICATE

# Disable SSL warnings. Not needed in production environments with valid certificates
# (REMOVE if you are not sure of its purpose)
urllib3.disable_warnings()

# Get device list
def get_device_list(token):
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    DEVICE_LIST_URL = "/dna/intent/api/v1/network-device/"

    try:
        response = requests.get(
            f"{BASE_URL}{DEVICE_LIST_URL}",
            headers=headers,
            data=None,
            verify=SSL_CERTIFICATE,
        )
        response.raise_for_status()
        print(
            "The request was successful. The result is contained in the response body.\n"
        )
        return response.json()["response"]
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)