# Sushant Sinha — Portfolio Web App

Full-stack portfolio with Django backend + PostgreSQL + cyberpunk UI.

## Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: PostgreSQL
- **Frontend**: Vanilla JS + CSS (same cyberpunk aesthetic)
- **Auth**: Django Admin for content management

## Quick Start

### 1. Clone & Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. PostgreSQL Setup

```sql
CREATE DATABASE portfolio_db;
CREATE USER portfolio_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;
```

### 3. Environment Variables

```bash
cp .env.example .env
```

### 4. Run Migrations & Start

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py seed_data
python manage.py runserver
```

### 5. Access

- Portfolio: http://localhost:8000/
- Admin Panel: http://localhost:8000/admin/
- API Docs: http://localhost:8000/api/
