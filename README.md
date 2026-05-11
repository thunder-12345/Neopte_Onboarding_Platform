# Neopte Foundation — Onboarding Platform

A web-based onboarding and management platform for Neopte Foundation, handling intern and volunteer lifecycle: hours tracking, task assignments, document management, grading, and admin oversight.

**Live:** [neopte-onboarding-platform-2.onrender.com](https://neopte-onboarding-platform-2.onrender.com)

---

## Overview

The platform supports five user roles, each with their own dashboard and permissions. Admins and board members manage the organization; interns and volunteers complete tasks, log hours, and upload documents through their own portals.

---

## Roles

| Role | Access |
|---|---|
| **Admin** | Full platform access — manage users, roles, tasks, hours, documents, view executive dashboard |
| **Board** | Create and grade tasks, approve hours and documents, view all user activity |
| **Intern** | Personal dashboard, task submissions, hours logging, document uploads, grades |
| **Volunteer** | Same as intern — personal dashboard, tasks, hours, documents, downloadable certificate |
| **User** | Default on registration — no access until assigned a role by an admin |

---

## Features

### Admin Dashboard
Executive summary visible to admins on login — no navigation required to get a pulse on the org:
- Org-wide headcount (interns, volunteers, board members)
- Pending approvals counter across hours, documents, and task submissions
- Action items inbox with direct links — hours queue, document queue, grading queue, unassigned accounts (auto-filtered)
- Intern progress table — task completion progress bar, average grade, pending tasks per intern, org-wide completion rate
- Hours overview — total approved hours, pending hours, top contributors this month
- Recent activity feed — last 10 platform events with actor and time-ago

### Role-Based Dashboards
Each role lands on a dashboard tailored to their workflow. Interns and volunteers see their task list, grade summary, hours total, and quick links to certificates and grade reports.

### Task Management
- Board members create tasks assigned to a role group or specific users
- Tasks are classified as **projects** (require submission and grading) or **reminders** (can auto-complete)
- Recurring reminders supported: daily, weekly, biweekly, monthly with an end date
- Tasks move through statuses: `pending → done → graded`
- File upload supported for project submissions

### Grading
- Board members grade submitted tasks with a score and denominator (e.g. 47/50)
- Graded scores appear on intern/volunteer dashboards and in their downloadable grades report PDF
- Average and highest grades calculated automatically

### Hours Tracking
- Interns and volunteers log hours with activity name, date, start/end time, and description
- Board members approve or deny submissions from a pending queue
- Approved hours accumulate on the user's profile and appear in admin reporting

### Document Management
- Users upload PDF documents with a type and description
- Board members review and approve or deny from a pending queue
- Documents viewable inline in the browser

### PDF Generation
- **Volunteer Certificate** — official certificate of service with total approved hours, generated on demand
- **Grades Report** — formatted transcript of all project assignments with scores, statuses, and averages

### Activity Log
- Immutable audit trail of every significant action on the platform
- Visible to admins and board members
- Shows actor, action type, target, and timestamp

### User Management
- Admins and board members can search and filter the full user list by name or role
- Role upgrades and downgrades applied directly from the user list
- Account deletion available

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | PostgreSQL (production), SQLite (local dev) |
| ORM | SQLAlchemy + Flask-Migrate |
| Auth | Flask-Login |
| Forms | Flask-WTF |
| PDF generation | ReportLab |
| Frontend | Jinja2 templates, Bootstrap 5, custom CSS |
| Hosting | Render |

---

## Local Setup

**Prerequisites:** Python 3.10+, pip or conda

```bash
# Clone the repo
git clone https://github.com/thunder-12345/Neopte_Onboarding_Platform.git
cd Neopte_Onboarding_Platform

# Install dependencies
pip install -r requirements.txt

# Create a .env file
echo "SECRET_KEY=your-secret-key" > .env

# Run the app
python app.py
```

The app runs at `http://127.0.0.1:5000`. A local SQLite database is created automatically on first run at `instance/project.db`.

**Using conda:**
```bash
conda env create -f environment.yml
conda activate neopteenv
python app.py
```

---

## Project Structure

```
├── app.py                  # All routes and PDF generation
├── project/
│   ├── __init__.py         # App factory, DB config, login manager
│   ├── models.py           # SQLAlchemy models
│   ├── forms.py            # WTForms form definitions
│   ├── decorators.py       # Role-based permission decorators
│   ├── activity.py         # Activity logging utility
│   ├── templates/          # Jinja2 HTML templates
│   ├── static/
│   │   ├── css/            # Stylesheets per page
│   │   └── js/             # Client-side scripts
│   └── uploads/            # Uploaded task files and documents
└── migrations/             # Flask-Migrate migration scripts
```

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Flask session secret | `mysecretkey` (change in prod) |
| `DATABASE_URL` | PostgreSQL connection string | Falls back to SQLite |
