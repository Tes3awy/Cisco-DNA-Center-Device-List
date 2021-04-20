#!/usr/bin/env python

# ---------------------------------------------------------------------------------------
#
# Demonstrates how to get Cisco DNA Center AO Labs devices and save them to an xlsx sheet
#
# (C) 2021 Osama Abbas, Cairo, Egypt
# Released under MIT License
#
# Filename: cisco_dna_lab.py
# Version: Python 3.9.4
# Authors: Osama Abbas (oabbas2512@gmail.com)
# Description:   This program is designed to get Cisco DNA Center AO Labs devices and
#                save them to an xlsx sheet.
#
# ---------------------------------------------------------------------------------------

import os
import requests
import base64
import json
import xlsxwriter
import datetime
import time
import webbrowser as xlsxviewer
import urllib3

from credentials import base_url, username, password, ssl_certificate

# Disable warnings when ssl_certificate = False
urllib3.disable_warnings()

# DNA Center AO Lab (Defaults to Cisco DNA Center AO 1.3.1.4 if credentials.py vars are empty)
BASE_URL = base_url if base_url != "" else "https://sandboxdnac.cisco.com"
USERNAME = username if username != "" else "devnetuser"
PASSWORD = password if password != "" else "Cisco123!"
SSL_CERTIFICATE = ssl_certificate if ssl_certificate != "" else True

# Generate Base64 string for authentication
auth_string = f"{USERNAME}:{PASSWORD}"
auth_string = auth_string.encode("ascii")
auth_string = base64.b64encode(auth_string)
auth_string = auth_string.decode("utf-8")
auth_string = f"Basic {auth_string}"

# POST: Get Auth Token from DNA Center AO Lab API
headers = {
    "Content-Type": "application/json",
    "Authorization": auth_string,
    "Accept": "application/json",
}
r = requests.request(
    "POST",
    f"{BASE_URL}/dna/system/api/v1/auth/token/",
    headers=headers,
    verify=SSL_CERTIFICATE,
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
        f"{BASE_URL}/dna/intent/api/v1/network-device/",
        headers=headers,
        verify=SSL_CERTIFICATE,
    )
    # Check the GET request status code
    if r.status_code == 200:
        print(
            "✔ The request was successful. The result is contained in the response body."
        )
        payload = json.loads(r.text)

        # Create xlsx file
        today = datetime.date.today()
        workbook_title = (
            f"{BASE_URL.replace('https://', '')}-DNA-Center_{str(today)}.xlsx"
        )
        workbook = xlsxwriter.Workbook(workbook_title)
        worksheet = workbook.add_worksheet(BASE_URL.replace("https://", ""))
        worksheet_range = "$A:$J"
        worksheet.set_column(worksheet_range, 20)
        # Green Format
        green_format = workbook.add_format(
            {
                "border": True,
                "align": "center",
                "valign": "vcenter",
                "font_color": "#006100",
                "bg_color": "#C6EFCE",
            }
        )
        worksheet.conditional_format(
            "J2:J1048576",
            {
                "type": "text",
                "criteria": "containing",
                "value": "Reachable",
                "format": green_format,
            },
        )
        # Red Format
        red_format = workbook.add_format(
            {
                "border": True,
                "align": "center",
                "valign": "vcenter",
                "font_color": "#9C0006",
                "bg_color": "#FFC7CE",
            }
        )
        worksheet.conditional_format(
            "J2:J1048576",
            {
                "type": "text",
                "criteria": "containing",
                "value": "Unreachable",
                "format": red_format,
            },
        )

        # Set xlsx file propertiess
        workbook.set_properties(
            {
                "title": BASE_URL.replace("https://", ""),
                "subject": "Cisco DNA AO Lab with Python",
                "author": "Osama Abbas",
                "category": "Technology",
                "keywords": "Cisco, DevNet",
                "created": today,
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
        worksheet.write_string("F1", "IOS Version", header_cell_format)
        worksheet.write_string("G1", "Role", header_cell_format)
        worksheet.write_string("H1", "Up Time", header_cell_format)
        worksheet.write_string("I1", "Last Updated", header_cell_format)
        worksheet.write_string("J1", "Reachability", header_cell_format)

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

        # Row and Column initial values
        row = 1
        col = 0

        # Save each device in a seperate row
        for data in payload["response"]:
            worksheet.write(
                row,
                col,
                data["hostname"],
                workbook.add_format(
                    {"border": True, "align": "left", "valign": "vcenter"}
                ),
            )
            worksheet.write(row, col + 1, data["managementIpAddress"], cell_format)
            worksheet.write(
                row, col + 2, data["serialNumber"], serial_number_cell_format
            )
            worksheet.write(row, col + 3, data["macAddress"], mac_addr_cell_format)
            worksheet.write(row, col + 4, data["platformId"], cell_format)
            worksheet.write(row, col + 5, data["softwareVersion"], cell_format)
            worksheet.write(row, col + 6, data["role"].title(), cell_format)
            worksheet.write(row, col + 7, data["upTime"], cell_format)
            worksheet.write(row, col + 8, data["lastUpdated"], cell_format)
            worksheet.write(row, col + 9, data["reachabilityStatus"], cell_format)

            row += 1

        # Open workbook
        while True:
            try:
                # Highlight alternate row
                worksheet.conditional_format(
                    "A2:J1048576",
                    {
                        "type": "formula",
                        "criteria": '=AND(ISEVEN(ROW()),A2<>"")',
                        "format": workbook.add_format({"bg_color": "#F2F2F2"}),
                    },
                )
                workbook.close()
                print(f"✔ {workbook_title} file is created successfully!")
                print(f"✔ Opening {workbook_title}, please wait ...")
                time.sleep(1)
                xlsxviewer.open(os.path.join(workbook_title))
            except xlsxwriter.exceptions.FileCreateError as e:
                print(
                    f"✖ Exception caught in workbook.close(): {e}\n"
                    f"❕ Please close '{workbook_title}' if it is already open in Excel or in use by another program."
                )
            break
    elif r.status_code == 204:
        print(f"❕ Status code:{r.status_code}. The request was successful, however no content was returned.")
    elif r.status_code == 206:
        print(
            f"❕ Status code:{r.status_code}. The GET request included a Range Header, and the server responded with the partial content matching the range."
        )
    elif r.status_code == 400:
        print(f"✖ Status code:{r.status_code}. The client made a request that the server could not understand.")
    elif r.status_code == 401:
        print(
            f"✖  Status code:{r.status_code}.The client's authentication credentials included with the request are missing or invalid."
        )
    elif r.status_code == 403:
        print(
            f"❕ Status code:{r.status_code}. The server recognizes the authentication credentials, but the client is not authorized to perform this request."
        )
    elif r.status_code == 404:
        print(
            f"❕ Status code:{r.status_code}. The client made a request for a resource that does not exist. Please check the URLs."
        )
    elif r.status_code == 409:
        print(f"✖ Status code:{r.status_code}. The target resource is in a conflicted state.")
    elif r.status_code == 415:
        print(
            f"✖ Status code:{r.status_code}. The client sent a request body in a format that the server does not support."
        )
    elif r.status_code == 500:
        print(f"✖ Status code:{r.status_code}. The server could not fulfill the request.")
    elif r.status_code == 501:
        print(
            f"✖ Status code:{r.status_code}. The server has not implemented the functionality required to fulfill the request."
        )
    elif r.status_code == 503:
        print(f"❕ Status code:{r.status_code}. The server is (temporarily) unavailable.")
    else:
        print(f"❕ Status code:{r.status_code}. The server did not respond inside time restrictions and timed-out.")

else:
    print(f"✖ Status code:{r.status_code}. Invalid Credentials.")
