#!/usr/bin/env python3

import os
from datetime import datetime

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from colorama import init
from termcolor import cprint

# use Colorama to make Termcolor work on Windows too
init(autoreset=True)


def export_network_health(network_health: dict, ENV: dict):
    """Exports network health into a matplotlib bar chart

    Args:
        network_health (dict): Network health
        ENV (dict): Environment Variables
    """

    # Values on x-axis
    categories = []
    # Values on y-axis
    health_score = []
    total_category_count = []

    # Get values from healthDistirubution
    for value in network_health:
        categories.append(value["category"])
        total_category_count.append(value["totalCount"])
        health_score.append(value["healthScore"])

    # Figures DIR
    NET_HEALTH_DIR = "net_health"
    FIG_NAME = ENV["DOMAIN"]

    # Check if net_health directory exists
    if not os.path.exists(NET_HEALTH_DIR):
        os.makedirs(NET_HEALTH_DIR)

    # Today's date
    today = datetime.today().strftime("%Y-%m-%d")

    # Image to save
    NET_HEALTH_FIG = os.path.join(NET_HEALTH_DIR, f"{FIG_NAME}-{today}.jpg")

    # Figure
    fig, (ax1, ax2) = plt.subplots(
        2, 1, sharex=True, sharey=False, constrained_layout=True
    )
    fig.suptitle(f"{FIG_NAME} DNAC", fontweight="bold")

    # Subpolot #1
    ax1.bar(categories, total_category_count, width=0.25, color="grey")
    ax1.set_title("Devices Count")
    ax1.set_ylabel("Count")
    ax1.grid(True)

    # Subplot #2
    # Conditional bar colors
    colors_list = list()
    for score in health_score:
        if score > 0 and score <= 39:
            colors_list.append("red")
        elif score >= 40 and score <= 79:
            colors_list.append("orange")
        elif score >= 80 and score <= 100:
            colors_list.append("green")

    # Adding legend
    ax2.get_legend_handles_labels()
    red_patch = mpatches.Patch(color="red", label="Critical issues")
    orange_patch = mpatches.Patch(color="orange", label="Warnings")
    green_patch = mpatches.Patch(color="green", label="No errors or warning")
    ax2.legend(handles=[red_patch, orange_patch, green_patch], loc="best")

    ax2.bar(categories, health_score, width=0.25, color=colors_list)
    ax2.set_title("Network Health")
    ax2.set_ylabel("Health Score (Pecentage)")
    ax2.grid(True)

    # Save plot to net_health/*.jpg
    plt.savefig(NET_HEALTH_FIG, dpi=300)

    cprint("export_network_health:", "magenta")
    cprint(f"Please check '{NET_HEALTH_FIG}'", "cyan")
