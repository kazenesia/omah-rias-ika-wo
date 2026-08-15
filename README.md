# Omah Rias Ika — Wedding Organizer

Django web app untuk wedding organizer — booking, katalog vendor, paket, dan admin panel.

## Struktur Project

```
angen2-wo-app/
├── AGENTS.md              # Agent framework config
├── README.md
├── backend/               # Django project
│   ├── manage.py
│   ├── config/            # Settings, URLs, WSGI
│   ├── core/              # Main app (models, views, API)
│   ├── templates/         # HTML templates
│   ├── static/            # CSS, JS, assets
│   └── media/             # Upload user
├── docs/                  # Dokumentasi & directives
├── scripts/               # Utility scripts (seed, setup)
└── .tmp/                  # Temporary data
```

## Setup

```powershell
# Install dependencies
python scripts/setup_env.py

# Migrate database
cd backend
..\backend\venv\Scripts\python.exe manage.py migrate

# Seed sample data (optional)
..\backend\venv\Scripts\python.exe ..\scripts\seed.py
```

## Menjalankan Server

```powershell
cd backend
..\backend\venv\Scripts\python.exe manage.py runserver
```

Buka http://127.0.0.1:8000/

## Admin Panel

- URL: http://127.0.0.1:8000/admin-panel/
- Username: `admin`
- Password: `admin123`
