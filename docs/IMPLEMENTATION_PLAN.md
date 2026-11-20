# PTVTI DIGITAL TRANSFORMATION: IMPLEMENTATION PLAN

**Target Institution:** Palazzolo Technical and Vocational Training Institute (PTVTI)  
**Target URL:** [https://palazzolotechnical.co.ke/](https://palazzolotechnical.co.ke/)  
**Version:** 2.0  
**Status:** Approved for Implementation  

---

## 1. Implementation Principles

1. **Preserve and Upgrade:** Build upon existing models, database relationships, and admin customizations. Do not discard working functionality.
2. **Zero Node/Frontend Bundler Dependency:** Complete HTML rendering via Django templates with reusable template tags, context processors, Bootstrap 5, and vanilla JavaScript.
3. **Institutional Authenticity:** Preserve official PTVTI branding, history (Poverelle Sisters, founded 2021), TVETA accreditation, NITA/UNESCO affiliations, and authentic photos from `media/` and frontend assets.
4. **Resilient Production Deployment:** Engineered specifically for HostPinnacle cPanel Python WSGI environment.

---

## 2. Phased Roadmap & Acceptance Criteria

### Phase 0: Codebase Audit & Technical Documentation *(Completed)*
- **Objective:** Complete 20-point audit, diagnose 404 and static issues, inventory models and migrations.
- **Deliverables:** `docs/PROJECT_AUDIT.md`, `docs/IMPLEMENTATION_PLAN.md`.
- **Status:** Complete.

---

### Phase 1: Database Protection & Architecture Preparation
- **Objective:** Fix settings bugs, configure static/media directories safely, eliminate import errors and test failures, and safeguard database models.
- **Key Tasks:**
  1. Clean `config/settings.py`:
     - Remove duplicate `JAZZMIN_SETTINGS` block.
     - Remove stray `from pickle import TRUE`.
     - Add `STATICFILES_DIRS = [BASE_DIR / 'static']`.
     - Configure safe static storage fallback (`WhiteNoise`).
     - Configure development and production media serving routes.
  2. Fix `contacts/serializers.py` (remove nonexistent `status` field on `DepartmentContactSerializer`).
  3. Fix `contacts/tests.py` and `content/tests.py` (resolve import error and trailing slash assertions).
  4. Test local migrations against SQLite and ensure compatibility with PostgreSQL.
- **Acceptance Criteria:** `python manage.py check` and existing tests pass with 0 errors.

---

### Phase 2: Brand Design System & Reusable Django Templates
- **Objective:** Implement a bespoke, modern PTVTI visual identity system inspired by modern civic platforms.
- **Key Tasks:**
  1. Create modular CSS architecture in `static/css/`:
     - `variables.css` (Colors: Navy `#181D2E`, Forest Green `#3C453E`, Gold `#D6AE69`, Background `#F7F8F6`, Typography: Inter & Poppins).
     - `base.css` (Typography, utilities, layout grids, buttons, badges, alerts).
     - `navigation.css` (Announcement top-bar, sticky brand navbar, mobile drawer).
     - `components.css` (Cards, stats counters, modals, tabs, forms).
     - `footer.css` (Institutional footer with contact details, accreditation logos).
  2. Create modular Vanilla JS in `static/js/`:
     - `main.js` (Mobile menu, sticky header, scroll to top).
     - `counters.js` (Lightweight count-up animation for verified statistics).
     - `filters.js` (Instant client-side course and category filtering).
  3. Create base template hierarchy in `templates/`:
     - `base.html` (Master layout, meta tags, responsive viewport, asset links).
     - `includes/navbar.html`
     - `includes/footer.html`
     - `includes/messages.html`
- **Acceptance Criteria:** Base templates render cleanly with responsive layout and 0 console errors.

---

### Phase 3: Public Website Redesign
- **Objective:** Deliver visually engaging, content-rich public institutional pages.
- **Key Pages:**
  1. **Homepage (`templates/pages/home.html`):**
     - Hero carousel (driven by `HeroCarouselItem` model with fallback).
     - Institutional announcement banner (`Announcement`).
     - "Why Choose Palazzolo" value pillars.
     - Dynamic courses & departments showcase (`Department`, `Course`).
     - Verified institutional statistics counter (150+ Graduates, 250+ Students, TVETA Accredited).
     - Campus gallery preview (`GalleryItem`).
     - Latest news & announcements (`NewsArticle`).
     - Upcoming workshops and events (`EventItem`).
     - Student testimonials slider (`Testimonial`).
     - Accreditation badges (TVETA Kenya, NITA, UNESCO).
     - Admissions CTA & contact info.
  2. **About PTVTI (`templates/pages/about.html`):**
     - History of PTVTI & Poverelle Sisters.
     - Vision, Mission & Core Values (Respect, Integrity, Dignity, Excellence, Collaboration).
     - Campus facilities & infrastructure (Workshops, ICT Labs, Training Kitchen, Salon & Barber Studio, Fashion Studio).
     - Leadership & faculty (`StaffMember`).
     - Accreditation & partner certifications.
  3. **Contact & Location (`templates/pages/contact.html`):**
     - Contact details (Kiambu County, Gachie-Kihara-Karura Road).
     - Functional contact submission form (`ContactMessage`).
     - Department direct contact phone/email directory (`DepartmentContact`).
     - Interactive campus map & directions.
- **Acceptance Criteria:** Homepage, About, and Contact pages render dynamically with verified data from database models.

---

### Phase 4: Courses & Admissions Improvements
- **Objective:** Transform course browsing and student applications into a seamless, modern experience.
- **Key Tasks:**
  1. **Courses Directory (`templates/courses/course_list.html`):**
     - Department category tabs and search filter.
     - Modern cards with duration, level, credits, department badge, and action buttons.
  2. **Course Detail Page (`templates/courses/course_detail.html`):**
     - Comprehensive overview, entry requirements, career outcomes, duration.
     - Direct "Apply for this Course" trigger linking directly into admissions.
  3. **Online Student Admission System (`admissions/`):**
     - Public admission form (`templates/admissions/apply.html`).
     - Capture personal details, contact info, selected course, academic qualifications, and statement.
     - Generate unique application tracking reference (e.g. `PTVTI-2026-XXXX`).
     - Application tracking portal (`templates/admissions/track.html`): Applicants enter email + reference to check live status (Pending, Under Review, Accepted, Rejected).
     - Admissions staff dashboard integration for updating status.
- **Acceptance Criteria:** Prospective students can browse courses, inspect details, apply online, and track status with a unique reference number.

---

### Phase 5: News, Community & Events
- **Objective:** Build an engaging institutional feed and event management workflow.
- **Key Tasks:**
  1. **News & Stories Feed (`templates/news/news_list.html` & `news_detail.html`):**
     - Featured articles, pagination, category filtering, search.
     - Clean typography, social share links, related articles.
  2. **Events Hub (`templates/content/event_list.html` & `event_detail.html`):**
     - Upcoming vs. past events filter.
     - Event registration modal / form with capacity limit and confirmation.
     - Prevention of duplicate registrations.
- **Acceptance Criteria:** Public visitors can read articles and register for events. Administrators can publish posts and view attendee rosters.

---

### Phase 6: Student Projects & Vocational Marketplace
- **Objective:** Showcase student practical innovations and institutional products.
- **Key Tasks:**
  1. **Student Projects Showcase:**
     - Data model for student innovations (title, description, department, team attribution, image, demonstrated skills).
     - Clean gallery view (`templates/community/projects.html`).
  2. **Institutional Marketplace:**
     - Showcase products crafted by vocational departments (garments, bakery products, electrical installations, craft goods).
     - Product detail card with specifications and "Order / Enquiry" modal (no financial checkout in v1).
- **Acceptance Criteria:** Projects and marketplace items are browsable with enquiry submissions stored for administrative follow-up.

---

### Phase 7: Custom Management Dashboard & Roles
- **Objective:** Provide staff and administrators with a dedicated, role-aware dashboard consistent with the PTVTI brand.
- **Key Tasks:**
  1. Build a custom management portal (`/portal/` or `/dashboard/`) accessible by staff roles:
     - Admissions management table with status toggling, search, filtering.
     - Application export (PDF, Excel, CSV) leveraging existing report generators.
     - Support ticket / contact message response management.
     - Event registrations review.
  2. Retain Jazzmin admin (`/admin/`) for superusers and technical operations.
- **Acceptance Criteria:** Authorized staff can log in, inspect metrics, review applications, and update records without entering raw database tooling.

---

### Phase 8: Email Notifications & Search
- **Objective:** Automated email communications and global search capabilities.
- **Key Tasks:**
  1. Implement HTML email templates for:
     - Admission application received (with tracking reference).
     - Admission status change (Accepted / Interview).
     - Contact enquiry confirmation.
     - Event registration confirmation.
  2. Implement global search route across Courses, News, and Events.
- **Acceptance Criteria:** Notifications trigger reliably via Django SMTP backend (Console in development, SMTP in production).

---

### Phase 9: Security, SEO, Performance & Testing
- **Objective:** Harden security, optimize assets, implement SEO metadata, and expand automated test suite.
- **Key Tasks:**
  1. Security: CSRF protection on all forms, file upload sanitization, SQL injection prevention, clickjacking headers.
  2. SEO: Dynamic `sitemap.xml`, `robots.txt`, Open Graph social metadata, structured schema markup for educational institutions.
  3. Performance: Image optimization, lazy loading, database query optimization (`select_related`, `prefetch_related`).
  4. Comprehensive testing: Unit and integration tests covering public pages, admissions workflow, course filtering, contact form, and exports.
- **Acceptance Criteria:** Test suite runs with 100% pass rate; Lighthouse accessibility and SEO audit scores above 90.

---

### Phase 10: Production Deployment Preparation (HostPinnacle cPanel)
- **Objective:** Provide turn-key deployment configuration and documentation for HostPinnacle cPanel.
- **Key Tasks:**
  1. Create `.htaccess` configuration for cPanel Apache + Passenger.
  2. Verify `STATIC_ROOT` collectstatic output and WhiteNoise settings.
  3. Provide comprehensive `docs/DEPLOYMENT_GUIDE.md` with environment variable templates and PostgreSQL migration steps.
- **Acceptance Criteria:** Verified deployment bundle ready for cPanel upload with zero manual code fixes required on the server.
