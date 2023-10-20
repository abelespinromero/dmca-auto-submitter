# DMCA Notice Email Extractor and Automated Google Form Responder

## Description

This project is designed to investigate and demonstrate techniques that could be used to extract emails containing "Notices of DMCA removal from Google Search" and to automate the sending of Google Forms to recover URLs that have been removed due to copyright issues. This project is strictly for research and educational purposes and should be used responsibly.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Modules Description](#modules-description)
- [Warning](#warning)
- [Contribution](#contribution)
- [Authors](#authors)
- [License](#license)

## Requirements

- Python 3.x
- Additional Libraries:
  - selenium
  - regex
  - pandas

## Setup

1. **Clone the Repository**: `git clone <repository_url>`
2. **Install Dependencies**: Navigate to the project directory and run `pip install -r requirements.txt`.
3. **Environment Variables**: Set up necessary environment variables or use a configuration file for email and application password credentials.

## Usage

Run `python main.py` to initiate the process which coordinates the execution of individual modules as described below.

## Modules Description

### `scrape_emails.py`
This script connects to an email mailbox using imap and searches for emails that match certain criteria (such as subject line, sender, etc.) for extraction. It leverages the imaplib and email libraries to fetch and parse email data.

### `extract_urls.py`
This script is responsible for extracting URLs that are related to DMCA notices from the emails. It searches for specific patterns in the email body to identify and extract such URLs.

### `send_forms.py`
This script is designed to automate the process of sending Google Forms to try and recover removed URLs. It uses Selenium to pre-fill and submit forms automatically.

### `forms_data.py`
This file contains data related to email used and the Google Forms that are to be sent. This could include question IDs, pre-filled answers, etc.

### `main.py`
This is the main script that coordinates all the above tasks. It calls each script in a specific order to ensure a smooth workflow.

## Orchestration with Apache Airflow

This project is configured to run daily jobs orchestrated by [Apache Airflow](https://airflow.apache.org/). Airflow allows us to schedule, monitor, and manage the project's workflow, ensuring that the email extraction and form submission tasks are carried out systematically.

The DAG (Directed Acyclic Graph) configuration for this project is defined in `airflow/dags.py`. This file specifies the schedule, tasks, and their dependencies.

## Warning

This project is intended for educational and research purposes only. Do not use this code for activities that violate laws or regulations.

## Contribution

Contributions are welcome. Open a pull request to propose changes or improvements.

## Authors

- [Author's Name](mailto:abel.espin.romero@gmail.com)

## License

This project is under a specific license that permits educational and research use only.
