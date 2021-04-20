import os
import xlsxwriter
import datetime
import time
import webbrowser as xlsxviewer

from credentials import BASE_URL

# Export device list to Excel sheet
def export_device_list(devices):

    # Vars
    today = datetime.date.today()
    workbook_title = f"{BASE_URL.replace('https://', '')}-DNA-Center_{str(today)}.xlsx"

    # Create Excel file
    workbook = xlsxwriter.Workbook(workbook_title, {"constant_memory": True})
    worksheet = workbook.add_worksheet(BASE_URL.replace("https://", ""))
    worksheet_range = "$A:$J"
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
    worksheet.set_column("B:B", 35)
    worksheet.set_column("C:C", 15)
    worksheet.set_column("D:D", 13)
    worksheet.set_column("E:E", 19)
    worksheet.set_column("F:F", 16)
    worksheet.set_column("G:G", 10)
    worksheet.set_column("H:H", 10)
    worksheet.set_column("I:I", 17)
    worksheet.set_column("J:J", 17)
    worksheet.set_column("K:K", 11)

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
            "title": BASE_URL.replace("https://", ""),
            "subject": "Cisco DNA Center",
            "author": "Osama Abbas",
            "hyperlink_base": BASE_URL,
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
    for device in devices:
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
            print(f"'{workbook_title}' Excel file is created successfully!")
            print(f"Opening '{workbook_title}', please wait ...")
            time.sleep(1)
            xlsxviewer.open(os.path.abspath(workbook_title))
        except xlsxwriter.exceptions.FileCreateError as err:
            raise SystemExit(
                f"Exception caught in workbook.close(): {err}\n"
                f"Please close '{workbook_title}' file if it is already open in Microsoft Excel or in use by another program."
            )
        break