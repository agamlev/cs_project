This document explains how to set up and run the **CS Ops Automation Toolkit** locally.

The project connects **Jira, Gmail, and Google Sheets** using Python and public APIs, with the goal of automating common CSOps workflows and reducing manual operational work.

This is a developer-friendly, ops-first internal tool — not a packaged SaaS product.

---

## Who is this for

This project is intended for:
- CS / Support Operations professionals with basic technical skills
- Developers supporting support or operations teams
- Teams looking to automate Jira-based workflows and reporting

Basic familiarity with Python and APIs is recommended.

---

## Prerequisites

Before you start, make sure you have:

- Python **3.9 or higher**
- A Jira Cloud account with API access
- A Google account with access to:
  - Gmail
  - Google Sheets
- A Google Cloud project

---

2. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Google Cloud setup (Gmail & Sheets)
4.1 Create a Google Cloud project

Go to Google Cloud Console

Create a new project

4.2 Enable required APIs

Enable the following APIs:

Gmail API

Google Sheets API

4.3 Create a Service Account

Navigate to IAM & Admin → Service Accounts

Create a new Service Account

Generate a JSON key file

Download the file locally

⚠️ Do not commit this file to the repository

5. Google Sheets access

Create or choose a Google Sheet

Copy the Sheet ID from the URL

Share the sheet with the service account email
(found inside the JSON credentials file)

6. Jira API setup

Generate a Jira API Token and make sure you have:

Jira base URL

Jira account email

Jira API token

7. Environment variables

Set the following environment variables:

export GOOGLE_SERVICE_ACCOUNT_JSON="path/to/service_account.json"
export GOOGLE_SHEET_ID="your-google-sheet-id"

export JIRA_BASE_URL="https://your-domain.atlassian.net"
export JIRA_EMAIL="your-email@example.com"
export JIRA_API_TOKEN="your-jira-api-token"


You may also use a .env file if preferred.

8. Running the scripts
8.1 Fetch Jira tickets into Google Sheets
python jira_fetch.py


This script:

Fetches Jira issues

Maps company identifiers to tickets

Overwrites the Google Sheet with fresh data

Maintains a single source of truth

8.2 Sync incoming emails with Jira tickets
python jira_gmail_sync.py


This script:

Scans incoming Gmail messages

Matches emails to existing Jira tickets

Preserves email context within ticket workflows

9. Expected output

After a successful run:

Google Sheets contains an up-to-date snapshot of Jira tickets

Email context is linked to the correct Jira issues

Manual tracking and copy-paste workflows are reduced

10. Operational notes

The project overwrites data on each run

Designed for batch execution (cron / scheduled jobs)

Optimized for internal Ops workflows

No secrets are hard-coded

11. Troubleshooting

If something fails:

Verify API permissions

Confirm environment variables are set

Check service account access to the Google Sheet

Review API quotas and limits

12. Extending the project

Common extensions:

Add alerts (Slack / email)

Add dashboards on top of Google Sheets

Schedule execution via cron or CI

Add support for additional Jira fields

License

Free to use and adapt for internal workflows.

## 1. Clone the repository

```bash
git clone https://github.com/agamlev/cs_project.git
cd cs_project
