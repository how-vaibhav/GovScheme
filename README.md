# GovAid – Government Schemes Portal

GovAid is a Django-based web platform that helps citizens discover, compare, and apply for government schemes, with eligibility matching, notifications, feedback workflows, and role-based access for citizens, employees, and administrators.

## Highlights

- Scheme directory with filtering and detail pages
- Profile-based eligibility checking
- Application submission and status tracking
- Notifications center (with mark-as-read)
- Favorites and comparison tools
- Feedback and employee reply workflow
- Dark/light mode support
- Mobile-responsive UI

## Tech Stack

- Backend: Django 5.2.1, Python 3.13
- Database: SQLite (default)
- Frontend: Tailwind CSS 3.4.1, Vanilla JavaScript
- Icons/Fonts: Font Awesome, Google Fonts

## Project Structure

```text
GovScheme/
├── gov_schemes/                 # Django project settings and root URLs
├── schemesapp/                  # Main app (views, models, forms, templates)
│   ├── management/commands/     # Custom management commands
│   ├── migrations/              # DB migrations
│   ├── templates/               # App templates
│   └── templatetags/            # Custom template tags/filters
├── templates/                   # Global templates (base layout)
├── static/                      # CSS, JS, images, downloadable assets
├── schemes_data/                # CSV data source(s)
├── manage.py
├── requirements.txt
├── package.json
└── tailwind.config.js
```

## Prerequisites

- Python 3.10+
- Node.js + npm
- Git

## Quick Start

1. Clone and enter project:

```bash
git clone <your-repo-url>
cd GovScheme
```

2. Create and activate virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
npm install
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. (Optional) Load sample schemes:

```bash
python manage.py populate_schemes
# or
python manage.py import_csv
```

6. Build CSS:

```bash
npm run build:css
```

7. Run server:

```bash
python manage.py runserver
```

Open:

- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Useful Commands

```bash
# Validate Django config and templates
python manage.py check

# Run tests
python manage.py test

# Tailwind watch mode
npm run watch:css

# Create admin user
python manage.py createsuperuser
```

## Core Features by Role

### Citizen

- Register/login
- Complete profile (`/userdetails/`)
- Browse/search schemes
- Check eligibility
- Apply and track applications
- Submit feedback

### Employee

- View and respond to feedback
- Review application workflows
- Add/update scheme data (as configured)

### Admin

- Full Django admin management
- User/role and content oversight

## Security Notes

- CSRF protection via Django middleware
- Role-based access in views/templates
- Sensitive Aadhaar application data handled with encryption logic in model layer

## Deployment Notes

For production, set:

- `DEBUG = False`
- Proper `ALLOWED_HOSTS`
- Secure secret key management (environment variables)
- Static/media serving strategy (e.g., Nginx + collectstatic)

## Troubleshooting

- **TemplateSyntaxError**: run `python manage.py check` and verify latest template edits.
- **CSS not updating**: run `npm run build:css` (or `watch:css`).
- **Missing data**: run `populate_schemes` or `import_csv` commands.

## License

This project is licensed under the terms in [LICENSE](LICENSE).

---

If you want, I can also create a short `CONTRIBUTING.md` and `ENVIRONMENT_SETUP.md` to make onboarding for collaborators even smoother.
