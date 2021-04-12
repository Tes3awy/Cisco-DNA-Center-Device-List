# Cisco DNA AO Lab Devices

This program is designed to get Cisco DNA Center AO Lab devices and save them to an `xlsx` sheet.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Collected Data from Response](#collected-data)
4. [Use it for your DNA Center](#use-it-for-your-dna-center)
5. [Preview](#preview)

## Installation

```bash
$ git clone https://github.com/Tes3awy/Cisco-DNA-AO-Lab-Devices.git
$ cd Cisco-DNA-AO-Lab-Devices
$ pip install -r requirements.txt
```

## Usage

```python3
python cisco_dna_lab.py
```

Voila :sparkles:! The `xlsx` file is automagically created for the devices on Cisco DNA Center AO Lab.

> The `xlsx` file opens immediately upon creation.

## Collected Data from Response

1. Hostname
2. Management IP Address
3. Serial Number
4. Mac Address
5. Platform ID _(Device Model)_
6. Software Version
7. Role
8. Up Time _(In Days)_
9. Reachability Status

## Use it for your DNA Center

This program is ready to be used for your deployed DNA Center. You need to provide your appropriate credentials.

Create a `credentials.py` file and store your secret data within.

> The `credentials.py` file should neither be committed nor pushed to any remote repos.

**Example:**

```bash
touch credentials.py
```

Open `credentials.py` and add:

```python
base_url = "https://10.10.1.1" # without a trailing slash (/)
username = "root"
password = "CiscoAdmin!2345"
ssl_certificate = False
```

## Preview

![Preview](/assets/preview.png)
