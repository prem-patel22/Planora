# 🚀 Quick Start Guide - Party Plot Management System

## Prerequisites
- Python 3.8+ installed
- pip (Python package manager)

## Step-by-Step Instructions

### 1. Open Terminal/PowerShell
Navigate to project directory:
```powershell
cd C:\Users\premp\Github\clones\PartyPlotManagementSystem
```

### 2. Create Virtual Environment (First Time Only)
```powershell
python -m venv venv
```

### 3. Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

**If you get an execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install Dependencies (First Time Only)
```powershell
pip install -r requirements.txt
```

This installs:
- Django (>=5.2.0)
- Pillow (>=10.0.0) for image handling

### 5. Run Database Migrations
```powershell
python manage.py migrate
```

### 6. Create Superuser (Optional - For Admin Access)
```powershell
python manage.py createsuperuser
```
Follow prompts to create admin username, email, and password.

### 7. Start Development Server
```powershell
python manage.py runserver
```

### 8. Access the Application
- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## Quick Commands Reference

### Start Server (After Initial Setup)
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run server
python manage.py runserver
```

### Stop Server
Press `Ctrl + C` in the terminal

### Deactivate Virtual Environment
```powershell
deactivate
```

---

## Troubleshooting

### Port Already in Use
If port 8000 is busy, use a different port:
```powershell
python manage.py runserver 8080
```

### Database Issues
If you need to reset the database:
```powershell
# Delete db.sqlite3 (backup first!)
# Then run:
python manage.py migrate
```

### Missing Dependencies
```powershell
pip install -r requirements.txt
```

---

## Project Structure Quick Reference

- **Templates**: `templates/` - HTML files
- **Static Files**: `static/` - CSS files
- **Backend Logic**: `ppms_app/views.py` - View functions
- **Database Models**: `ppms_app/models.py` - Data models
- **URL Routing**: `ppms_app/urls.py` - URL patterns
- **Settings**: `ppms/settings.py` - Configuration

---

## Default URLs

- `/` - Home page
- `/index/` - User homepage
- `/index1/` - Admin homepage
- `/login/` - Login page
- `/register-login/` - User registration
- `/book-venue/` - Book a venue
- `/search-venues/` - Search venues
- `/admin/` - Django admin panel

---

**Note**: The database (`db.sqlite3`) already exists with data, so migrations may show "No migrations to apply" - this is normal!
