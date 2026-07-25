# Healthcare Backend API

A Django REST Framework backend for a healthcare application with JWT authentication, patient and doctor management, and patient-doctor mapping.

---

## Tech Stack

- Python 3.12 / Django 6.0
- Django REST Framework
- PostgreSQL
- JWT Authentication (SimpleJWT)
- OpenAPI / Swagger (drf-spectacular)

---

## Setup

### 1. Clone and enter the project

```bash
git clone <repo-url>
cd healthcare
```

### 2. Create virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` and adjust values:

```bash
cp .env.example .env
```

Default `.env`:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5433
```

### 4. Create the database

```bash
createdb -h localhost -p 5433 -U postgres healthcare_db
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (optional, for admin access)

```bash
python manage.py createsuperuser
```

### 7. Start the server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`.

Swagger documentation: `http://localhost:8000/api/docs/`

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Login and receive JWT tokens |

**Register**
```json
POST /api/auth/register/
{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "securepass123"
}
```

**Login**
```json
POST /api/auth/login/
{
    "email": "user@example.com",
    "password": "securepass123"
}
```

Both endpoints return:
```json
{
    "message": "...",
    "user": {"id": 1, "email": "...", "name": "..."},
    "tokens": {"access": "...", "refresh": "..."}
}
```

All subsequent requests require `Authorization: Bearer <access_token>` header.

---

### Patients (Authenticated)

Patients are scoped to the authenticated user. Users can only see/edit their own patients.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/patients/` | Create a patient |
| GET | `/api/patients/` | List your patients |
| GET | `/api/patients/<id>/` | Get patient details |
| PUT | `/api/patients/<id>/` | Update patient |
| DELETE | `/api/patients/<id>/` | Delete patient |

**Patient fields:**

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| name | string | Yes | |
| age | integer | Yes | 0-150 |
| gender | string | Yes | M, F, or O |
| contact_number | string | Yes | At least 10 digits |
| address | string | No | |

---

### Doctors (Authenticated)

All authenticated users can view and manage all doctors.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/doctors/` | Create a doctor |
| GET | `/api/doctors/` | List all doctors |
| GET | `/api/doctors/<id>/` | Get doctor details |
| PUT | `/api/doctors/<id>/` | Update doctor |
| DELETE | `/api/doctors/<id>/` | Delete doctor |

**Doctor fields:**

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| name | string | Yes | |
| specialization | string | Yes | |
| email | string | Yes | Must be unique |
| contact_number | string | Yes | |
| experience | integer | No | Cannot be negative |
| available_from | time (HH:MM) | No | |
| available_to | time (HH:MM) | No | |

---

### Mappings (Authenticated)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/mappings/` | Assign a doctor to a patient |
| GET | `/api/mappings/` | List all mappings |
| GET | `/api/mappings/by-patient/<patient_id>/` | Get doctors for a patient |
| DELETE | `/api/mappings/<id>/` | Delete a mapping |

Duplicate patient-doctor pairs are prevented.

---

## Error Responses

All errors return consistent JSON:

```json
// Validation errors (field-specific)
{"errors": {"age": ["Age must be between 0 and 150"]}}

// General errors
{"error": "Invalid email or password"}

// Authentication errors
{"error": "Authentication credentials were not provided."}
```

---

## Admin Interface

Accessible at `/admin/` after creating a superuser. All models (Users, Patients, Doctors, Mappings) are registered.

---

## Project Structure

```
healthcare/
├── manage.py
├── requirements.txt
├── .env / .env.example
├── config/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── exceptions.py
├── accounts/            # User auth (register, login, JWT)
│   ├── models.py        # CustomUser (email-based)
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── patients/            # Patient CRUD
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py   # IsOwner
│   ├── views.py
│   └── urls.py
├── doctors/             # Doctor CRUD
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
└── mappings/            # Patient-Doctor mappings
    ├── models.py
    ├── serializers.py
    ├── views.py
    └── urls.py
```
