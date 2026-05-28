# JobPortal — Flask + SocketIO + Scikit-Learn

A modern, SaaS-style job portal with AI-powered matching, real-time activity feed, and a sleek glassmorphism UI.

## Features

- **AI Match Scores** — TF-IDF cosine similarity (scikit-learn) ranks jobs by candidate skill fit
- **Real-time Feed** — Socket.IO broadcasts application events live to the admin dashboard
- **Slide-over Panel** — Job details and apply form open in a slide-over without page reload
- **Status Stepper** — Visual Applied → Interview → Hired tracker per application
- **Smart Filter** — Search jobs by title, type, and location
- **Admin Dashboard** — Post jobs, view all applications, update candidate statuses live
- **Glassmorphism UI** — Dark slate theme with Electric Blue accents (Tailwind CSS + DM Sans)

## Stack

| Layer | Tech |
|-------|------|
| Backend | Flask, Flask-Login, Flask-SQLAlchemy |
| Realtime | Flask-SocketIO (threading mode) |
| AI | scikit-learn TF-IDF + cosine similarity |
| DB | SQLite (swappable via DATABASE_URL env var) |
| Frontend | Tailwind CSS (CDN), Vanilla JS, Socket.IO client |
| Fonts | DM Sans + DM Mono |

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python run.py
```

Open http://localhost:5000

## Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin / Recruiter | admin@jobportal.com | admin123 |
| Job Seeker | user@jobportal.com | user123 |

The seeker account has skills: `Python, Flask, React, SQL, Docker` — so you'll see real match scores right away.

## Project Structure

```
jobportal/
├── run.py                   # Entry point + DB seed
├── config.py                # Config (secret key, DB URL)
├── requirements.txt
└── app/
    ├── __init__.py          # App factory
    ├── extensions.py        # db, login_manager
    ├── models.py            # User, Job, Application
    ├── ai_matcher.py        # TF-IDF match scoring
    ├── socket_events.py     # Socket.IO events
    ├── routes/
    │   ├── auth.py          # Login, register, logout
    │   └── main.py          # Dashboard, jobs, apply, admin
    └── templates/
        ├── base.html        # Sidebar, topbar, slide-over, socket
        ├── auth/            # login.html, register.html
        ├── jobs/            # list.html, detail.html
        ├── seeker/          # dashboard.html, applications.html
        └── dashboard/       # admin.html, new_job.html
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `dev` | Flask session secret |
| `DATABASE_URL` | `sqlite:///jobportal.db` | SQLAlchemy DB URI |

## Switching to PostgreSQL

```bash
export DATABASE_URL="postgresql://user:pass@localhost/jobportal"
python run.py
```
