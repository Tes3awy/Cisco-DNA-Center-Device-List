#!/usr/bin/env python3

import os
import requests
from requests.packages import urllib3
import json
import time
import matplotlib.pyplot as plt
from colorama import init
from termcolor import cprint
from datetime import datetime
from distutils.util import strtobool

# Disable SSL warnings. Not needed in production environments with valid certificates
# (REMOVE if you are not sure of its purpose)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# use Colorama to make Termcolor work on Windows too
init(autoreset=True)


def get_network_health(token: str, ENV: dict):
    """Gets Network Health information

    Args:
        token (str): Cisco DNA Center Token
        ENV (dict): Environment Variables

    Raises:
        SystemExit: HTTP Errors
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
        cprint("get_network_health:", "magenta")
        cprint(
            "The request was successful. The result is contained in the response body.\n",
            "green",
        )

        health_distribution = response.json()["healthDistirubution"]

        # Values on x-axis
        categories = list()
        total_category_count = list()
        # Values on y-axis
        health_score = list()

        # Get values from healthDistirubution
        for value in health_distribution:
            categories.append(value["category"])
            total_category_count.append(value["totalCount"])
            health_score.append(value["healthScore"])

        # Figures DIR
        NET_HEALTH_DIR = "net_health"
        FIG_NAME = ENV["BASE_URL"].replace("https://", "")

        # Check if net_health exists
        if not os.path.exists(NET_HEALTH_DIR):
            os.makedirs(NET_HEALTH_DIR)

        # Today's date
        today = datetime.today().strftime("%Y-%m-%d")

        # Image to save
        NET_HEALTH_FIG = os.path.join(NET_HEALTH_DIR, f"{FIG_NAME}-{today}.jpg")

        # Figure
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, sharey=False)
        fig.suptitle(f"{FIG_NAME}")
        # Subplot #1
        ax1.bar(categories, health_score, width=0.35, color="green", alpha=0.65)
        ax1.set_title("Network Health")
        ax1.set_ylabel("Health Score (Pecentage)")
        ax1.grid(True)
        # Subpolot #2
        ax2.bar(categories, total_category_count, width=0.35, color="#D0D0D0")
        ax2.set_ylabel("Count")
        ax2.grid(True)
        # Save plot to net_health/*.jpg
        plt.savefig(NET_HEALTH_FIG, dpi=300)
        cprint(f"Please check '{NET_HEALTH_FIG}'", "cyan")

    except requests.exceptions.HTTPError as err:
        raise SystemExit(cprint(err, "red"))