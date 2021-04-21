import requests
import urllib3
import json
import time
import matplotlib.pyplot as plt

from credentials import BASE_URL, SSL_CERTIFICATE

# Disable SSL warnings. Not needed in production environments with valid certificates
# (REMOVE if you are not sure of its purpose)
urllib3.disable_warnings()

# Get device list
def get_network_health(token):
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    epoch_time = int(time.time()) * 1000
    NETWORK_HEALTH_URL = f"/dna/intent/api/v1/network-health?timestamp={epoch_time}"

    try:
        response = requests.get(
            f"{BASE_URL}{NETWORK_HEALTH_URL}",
            headers=headers,
            data=None,
            verify=SSL_CERTIFICATE,
        )
        response.raise_for_status()
        print(
            "The request was successful. The result is contained in the response body.\n"
        )

        health_distribution = response.json()["healthDistirubution"]

        # Values on x-axis
        categories = list()
        total_category_count = list()
        # Values on y-axis
        health_score = list()

        for value in health_distribution:
            print(value)
            categories.append(value["category"])
            total_category_count.append(value["totalCount"])
            health_score.append(value["healthScore"])

        # Figure
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, sharey=False)
        fig.suptitle(f'{BASE_URL.replace("https://", "")}')
        # Subplot #1
        ax1.bar(categories, health_score, width=0.35, color="green", alpha=0.65)
        ax1.set_title("Network Health")
        ax1.set_ylabel("Health Score (Pecentage)")
        ax1.grid(True)
        # Subpolot #2
        ax2.bar(categories, total_category_count, width=0.35, color="#D0D0D0")
        ax2.set_title("Count")
        ax2.set_ylabel("Count")
        ax2.grid(True)
        # Show and save plot
        plt.show()
        plt.savefig(f'{BASE_URL.replace("https://", "")}.jpg', dpi=400)

    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)