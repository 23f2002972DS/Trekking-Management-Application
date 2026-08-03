# Trekking Management System

A Flask-based trekking management web application that allows clients to browse treks, guides to manage assigned treks, and managers to oversee users, bookings, and trek operations.

## Features
- Client login and trek booking
- Guide dashboard for managing assigned treks
- Manager dashboard for creating, editing, deleting, and approving records
- Reservation tracking and slot management
- SQLite-backed persistence

## Tech Stack
- Python
- Flask
- Flask-SQLAlchemy
- Jinja2
- HTML/CSS
- SQLite

## Project Structure
- main.py - application entry point
- Database/models.py - database models
- routes/ - route blueprints for authentication, clients, guides, and admins
- views/ - HTML templates
- style/ - static stylesheets

## Setup Instructions
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

## Demo Credentials
- Manager: username `manager`, password `manager`
- Guide: username `charlie_guide`, password `password123`
- Client: username `alice_client`, password `password123`

## Notes
The application is designed as a simple management system for trekking operations with role-based access for clients, guides, and managers.
