# Appointment Booking System

A Django-based web application designed for small service providers to manage client appointments efficiently.

## Features
- **Create, Read, Update, Archive (CRUD):** Manage appointments with a clean interface.
- **Soft Delete (Archive):** Archiving keeps the record in the database but hides it from the active list.
- **Validation:** Prevents past-date bookings, enforces 30-minute intervals, and blocks double bookings.
- **Search & Filter:** Search by client name and filter by status (Scheduled, Completed, Cancelled).
- **Responsive UI:** Built with Tailwind CSS for a clean, professional look.

## Tech Stack
- Django 6.1.2
- SQLite (Database)
- Tailwind CSS (via CDN)

## Installation
1. Clone this repository.
2. Activate a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Start the server: `python manage.py runserver`

## Demo Script (For Presentation)
1. Show the **Appointment List** (Upcoming appointments).
2. **Create a New Appointment:** Show validation errors (past date, double booking).
3. **Edit an Appointment:** Change status from "Scheduled" to "Completed".
4. **Archive an Appointment:** Click "Archive", confirm, and show that it disappears from the list. Check "Show Archived" to see it.
5. **Search and Filter:** Type a client name and filter by status.