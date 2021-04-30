#!/usr/bin/env python3

import os
import xlsxwriter
import datetime
import time
import webbrowser as xlsxviewer
from colorama import init
from termcolor import cprint

# use Colorama to make Termcolor work on Windows too
init(autoreset=True)


def export_device_list(device_list: list, ENV: dict):
    """Exports Device List to an Excel file

    Args:
        devices (list): Device List to export
        ENV (dict): Environment Variables

    Raises:
        SystemExit: HTTP Errors
    """

    # Vars
    today = datetime.date.today()
    workbook_title = (
        f"{ENV['BASE_URL'].replace('https://', '')}-DNA-Center_{str(today)}.xlsx"
    )

    # Create Excel file
    workbook = xlsxwriter.Workbook(workbook_title, {"constant_memory": True})
    worksheet = workbook.add_worksheet(ENV["BASE_URL"].replace("https://", ""))
    worksheet_range = "$A:$K"
    worksheet.autofilter("A1:K1")
    worksheet.set_column(worksheet_range, 20)

    # Header cells format
    header_cell_format = workbook.add_format(
        {
            "border": True,
            "bold": True,
            "font_color": "white",
            "bg_color": "#1e4471",
            "align": "center",
            "valign": "vcenter",
        }
    )

    # Set Columns Width
    worksheet.set_column("A:A", 15)
    worksheet.set_column("B:B", 35.56)
    worksheet.set_column("C:C", 19.78)
    worksheet.set_column("D:D", 16.56)
    worksheet.set_column("E:E", 20)
    worksheet.set_column("F:F", 15.67)
    worksheet.set_column("G:G", 14.33)
    worksheet.set_column("H:H", 12)
    worksheet.set_column("I:I", 18.22)
    worksheet.set_column("J:J", 17.33)
    worksheet.set_column("K:K", 14.89)

    # Header cells
    worksheet.write_string("A1", "Hostname", header_cell_format)
    worksheet.write_string("B1", "Device ID", header_cell_format)
    worksheet.write_string("C1", "MGMT IP Address", header_cell_format)
    worksheet.write_string("D1", "Serial Number", header_cell_format)
    worksheet.write_string("E1", "Mac Address", header_cell_format)
    worksheet.write_string("F1", "Platform ID", header_cell_format)
    worksheet.write_string("G1", "IOS Version", header_cell_format)
    worksheet.write_string("H1", "Role", header_cell_format)
    worksheet.write_string("I1", "Up Time", header_cell_format)
    worksheet.write_string("J1", "Last Updated", header_cell_format)
    worksheet.write_string("K1", "Reachability", header_cell_format)

    # Set Excel file properties
    workbook.set_properties(
        {
            "title": ENV["BASE_URL"].replace("https://", ""),
            "subject": "Cisco DNA Center",
            "author": "Osama Abbas",
            "hyperlink_base": ENV["BASE_URL"],
            "category": "Technology",
            "keywords": "Cisco, DNA Center, DevNet",
            "created": today,
            "comments": "Created with Python and XlsxWriter",
            "status": "Completed",
        }
    )

    # Entry cells format
    cell_format = workbook.add_format(
        {"border": True, "align": "center", "valign": "vcenter"}
    )

    serial_cell_format = workbook.add_format(
        {
            "border": True,
            "align": "center",
            "valign": "vcenter",
            "font_name": "Consolas",
        }
    )

    mac_cell_format = workbook.add_format(
        {
            "border": True,
            "align": "center",
            "valign": "vcenter",
            "font_name": "Consolas",
        }
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
        "K2:K1048576",
        {
            "type": "text",
            "criteria": "containing",
            "value": "Unreachable",
            "format": red_format,
        },
    )

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
        "K2:K1048576",
        {
            "type": "text",
            "criteria": "containing",
            "value": "Reachable",
            "format": green_format,
        },
    )

    # Highlight non blank rows (alternate) formula
    worksheet.conditional_format(
        "A2:J1048576",
        {
            "type": "formula",
            "criteria": '=AND(ISEVEN(ROW()),A2<>"")',
            "format": workbook.add_format({"bg_color": "#F2F2F2"}),
        },
    )

    # Row and Column initial values
    row = 1
    col = 0

    # Save each device in a seperate row
    for device in device_list:
        worksheet.write(row, col, device["hostname"], cell_format)
        worksheet.write(row, col + 1, device["id"], cell_format)
        worksheet.write(row, col + 2, device["managementIpAddress"], cell_format)
        worksheet.write(row, col + 3, device["serialNumber"], serial_cell_format)
        worksheet.write(row, col + 4, device["macAddress"], mac_cell_format)
        worksheet.write(row, col + 5, device["platformId"], cell_format)
        worksheet.write(row, col + 6, device["softwareVersion"], cell_format)
        worksheet.write(row, col + 7, device["role"].title(), cell_format)
        worksheet.write(row, col + 8, device["upTime"], cell_format)
        worksheet.write(row, col + 9, device["lastUpdated"], cell_format)
        worksheet.write(row, col + 10, device["reachabilityStatus"], cell_format)

        row += 1

    # Open workbook
    while True:
        try:
            workbook.close()
            cprint("export_device_list:", "magenta")
            cprint(f"'{workbook_title}' Excel file is created successfully!", "cyan")
            cprint(f"Opening '{workbook_title}', please wait ...\n", "cyan")
            time.sleep(1)
            xlsxviewer.open(os.path.abspath(workbook_title))
        except xlsxwriter.exceptions.FileCreateError as err:
            raise SystemExit(
                cprint(
                    f"Exception caught in workbook.close(): {err}\n"
                    f"Please close '{workbook_title}' file if it is already open in Microsoft Excel or in use by another program.",
                    "red",
                )
            )
        break