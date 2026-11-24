# Palazzolo Technical & Vocational Training Institute (PTVTI)

[![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Accreditation](https://img.shields.io/badge/TVETA-Accredited-D4AF37?style=for-the-badge)](https://www.tveta.go.ke/)
[![Partners](https://img.shields.io/badge/NITA_%26_UNESCO-Partner-0B2545?style=for-the-badge)](https://www.nita.go.ke/)

The official web platform and student portal for **Palazzolo Technical & Vocational Training Institute (PTVTI)** located in Kiambu County, Kenya.

Established in November 2021 by the **Poverelle Sisters** (*Institute of the Sisters of the Poor - Palazzolo*), PTVTI delivers values-based, competency-centered technical and vocational education (TVET) to transform youth into skilled, self-reliant professionals.

> *"With God at the Centre, we serve, train and transform"*

---

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Departments & Courses](#departments--courses)
- [Technology Stack](#technology-stack)
- [Project Architecture](#project-architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database & Seed Data](#database--seed-data)
  - [Running the Server](#running-the-server)
  - [Running Tests](#running-tests)
- [Administration & Staff Access](#administration--staff-access)
- [API Documentation](#api-documentation)
- [Contributing & License](#contributing--license)

---

## Overview

The PTVTI rebrand site provides a modern, accessible, and mobile-responsive online experience for prospective students, parents, industry partners, and staff. It integrates curriculum discovery, online application submissions with automated reference tracking, event registrations, news feeds, and an administrative portal.

---

## Key Features

1. **Brand Identity & Responsive Design:**
   - Bespoke PTVTI color palette: Institutional Gold (`#D4AF37`), Deep Navy (`#0B2545`), crisp whites, and high-contrast typography.
   - Fully responsive layout across mobile, tablet, desktop, and ultra-wide displays with safe viewport padding and zero overflow.
   - Smooth horizontal scrolling for course filters and category badges.

2. **Course & Department Discovery:**
   - Dedicated pages for all 5 vocational departments with robust slug-matching and alias resolution.
   - Filterable catalog supporting full-length TVETA accredited programmes and 3-month modular short courses.
   - Detailed course outlines including duration, fees, requirements, and direct application links.

3. **Online Admissions & Application Tracking:**
   - Multi-step online application form with real-time course fee lookups and automatic application fee calculation.
   - Instant generation of unique application tracking codes (e.g. `PTVTI-APP-XXXXXXXX`).
   - Self-service application tracking portal allowing applicants to check approval status and intake schedules anytime.

4. **Dynamic Hero Carousel & Announcements:**
   - Interactive hero carousel managed via Django Admin.
   - Supports both internal relative paths (e.g. `/courses/`, `/admissions/apply/`) and full external URLs with automated protocol validation.
   - Top banner announcement strip for urgent institutional notices.

5. **Events & Workshop Registration:**
   - Upcoming campus workshops and open day listings with date badges and venue details.
   - Public RSVP form with duplicate prevention per email address.

6. **News & Stories:**
   - Institutional announcements, graduation highlights, and student success features.

7. **Staff & Administration Portal:**
   - Full-featured Django administration suite for managing admissions, student applications, course listings, staff directory, hero slides, and testimonials.

---

## Departments & Courses

PTVTI offers training across 5 key vocational departments:

| Department | Program Offerings |
| :--- | :--- |
| **Engineering Department** | Electrical Installation, Electrical Wireman, Plumbing & Pipe Fitting, Arc & Gas Welding, Masonry, Solar PV Technology |
| **ICT & Computing** | Graphic Design, Computer Applications, Web Development, 2D Animation, Network Maintenance |
| **Fashion & Design** | Garment Making, Tailoring, Dressmaking, Screen Printing, Bag & Accessory Craft |
| **Cosmetology & Hairdressing** | Hairdressing, Barbering, Dreadlocks, Nail Technology, Esthetics & Skin Care |
| **Hospitality & Catering** | Baking & Pastry Production, Food & Beverage Service, Bakery Management, Event Catering |

---

## Technology Stack

- **Backend Framework:** Django 5.x / Python 3.10+
- **REST API:** Django REST Framework (DRF)
- **Database:** SQLite (default for development) / PostgreSQL ready for production
- **Frontend / Styling:** Bootstrap 5.3.3, Vanilla CSS Design System, FontAwesome 6
- **Interactions:** Lightweight vanilla JavaScript modules (no bulky frontend framework overhead)
- **Media / Assets:** Pillow for dynamic image uploads and thumbnail rendering

---

## Project Architecture

```
palazzolo-rebrandsite/
├── admissions/              # Online application forms, fee tracking & status lookups
├── config/                  # Django project configuration, settings, context processors, URLs
├── contacts/                # Contact inquiry forms, messages & department contacts
├── content/                 # Hero carousel, announcements, events, staff, testimonials & gallery
├── courses/                 # Departments, full-length & short courses, templatetags
├── news/                    # News items, category filters & updates
├── static/
│   ├── css/                 # Modular design system (variables, navigation, homepage, etc.)
│   ├── js/                  # Main JS, counters, filters, forms, horizontal-scroll
│   └── images/              # Institutional logos, banners, workshop photos
├── templates/
│   ├── admissions/          # Apply & Track templates
│   ├── courses/             # Course catalog & detail templates
│   ├── departments/         # Department overview & curriculum templates
│   ├── includes/            # Navbar, footer, announcement strip, messages
│   ├── news/                # News list & article detail templates
│   └── pages/               # Homepage, About, Contact
├── manage.py
└── requirements.txt
```

---

## Getting Started

### Prerequisites
- Python 3.10 or higher installed:
  ```bash
  python --version
  ```
- Git installed on your machine.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ashirumah11/palazzolo-rebrandsite.git
   cd palazzolo-rebrandsite
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Database & Seed Data

1. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

2. **Seed initial institutional content & courses (optional but recommended):**
   ```bash
   python manage.py seed_ptvti_data
   ```

3. **Create an administrator account:**
   ```bash
   python manage.py createsuperuser
   ```

### Running the Server

Start the local development server:
```bash
python manage.py runserver 127.0.0.1:8000
```
Open your browser and visit:
- **Public Website:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin Portal:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **REST API:** [http://127.0.0.1:8000/api/v1/](http://127.0.0.1:8000/api/v1/)

### Running Tests

Execute the automated test suite to ensure system integrity:
```bash
python manage.py test
```

---

## Administration & Staff Access

Staff and administrators can manage all site content through the Django Admin interface at `/admin/`. Key management modules include:
- **Hero Carousel:** Update hero banners, taglines, button labels, and internal/external target links.
- **Applications:** Review submitted student admissions, track verification status, and update applicant notes.
- **Courses & Departments:** Update tuition fees, durations, requirements, and assign modular short courses.
- **Announcements:** Post real-time admission or term opening notices displayed in the top bar.

---

## API Documentation

The platform provides RESTful JSON endpoints under `/api/v1/`:
- `GET /api/v1/courses/` — List all active vocational courses
- `GET /api/v1/departments/` — List all institutional departments
- `GET /api/v1/content/hero-carousel/` — Active carousel slides
- `GET /api/v1/content/events/` — Upcoming events and workshops
- `POST /api/v1/content/events/<id>/register/` — RSVP registration for an event
- `POST /api/v1/admissions/applications/` — Submit application via API

---

## License & Organization

&copy; 2026 **Palazzolo Technical & Vocational Training Institute**. All rights reserved.  
Operated by the **Institute of the Sisters of the Poor (Poverelle Sisters)**.  
Accredited by **TVETA Kenya** | Affiliated with **NITA & UNESCO**.
