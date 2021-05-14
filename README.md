[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/Tes3awy/Cisco-DNA-Center-Device-List)
[![Visual Studio Code](https://img.shields.io/badge/VSCode-1.56.0-blue.svg?logo=visual-studio-code)](https://code.visualstudio.com/)
[![Tested on Python 3.9.4](https://img.shields.io/badge/Tested%20-Python%203.9.4-blue.svg?logo=python)](https://www.python.org/downloads)
[![Code Size](https://img.shields.io/github/languages/code-size/Tes3awy/Cisco-DNA-Center-Device-List?color=green)](https://github.com/Tes3awy/Cisco-DNA-Center-Device-List)
[![Contributions Welcome](https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=0059b3)](https://github.com/Tes3awy/Cisco-DNA-Center-Device-List/blob/main/CONTRIBUTING.md)
[![License](https://img.shields.io/github/license/Tes3awy/Cisco-DNA-Center-Device-List)](https://github.com/Tes3awy/Cisco-DNA-Center-Device-List)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Cisco DNA Center Device List, Device Config, and Network Health

This program is designed to export a Cisco DNAC device list and save them to an Excel sheet, device configurations and save them to text file, and network health and generate a bar chart.

## Table of Contents

1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Usage](#usage)
4. [Collected Data from Response](#collected-data)
5. [Use it for your DNA Center](#use-it-for-your-dna-center)
6. [References](#references)
7. [Previews](#previews)

### Installation

```bash
$ git clone https://github.com/Tes3awy/Cisco-DNA-Center-Device-List.git
$ cd Cisco-DNA-Center-Device-List
$ pip install -r requirements.txt
```

### Getting Started

```bash
│   main.py
│   get_auth_token.py
│   get_device_list.py
│   export_device_list.py
│   export_device_config.py
│   get_network_health.py
│   .env.example
│   requirements.txt
│   README.md
│   CONTRIBUTING.md
│   CODE_OF_CONDUCT.md
│   .gitignore
│   LICENSE
│
├───.github
│   └───ISSUE_TEMPLATE
│           bug_report.md
│           feature_request.md
│
└───assets
        preview.png
        sandboxdnac2.cisco.com.jpg
        script-logs.png
```

### Usage

You need to provide your DNA Center credentials in a `.env` file. Create a `.env` file from `.env.example` and **DON'T** delete the latter (Check **Use it for your DNA Center** section).

> **A `.env` file in the current working directory will override the `.env.example`.**

**Then run:**

```python
python main.py
```

Voila :sparkles:! An Excel file is created automatically from the device list on Cisco DNAC in the current working directory, configuration files of those devices are created in `configs/<DOMAIN>/<today>/<config_id>_<today>.txt`, and a network health diagram **(a bar chart with legend)** is created in `net_health/<BASE_URL>-<today>.jpg`.

> You will be prompted either to open the generated Excel file or just skip and continue running the program.

> `XlsxWriter` does not give you the option to append new data to a created opened file (As with text files). So every time you send a request, the Excel file will be overwritten.

> **NOTE:** You should close the Excel program before sending any new requests.

### Collected Data from Response

1. Hostname
2. Device ID
3. Management IP Address
4. Serial Number
5. Mac Address
6. Platform ID _(Device Model)_
7. Software Version
8. Role
9. Up Time
10. Last Update
11. Reachability Status

### Use it for your DNA Center

This program is ready to be used for your deployed DNA Center.

**Create a `.env` file from `.env.example`:**

```bash
$ cp .env.example .env
```

Repalce the `.env` file values with your Cisco DNA Center credentials.

**Example:**

`.env`

```vim
DOMAIN=10.10.1.1 # without a trailing slash (/)
BASE_URL=https://${DOMAIN}
USERNAME=root
PASSWORD=CiscoAdmin!2345
SSL_CERTIFICATE=False # set to True if you have a SSL valid certificate
```

### References

**APIs List**

[DNA Center Platform](https://developer.cisco.com/docs/dna-center/#!authentication-api)

**Documentation**

[Cisco DNA Assurance User Guide](https://www.cisco.com/c/en/us/td/docs/cloud-systems-management/network-automation-and-management/dna-center-assurance/1-3/b_cisco_dna_assurance_1_3_ug/b_cisco_dna_assurance_1_3_ug_chapter_0101.html#task_rn2_zdr_yy__p_assurance_score)

### Previews

**_Logs_**
![Script Logs](assets/script-logs.png)

**_Excel File Preview_**
![Excel File Preview](assets/preview.png)

**_A demonstration for color formatting_**
![Network Health Bar Chart](assets/sandboxdnac2.cisco.com.jpg)
