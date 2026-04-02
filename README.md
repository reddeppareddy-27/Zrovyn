# Finance Dashboard Backend

A Django-based backend API for a finance dashboard system with role-based access control, financial record management, and advanced analytics.

## Overview

This project implements a robust finance management system backend with the following features:

- **User and Role Management**: Support for Viewer, Analyst, and Admin roles with granular permission controls
- **Financial Records Management**: CRUD operations for financial transactions with validation
- **Dashboard Analytics**: Summary-level APIs for income, expenses, and financial insights
- **Access Control**: Role-based permission system for data protection
- **Error Handling**: Comprehensive validation and error responses
- **Data Persistence**: PostgreSQL database for reliable data storage

## Tech Stack

- **Framework**: Django 4.2.8 + Django REST Framework 3.14.0
- **Database**: PostgreSQL
- **Authentication**: Token-based authentication
- **Additional**: CORS support, comprehensive logging, pagination

## Project Structure

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

## Prerequisites

- Python 3.8+
- PostgreSQL 10+
- pip or conda for dependency management

## Setup Instructions

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

## Role-Based Access Control

### Viewer Role
- ✅ View own financial records
- ✅ Access dashboard summaries
- ✅ View analytics and insights
- ❌ Cannot create or edit records
- ❌ Cannot manage users

### Analyst Role
- ✅ View own financial records
- ✅ Create and edit own records
- ✅ Access all dashboard analytics
- ✅ View user list
- ✅ Bulk create records
- ❌ Cannot delete records
- ❌ Cannot manage users (except viewing)
- ❌ Cannot manage system roles

### Admin Role
- ✅ Full access to all records
- ✅ Create, read, update, delete records (any user's)
- ✅ Create and manage users
- ✅ Manage roles and permissions
- ✅ View all system data
- ✅ Access all analytics for any user
- ✅ Perform all administrative actions

## Data Models

### CustomUser
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

### Role
Defines user roles and permissions.

**Fields:**
- `name` (choice): viewer | analyst | admin
- `description` (text): Role description
- `created_at` (datetime): Creation timestamp

### FinancialRecord
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

## Validation and Error Handling

### Input Validation

- **Amount**: Must be positive (> 0)
- **Date**: Cannot be in the future
- **Required Fields**: Enforced on all models
- **Enum Values**: Type, category, status must be valid choices

### Error Responses

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

## Key Features

### 1. Soft Delete
Financial records are soft-deleted (marked as deleted but not removed from database).

### 2. Pagination
All list endpoints support pagination:
```bash
?page=1&page_size=20
```

### 3. Filtering and Search
- **Date Range**: `?start_date=2024-01-01&end_date=2024-01-31`
- **Type**: `?type=income`
- **Category**: `?category=salary`
- **Search**: `?search=bonus`

### 4. Comprehensive Analytics
- Dashboard summary: income, expenses, net balance
- Category-wise breakdown
- Monthly trends
- Recent activity
- Custom date range statistics

### 5. Bulk Operations
Create multiple records in a single request:
```json
{
  "records": [
    {...},
    {...}
  ]
}
```

## Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test class
python manage.py test finance.tests.RoleTestCase

# Run specific test method
python manage.py test finance.tests.RoleTestCase.test_role_creation

# Run with pytest
pytest

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
