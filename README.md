# Working Hours Project

*A comprehensive Django application for corporate time tracking and analytics.*

This repository hosts the **Working Hours Project**, an internal tool designed to streamline how employees log their daily work, manage projects, and provide leadership with actionable insights. Developed for use within your organization, it integrates with ClickUp, Google Sheets, and Slack via Zapier to automate project creation, client updates, and timely reminders.

---

## Key Features

- **ClickUp Integration**: Automatically create new projects in Django when a task is added in ClickUp; update project records when client information changes.
- **Employee Time Entry**: Responsive front‑end form for logging tasks, durations (`hours:minutes`), and comments; supports adding new tasks on the fly.
- **WorkLog Management**: Stores entries in a PostgreSQL database with regular vs. overtime classification.
- **Admin Dashboard**:
  - Filter by project, employee, date, and overtime status.
  - Paginated work log listing (5 entries per page).
  - Interactive **Chart.js** visualizations:
    - **Horizontal bar chart** of total hours per task (scrollable or paginated for long lists).
    - **Doughnut chart** showing hours distribution across employees.
- **Slack Notifications**: Zapier‑powered alerts to remind team members to submit daily logs (configurable times, e.g., 7 PM and 2 AM).
- **Responsive Design**: Ensures usability across desktop and mobile without unnecessary scrolling.

## Tech Stack

- **Backend**: Python 3.12, Django 5.1
- **Database**: PostgreSQL (`psycopg2-binary`)
- **Frontend**: HTML5, CSS3 (custom theme), JavaScript, Chart.js
- **Deployment**: Vercel (serverless Django via WSGI)
- **Integrations**: ClickUp API, Zapier (Google Sheets & Slack)

## Repository Structure

```
├── myapp/                 # Django app containing models, views, templates
├── working_hours_detecting/  # Django project settings & WSGI entry point
├── static/                # CSS, JS, and Chart.js assets
├── templates/             # Overridden admin and front‑end templates
├── requirements.txt       # Python dependencies
└── vercel.json            # Vercel deployment configuration
```

## Installation & Setup

1. **Clone & Virtual Environment**

   ```bash
   git clone https://github.com/yourorg/working-hours-project.git
   cd working-hours-project
   python -m venv .venv
   source .venv/bin/activate      # macOS/Linux
   .\.venv\Scripts\activate     # Windows
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables** Create a `.env` in the root with:

   ```ini
   SECRET_KEY=<django-secret-key>
   DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DBNAME
   CLICKUP_API_TOKEN=pk_xxx_xxxxxxxxxxxx
   ```

4. **Database Migrations & Superuser**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Collect Static Files**

   ```bash
   python manage.py collectstatic
   ```

6. **Run Locally**

   ```bash
   python manage.py runserver
   ```

   Access the app at [http://localhost:8000](http://localhost:8000)

## Deployment on Vercel

- Install Vercel CLI: `npm i -g vercel`
- Configure `vercel.json` for Python WSGI and environment variables.
- Deploy: `vercel --prod`

## Zapier Workflows

1. **ClickUp → Google Sheets**: Add or update project rows.
2. **Google Sheets → Webhook**: Notify `/populate-clientupdated/` to update client info.
3. **Google Sheets → Slack**: Send reminders at designated times, matching employee IDs to Slack user IDs.

## Contributing

1. Fork this repo
2. Create a feature branch: `git checkout -b feature/xyz`
3. Commit your changes and push
4. Open a Pull Request for review

---
 

