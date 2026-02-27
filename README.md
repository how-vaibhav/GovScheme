# GovAid - Government Schemes Portal

GovAid is a Django-based citizen services platform for discovering, comparing, and applying to government welfare schemes. It includes profile-driven eligibility checks, scheme recommendations, application workflows, feedback handling, and role-based operations for citizens, employees, and administrators.

## Why this project

- Centralizes scheme discovery and filtering in one portal.
- Matches users to schemes using profile attributes (age range, income, caste, location, BPL, disability, minority, etc.).
- Supports end-to-end application flow with encrypted Aadhaar storage.
- Provides operational tools for employees (feedback reply + application status decisions).
- Offers user engagement features (favorites, comparison, notification center, advanced search).

## Feature overview

### Citizen features

- Authentication (register/login/logout).
- Profile capture and editing (`UserDetails`).
- Scheme browsing and detail pages.
- Eligibility checks (single-scheme and all-schemes).
- Scheme application submission.
- Favorites/bookmarks.
- Side-by-side scheme comparison.
- Advanced multi-filter search.
- Notification center and mark-as-read.
- Feedback submission.

### Employee features

- Respond to user feedback.
- View applications and update status (`pending`, `accepted`, `rejected`).

### Admin features

- Django admin management.
- Employee group assignment via custom UI (`addemployee/`).
- Scheme creation and lifecycle management.

## Technical stack (detailed)

| Layer         | Technology                    | Version / Notes        | Purpose                                            |
| ------------- | ----------------------------- | ---------------------- | -------------------------------------------------- |
| Runtime       | Python                        | 3.12+ (Pipfile)        | Core backend runtime                               |
| Web framework | Django                        | 5.2.1                  | MVC-ish server rendering, ORM, auth, admin         |
| Database      | SQLite                        | Default (`db.sqlite3`) | Local persistence for users, schemes, applications |
| Styling       | Tailwind CSS                  | 3.4.1                  | Utility-first styling pipeline                     |
| Frontend      | Django Templates + Vanilla JS | Server-first UI        | Fast pages without SPA complexity                  |
| Config        | python-decouple               | 3.8                    | Environment-driven settings (`.env`)               |
| Crypto        | cryptography (Fernet)         | 45.0.2                 | Aadhaar encryption at model layer                  |
| HTTP clients  | requests                      | 2.32.3                 | Integration calls (translation, utility endpoints) |
| HTML parsing  | beautifulsoup4 + lxml         | 4.13.4 / 5.4.0         | Data scraping and parsing utilities                |
| Build tooling | npm + Tailwind CLI            | package scripts        | CSS build/watch pipeline                           |

### Dependency profile

- **Core backend**: `Django`, `asgiref`, `sqlparse`, `tzdata`.
- **Security + config**: `cryptography`, `cffi`, `python-decouple`.
- **Data ingestion/integration**: `requests`, `beautifulsoup4`, `lxml`.
- **Frontend pipeline**: `tailwindcss` via `build:css` and `watch:css` scripts.

### Compatibility notes

- `requirements.txt` pins Django ecosystem and supporting libs for reproducibility.
- `Pipfile` targets Python `3.12`; align your local interpreter with this for least friction.
- SQLite is ideal for local/dev; for production scale, migrate to Postgres/MySQL.

## Engineering architecture

### Service boundaries

- **Web App Service (Django, port 8000)**
  - Handles auth, profile management, scheme catalog, application workflows, and notifications.
- **Translation/Bot Side Services (external ports 5000/5055/5005 depending on script)**
  - Used by helper integration flows (`translate_page`, startup scripts, Rasa command wrappers).

### Application modules

- **Domain models**: `UserDetails`, `Scheme`, `Application`, `Notification`, `Feedback`, `Favorite`, `ApplicationTimeline`.
- **Business logic**: eligibility checks in `Scheme.is_user_eligible`, recommendation scoring in views.
- **Security logic**: Verhoeff checksum validation + Fernet encryption/decryption for Aadhaar.
- **Eventing**: `post_save` signal on `Scheme` to fan out user notifications.

### Request lifecycle (example: apply to scheme)

1. Authenticated user submits Aadhaar + scheme selection on `/apply/`.
2. Aadhaar is validated using Verhoeff checksum.
3. Value is encrypted through `Application.sensitive_data` setter.
4. Application row is persisted with `pending` status.
5. Session stores masked Aadhaar for success confirmation page.
6. Employee later accepts/rejects from `/applications/`, triggering notification creation.

## Data model snapshot

| Entity                | Key fields                                | Core relationships                                |
| --------------------- | ----------------------------------------- | ------------------------------------------------- |
| `UserDetails`         | demographics, socioeconomic fields        | One-to-one with `User`                            |
| `Scheme`              | benefit metadata + eligibility criteria   | Referenced by applications/feedback/notifications |
| `Application`         | encrypted Aadhaar + status + timestamps   | Many-to-one to `User` and `Scheme`                |
| `Notification`        | message, read state, optional scheme link | Many-to-one to `User`                             |
| `Feedback`            | message + optional employee reply         | Linked to `User` and optional `Scheme`            |
| `Favorite`            | user-scheme bookmark                      | Unique pair (`user`, `scheme`)                    |
| `ApplicationTimeline` | status events and timestamps              | Many-to-one to `Application`                      |

## Repository layout

```text
GovScheme/
├── gov_schemes/                       # Project config (settings, urls, wsgi/asgi)
├── schemesapp/
│   ├── management/commands/           # Data import, seed, utility commands
│   ├── migrations/
│   ├── templates/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── schemes_data/                      # CSV dataset(s)
├── static/                            # Source static files (input/output CSS, JS, images)
├── staticfiles/                       # collectstatic output
├── templates/                         # Global templates (base layouts)
├── manage.py
├── requirements.txt
├── package.json
├── run_all_servers.py
└── START_SERVERS.bat
```

## Architecture at a glance

1. **User profile as eligibility anchor**
   - `UserDetails` stores user attributes used for matching.
2. **Eligibility engine on `Scheme` model**
   - `Scheme.is_user_eligible(details)` applies criteria checks.
3. **Recommendation layer in views**
   - `get_smart_recommendations(user)` computes simple score-based top matches.
4. **Event-driven notifications**
   - `post_save` signal on `Scheme` creates per-user notifications.
5. **Application workflow**
   - Aadhaar is validated (Verhoeff), encrypted, and status-managed by employees.

## Environment configuration

This project expects a `.env` file (loaded via `python-decouple`) with at least:

```env
SECRET_KEY=replace-with-django-secret
FIELD_ENCRYPTION_KEY=replace-with-fernet-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Optional production hardening values
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False
```

### Generate `FIELD_ENCRYPTION_KEY`

Run once and copy output into `.env`:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## Local setup (recommended)

### 1) Clone and enter project

```bash
git clone <your-repository-url>
cd GovScheme
```

### 2) Create virtual environment

```bash
python -m venv .venv
```

Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
npm install
```

### 4) Configure environment variables

- Create `.env` in project root using the values shown above.

### 5) Apply migrations + create admin

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6) Build Tailwind CSS

```bash
npm run build:css
```

For active frontend edits:

```bash
npm run watch:css
```

### 7) Run app

```bash
python manage.py runserver
```

App URLs:

- Home: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Seed and data import commands

```bash
# Bulk seed curated sample schemes
python manage.py populate_schemes

# Import from CSV (schemes_data/sikkim_schemes.csv)
python manage.py import_csv

# Update long descriptions for known scheme names
python manage.py update_full_descriptions
```

## Route map (major flows)

- `/schemes/` - scheme listing
- `/scheme/<id>/` - scheme detail
- `/advanced-search/` - advanced filtering
- `/check-eligibility/` - all eligible schemes for logged-in user
- `/apply/` - application form
- `/applications/` - application dashboard (employee)
- `/favorites/` - saved schemes
- `/comparison/` - compare up to 5 schemes
- `/notifications/` - notification center
- `/feedback/` and `/feedbacks/` - feedback submission/review

## Security notes

- Sensitive Aadhaar value in `Application` is stored encrypted (`cryptography.Fernet`) via model property `sensitive_data`.
- Aadhaar number is validated with Verhoeff checksum before persistence.
- Authentication and role checks are enforced through `@login_required` and group-based `@user_passes_test`.
- CSRF middleware is enabled globally (except explicitly exempted endpoints).

## Running Django + external bot stack

This repository includes helper scripts for dual-server startup:

- `run_all_servers.py`
- `START_SERVERS.bat`
- `start_servers.sh`
- `python manage.py run_rasa_server`

### Important caveat

These scripts currently include machine-specific absolute paths (for example, `C:\Users\LENOVO\...`) and may not work out-of-the-box on another system. Update those paths before use.

Also verify expected service ports in your environment:

- `translate_page` view posts to `http://localhost:5000/translate`
- Rasa helper command uses port `5055`
- `run_all_servers.py` text references port `5005`

Unify these in your deployment for stable integration.

## Quality checks

```bash
# Django system checks
python manage.py check

# App tests
python manage.py test

# Utility validation scripts included in repo
python test_servers.py
python test_notifications.py
```

## Common troubleshooting

- **`SECRET_KEY` / `FIELD_ENCRYPTION_KEY` missing**: ensure `.env` exists and has both values.
- **CSS not updating**: run `npm run build:css` or keep `npm run watch:css` running.
- **No schemes visible**: run `python manage.py populate_schemes` or `python manage.py import_csv`.
- **App crashes on another machine with startup scripts**: replace hard-coded paths in server scripts.
- **Eligibility empty for logged-in user**: ensure profile is created at `/userdetails/`.

## Production readiness checklist

Before deployment:

- Set `DEBUG=False`
- Set strict `ALLOWED_HOSTS`
- Rotate and securely store `SECRET_KEY` and `FIELD_ENCRYPTION_KEY`
- Enable HTTPS + secure cookie settings
- Run `collectstatic`
- Replace SQLite with production-grade DB if required by scale
- Align bot/translation ports and endpoints

## License

This project is licensed under [LICENSE](LICENSE).
