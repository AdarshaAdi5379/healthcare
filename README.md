# Healthcare Backend API

A Django REST Framework backend for a healthcare application built as an internship assignment. The system provides JWT-based authentication, patient and doctor management, and patient-doctor assignment mapping.

---

## Features

- **JWT Authentication** — Register and login with email/password, receives access and refresh tokens
- **Patient Management** — Create, read, update, and delete patients (scoped to the owning user)
- **Doctor Management** — Create, read, update, and delete doctors (visible to all authenticated users)
- **Patient-Doctor Mapping** — Assign doctors to patients, list mappings, query doctors by patient
- **Swagger Documentation** — Auto-generated OpenAPI schema with interactive Swagger UI
- **Validation** — Field-level validation with meaningful error messages
- **Error Handling** — Consistent JSON error responses across all endpoints
- **Security** — Passwords hashed with PBKDF2, JWT auth required for protected endpoints, ownership enforced for patient data

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Django 6.0 / Django REST Framework 3.17 |
| Database | PostgreSQL |
| Authentication | JWT (djangorestframework-simplejwt) |
| API Docs | drf-spectacular (OpenAPI 3 / Swagger) |
| Environment | python-decouple |
| Testing | Django TestCase (41 tests) |

---

## Project Structure

```
healthcare/
├── manage.py
├── requirements.txt
├── .env / .env.example
├── .gitignore
├── README.md
├── config/                    # Django project configuration
│   ├── settings.py            # DRF, JWT, PostgreSQL, CORS, Swagger
│   ├── urls.py                # Root URL routing
│   ├── exceptions.py          # Custom error handler
│   ├── utils.py               # Shared response helpers
│   └── wsgi.py / asgi.py
├── accounts/                  # User authentication app
│   ├── models.py              # CustomUser (email-based, no username)
│   ├── serializers.py         # RegisterSerializer, LoginSerializer
│   ├── views.py               # register_view, login_view
│   ├── urls.py                # POST /api/auth/register/, /api/auth/login/
│   ├── admin.py               # CustomUser admin (UserAdmin)
│   └── tests.py               # 8 tests
├── patients/                  # Patient management app
│   ├── models.py              # Patient (name, age, gender, contact, address)
│   ├── serializers.py         # PatientSerializer with field validation
│   ├── views.py               # PatientViewSet (owner-scoped)
│   ├── urls.py                # /api/patients/ CRUD
│   ├── permissions.py         # IsOwner permission
│   ├── admin.py               # Patient admin
│   └── tests.py               # 14 tests
├── doctors/                   # Doctor management app
│   ├── models.py              # Doctor (name, specialization, email, experience)
│   ├── serializers.py         # DoctorSerializer with validation
│   ├── views.py               # DoctorViewSet
│   ├── urls.py                # /api/doctors/ CRUD
│   ├── admin.py               # Doctor admin
│   └── tests.py               # 9 tests
└── mappings/                  # Patient-Doctor mapping app
    ├── models.py              # Mapping (patient, doctor, assigned_by)
    ├── serializers.py         # MappingSerializer
    ├── views.py               # MappingViewSet + PatientDoctorsView
    ├── urls.py                # /api/mappings/ CRUD + by-patient lookup
    ├── admin.py               # Mapping admin
    └── tests.py               # 10 tests
```

---

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL (running on port 5433 or configured otherwise)
- pip

### Setup Steps

```bash
# 1. Clone the repository
git clone <repo-url>
cd healthcare

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your database credentials

# 5. Create the database
createdb -h localhost -p 5433 -U postgres healthcare_db

# 6. Run migrations
python manage.py migrate

# 7. (Optional) Create superuser for admin access
python manage.py createsuperuser

# 8. Run tests
python manage.py test

# 9. Start the server
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`.

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | (required) | Django secret key |
| `DEBUG` | `True` | Debug mode |
| `ALLOWED_HOSTS` | `*` | Comma-separated allowed hosts |
| `DB_NAME` | `healthcare_db` | PostgreSQL database name |
| `DB_USER` | `postgres` | Database user |
| `DB_PASSWORD` | `postgres` | Database password |
| `DB_HOST` | `localhost` | Database host |
| `DB_PORT` | `5433` | Database port |
| `CORS_ALLOW_ALL_ORIGINS` | `True` | Allow all CORS origins |
| `CORS_ALLOWED_ORIGINS` | `` | Comma-separated allowed origins |

---

## Authentication Flow

1. **Register** at `POST /api/auth/register/` with `email`, `name`, and `password`
2. **Login** at `POST /api/auth/login/` with `email` and `password`
3. Both endpoints return `{ message, data: { user, tokens: { access, refresh } } }`
4. Include the access token in subsequent requests: `Authorization: Bearer <access_token>`
5. Access tokens expire after 1 day; refresh tokens expire after 7 days

---

## API Endpoints

### Authentication (public)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Login and receive JWT tokens |

### Patients (authenticated, owner-scoped)

Only the user who created a patient can view, update, or delete it.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/patients/` | Create a patient |
| GET | `/api/patients/` | List your patients |
| GET | `/api/patients/<id>/` | Get patient details |
| PUT | `/api/patients/<id>/` | Update patient |
| DELETE | `/api/patients/<id>/` | Delete patient |

### Doctors (authenticated)

All authenticated users can view and manage all doctors.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/doctors/` | Create a doctor |
| GET | `/api/doctors/` | List all doctors |
| GET | `/api/doctors/<id>/` | Get doctor details |
| PUT | `/api/doctors/<id>/` | Update doctor |
| DELETE | `/api/doctors/<id>/` | Delete doctor |

### Mappings (authenticated)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/mappings/` | Assign a doctor to a patient |
| GET | `/api/mappings/` | List all mappings |
| GET | `/api/mappings/by-patient/<patient_id>/` | Get doctors for a patient |
| DELETE | `/api/mappings/<id>/` | Delete a mapping |

---

## Response Format

### Success

```json
// Create / Update
{
    "message": "Patient created successfully",
    "data": { ... }
}

// List / Retrieve (returns data directly)
[ ... ]

// Delete (returns 204 No Content with no body)
```

### Error

```json
// Authentication error
{"error": "Authentication credentials were not provided."}

// Validation error (field-level)
{"errors": {"age": ["Age must be between 0 and 150"]}}

// General error
{"error": "Invalid email or password"}

// Not found
{"error": "Not found."}
```

---

## Validation Rules

### Patient

| Field | Rule |
|-------|------|
| name | Required, cannot be empty |
| age | Required, must be 0-150 |
| gender | Required, must be M, F, or O |
| contact_number | Required, at least 10 digits |
| address | Optional |

### Doctor

| Field | Rule |
|-------|------|
| name | Required, cannot be empty |
| specialization | Required |
| email | Required, must be unique |
| experience | Must be 0 or greater |
| available_from / available_to | available_from must be earlier than available_to |

### Mapping

| Rule | Description |
|------|-------------|
| patient | Must exist |
| doctor | Must exist |
| Duplicate | Same patient-doctor pair cannot exist |

---

## Testing

```bash
python manage.py test

# Run tests for a specific app
python manage.py test accounts
python manage.py test patients
python manage.py test doctors
python manage.py test mappings
```

The test suite covers:

- **Authentication**: Registration, login, invalid credentials, duplicate emails, password hashing, unauthenticated access
- **Patients**: CRUD, ownership scoping, cross-user isolation, validation (age, phone, gender, empty name)
- **Doctors**: CRUD, auth requirements, validation (email uniqueness, negative experience, empty name, time range)
- **Mappings**: Create, duplicate prevention, list, doctors-by-patient lookup, delete, invalid references

---

## API Documentation

Swagger UI: `http://localhost:8000/api/docs/`
OpenAPI Schema: `http://localhost:8000/api/schema/`

---

## Admin Interface

Accessible at `http://localhost:8000/admin/` after creating a superuser.

All four models are registered with search, filtering, date hierarchy, and custom display fields.

---

## Assumptions

- The assignment assumes a single backend with no frontend
- PostgreSQL is the required database (SQLite not used)
- Patients are scoped to the creating user; doctors are visible to all authenticated users
- The `GET /api/mappings/by-patient/<patient_id>/` URL is used instead of `GET /api/mappings/<patient_id>/` due to URL routing conflicts with mapping IDs
- CORS is wide open by default for development convenience
- Access tokens expire in 1 day, refresh tokens in 7 days

---

## Future Improvements

- Add pagination for patient and doctor list endpoints
- Implement email verification during registration
- Add password reset flow
- Add role-based access control (admin, doctor, patient roles)
- Add rate limiting on auth endpoints
- Add request throttling
- Add CI/CD pipeline with GitHub Actions
- Containerize with Docker and docker-compose
- Add filtering and search query parameters to list endpoints
- Implement refresh token rotation for enhanced security
- Add audit logging for sensitive operations
