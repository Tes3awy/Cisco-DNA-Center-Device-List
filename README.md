[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/Tes3awy/Cisco-DNA-Center-Device-List)

# Cisco DNA Center Device List and Device Config

This program is designed to export a Cisco DNA Center device list and save them to an Excel sheet and device configs and save them to text file.

## Table of Contents

1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Usage](#usage)
4. [Collected Data from Response](#collected-data)
5. [Use it for your DNA Center](#use-it-for-your-dna-center)
6. [References](#references)
7. [Preview](#preview)

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
│   credentials.py
│   requirements.txt
│   README.md
│   .gitignore
│   LICENSE
│
└───assets
        preview.png
```

Once you clone the repo, please open `.gitignore` and uncomment `credentials.py`.

> The `credentials.py` file should **NEVER** be committed nor pushed to any remote repos. _(The `credentials.py` in this repo is the `Cisco AO Lab 2.1.2.5` that is a free to lab.)_

### Usage

You need to provide your DNA Center credentials in `credentials.py` file.

Then run:

```python3
python main.py
```

Voila :sparkles:! The Excel file is created automatically for the device list on Cisco DNA Center and configuration files of those devices are created in `configs/<device_hostname>.txt`.

> The Excel file opens immediately upon creation.

> `XlsxWriter` does not give you the option to append new data to a created file. So every time you send a request, the Excel file will be overwritten. You should close the Excel program before sending any new requests.

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

**Example:**

`credentials.py`

```python
BASE_URL = "https://10.10.1.1" # without a trailing slash (/)
USERNAME = "root"
PASSWORD = "CiscoAdmin!2345"
SSL_CERTIFICATE = False # set to True if you have a valid certificate
```

### References

**APIs List**

[DNA Center Platform](https://developer.cisco.com/docs/dna-center/#!authentication-api)

### Preview

![Preview](/assets/preview.png)
