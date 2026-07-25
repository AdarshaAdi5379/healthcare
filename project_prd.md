# Healthcare Backend — Django Assignment PRD

## Objective

Build a backend system for a healthcare application using **Django**, **Django REST Framework (DRF)**, and **PostgreSQL**. The system allows users to register, log in, and manage patient and doctor records securely.

---

## Requirements

- Use **Django** and **Django REST Framework (DRF)** for the backend.
- Use **PostgreSQL** as the database.
- Implement **JWT authentication** using `djangorestframework-simplejwt`.
- Create **RESTful API endpoints** for managing patients and doctors.
- Use **Django ORM** for database modeling.
- Implement **error handling** and **validation**.
- Use **environment variables** for sensitive configurations.

---

## API Endpoints

### 1. Authentication APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register a new user with name, email, and password |
| POST | `/api/auth/login/` | Log in a user and return a JWT token |

### 2. Patient Management APIs (Authenticated)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/patients/` | Add a new patient |
| GET | `/api/patients/` | Retrieve all patients created by the authenticated user |
| GET | `/api/patients/<id>/` | Get details of a specific patient |
| PUT | `/api/patients/<id>/` | Update patient details |
| DELETE | `/api/patients/<id>/` | Delete a patient record |

### 3. Doctor Management APIs (Authenticated)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/doctors/` | Add a new doctor |
| GET | `/api/doctors/` | Retrieve all doctors |
| GET | `/api/doctors/<id>/` | Get details of a specific doctor |
| PUT | `/api/doctors/<id>/` | Update doctor details |
| DELETE | `/api/doctors/<id>/` | Delete a doctor record |

### 4. Patient-Doctor Mapping APIs (Authenticated)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/mappings/` | Assign a doctor to a patient |
| GET | `/api/mappings/` | Retrieve all patient-doctor mappings |
| GET | `/api/mappings/<patient_id>/` | Get all doctors assigned to a specific patient |
| DELETE | `/api/mappings/<id>/` | Remove a doctor from a patient |

---

## Database Models

### User (Django's built-in `AbstractUser` or custom)
- name
- email (unique)
- password

### Patient
- id (auto-generated)
- name
- age
- gender
- contact_number
- address
- created_by (ForeignKey to User — the authenticated user who created it)
- created_at
- updated_at

### Doctor
- id (auto-generated)
- name
- specialization
- contact_number
- email
- available_from
- available_to
- created_at
- updated_at

### PatientDoctorMapping (Many-to-Many through model)
- id (auto-generated)
- patient (ForeignKey to Patient)
- doctor (ForeignKey to Doctor)
- assigned_by (ForeignKey to User)
- assigned_at

---

## Project Structure

```
healthcare/
├── manage.py
├── requirements.txt
├── .env
├── .env.example
├── healthcare/              # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                # User authentication app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── patients/                # Patient management app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── doctors/                 # Doctor management app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
└── mappings/                # Patient-Doctor mapping app
    ├── migrations/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── urls.py
    └── views.py
```

---

## Key Dependencies (`requirements.txt`)

- Django >= 5.0
- djangorestframework
- djangorestframework-simplejwt
- psycopg2-binary
- python-decouple (or python-dotenv)

---

## Implementation Plan

### Step 1 — Project Setup
1. Create Django project and apps
2. Configure settings.py for DRF, JWT, and PostgreSQL
3. Set up `.env` for DATABASE_URL, SECRET_KEY, etc.

### Step 2 — User Authentication
1. Custom user model (or extend AbstractUser) with `name`, `email`, `password`
2. Register serializer with validation
3. Login view returning access + refresh JWT tokens
4. Token obtain pair / refresh views from simplejwt

### Step 3 — Patient CRUD
1. Patient model with all required fields + `created_by` FK to User
2. Serializer with field validation
3. ViewSet with `permission_classes = [IsAuthenticated]`
4. Override `get_queryset` to filter by `request.user`
5. Router registration

### Step 4 — Doctor CRUD
1. Doctor model with all required fields
2. Serializer with field validation
3. ViewSet with `permission_classes = [IsAuthenticated]`
4. Router registration

### Step 5 — Patient-Doctor Mapping
1. Mapping model with FKs to Patient, Doctor, and User (assigned_by)
2. Serializer with validation (prevent duplicates)
3. Custom view: `GET /api/mappings/<patient_id>/` returns doctors for a patient
4. Delete mapping endpoint

### Step 6 — Error Handling & Validation
1. Custom exception handler for DRF
2. Input validation in serializers
3. Proper HTTP status codes (201, 400, 401, 403, 404, 204)

### Step 7 — Testing
1. Test all endpoints via Postman or DRF's browsable API
2. Verify authentication scoping (patients scoped to user, doctors global)

---

## Expected Outcome

- Users can register and log in.
- Authenticated users can add and manage patient and doctor records.
- Patients can be assigned to doctors via mappings.
- Data is stored securely in PostgreSQL.
- All endpoints return appropriate HTTP status codes and error messages.
