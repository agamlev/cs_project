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

## 1. Clone the repository

```bash
git clone https://github.com/agamlev/cs_project.git
cd cs_project
