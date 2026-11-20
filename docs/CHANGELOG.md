# PTVTI REBRANDING & MODERNIZATION CHANGELOG

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
