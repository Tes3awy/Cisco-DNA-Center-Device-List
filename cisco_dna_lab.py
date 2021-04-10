#!/usr/bin/env python

# --------------------------------------------------------------------------------------
#
# Demonstrates how to get Cisco DNA Center AO Lab devices and save them to an xlsx sheet
#
# (C) 2021 Osama Abbas, Cairo, Egypt
# Released under MIT License
#
# Filename: cisco_dna_lab.py
# Version: Python 3.9.4
# Authors: Osama Abbas (oabbas2512@gmail.com)
# Description:   This program is designed to get Cisco DNA Center AO Lab devices and
#                save them to an xlsx sheet.
#
# --------------------------------------------------------------------------------------

import os
import requests
import base64
import json
import xlsxwriter
import datetime
import time
import webbrowser

# DNA Center AO Lab
base_url = "https://sandboxdnac.cisco.com/dna/"
username = "devnetuser"
password = "Cisco123!"
ssl_certificate = True

# Generate Base64 string for authentication
auth_string = f"{username}:{password}"
auth_string = auth_string.encode("ascii")
auth_string = base64.b64encode(auth_string)
auth_string = str(auth_string, "utf-8")
auth_string = f"Basic {auth_string}"

# POST: Get Auth Token from DNA Center AO Lab API
headers = {
    "Content-Type": "application/json",
    "Authorization": auth_string,
    "Accept": "application/json",
}
r = requests.request(
    "POST",
    f"{base_url}system/api/v1/auth/token/",
    headers=headers,
    verify=ssl_certificate,
)

# Check the POST response status code
if r.status_code == 200:
    payload = json.loads(r.text)
    auth_Token = payload["Token"]
    print("✔ Hooray! Successful Token Generation.")

    # GET: Get all Devices
    headers = {
        "x-auth-token": auth_Token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    r = requests.request(
        "GET",
        f"{base_url}intent/api/v1/network-device/",
        headers=headers,
        verify=ssl_certificate,
    )
    # Check the GET request status code
    if r.status_code == 200:
        print(
            "✔ The request was successful. The result is contained in the response body."
        )
        payload = json.loads(r.text)

        # Create xlsx file
        workbook_title = "Cisco-DNA-Lab.xlsx"
        workbook = xlsxwriter.Workbook(workbook_title)
        worksheet = workbook.add_worksheet("Cisco DNA AO Lab")
        worksheet.set_column("$A:$I", 20)

        # Set xlsx file properties
        workbook.set_properties(
            {
                "title": "Cisco DNA AO Lab",
                "subject": "Cisco DNA AO Lab with Python",
                "author": "Osama Abbas",
                "category": "Technology",
                "keywords": "Cisco, DevNet",
                "created": datetime.date.today(),
                "comments": "Created with Python and XlsxWriter",
            }
        )

        # Header cells format
        header_cell_format = workbook.add_format(
            {
                "border": True,
                "bold": True,
                "font_color": "yellow",
                "bg_color": "#002060",
                "align": "center",
                "valign": "vcenter",
            }
        )

        # Header cells
        worksheet.write_string("A1", "Hostname", header_cell_format)
        worksheet.write_string("B1", "MGMT IP Address", header_cell_format)
        worksheet.write_string("C1", "Serial Number", header_cell_format)
        worksheet.write_string("D1", "Mac Address", header_cell_format)
        worksheet.write_string("E1", "Platform ID", header_cell_format)
        worksheet.write_string("F1", "Software Version", header_cell_format)
        worksheet.write_string("G1", "Role", header_cell_format)
        worksheet.write_string("H1", "Up Time", header_cell_format)
        worksheet.write_string("I1", "Reachability", header_cell_format)

        # Entry cells format
        cell_format = workbook.add_format(
            {"border": True, "align": "center", "valign": "vcenter"}
        )

        serial_number_cell_format = workbook.add_format(
            {
                "border": True,
                "align": "center",
                "valign": "vcenter",
                "font_name": "Consolas",
            }
        )

        mac_addr_cell_format = workbook.add_format(
            {
                "border": True,
                "align": "center",
                "valign": "vcenter",
                "font_name": "Consolas",
            }
        )

        success_cell_format = workbook.add_format(
            {
                "border": True,
                "align": "center",
                "valign": "vcenter",
                "font_color": "#006100",
                "bg_color": "#C6EFCE",
            }
        )
        error_cell_format = workbook.add_format(
            {
                "border": True,
                "align": "center",
                "valign": "vcenter",
                "font_color": "#9C0006",
                "bg_color": "#FFC7CE",
            }
        )

        # Row and Column initial values
        row = 1
        col = 0

        # Save each device in a seperate row
        for data in payload["response"]:
            worksheet.write(row, col, row, cell_format)
            worksheet.write(row, col, data["hostname"], cell_format)
            worksheet.write(row, col + 1, data["managementIpAddress"], cell_format)
            worksheet.write(
                row, col + 2, data["serialNumber"], serial_number_cell_format
            )
            worksheet.write(row, col + 3, data["macAddress"], mac_addr_cell_format)
            worksheet.write(row, col + 4, data["platformId"], cell_format)
            worksheet.write(row, col + 5, data["softwareVersion"], cell_format)
            worksheet.write(row, col + 6, data["role"], cell_format)
            worksheet.write(row, col + 7, data["upTime"].split(",", 1)[0], cell_format)
            if data["reachabilityStatus"] == "Reachable":
                worksheet.write(
                    row, col + 8, data["reachabilityStatus"], success_cell_format
                )
            else:
                worksheet.write(
                    row, col + 8, data["reachabilityStatus"], error_cell_format
                )

            row += 1

        # Open workbook
        while True:
            try:
                workbook.close()
                print(f"✔ {workbook_title} file is created successfully!")
                time.sleep(1)
                webbrowser.open(os.path.join(workbook_title))
            except xlsxwriter.exceptions.FileCreateError as e:
                print(
                    f"❌ Exception caught in workbook.close(): {e}\n"
                    "❕ Please close the file if it is open in Excel.\n"
                )
            break
    elif r.status_code == 204:
        print("❕ The request was successful, however no content was returned.")
    else:
        print(
            "❌ Something went wrong! The client made a request for a resource that does not exist."
        )

elif r.status_code == 404:
    print("❕ Please check the URLs")
elif r.status_code == 401:
    print("❌ Invalid Credentials")
else:
    print(
        "❌ Oops! Something went wrong. Can't get an Auth Token now. Please try again later."
    )
