#!/usr/bin/env python3

from datetime import date
from typing import Dict, List

from termcolor import colored, cprint
from xlsxwriter import Workbook
from xlsxwriter.exceptions import FileCreateError


def export_device_list(device_list: List, ENV: Dict) -> None:
    """Exports Device List to an Excel file

    Args:
        devices (List): Device List to export
        ENV (Dict): Environment Variables
    """

    # Vars
    today = date.today()
    workbook_title = f"{ENV['DOMAIN']}-DNA-Center_{str(today)}.xlsx"

    # Create Excel file
    workbook = Workbook(workbook_title, {"constant_memory": True})
    worksheet = workbook.add_worksheet(ENV["DOMAIN"])
    worksheet_range = "$A:$K"
    worksheet.autofilter("A1:K1")
    worksheet.freeze_panes(1, 1)
    worksheet.set_column(worksheet_range, 20)

    # Header cells format
    h_frmt = workbook.add_format(
        {
            "border": True,
            "bold": True,
            "font_color": "white",
            "bg_color": "#1e4471",
            "align": "center",
            "valign": "vcenter",
        }
    )

    # Header line cells
    header = {
        "A1": "Hostname",
        "B1": "Device ID",
        "C1": "MGMT IP Address",
        "D1": "Serial Number",
        "E1": "MAC Address",
        "F1": "Platform ID",
        "G1": "IOS Version",
        "H1": "Role",
        "I1": "Up Time",
        "J1": "Last Updated",
        "K1": "Reachability",
    }

    for key, value in header.items():
        worksheet.write_string(key, value, h_frmt)

    # Set Excel file properties
    workbook.set_properties(
        {
            "title": ENV["DOMAIN"],
            "subject": "Cisco DNA Center",
            "author": "Osama Abbas",
            "manager": "Osama Abbas",
            "hyperlink_base": ENV["BASE_URL"],
            "category": "Technology",
            "keywords": "Cisco, DNAC, Cisco DevNet, Python3, APIs",
            "created": today,
            "comments": "Created with Python and XlsxWriter",
            "status": "Completed",
        }
    )

    # Entry cells format
    cell_frmt = workbook.add_format(
        {"border": True, "align": "center", "valign": "vcenter"}
    )

    serial_cell_frmt = workbook.add_format(
        {
            "border": True,
            "align": "center",
            "valign": "vcenter",
            "font_name": "Consolas",
        }
    )

    mac_cell_frmt = workbook.add_format(
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
    row, col = 1, 0

    # Save each device in a seperate row
    for device in device_list:
        worksheet.write(row, col + 0, device["hostname"], cell_frmt)
        worksheet.write(row, col + 1, device["id"], cell_frmt)
        worksheet.write(row, col + 2, device["managementIpAddress"], cell_frmt)
        worksheet.write(row, col + 3, device["serialNumber"], serial_cell_frmt)
        worksheet.write(row, col + 4, device["macAddress"], mac_cell_frmt)
        worksheet.write(row, col + 5, device["platformId"], cell_frmt)
        worksheet.write(row, col + 6, device["softwareVersion"], cell_frmt)
        worksheet.write(row, col + 7, device["role"].title(), cell_frmt)
        worksheet.write(row, col + 8, device["upTime"], cell_frmt)
        worksheet.write(row, col + 9, device["lastUpdated"], cell_frmt)
        worksheet.write(row, col + 10, device["reachabilityStatus"], cell_frmt)

        row += 1

    # Close workbook
    while True:
        try:
            workbook.close()
            cprint("Exporting device list", "magenta")
            cprint(f"INFO: '{workbook_title}' is saved in your PWD.\n", "blue")
        except FileCreateError as e:
            raise SystemExit(
                colored(
                    f"Exception caught in workbook.close(): {e}\n"
                    f"Please close '{workbook_title}' file if it is already open in Microsoft Excel or in use by another program.",
                    "red",
                )
            )
        break
