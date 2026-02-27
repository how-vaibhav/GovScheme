# GovAid

## Government Schemes Portal

> A production-oriented Django platform for discovering, evaluating, and applying to government welfare schemes with profile-based eligibility and secure application workflows.

| Build  | Backend      | Frontend           | Database         | License                      |
| ------ | ------------ | ------------------ | ---------------- | ---------------------------- |
| Stable | Django 5.2.1 | Tailwind CSS 3.4.1 | SQLite (default) | MIT-compatible (see LICENSE) |

---

## Documentation Navigation

- [Product Overview](#product-overview)
- [Core Capabilities](#core-capabilities)
- [Technical Stack](#technical-stack)
- [Architecture](#architecture)
- [Data Model](#data-model)
- [Repository Structure](#repository-structure)
- [Environment Configuration](#environment-configuration)
- [Local Development Setup](#local-development-setup)
- [Data Seeding and Import](#data-seeding-and-import)
- [Primary Routes](#primary-routes)
- [Security Controls](#security-controls)
- [Bot and Translation Integration](#bot-and-translation-integration)
- [Quality Assurance](#quality-assurance)
- [Troubleshooting](#troubleshooting)
- [Production Checklist](#production-checklist)
- [License](#license)

---

## Product Overview

GovAid is a citizen-service web system designed to streamline public scheme access. It supports role-specific workflows for citizens, employees, and administrators while maintaining security for sensitive application fields.

### Strategic Goals

- Centralize scheme discovery and eligibility evaluation.
- Improve application completion with guided flows.
- Enable operational handling through employee/admin interfaces.
- Preserve trust through input validation and encrypted storage.

## Core Capabilities

### Citizen Experience

- Register, authenticate, and manage profile details (`UserDetails`).
- Discover schemes through listing, advanced filtering, and comparison.
- Run eligibility checks per scheme or across all schemes.
- Submit applications with Aadhaar validation and masked confirmation.
- Manage favorites, notifications, and feedback history.

### Employee Operations

- Review and reply to user feedback.
- Process application statuses (`pending`, `accepted`, `rejected`).

### Administrative Control

- Manage users, schemes, and content via Django admin.
- Assign employee access using the custom employee onboarding flow.

---

## Technical Stack

| Layer           | Technology                    | Version / Notes              | Responsibility                                |
| --------------- | ----------------------------- | ---------------------------- | --------------------------------------------- |
| Runtime         | Python                        | 3.12+ (Pipfile target)       | Application execution                         |
| Framework       | Django                        | 5.2.1                        | Routing, ORM, auth, middleware, admin         |
| Data Store      | SQLite                        | `db.sqlite3` (default)       | Persistent domain storage                     |
| UI Layer        | Django Templates + Vanilla JS | Server-rendered architecture | HTML rendering and light client interactivity |
| Design System   | Tailwind CSS                  | 3.4.1                        | Utility-driven styling                        |
| Configuration   | python-decouple               | 3.8                          | `.env`-based settings management              |
| Cryptography    | cryptography (Fernet)         | 45.0.2                       | Field-level Aadhaar encryption/decryption     |
| Integration     | requests                      | 2.32.3                       | External service calls                        |
| Data Extraction | beautifulsoup4 + lxml         | 4.13.4 / 5.4.0               | HTML parsing and scraping support             |
| Tooling         | npm + Tailwind CLI            | package scripts              | CSS compile and watch pipeline                |

### Dependency Groups

- **Platform core**: `Django`, `asgiref`, `sqlparse`, `tzdata`
- **Security and configuration**: `cryptography`, `cffi`, `python-decouple`
- **Integrations and ingestion**: `requests`, `beautifulsoup4`, `lxml`
- **Frontend pipeline**: `tailwindcss` via `npm run build:css` / `npm run watch:css`

> Note: `requirements.txt` is pinned for reproducibility. Keep local Python aligned with `Pipfile` (`3.12`) for predictable behavior.

---

## Architecture

### Service Boundaries

- **Primary Web Service (Django on 8000)**
  - Auth, profile, scheme catalog, applications, notifications, feedback.
- **Auxiliary Services (Translation/Bot endpoints)**
  - External service interactions for translation/chat workflows.

### Domain Modules

- **Models**: `UserDetails`, `Scheme`, `Application`, `Notification`, `Feedback`, `Favorite`, `ApplicationTimeline`
- **Eligibility Engine**: `Scheme.is_user_eligible(details)`
- **Recommendation Layer**: `get_smart_recommendations(user)`
- **Eventing**: `post_save` signal on `Scheme` for notification fan-out
- **Sensitive Flow Controls**: Verhoeff checksum + Fernet encryption

### Application Flow (Apply Scheme)

1. Authenticated user submits Aadhaar + selected scheme (`/apply/`).
2. Aadhaar input is validated with Verhoeff checksum.
3. Aadhaar is encrypted through `Application.sensitive_data` before save.
4. Application is persisted with default `pending` status.
5. Session stores masked Aadhaar for confirmation page rendering.
6. Employee status action triggers user notification.

## Data Model

| Entity                | Key Attributes                                 | Relationships                                       |
| --------------------- | ---------------------------------------------- | --------------------------------------------------- |
| `UserDetails`         | demographic and socioeconomic fields           | One-to-one with `User`                              |
| `Scheme`              | metadata, eligibility rules, contact fields    | Referenced by applications, feedback, notifications |
| `Application`         | encrypted Aadhaar, status, timestamps          | Many-to-one with `User` and `Scheme`                |
| `Notification`        | message, read state, optional scheme reference | Many-to-one with `User`                             |
| `Feedback`            | user message and optional employee reply       | Linked to `User` and optional `Scheme`              |
| `Favorite`            | bookmark mapping                               | Unique pair (`user`, `scheme`)                      |
| `ApplicationTimeline` | status transition records                      | Many-to-one with `Application`                      |

---

## Repository Structure

```text
GovScheme/
├── gov_schemes/                       # Project configuration (settings, urls, wsgi/asgi)
├── schemesapp/
│   ├── management/commands/           # Seed/import/integration commands
│   ├── migrations/
│   ├── templates/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── schemes_data/                      # CSV datasets
├── static/                            # Static sources (CSS/JS/images)
├── staticfiles/                       # collectstatic output
├── templates/                         # Shared template layer
├── manage.py
├── requirements.txt
├── package.json
├── run_all_servers.py
└── START_SERVERS.bat
```

---

## Environment Configuration

Create a `.env` file in project root:

```env
SECRET_KEY=replace-with-django-secret
FIELD_ENCRYPTION_KEY=replace-with-fernet-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Optional production hardening
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False
```

Generate `FIELD_ENCRYPTION_KEY`:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

---

## Local Development Setup

### 1) Clone repository

```bash
git clone <your-repository-url>
cd GovScheme
```

### 2) Create and activate virtual environment

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

### 4) Initialize database and admin

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5) Build frontend assets

```bash
npm run build:css
```

Development watch mode:

```bash
npm run watch:css
```

### 6) Launch application

```bash
python manage.py runserver
```

- Home: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

---

## Data Seeding and Import

```bash
# Seed curated in-code schemes
python manage.py populate_schemes

# Import schemes from CSV
python manage.py import_csv

# Enrich long descriptions for known scheme names
python manage.py update_full_descriptions
```

## Primary Routes

| Route                       | Purpose                         |
| --------------------------- | ------------------------------- |
| `/schemes/`                 | Scheme index/listing            |
| `/scheme/<id>/`             | Scheme detail view              |
| `/advanced-search/`         | Multi-criteria filtering        |
| `/check-eligibility/`       | User-wide eligibility results   |
| `/apply/`                   | Scheme application submission   |
| `/applications/`            | Employee application operations |
| `/favorites/`               | User bookmarks                  |
| `/comparison/`              | Side-by-side scheme comparison  |
| `/notifications/`           | Notification center             |
| `/feedback/`, `/feedbacks/` | Feedback and response workflows |

---

## Security Controls

- Field-level encryption for Aadhaar using `cryptography.Fernet`.
- Aadhaar checksum validation (Verhoeff) prior to persistence.
- Access control using `@login_required` and role/group checks.
- CSRF middleware enabled globally, with explicit exemptions only where configured.

## Bot and Translation Integration

Supported helper scripts:

- `run_all_servers.py`
- `START_SERVERS.bat`
- `start_servers.sh`
- `python manage.py run_rasa_server`

> Important: startup scripts include machine-specific absolute paths (e.g., `C:\Users\LENOVO\...`). Update these for your environment before running.

Integration endpoints to reconcile in deployment:

- `translate_page` expects `http://localhost:5000/translate`
- Rasa management command expects `5055`
- `run_all_servers.py` references `5005`

Standardize these ports/endpoints to avoid runtime mismatch.

---

## Quality Assurance

```bash
# Django system checks
python manage.py check

# App tests
python manage.py test

# Utility scripts
python test_servers.py
python test_notifications.py
```

## Troubleshooting

- Missing `SECRET_KEY` / `FIELD_ENCRYPTION_KEY`: verify `.env` exists and includes both keys.
- CSS not reflecting changes: run `npm run build:css` or keep `npm run watch:css` active.
- Empty scheme list: run `python manage.py populate_schemes` or `python manage.py import_csv`.
- Startup script failures on new machines: replace hard-coded path values.
- No eligibility results: ensure user profile is completed at `/userdetails/`.

## Production Checklist

- Set `DEBUG=False`.
- Restrict `ALLOWED_HOSTS`.
- Rotate and protect `SECRET_KEY` and `FIELD_ENCRYPTION_KEY`.
- Enforce HTTPS and secure cookie flags.
- Run `collectstatic`.
- Replace SQLite with production-grade database as needed.
- Standardize external bot/translation endpoint configuration.

---

## License

This project is licensed under [LICENSE](LICENSE).
