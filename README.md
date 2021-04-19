# Cisco DNA AO Lab Devices

This program is designed to get Cisco DNA Center AO Lab devices and save them to an `xlsx` sheet.

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
$ git clone https://github.com/Tes3awy/Cisco-DNA-AO-Lab-Devices.git
$ cd Cisco-DNA-AO-Lab-Devices
$ pip install -r requirements.txt
```

### Getting Started

```bash
│   cisco_dna_lab.py
│   credentials.py
│   requirements.txt
│   .gitignore
│   README.md
│   LICENSE
│
└───assets
        preview.png

```

Once the repo is cloned, please open `.gitignore` and uncomment `credentials.py`.

### Usage

```python3
python cisco_dna_lab.py
```

Voila :sparkles:! The `xlsx` file is automatically created for the devices on Cisco DNA Center AO Lab.

> The `xlsx` file opens immediately upon creation.

> `XlsxWriter` doesn't give you the option to append new data. So every time a request is made, the `xlsx` file will be overwritten.

### Collected Data from Response

1. Hostname
2. Management IP Address
3. Serial Number
4. Mac Address
5. Platform ID _(Device Model)_
6. Software Version
7. Role
8. Up Time
9. Last Update
10. Reachability Status

### Use it for your DNA Center

This program is ready to be used for your deployed DNA Center. You need to provide your appropriate credentials.

> The `credentials.py` file should **NEVER** be committed nor pushed to any remote repos. _(The one in this repo is the `Cisco AO Lab 2.1.2.5` which is a public and free to use Lab.)_

**Example:**

`credentials.py`

```python
base_url = "https://10.10.1.1" # without a trailing slash (/)
username = "root"
password = "CiscoAdmin!2345"
ssl_certificate = False
```

### References

**APIs**

[DNA Center Platform](https://developer.cisco.com/docs/dna-center/#!authentication-api)

### Preview

![Preview](/assets/preview.png)
