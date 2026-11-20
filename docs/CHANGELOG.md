# PTVTI REBRANDING & MODERNIZATION CHANGELOG

## [Phase 5: News, Community & Events] - 2026-11-20

### Added
- **News & Stories Feed** (`news/views.py`, `templates/news/news_list.html`, `templates/news/news_detail.html`):
  - Public news listing with full-text search across title, summary, and content.
  - Category filtering (Announcements, Events, Achievements).
  - Pagination (9 articles per page) with accessible navigation.
  - Article detail pages with related articles sidebar (4 most recent).
  - Social sharing links (Facebook, Twitter, LinkedIn, Email).
  - Responsive card grid using PTVTI design system (`ptvti-card`, `ptvti-section`).
- **Events Hub** (`content/views.py`, `templates/content/event_list.html`, `templates/content/event_detail.html`):
  - Upcoming vs. Past filter with clean toggle UI.
  - Event cards showing date, time, location, and registration count.
  - Event detail pages with full description and metadata.
  - Public registration form (`EventRegistrationForm`) with name, email, phone fields.
  - Duplicate prevention via unique constraint on (event, email) with user-friendly error message.
  - Flash messages for registration success and duplicate detection.
  - Social sharing and "Back to Events" navigation.
- **Models & Admin**:
  - `EventRegistration` model with unique_together constraint on (event, email).
  - `EventRegistrationAdmin` with list display, search, and date hierarchy.
  - `EventRegistrationSerializer` for DRF API access.
  - `EventRegistrationViewSet` for API CRUD operations.
- **Tests** (`content/tests.py`):
  - 6 new test cases covering news list, news detail, event list, event detail, registration success, and duplicate prevention.
  - All 27 tests passing.

### Fixed
- **Clean Events CSS Architecture:** Extracted event-specific styles into a dedicated `static/css/events.css` (`event-hero`, `event-meta-strip`, `event-meta-pill`, `event-sidebar-card`, `event-card`, `event-date-badge`, `event-title`, `sidebar-guidance-card`). Event templates now use event-specific classes instead of borrowing course classes (`course-detail-hero`, `course-meta-strip`, `course-meta-pill`), eliminating the layout overlay coupling smell.
- **Home "Need Guidance?" Card Visibility:** Replaced low-contrast `text-muted` body copy with `var(--ptvti-text-body)` and gave the card a white surface, strong border, gold left accent bar, and forced navy heading for legibility.
- **Home Event Card Navigation:** Event cards now link to their individual detail page (`{% url 'event_detail' event.pk %}`) instead of the hub.
- **News CSS Architecture:** Created dedicated `static/css/news.css` with `news-hero`, `news-meta-strip`, `news-meta-pill`, `news-content`, `related-articles-card`, and `news-social-share` classes. Refactored `news_list.html` and `news_detail.html` to use news-specific hero and meta classes instead of course borrowings.
- **Static Files Collection:** Verified `events.css` and `news.css` are collected into `staticfiles/` via `python manage.py collectstatic --noinput`.
- **Cache-Busting:** All 12 local CSS links in `base.html` include `?v=5` query parameter to prevent stale browser cache.

## [Phase 4: Courses & Admissions Improvements] - 2026-11-20

### Added
- Courses directory (`templates/courses/course_list.html`) with department tabs and search filter.
- Course detail page (`templates/courses/course_detail.html`) with entry requirements, career outcomes and Apply CTA.
- Public admission form (`templates/admissions/apply.html`) with unique tracking reference generation.
- Application tracking portal (`templates/admissions/track.html`).
- Tests for courses and admissions views.

## [Phase 3: Public Core Pages & Dynamic Seed Data] - 2026-11-20

### Added
- **Institutional Management Command:**
  - `content/management/commands/seed_ptvti_data.py`: Idempotent data seeder populating authentic PTVTI records without altering existing primary keys:
    - 5 Official TVET Departments (Engineering, ICT, Fashion & Design, Cosmetology & Hairdressing, Hospitality).
    - 12 Verified Artisan, Certificate, and Diploma Courses with authentic durations, exam bodies (CDACC, KNEC, NITA), and entry criteria.
    - 3 Hero Carousel Slides with verified institutional imagery and actionable CTAs.
    - Active Admissions Announcement Banner.
    - 6 Leadership & Academic Staff Profiles.
    - Authentic Student and Alumnus Testimonials.
    - Upcoming Institutional Events and News Items.
    - Official Departmental Contact directory.
- **Dynamic Public Views & Templates:**
  - `templates/pages/home.html` & `content/views.py:home_view`:
    - Dynamic Hero Banner with slide transitions.
    - "Why Choose Palazzolo" institutional value propositions.
    - Verified Interactive Stats Counter grid (1,200+ Trained, 85% Employment, 15+ Accredited Courses).
    - Department & Featured Programme Cards with category pills and direct links.
    - Campus Experience & Workshop Facilities showcase.
    - Student Innovation & Testimonial Carousel.
    - Latest Institutional News & Upcoming Events grid.
    - Accreditation logo band (TVETA, NITA, CDACC, UNESCO-UNEVOC).
    - Prominent Application CTA.
  - `templates/pages/about.html` & `content/views.py:about_view`:
    - Full institutional history (founded November 2021 by the Poverelle Sisters in Kiambu County in response to COVID-19 youth empowerment needs).
    - Institutional Motto (*"With God at the Centre, we serve, train and transform"*), Mission, Vision, and Core Values.
    - Leadership & Department Heads directory.
    - Practical campus workshop and facility highlights.
  - `templates/pages/contact.html`, `contacts/forms.py:ContactForm`, & `contacts/views.py:contact_view`:
    - Interactive inquiry form with anti-duplicate submission safeguards.
    - Auto-generation of unique tracking inquiry reference codes (`PTVTI-MSG-XXXX`).
    - Departmental phone, email, and campus location directory.
    - Google Maps interactive campus location embed (Kihara-Gachie-Karura Road, Kiambu).
- **Automated Test Coverage:**
  - Added `content/tests.py:PublicPagesViewTests` covering `/`, `/about/`, and `/contact/` (GET and POST inquiry submissions).
  - All 17 automated tests passing (`Ran 17 tests in 18.673s OK`).

## [Phase 2: Brand Design System & Reusable Django Templates] - 2026-11-20

### Added
- **Design System CSS Architecture:**
  - `static/css/variables.css`: Defined official institutional color tokens (Navy `#181D2E`, Forest Green `#3C453E`, Gold `#D6AE69`, Background `#F7F8F6`, Typography: Inter & Poppins, spacing scale, shadows, radius, and transitions).
  - `static/css/base.css`: Global typography scale, buttons (`btn-ptvti-primary`, `btn-ptvti-gold`, `btn-ptvti-outline`), badges, section containers, and scroll-to-top button.
  - `static/css/navigation.css`: Top announcement strip, brand navbar with logo presentation, dropdown menus, and mobile toggler.
  - `static/css/components.css`: Modern card designs with media aspect ratio, floating badges, stats counter widget, forms, and alert banners.
  - `static/css/homepage.css`: Hero carousel presentation, "Why Choose" cards, split section layouts, stats grid banner, and accreditation logo band.
  - `static/css/courses.css`: Category filter pills, search input, and course detail layout.
  - `static/css/admissions.css`: 4-step admission wizard, application form card, and timeline status tracker.
  - `static/css/dashboard.css`: Staff management portal layout, KPI summary cards, and clean data tables.
  - `static/css/footer.css`: Institutional footer with brand motto, accreditation badges, and contact directory.
  - `static/css/responsive.css`: Breakpoints for desktop, tablet, and mobile views.
- **Modular Vanilla JavaScript Utilities:**
  - `static/js/main.js`: Sticky navbar scroll handling, scroll-to-top trigger, auto-dismissing flash alerts.
  - `static/js/navigation.js`: Active menu item highlighting based on current path, accessible keyboard closing (Escape).
  - `static/js/counters.js`: Smooth IntersectionObserver count-up animation for verified institutional metrics.
  - `static/js/filters.js`: Instant client-side course / category filtering without full page reloads.
  - `static/js/forms.js`: File upload size validation (5MB max) and duplicate submission prevention with button spinner.
  - `static/js/interactions.js`: Copy-to-clipboard controller for application tracking references.
- **Global Context Processor:**
  - `config.context_processors.ptvti_public_context`: Automatically injects active institutional announcements, department taxonomy, brand identity, and verified stats into all public templates.
- **Template Inheritance & Component Partials:**
  - `templates/base.html`: Master HTML5 layout with SEO meta tags, Open Graph cards, Google Fonts, Bootstrap 5.3.3, and FontAwesome 6.
  - `templates/includes/announcement_bar.html`: Dynamic announcement banner with fallback.
  - `templates/includes/navbar.html`: Sticky navigation bar with official logo, course dropdown, and CTA.
  - `templates/includes/footer.html`: Full institutional footer with history and contact info.
  - `templates/includes/messages.html`: Dismissible Bootstrap 5 flash alert cards.
- **Testing:**
  - Added `BaseTemplateRenderingTests` in `config/tests.py`, confirming clean template compilation, context processor binding, and brand asset inclusion (13/13 passing tests).

---

## [Phase 1: Architecture Stabilization & Settings Cleanup] - 2026-11-20

### Fixed
- **Settings Duplication:** Eliminated redundant duplicate `JAZZMIN_SETTINGS` dictionary block from `config/settings.py`.
- **Stray Imports:** Removed `from pickle import TRUE` from `config/settings.py` and `config/settings.postgresql.py`.
- **WhiteNoise Static Serving:** Added `STATICFILES_DIRS = [BASE_DIR / 'static']` and switched storage backend to `whitenoise.storage.CompressedStaticFilesStorage`, preventing manifest lookup crashes on dynamic/admin static references.
- **Media Delivery Resilience:** Configured media URL routes with `django.views.static.serve` in `config/urls.py` to prevent 404s for uploaded media files.
- **Host & Test Server Resolution:** Added `'testserver'`, `'palazzolotechnical.co.ke'`, and `'www.palazzolotechnical.co.ke'` to `ALLOWED_HOSTS`.
- **SSL Redirects:** Controlled `SECURE_SSL_REDIRECT` with `ENABLE_SSL_REDIRECT` environment variable to prevent HTTPS redirection failures during local development and testing.
- **Serializer Crash in Contacts:** Removed nonexistent `status` field from `DepartmentContactSerializer.Meta.fields`.
- **Test Failures:** Replaced corrupted `contacts/tests.py` with valid unit tests; resolved trailing-slash and SSL redirect issues across `content/tests.py` and `config/tests.py`.

### Verified
- `python manage.py check`: 0 errors.
- `python manage.py makemigrations --check`: No unmigrated changes.
- `python manage.py test`: 12/12 tests passing (100% OK).
- `python manage.py collectstatic --noinput`: Cleanly copied and post-processed 130+ static files.
