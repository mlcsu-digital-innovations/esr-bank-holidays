# ESR Bank Holiday Importer

This Python script automates the process of importing UK bank holidays into the NHS Electronic Staff Record (ESR) system using Selenium and official data from the UK government.

## Features

- Automatically fetches official UK bank holidays for the **current financial year** (April 1 – March 31).
- Logs into the ESR portal using your NHS login.
- Adds each bank holiday as an annual leave entry marked **"Bank Holiday"**.
- Supports **test mode** to simulate actions without submitting entries.

## Requirements

- Python 3.7+
- Google Chrome
- ChromeDriver (must be installed and in your PATH)
- Internet connection

## Python Dependencies

Install required packages using pip:

```bash
pip install selenium requests
```

## Configuration

You can configure the script by editing these variables at the top of the script:

```python
ESR_URL = "https://my.esr.nhs.uk/dashboard/..."
GOV_HOLIDAYS_URL = "https://www.gov.uk/bank-holidays.json"
TEST_MODE = 1  # Set to 0 to actually submit entries in ESR
```

> 💡 With `TEST_MODE = 1`, the script will go through the motions without submitting holidays.

## Usage

Run the script from your terminal:

```bash
python esr_bank_holiday_importer.py
```

You will be prompted to enter your ESR password securely. The script assumes your username is defined in the `ESR_USERNAME` variable.

## What It Does

1. Downloads official bank holidays from `gov.uk`.
2. Filters them by the current **financial year** (April–March).
3. Launches Chrome and logs into the ESR portal.
4. Enters each holiday with appropriate comments and dates.
5. Submits (or cancels in test mode) each leave request.

## Security Notes

- Password is entered via secure prompt (`getpass`) and is **not stored**.
- Credentials are used only within your local session.

## Disclaimer

This script is not officially affiliated with ESR. Use it at your own risk, and ensure you verify entries if using in non-test mode.

---

**Author:** Dr Matthew Bennion - ML CSU Innovation - Digital Innovation Unit  
**License:** MIT
