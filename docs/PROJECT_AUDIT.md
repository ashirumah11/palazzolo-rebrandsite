# PTVTI DIGITAL TRANSFORMATION & REBRANDING: COMPREHENSIVE PROJECT AUDIT

**Project:** Palazzolo Technical and Vocational Training Institute (PTVTI)  
**Domain:** [https://palazzolotechnical.co.ke/](https://palazzolotechnical.co.ke/)  
**Audit Date:** November 2026  
**Auditor:** Senior Full-Stack Django Developer & Software Architect  

---

## 1. Executive Summary

Palazzolo Technical and Vocational Training Institute (PTVTI) is a registered technical institution founded in November 2021 by the Poverelle Sisters (Institute of the Sisters of the Poor - Palazzolo) in Kiambu County, Kenya. Accredited by TVETA Kenya and affiliated with NITA and UNESCO, the institution provides competency-based vocational education across Engineering, ICT, Fashion & Design, Cosmetology & Hairdressing, and Hospitality.

The previous digital platform suffered from architectural fragmentation: a split architecture consisting of a headless Django REST Framework backend coupled with an external, disconnected React/Vite frontend. The Django application lacked customer-facing template views, had broken static asset delivery configurations in production, lacked a media-serving mechanism in `DEBUG=False` mode on cPanel, contained duplicated configurations, and caused frequent 404s for public routes such as `/courses`.

This audit comprehensively documents the current state of the backend across all 20 required dimensions, verifies the root causes of all historical defects, and establishes the blueprint for upgrading PTVTI into a unified, high-performance, template-driven Django platform styled to modern institutional standards without React or Node build dependencies.

---

## 2. Comprehensive Codebase Audit (20 Inspection Areas)

### 2.1 Root Directory Structure
The inspected Django backend structure:
```
palazzolo-rebrandsite/
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
├── accounts/
├── admissions/
├── config/
├── contacts/
├── content/
├── courses/
├── media/
│   ├── departments/
│   ├── events/
│   ├── gallery/
│   ├── hero-carousel/
│   └── staff/
├── news/
├── static/
│   └── images/
├── staticfiles/
│   ├── admin/
│   ├── jazzmin/
│   ├── rest_framework/
│   └── vendor/
└── templates/
    └── admin/
        ├── index.html
        └── login.html
```

### 2.2 manage.py
- Standard Django management script configured for `config.settings`.
- Properly configured; no custom flags or non-standard command overrides.

### 2.3 Requirements & Dependencies (`requirements.txt`)
- **Django:** `6.0.7` (runs on Python 3.12 / 3.14).
- **Database:** `psycopg==3.3.4`, `dj-database-url==3.1.2`.
- **API Framework:** `djangorestframework==3.17.1`, `djangorestframework_simplejwt==5.5.1`.
- **Static Assets & Serving:** `whitenoise==6.9.0`.
- **Admin & UI:** `django-jazzmin==3.0.5`.
- **Media & Documents:** `pillow==12.3.0`, `openpyxl==3.1.5`, `reportlab==5.0.1`.
- **WSGI Server:** `gunicorn==23.0.0`.
- **Environment & Utilities:** `python-dotenv==1.2.3`, `sqlparse==0.5.5`, `asgiref==3.12.1`.

### 2.4 Django Settings (`config/settings.py` & `config/settings.postgresql.py`)
- **Duplication Bug:** `JAZZMIN_SETTINGS` dictionary is defined twice in `config/settings.py` (lines 155–276 and repeated lines 278–399).
- **Stray Imports:** `from pickle import TRUE` is present at line 3 of `config/settings.py` and `settings.postgresql.py`.
- **Static Files Configuration:**
  - `STATIC_URL = '/static/'`
  - `STATIC_ROOT = BASE_DIR / 'staticfiles'`
  - **Missing:** `STATICFILES_DIRS` is completely absent from `settings.py`. Global project-wide static directories (`static/`) are ignored by `collectstatic`.
  - Storage is set to `whitenoise.storage.CompressedManifestStaticFilesStorage`. In production, if referenced assets (e.g. `content/admin_theme.css` in Jazzmin) are unhashed or missing from the manifest, 500/404 errors occur.
- **Media Files Configuration:**
  - `MEDIA_URL = '/media/'`
  - `MEDIA_ROOT = BASE_DIR / 'media'`
  - **Defect:** In `config/urls.py`, media serving is only appended `if settings.DEBUG:`. On HostPinnacle cPanel with `DEBUG=False`, Django provides zero URL route for media files, resulting in 404 for all uploaded media unless Apache alias is mapped manually.
- **Allowed Hosts:** Hardcoded to `['localhost', '127.0.0.1', 'wrongness-prude-calzone.ngrok-free.dev', '[::1]']` when `ALLOWED_HOSTS` environment variable is not supplied.
- **SSL Redirects:** `SECURE_SSL_REDIRECT = True` triggers when `DEBUG=False`. When test environments run with `DEBUG != 'True'`, tests fail due to 301 redirect assertions.
- **Template Engine:** Configured with `APP_DIRS: True` and `DIRS: [BASE_DIR / 'templates']`. Context processors include `django.template.context_processors.request`, `django.contrib.auth.context_processors.auth`, `django.contrib.messages.context_processors.messages`, and `config.context_processors.admin_dashboard`.

### 2.5 Main URL Configuration (`config/urls.py` & `config/api_urls.py`)
- **Root Route Defect:** `path('', RedirectView.as_view(url=frontend_url, permanent=False))` redirects users to `http://localhost:5173` (the external Vite dev server).
- **Root 404 Defect:** There are NO public views mapped to `/courses`, `/about`, `/contact`, `/admissions`, etc. Only `api/v1/courses/`, `api/v1/admissions/` exist. Navigating directly to `/courses` on the Django server returned HTTP 404.
- **Admin Route:** Mapped to `/admin/`.
- **API Routes:** Routed through `/api/v1/` to sub-applications.

### 2.6 Existing Applications
1. **`accounts`:** User registration and user listing API endpoints using standard Django `auth.User`. No custom models.
2. **`admissions`:** Model `Admission`, serializers, views, and an extensive custom Jazzmin export dashboard (PDF via ReportLab, Excel via OpenPyXL, CSV).
3. **`contacts`:** Models `ContactMessage` and `DepartmentContact`, contact message submission and admin views.
4. **`content`:** Models `Announcement`, `StaffMember`, `EventItem`, `Testimonial`, `GalleryItem`, and `HeroCarouselItem`. Custom Jazzmin widgets, multiple image upload, TinyMCE support.
5. **`courses`:** Models `Department` and `Course`, DRF API endpoints and admin definitions.
6. **`news`:** Model `NewsArticle` with slug, summary, content, publication flag, and image.

### 2.7 Models Audit
- **`admissions.Admission`:** `first_name`, `last_name`, `email`, `phone`, `course` (FK), `applied_at`, `status` ('pending', 'accepted', 'rejected'), `message`.
- **`contacts.ContactMessage`:** `name`, `email`, `phone`, `subject`, `message`, `status` (default 'new'), `created_at`.
- **`contacts.DepartmentContact`:** `department`, `phone`, `email`, `address`, `updated_at`.
- **`content.Announcement`:** `title`, `message`, `link`, `phone`, `email`, `is_active`, `starts_at`, `ends_at`, `order`, `created_at`, `updated_at`.
- **`content.StaffMember`:** `name`, `role`, `department`, `bio`, `image`, `email`, `phone`, `is_active`, `display_order`, `created_at`, `updated_at`.
- **`content.EventItem`:** `title`, `description`, `location`, `starts_at`, `ends_at`, `image`, `is_featured`, `is_active`, `created_at`, `updated_at`.
- **`content.Testimonial`:** `author`, `role`, `quote`, `image`, `is_featured`, `is_active`, `order`, `created_at`.
- **`content.GalleryItem`:** `title`, `image`, `caption`, `alt_text`, `category`, `is_active`, `order`, `created_at`, `updated_at`.
- **`content.HeroCarouselItem`:** `title`, `subtitle`, `image`, `button_text`, `button_link`, `is_active`, `order`, `created_at`, `updated_at`.
- **`courses.Department`:** `name`, `description`, `requirements`, `image`, `duration_months`, `created_at`, `updated_at`.
- **`courses.Course`:** `title`, `slug`, `department` (FK), `description`, `duration_months`, `duration_weeks`, `credits`, `is_active`, `created_at`.
- **`news.NewsArticle`:** `title`, `slug`, `summary`, `content`, `image`, `author`, `published_at`, `updated_at`, `is_published`.

### 2.8 Views Audit
- Current views in `courses`, `admissions`, `contacts`, `content`, and `news` are almost exclusively Django REST Framework `ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`, and `ModelViewSet`.
- **Public Django Template Views are absent.** All rendering was previously offloaded to the React frontend.

### 2.9 Forms Audit
- Only admin forms existed:
  - `content.admin.GalleryItemForm` (with `MultipleImageField`).
  - Standard ModelAdmin generated forms.
- Public customer-facing Django forms (`AdmissionForm`, `ContactForm`, `EventRegistrationForm`) must be built.

### 2.10 Serializers & API Endpoints
- Existing DRF serializers exist for all models in `api_urls.py`.
- **Bug Detected:** In `contacts/serializers.py`, `DepartmentContactSerializer` defines `fields = ['id', 'department', 'phone', 'email', 'address', 'status', 'updated_at']`. However, `DepartmentContact` model does NOT have a `status` field, causing an immediate runtime error if accessed.

### 2.11 Templates Audit
- Only two custom templates existed:
  - `templates/admin/index.html`: Custom Jazzmin dashboard overview containing trend bar charts, calendar widget, analytics counters, and export buttons.
  - `templates/admin/login.html`: Branded admin login screen.
- Public web templates (`base.html`, `home.html`, `about.html`, `courses.html`, `course_detail.html`, `admissions.html`, `news.html`, etc.) are entirely missing.

### 2.12 Static Files Audit
- `staticfiles/` contains collected static assets from previous builds (Jazzmin, AdminLTE, FontAwesome, Bootstrap bootswatch themes).
- App static files only existed in `content/static/content/` (`admin_theme.css`, `gallery_upload.js`, `ptvti-logo.jpg`, `rich_text.js`).
- No public branding CSS/JS was present in Django.

### 2.13 Media Configuration Audit
- Real institutional media files exist on disk in `media/`:
  - `media/departments/software.webp`
  - `media/events/` (9 high-resolution workshop & institutional photos)
  - `media/gallery/` (6 institutional photos)
  - `media/hero-carousel/` (12 workshop and student photos)
  - `media/staff/` (7 faculty photos)
- These verified media files must be preserved and used directly in the Django template views.

### 2.14 Authentication Implementation
- Standard `django.contrib.auth` with session authentication for admin and JWT authentication (`rest_framework_simplejwt`) for API.
- Standard `User` model; no custom user model has been activated in `AUTH_USER_MODEL`.

### 2.15 Roles & Permissions
- Standard Django `is_staff` and `is_superuser`.
- No granular role-based dashboard for Admissions Officers, Editors, or Students yet existed.

### 2.16 PostgreSQL Configuration
- Configured via `dj_database_url.parse(os.environ.get('DATABASE_URL'))`.
- Uses `psycopg` (v3). Fallback to local SQLite when `DATABASE_URL` is omitted.
- Fully compatible with HostPinnacle PostgreSQL and local development.

### 2.17 Migrations Audit
- All migration graphs are intact:
  - `admissions`: 0001
  - `contacts`: 0001, 0002
  - `content`: 0001, 0002, 0003
  - `courses`: 0001, 0002, 0003, 0004
  - `news`: 0001, 0002, 0003
- Migrations apply cleanly to both SQLite and PostgreSQL.

### 2.18 Deployment & WSGI Configuration
- `config/wsgi.py` exposes standard `application = get_wsgi_application()`.
- Production requires compatibility with HostPinnacle cPanel (Python Passenger / WSGI).
- Static assets must be served via WhiteNoise with properly configured `STATICFILES_DIRS`.

### 2.19 Tests Audit
- Found 9 test cases in `config/tests.py`, `content/tests.py`, and `contacts/tests.py`.
- **Failures Identified:**
  1. `contacts/tests.py` attempted `from backend import content` (ModuleNotFoundError).
  2. `contacts/tests.py` duplicated content tests instead of testing contact messages.
  3. `content/tests.py` failed with `301 != 200` because `SECURE_SSL_REDIRECT = True` was active under `DEBUG=False` without HTTPS request headers.

### 2.20 Environment Variables
Configured via `.env`:
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DATABASE_URL`
- `CORS_ALLOWED_ORIGINS`
- `CSRF_TRUSTED_ORIGINS`
- `FRONTEND_URL`

---

## 3. Investigation of Previously Reported Issues

| Issue Reported | Root Cause Found | Solution / Fix |
|---|---|---|
| **`/courses` page returned 404** | Django `config/urls.py` had no public URL route for `/courses`. Only `/api/v1/courses/` existed, and the root URL redirected to an external Vite frontend. | Add Django template route `path('courses/', ...)` with view and template. |
| **Static files returned 404 after `collectstatic`** | `STATICFILES_DIRS` was not defined in `settings.py`. WhiteNoise was configured with `CompressedManifestStaticFilesStorage`, which fails when unhashed or external assets are referenced. | Configure `STATICFILES_DIRS = [BASE_DIR / 'static']`, ensure WhiteNoise serves static files safely. |
| **Uploaded images failed to display** | In `config/urls.py`, `urlpatterns += static(settings.MEDIA_URL, ...)` was only included when `DEBUG=True`. In production `DEBUG=False`, Django had no media handler and cPanel had no media alias. | Implement media URL serving route in development and document/configure `.htaccess` / `whitenoise`/django-media serving for cPanel. |
| **Admin styling differed in production** | Jazzmin's `custom_css` (`content/admin_theme.css`) and logo were referenced with paths that WhiteNoise manifest storage failed to resolve or that Apache bypassed. | Fix static asset declaration, ensure static collection includes all admin theme overrides. |

---

## 4. Architectural Target & Stack Confirmation

- **Backend:** Python + Django 6 + Django ORM + Django Auth.
- **Frontend Architecture:** 100% Server-side Django Templates (NO React, Vite, Vue, Next.js or Node build pipelines).
- **Styling:** Bootstrap 5 (served locally from static assets) + custom modern CSS design system.
- **Interactivity:** Clean, robust vanilla JavaScript (AJAX filters, animated stats counters, modal preview, application tracker).
- **Database:** PostgreSQL on HostPinnacle cPanel (with seamless SQLite fallback for local test execution).
- **Brand Aesthetic:** Professional, premium technical institute identity inspired by modern civic platforms (Navy `#181D2E`, Forest Green `#3C453E`, Warm Gold `#D6AE69`, Background `#F7F8F6`).

---
