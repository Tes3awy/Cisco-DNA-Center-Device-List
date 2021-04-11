# Cisco DNA AO Lab Devices

This program is designed to get Cisco DNA Center AO Lab devices and save them to an xlsx sheet.

---

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Collected Data from Response](#collected-data)
4. [Preview](#preview)

## Installation

```python3
pip install -r requirements.txt
```

## Usage

```python3
python cisco_dna_lab.py
```

Voila! The xlsx file is automatically created for the devices on Cisco DNA Center AO Lab.

> The xlsx file opens immediately upon creation.

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

## Preview

![Preview](/assets/preview.png)
