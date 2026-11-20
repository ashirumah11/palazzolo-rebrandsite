# PTVTI REBRANDING & MODERNIZATION CHANGELOG

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
