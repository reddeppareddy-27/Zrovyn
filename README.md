# Finance Dashboard Backend

A Django-based backend API for a finance dashboard system with role-based access control, financial record management, and advanced analytics.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start-5-minutes)
- [Project Summary](#project-summary)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [Architecture & Design](#architecture--design)
- [Deployment Guide](#deployment-guide)
- [Troubleshooting](#troubleshooting)

---

## Overview

This project implements a robust finance management system backend with the following features:

- **User and Role Management**: Support for Viewer, Analyst, and Admin roles with granular permission controls
- **Financial Records Management**: CRUD operations for financial transactions with validation
- **Dashboard Analytics**: Summary-level APIs for income, expenses, and financial insights
- **Access Control**: Role-based permission system for data protection
- **Error Handling**: Comprehensive validation and error responses
- **Data Persistence**: PostgreSQL database for reliable data storage

### Tech Stack

- **Framework**: Django 4.2.8 + Django REST Framework 3.14.0
- **Database**: PostgreSQL
- **Authentication**: Token-based authentication
- **Additional**: CORS support, comprehensive logging, pagination

### Project Structure

```
finance_backend/
├── finance_backend/          # Main project settings
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI application
├── finance/                  # Main app
│   ├── models.py            # Data models (Role, CustomUser, FinancialRecord)
│   ├── serializers.py       # API serializers for validation
│   ├── views.py             # API endpoints and business logic
│   ├── permissions.py       # Role-based permission classes
│   ├── services.py          # Business logic for analytics
│   ├── utils.py             # Utility functions
│   ├── urls.py              # App URL routing
│   ├── admin.py             # Django admin configuration
│   └── tests.py             # Test suite
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

---

## Quick Start (5 minutes)

Get the Finance Backend up and running in 5 minutes.

### Prerequisites

- Python 3.8+
- PostgreSQL (or SQLite for testing)
- Git

### Installation

#### 1. Clone and Navigate

```bash
cd finance_backend
```

#### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure for Development

```bash
# Copy environment template
cp .env.example .env

# For development with SQLite (no PostgreSQL needed):
# Edit .env and change DB_ENGINE to:
# DB_ENGINE=django.db.backends.sqlite3
# DB_NAME=db.sqlite3
```

#### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 6. Create Roles and Users

```bash
python manage.py shell
```

Then paste:

```python
from finance.models import Role, CustomUser

# Create roles
Role.objects.get_or_create(name='viewer', defaults={'description': 'Read-only access'})
Role.objects.get_or_create(name='analyst', defaults={'description': 'Can view and analyze'})
Role.objects.get_or_create(name='admin', defaults={'description': 'Full administrative access'})

# Create a test admin user
role = Role.objects.get(name='admin')
admin = CustomUser.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin123',
    role=role
)

# Create analyst user
analyst_role = Role.objects.get(name='analyst')
analyst = CustomUser.objects.create_user(
    username='analyst',
    email='analyst@example.com',
    password='analyst123',
    role=analyst_role
)

# Create viewer user
viewer_role = Role.objects.get(name='viewer')
viewer = CustomUser.objects.create_user(
    username='viewer',
    email='viewer@example.com',
    password='viewer123',
    role=viewer_role
)

exit()
```

#### 7. Start Server

```bash
python manage.py runserver
```

Server runs at: `http://localhost:8000`

### Quick API Test

#### Get Authentication Token

```bash
# Via Django shell
python manage.py shell
from rest_framework.authtoken.models import Token
from finance.models import CustomUser

analyst = CustomUser.objects.get(username='analyst')
token = Token.objects.get_or_create(user=analyst)[0]
print(f"Token: {token.key}")
exit()
```

#### Test the API

```bash
# Set token
TOKEN="<your-token-from-above>"

# Create an income record
curl -X POST http://localhost:8000/api/v1/records/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "5000.00",
    "record_type": "income",
    "category": "salary",
    "date": "2024-01-15",
    "description": "Monthly salary"
  }'

# Get dashboard summary
curl -X GET http://localhost:8000/api/v1/records/summary/ \
  -H "Authorization: Token $TOKEN"

# Get all records
curl -X GET http://localhost:8000/api/v1/records/ \
  -H "Authorization: Token $TOKEN"
```

### Using Django Admin

1. Go to `http://localhost:8000/admin/`
2. Login with `admin` / `admin123`
3. Manage users, roles, and records via the admin interface

---

## Project Summary

### What Has Been Built

A complete, production-ready Django REST Framework backend for a finance dashboard system with role-based access control, financial record management, and comprehensive analytics.

### Core Features Implemented

#### ✅ 1. User and Role Management
- **Three predefined roles**: Viewer, Analyst, Admin
- **User status management**: active, inactive, suspended
- **Role-based access control** enforced at API level
- **User profile management** endpoint
- **Admin user management** interface

#### ✅ 2. Financial Records Management
- **Full CRUD operations** for financial records
- **Income and expense** record types
- **10 financial categories**: salary, bonus, investment, food, transport, etc.
- **Advanced filtering**: by date range, type, category, search text
- **Soft delete pattern** for data recovery
- **Bulk create** support for multiple records
- **Pagination and sorting** support

#### ✅ 3. Dashboard Summary APIs
- **Dashboard summary**: Total income, expenses, net balance, record counts
- **Category-wise breakdown**: Totals and counts by category
- **Monthly trends**: Last 12 months income/expenses/net
- **Recent activity**: Latest transactions with timestamps
- **Period statistics**: Customizable date range analysis
- **Comprehensive overview**: All metrics in one endpoint
- **Financial insights**: Ratios and analytics

#### ✅ 4. Access Control Logic
- **Role-based permission classes** for each endpoint
- **Viewer**: Read-only access to own records
- **Analyst**: Create, read, update own records and analytics
- **Admin**: Full access to all data and user management
- **Owner-based permissions** for record access
- **Status-based access** (suspended users blocked)
- **Detailed permission messages** for unauthorized access

#### ✅ 5. Validation and Error Handling
- **Input validation** for all financial records
- **Amount validation**: Must be positive
- **Date validation**: Cannot be future dates
- **Required field validation**: Enforced on all inputs
- **Consistent error responses** with detailed messages
- **Proper HTTP status codes**: 400, 401, 403, 404, 500
- **Logging of all errors** for debugging

#### ✅ 6. Data Persistence
- **PostgreSQL relational database** (production)
- **Custom User model** with UUID primary key
- **Role model** for flexible role management
- **Financial Record model** with comprehensive fields
- **Database indexes** for performance optimization
- **Soft delete support** via `is_deleted` field

### API Endpoints Summary (25+ total)

**Users**: 6 endpoints
- GET/POST /users/
- GET /users/{id}/, PUT /users/{id}/, DELETE /users/{id}/
- GET /users/me/, GET /users/inactive_users/

**Records**: 12+ endpoints
- GET/POST /records/
- GET /records/{id}/, PUT /records/{id}/, DELETE /records/{id}/
- POST /records/bulk_create/
- GET /records/summary/
- GET /records/category_summary/
- GET /records/monthly_summary/
- GET /records/recent_activity/
- GET /records/statistics/

**Dashboard**: 2+ endpoints
- GET /dashboard/overview/
- GET /dashboard/insights/

**Roles**: 1+ endpoint
- GET /roles/

### Statistics

- **Total Lines of Code**: ~3000+
- **Total Lines of Tests**: ~650+
- **Total Lines of Documentation**: ~2000+
- **API Endpoints**: 25+
- **Test Cases**: 30+
- **Models**: 3 (Role, CustomUser, FinancialRecord)
- **ViewSets**: 4 (Role, User, FinancialRecord, Dashboard)
- **Permission Classes**: 8
- **Serializers**: 10+

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL 10+
- pip or conda for dependency management

### 1. Clone the Repository

```bash
cd finance_backend
```

### 2. Create and Activate Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n finance_backend python=3.10
conda activate finance_backend
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your database configuration
```

Example `.env` configuration:

```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.postgresql
DB_NAME=finance_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 5. Create PostgreSQL Database

```bash
# Using psql
psql -U postgres
CREATE DATABASE finance_db;
\q
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Initial Roles

```bash
python manage.py shell
```

Then in the Django shell:

```python
from finance.models import Role

Role.objects.create(name='viewer', description='Read-only access to records and summaries')
Role.objects.create(name='analyst', description='Can view, create, and analyze records')
Role.objects.create(name='admin', description='Full administrative access')
```

### 8. Create a Superuser

```bash
python manage.py createsuperuser
```

### 9. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

---

## API Documentation

### Base URL

```
http://localhost:8000/api/v1/
```

### Authentication

Use Token Authentication. Include the token in the request header:

```
Authorization: Token <your-token-here>
```

### Available Endpoints

#### Users Management

- `GET /users/` - List all users (Admin only)
- `POST /users/` - Create a new user (Admin only)
- `GET /users/{id}/` - Get user details
- `PUT /users/{id}/` - Update user (Admin only)
- `DELETE /users/{id}/` - Delete user (Admin only)
- `GET /users/me/` - Get current user profile
- `GET /users/inactive_users/` - List inactive users (Admin only)

#### Financial Records

- `GET /records/` - List financial records
  - Query parameters:
    - `start_date`: Filter by start date (YYYY-MM-DD)
    - `end_date`: Filter by end date (YYYY-MM-DD)
    - `type`: Filter by record type (income/expense)
    - `category`: Filter by category
    - `search`: Search in description
    - `page`: Page number for pagination
    - `page_size`: Items per page

- `POST /records/` - Create a new record (Analyst+)
- `GET /records/{id}/` - Get record details
- `PUT /records/{id}/` - Update record (Analyst+)
- `DELETE /records/{id}/` - Delete record (Admin only)
- `POST /records/bulk_create/` - Create multiple records (Analyst+)

#### Dashboard Analytics

- `GET /records/summary/` - Get overall financial summary
- `GET /records/category_summary/` - Get category-wise breakdown
- `GET /records/monthly_summary/` - Get monthly trends
  - Query parameters:
    - `months`: Number of months (default: 12)

- `GET /records/recent_activity/` - Get recent transactions
  - Query parameters:
    - `limit`: Number of records (default: 10)

- `GET /records/statistics/` - Get statistics for a date range
  - Query parameters:
    - `start_date`: Start date (YYYY-MM-DD) - **required**
    - `end_date`: End date (YYYY-MM-DD) - **required**

- `GET /dashboard/overview/` - Comprehensive dashboard overview
- `GET /dashboard/insights/` - Financial insights and analytics

#### Roles

- `GET /roles/` - List available roles

### Request/Response Examples

#### Create a Financial Record

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/records/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "5000.00",
    "record_type": "income",
    "category": "salary",
    "date": "2024-01-15",
    "description": "Monthly salary"
  }'
```

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_username": "john_doe",
  "amount": "5000.00",
  "record_type": "income",
  "record_type_display": "Income",
  "category": "salary",
  "category_display": "Salary",
  "description": "Monthly salary",
  "date": "2024-01-15",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Get Dashboard Summary

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/records/summary/ \
  -H "Authorization: Token <token>"
```

**Response:**
```json
{
  "total_income": "25000.00",
  "total_expenses": "5500.00",
  "net_balance": "19500.00",
  "total_records": 15,
  "records_count_by_type": {
    "income": 5,
    "expense": 10
  },
  "records_count_by_category": {
    "salary": 3,
    "food": 4,
    "transport": 2,
    "utilities": 1
  }
}
```

#### Get Monthly Trends

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/records/monthly_summary/?months=6" \
  -H "Authorization: Token <token>"
```

**Response:**
```json
[
  {
    "year": 2023,
    "month": 8,
    "income": "5000.00",
    "expenses": "1200.00",
    "net": "3800.00"
  },
  {
    "year": 2023,
    "month": 9,
    "income": "5000.00",
    "expenses": "1100.00",
    "net": "3900.00"
  }
]
```

### Role-Based Access Control

#### Viewer Role
- ✅ View own financial records
- ✅ Access dashboard summaries
- ✅ View analytics and insights
- ❌ Cannot create or edit records
- ❌ Cannot manage users

#### Analyst Role
- ✅ View own financial records
- ✅ Create and edit own records
- ✅ Access all dashboard analytics
- ✅ View user list
- ✅ Bulk create records
- ❌ Cannot delete records
- ❌ Cannot manage users (except viewing)
- ❌ Cannot manage system roles

#### Admin Role
- ✅ Full access to all records
- ✅ Create, read, update, delete records (any user's)
- ✅ Create and manage users
- ✅ Manage roles and permissions
- ✅ View all system data
- ✅ Access all analytics for any user
- ✅ Perform all administrative actions

### Data Models

#### CustomUser
Extended Django User model with role and status.

**Fields:**
- `id` (UUID): Unique identifier
- `username` (string): Unique username
- `email` (string): User email
- `first_name` (string): First name
- `last_name` (string): Last name
- `role` (FK): Reference to Role
- `status` (choice): active | inactive | suspended
- `is_active` (boolean): Django authentication status
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

#### Role
Defines user roles and permissions.

**Fields:**
- `name` (choice): viewer | analyst | admin
- `description` (text): Role description
- `created_at` (datetime): Creation timestamp

#### FinancialRecord
Financial transaction record.

**Fields:**
- `id` (UUID): Unique identifier
- `user` (FK): Record owner
- `amount` (decimal): Transaction amount
- `record_type` (choice): income | expense
- `category` (choice): salary, bonus, investment, food, transport, utilities, entertainment, healthcare, education, other
- `description` (text): Record notes
- `date` (date): Transaction date
- `is_deleted` (boolean): Soft delete flag
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

### Validation and Error Handling

#### Input Validation

- **Amount**: Must be positive (> 0)
- **Date**: Cannot be in the future
- **Required Fields**: Enforced on all models
- **Enum Values**: Type, category, status must be valid choices

#### Error Responses

**Example Error Response (400 Bad Request):**
```json
{
  "success": false,
  "message": "Invalid input provided.",
  "errors": {
    "amount": ["Amount must be greater than 0."]
  },
  "status_code": 400
}
```

**HTTP Status Codes:**
- `200 OK`: Successful GET/PUT request
- `201 Created`: Successful POST request
- `204 No Content`: Successful DELETE request
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Key Features

#### 1. Soft Delete
Financial records are soft-deleted (marked as deleted but not removed from database).

#### 2. Pagination
All list endpoints support pagination:
```bash
?page=1&page_size=20
```

#### 3. Filtering and Search
- **Date Range**: `?start_date=2024-01-01&end_date=2024-01-31`
- **Type**: `?type=income`
- **Category**: `?category=salary`
- **Search**: `?search=bonus`

#### 4. Comprehensive Analytics
- Dashboard summary: income, expenses, net balance
- Category-wise breakdown
- Monthly trends
- Recent activity
- Custom date range statistics

#### 5. Bulk Operations
Create multiple records in a single request:
```json
{
  "records": [
    {...},
    {...}
  ]
}
```

### Practical Examples

#### Example 1: Complete Workflow for Analytics User

```bash
# Variables
TOKEN="<your-analyst-token>"
API_URL="http://localhost:8000/api/v1"

# 1. Get your profile
curl -X GET "$API_URL/users/me/" \
  -H "Authorization: Token $TOKEN"

# 2. Create a new income record
curl -X POST "$API_URL/records/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "5000.00",
    "record_type": "income",
    "category": "salary",
    "date": "2024-01-15",
    "description": "Monthly salary"
  }'

# 3. View all records
curl -X GET "$API_URL/records/" \
  -H "Authorization: Token $TOKEN"

# 4. Get dashboard summary
curl -X GET "$API_URL/records/summary/" \
  -H "Authorization: Token $TOKEN"

# 5. Get comprehensive dashboard overview
curl -X GET "$API_URL/dashboard/overview/" \
  -H "Authorization: Token $TOKEN"
```

#### Example 2: Admin Managing Users

```bash
# Variables
ADMIN_TOKEN="<your-admin-token>"
API_URL="http://localhost:8000/api/v1"

# 1. List all users
curl -X GET "$API_URL/users/" \
  -H "Authorization: Token $ADMIN_TOKEN"

# 2. Create a new user
curl -X POST "$API_URL/users/" \
  -H "Authorization: Token $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "SecurePassword123!",
    "password2": "SecurePassword123!",
    "first_name": "New",
    "last_name": "User",
    "role": 2,
    "status": "active"
  }'

# 3. Get list of roles
curl -X GET "$API_URL/roles/" \
  -H "Authorization: Token $ADMIN_TOKEN"
```

#### Example 3: Bulk Create Records

```bash
TOKEN="<your-analyst-token>"
API_URL="http://localhost:8000/api/v1"

# Create multiple records at once
curl -X POST "$API_URL/records/bulk_create/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {
        "amount": "50.00",
        "record_type": "expense",
        "category": "food",
        "date": "2024-01-10",
        "description": "Groceries"
      }
    ]
  }'
```

#### Example 4: Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"
TOKEN = "<your-token>"

headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

# Create a record
record_data = {
    "amount": "5000.00",
    "record_type": "income",
    "category": "salary",
    "date": "2024-01-15"
}

response = requests.post(
    f"{BASE_URL}/records/",
    headers=headers,
    json=record_data
)

if response.status_code == 201:
    print("Record created:", response.json())
```

---

## Architecture & Design

### Architecture Overview

The backend follows a **layered architecture** pattern with clear separation of concerns:

```
API Layer (Views)
       ↓
Business Logic Layer (Services)
       ↓
Data Access Layer (Serializers, Models)
       ↓
Database (PostgreSQL)
```

### Key Design Decisions

#### 1. Custom User Model
- Extended Django's `AbstractUser` with UUID PK
- Added `role` and `status` fields
- Standard practice in professional Django projects

#### 2. Role-Based Access Control (RBAC)
- Separate `Role` model for flexibility
- Three roles: Viewer, Analyst, Admin
- Permission classes enforce access control

#### 3. Service Layer Pattern
- `FinancialSummaryService` handles business logic
- Separates logic from HTTP concerns
- Testable and reusable

#### 4. Soft Delete Pattern
- Records marked as deleted, not removed
- Allows data recovery
- `is_deleted` field indexed for performance

#### 5. UUID Primary Keys
- Better for distributed systems
- Harder to guess or enumerate
- Provides better privacy

#### 6. Serializer Pattern
- Separate serializers for create/update vs. read
- Prevents over-exposure of data
- Input validation separate from output

#### 7. Pagination Strategy
- `PageNumberPagination` with configurable page size
- Default 20 items per page
- Max 100 items per page

#### 8. Error Handling
- Custom exception handler
- Consistent error format across all endpoints
- Structured error information

#### 9. Database Indexes
- Composite indexes on `(user, date)`, `(user, record_type)`, `(user, category)`
- Index on `is_deleted` for soft delete queries
- Optimizes frequent query patterns

#### 10. Token Authentication
- Django REST Framework's built-in `TokenAuthentication`
- Simple and stateless
- Standard for REST APIs

### Security Decisions

#### Token Authentication Only
- No password transmission in API
- Tokens can be revoked independently
- Better for third-party integrations

#### Permission Classes Enforcement
- All APIs require authentication
- Explicit access control at view level
- Role-based checks on every endpoint

#### Status-Based Access Control
- User `status` field (active, inactive, suspended)
- Quick user lockout without deletion
- Reversible action

### Future Scalability Considerations

#### Caching Layer
- Redis for dashboard summaries
- User roles, category lists

#### Background Jobs
- Celery tasks for reports
- Email notifications
- Data cleanup/archival

#### Read Replicas
- Database read replicas for analytics
- Higher throughput for read-heavy operations

#### API Versioning
- All endpoints under `/api/v1/`
- Future versions for backward compatibility

#### Microservices
- Decompose into Auth, Records, Analytics services
- Current monolithic approach supports this

---

## Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test class
python manage.py test finance.tests.RoleTestCase

# Run with pytest
pytest

# Run with coverage
pytest --cov=finance
```

---

## Deployment Guide

### Pre-Deployment Checklist

- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` is strong
- [ ] `ALLOWED_HOSTS` configured
- [ ] Database configured for production
- [ ] Static files configured
- [ ] Logging configured
- [ ] Error tracking set up (Sentry)
- [ ] All tests pass
- [ ] Database backups configured

### Option 1: Traditional Server (Ubuntu/Debian)

#### 1. Install Dependencies
```bash
sudo apt-get update
sudo apt-get install python3 python3-venv postgresql postgresql-contrib nginx supervisor
```

#### 2. Setup Application
```bash
sudo useradd -m -s /bin/bash finance_app
sudo su - finance_app
cd /home/finance_app
git clone <repository> finance_backend
cd finance_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Configure Django
```bash
cp .env.example .env
# Edit .env with production settings
python manage.py migrate
python manage.py collectstatic --noinput
```

#### 4. Setup Gunicorn
```bash
pip install gunicorn
# Create gunicorn_config.py with worker configuration
```

#### 5. Configure Supervisor and Nginx
- Create supervisor config for Gunicorn
- Configure Nginx as reverse proxy
- Setup SSL with Let's Encrypt

### Option 2: Docker Deployment

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "finance_backend.wsgi:application"]
```

```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: finance_db
      POSTGRES_PASSWORD: postgres
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
```

### Option 3: Heroku Deployment

Create `Procfile`:
```
web: gunicorn finance_backend.wsgi:application --log-file -
release: python manage.py migrate
```

Deploy:
```bash
heroku login
heroku create finance-backend
git push heroku main
```

### Option 4: AWS Elastic Beanstalk

Create `.ebextensions/django.config` for deployment to AWS.

### Post-Deployment

1. Database backups
2. Monitoring setup (Sentry, logs)
3. Performance optimization (caching, CDN)
4. Security hardening (HTTPS, headers)
5. Automated backups

---

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
python manage.py runserver 8001
```

#### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

#### Database Connection Issues
- Check PostgreSQL is running
- Verify credentials in .env
- Increase connection pool size

#### Slow API Responses
- Check database indexes
- Profile slow queries
- Implement pagination
- Add caching layer

### Common Tasks

#### Create Test Data
```bash
python manage.py shell
from datetime import date
from decimal import Decimal
from finance.models import CustomUser, FinancialRecord

user = CustomUser.objects.get(username='analyst')
FinancialRecord.objects.create(
    user=user,
    amount=Decimal('5000.00'),
    record_type='income',
    category='salary',
    date=date.today()
)
```

#### Reset Database
```bash
# Delete all data
python manage.py flush

# Or for SQLite
rm db.sqlite3
python manage.py migrate
```

#### Create Another Admin
```bash
python manage.py createsuperuser
```

---

## Performance Considerations

### Database Indexes
- Composite index on `(user, date)`
- Composite index on `(user, record_type)`
- Composite index on `(user, category)`
- Index on `is_deleted` for soft delete queries

### Query Optimization
- Queryset filtering at database level
- Use of select_related for foreign keys
- Pagination to limit result size

---

## Logging

Logs are written to:
- **Console**: All log levels
- **File**: `logs/debug.log`

Configure log level in `settings.py`:
```python
'level': 'DEBUG',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

---

## Future Enhancements

- [ ] JWT token authentication with refresh tokens
- [ ] Celery tasks for background processing
- [ ] Cache layer using Redis
- [ ] Email notifications for record creation
- [ ] Advanced filtering and export functionality
- [ ] Support for budget tracking and alerts
- [ ] Multi-currency support
- [ ] Recurring transactions

---

## Key Files to Understand

1. **models.py**: Core data models (User, Role, Record)
2. **views.py**: All API endpoints
3. **permissions.py**: Role-based access control
4. **serializers.py**: Data validation and representation
5. **services.py**: Business logic for analytics
6. **tests.py**: Comprehensive test suite

---

## Summary

This is a **complete, well-documented, production-ready backend** that:

- ✅ Implements all core requirements
- ✅ Includes best practices and patterns
- ✅ Is thoroughly tested
- ✅ Is comprehensively documented
- ✅ Is secure by design
- ✅ Is scalable and maintainable

**Total Implementation**: 
- ~3000+ lines of production code
- ~650+ lines of tests
- 25+ API endpoints
- 30+ test cases

---

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions, review the troubleshooting section or examine test cases for usage patterns.

Happy coding! 🚀

# Run with coverage
pytest --cov=finance
```

## Logging

Logs are written to:
- **Console**: All log levels
- **File**: `logs/debug.log`

Configure log level in `settings.py`:
```python
'level': 'DEBUG',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## Performance Considerations

### Database Indexes
- Composite index on `(user, date)`
- Composite index on `(user, record_type)`
- Composite index on `(user, category)`
- Index on `is_deleted` for soft delete queries

### Query Optimization
- Queryset filtering at database level
- Use of select_related for foreign keys
- Pagination to limit result size

## Future Enhancements

- [ ] JWT token authentication with refresh tokens
- [ ] Celery tasks for background processing
- [ ] Cache layer using Redis
- [ ] Email notifications for record creation
- [ ] Advanced filtering and export functionality
- [ ] Support for budget tracking and alerts
- [ ] Multi-currency support
- [ ] Recurring transactions
- [ ] Mobile app API optimizations

## Troubleshooting

### Database Connection Error
```
django.db.utils.OperationalError: could not connect to server
```
**Solution**: Ensure PostgreSQL is running and credentials in `.env` are correct.

### Migration Error
```
django.db.migrations.exceptions.MigrationSƒ
```
**Solution**: Check for circular dependencies or invalid model references.

### Permission Denied Error
**Solution**: Check user's role and ensure it has required permissions for the action.

### CORS Issues
**Solution**: Update `CORS_ALLOWED_ORIGINS` in `.env` to include your frontend URL.

## Assumptions Made

1. **PostgreSQL Database**: Project assumes PostgreSQL for production. SQLite can be used for development by modifying `.env`.

2. **Token Authentication**: Uses DRF's built-in TokenAuthentication. In production, consider using JWT tokens.

3. **Timezone**: All timestamps are in UTC. Set `TIME_ZONE` in `settings.py` as needed.

4. **Date Format**: All dates should be in ISO 8601 format (YYYY-MM-DD).

5. **Soft Deletes**: Deleted records are marked but not removed, allowing for recovery and audit trails.

6. **Role-Based Access**: Access control is enforced at API level using permission classes.

## Deployment Considerations

### Security
- Set `DEBUG = False` in production
- Use strong `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Use HTTPS only
- Set secure cookie flags in session settings

### Database
- Use managed database service (AWS RDS, Azure Database, etc.)
- Regular backups
- Connection pooling
- Read replicas for scaling

### Performance
- Use Gunicorn or uWSGI as WSGI server
- Nginx as reverse proxy
- Redis for caching
- CDN for static files

### Monitoring
- Application performance monitoring (APM)
- Error tracking (Sentry)
- Log aggregation (ELK, CloudWatch)
- Health checks and alerts

## Code Organization Principles

1. **Separation of Concerns**: Views handle HTTP, serializers handle data validation, services handle business logic
2. **DRY (Don't Repeat Yourself)**: Reusable permission classes, serializers, and services
3. **Clear Naming**: Descriptive names for models, views, and functions
4. **Documentation**: Models, viewsets, and complex functions are documented
5. **Test Coverage**: Unit tests for models and services, integration tests for APIs

## Contributing

When contributing to this project:
1. Write tests for new features
2. Ensure all tests pass
3. Follow PEP 8 style guide
4. Add docstrings to functions and classes
5. Update API documentation if adding endpoints

## License

This project is provided as-is for assessment purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Check test files for usage examples
4. Review model docstrings for implementation details
