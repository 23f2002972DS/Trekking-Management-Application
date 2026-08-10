# Trekking Management System

A Flask-based trekking management system for coordinating trek listings, client bookings, guide assignments, and manager approvals.

## Overview
This application supports three main user roles:
- Client: browse available treks, book open slots, and view reservations.
- Guide: manage assigned treks, update trek status, and adjust open slots.
- Manager: add, edit, delete, and approve treks and users, view reservations, and monitor system statistics.

The backend uses Flask with SQLAlchemy and an SQLite database for persistence.

## Features
- Role-based authentication and session handling
- Client dashboard for searching and booking treks
- Guide dashboard for trek status updates and slot control
- Manager dashboard for trek management and user approvals
- Admin actions for approving guides, banning users, and deleting records
- SQLite database created automatically at runtime

## Project Structure
- `main.py` — application entry point and database initialization
- `Database/models.py` — SQLAlchemy models for users, treks, and reservations
- `routes/auth_routes.py` — login, registration, and logout routes
- `routes/client_routes.py` — client dashboard, trek search, and booking actions
- `routes/guide_routes.py` — guide dashboard and trek update actions
- `routes/admin_routes.py` — manager dashboard and administrative controls
- `views/` — HTML templates for each role and UI pages
- `style/` — CSS stylesheet(s)

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python main.py
   ```
3. Open the browser at:
   ```text
   http://127.0.0.1:8112
   ```

## Default Credentials
The app automatically creates a default manager account on first run:
- Manager: `manager` / `manager`

Additional client and guide accounts can be created via the registration page.

## Notes
- Registered clients are approved automatically and can access the client dashboard immediately.
- Guide registrations require manager approval before the guide dashboard becomes available.
- The app uses `TMAS_sqlite.db` in the project root for storage.
- The root URL redirects to `/client/login`.

## Improvements
Potential future enhancements include:
- payment processing integration
- email notifications for bookings and approvals
- improved search and filtering for treks
- responsive/mobile-friendly UI
- reporting and analytics for manager insights 