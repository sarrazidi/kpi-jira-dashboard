# KPI Jira Dashboard

A web application that **extracts tickets from a Jira project, stores them in a SQL database and computes performance indicators (KPIs)**, exposed through a Flask REST API and displayed in a dashboard.

> The Jira data used in this project is **test data I created myself**. No company or client data is included.

---

## Table of contents

- [Context and goal](#context-and-goal)
- [Features](#features)
- [Tech stack](#tech-stack)
- [Architecture](#architecture)
- [Screenshots](#screenshots)
- [Project structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the project](#running-the-project)
- [API](#api)
- [Computed KPIs](#computed-kpis)
- [Security](#security)
- [Challenges and lessons learned](#challenges-and-lessons-learned)
- [Future improvements](#future-improvements)
- [Author](#author)

---

## Context and goal

Jira holds a lot of data about a team's work (tickets, statuses, types, dates), but it is hard to turn it quickly into usable numbers.

This project answers one question: **how can Jira tickets be turned into clear indicators to track a team's activity?**

The application automates the whole pipeline: fetching data from the Jira API, storing it, computing KPIs with pandas, then displaying them.

## Features

- Automatic ticket extraction from the **Jira REST API**
- Data storage in a **SQL database** (SQLite)
- **Volume KPIs** (tickets by status, by type)
- **Time KPIs** (ticket processing time)
- **REST API** built with Flask, returning KPIs as JSON
- **Admin authentication** (email and password)
- **Web dashboard** to visualize the indicators
- Configuration through **environment variables** (no secrets in the code)

## Tech stack

| Area | Tools |
|---|---|
| Language | Python 3 |
| Backend / API | Flask |
| Data analysis | pandas |
| Database | SQLite (SQL) |
| Data source | Jira REST API (`requests`) |
| Frontend | *(to complete: React / HTML-CSS-JS)* |
| Configuration | python-dotenv |
| Version control | Git and GitHub |

## Architecture

```
┌──────────┐   REST API   ┌──────────────┐   SQL    ┌───────────────┐
│   Jira   │ ───────────► │ extraction.py│ ───────► │ jira_kpi.db   │
└──────────┘              └──────────────┘          └───────┬───────┘
                                                            │ pandas
                                                            ▼
┌──────────────┐   JSON    ┌──────────────┐        ┌───────────────┐
│   Frontend   │ ◄──────── │   app.py     │ ◄───── │ KPI computing │
│ (dashboard)  │   /api/*  │   (Flask)    │        └───────────────┘
└──────────────┘           └──────────────┘
```

1. `extraction.py` queries Jira and saves the tickets in the database.
2. The `kpi_*.py` scripts compute the indicators with pandas.
3. `app.py` exposes the results through `/api/...` routes.
4. The frontend calls the API and displays the charts.


## Project structure

```
projet-kpi-jira/
├── frontend/            # Web interface (dashboard)
├── screenshots/         # Screenshots used in the README
├── app.py               # Flask API (routes, login)
├── extraction.py        # Ticket extraction from Jira
├── kpi_temps.py         # Time KPIs
├── kpi_volume.py        # Volume KPIs
├── kpi_final.py         # Final KPI computation
├── requirements.txt     # Python dependencies
├── .env.example         # Configuration template
├── .gitignore
└── README.md
```

## Installation

### Prerequisites

- Python 3.10 or higher
- Node.js (if the frontend uses npm)
- A Jira Cloud account with an **API token**
- Git

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/sarrazidi/kpi-jira-dashboard.git
cd kpi-jira-dashboard

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it (Windows PowerShell)
venv\Scripts\Activate.ps1
# (macOS / Linux: source venv/bin/activate)

# 4. Install dependencies
pip install -r requirements.txt
```

Frontend (if applicable):

```bash
cd frontend
npm install
```

## Configuration

Secrets are **never** written in the code. They are read from a `.env` file that you create yourself.

1. Copy the template:

   ```bash
   copy .env.example .env      # Windows
   # cp .env.example .env      # macOS / Linux
   ```

2. Fill in `.env` with your own values:

   | Variable | Description |
   |---|---|
   | `JIRA_URL` | Your Jira URL (e.g. `https://your-space.atlassian.net`) |
   | `JIRA_EMAIL` | Jira account email |
   | `JIRA_API_TOKEN` | Jira API token ([create one here](https://id.atlassian.com/manage-profile/security/api-tokens)) |
   | `ADMIN_EMAIL` | Login email for the application |
   | `ADMIN_PASSWORD` | Login password for the application |
   | `SECRET_TOKEN` | Long random value returned after login |

   > Check that these names match the ones in your `.env.example`.

The `.env` file is listed in `.gitignore`: it is never pushed to GitHub.

## Running the project

**1. Extract data from Jira and fill the database:**

```bash
python extraction.py
```

**2. Start the API:**

```bash
python app.py
```

The API runs on `http://127.0.0.1:5000`.

**3. Start the frontend** (if applicable):

```bash
cd frontend
npm run dev
```

## API

| Method | Route | Description |
|---|---|---|
| `POST` | `/api/login` | Authentication, returns a token |
| `GET` | `/api/kpi/statut` | Number of tickets per status |
| `GET` | `/api/kpi/type` | Number of tickets per type |

> Add the other routes from your `app.py` here.

**Login request example:**

```bash
curl -X POST http://127.0.0.1:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "your_password"}'
```

**Response example:**

```json
{ "success": true, "token": "..." }
```

**`/api/kpi/statut` response example:**

```json
[
  { "statut": "To Do", "total": 4 },
  { "statut": "In Progress", "total": 3 },
  { "statut": "Done", "total": 12 }
]
```

## Computed KPIs

| KPI | Description | File |
|---|---|---|
| Tickets by status | Distribution of tickets by progress | `kpi_volume.py` |
| Tickets by type | Split between bugs, tasks, stories, etc. | `kpi_volume.py` |
| Processing time | Time between ticket creation and resolution | `kpi_temps.py` |
| Summary | Combination of the indicators | `kpi_final.py` |

## Security

- Secrets (Jira token, passwords) stored in a `.env` file excluded from Git
- No sensitive value hardcoded in the source
- `.env.example` provided with variable names only, no real values
- Local database excluded from the repository (`*.db`)
- Routes protected by an authentication token

## Challenges and lessons learned

- Fetching data from the Jira API and structuring it cleanly for the database
- Computing reliable indicators with pandas from raw data
- Securing a project before publishing it (environment variables, `.gitignore`)
- Organizing a project so that someone else can install and run it

## Future improvements

- Filters by period, assignee or project
- More charts (trends over time, burndown)
- Hashed passwords and real JWT tokens with expiration
- Move from SQLite to PostgreSQL
- Online deployment (Render or PythonAnywhere)
- Unit tests for the KPI calculations
- Docker containerization

