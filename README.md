# 💰 Finance Dashboard Backend

A professional Django REST Framework API for financial record management with role-based access control and comprehensive analytics.

---

## 🔐 Quick Credentials

Use these credentials to access the live application:

### Admin Account
- **URL**: `https://zrovyn-finance-backend.onrender.com/admin/`
- **Username**: `admin`
- **Password**: `admin123`
- **Permissions**: Full access - manage users, roles, records, and complete administrative control

### Analyst Account
- **Username**: `reddy`
- **Password**: `analyst123`
- **Permissions**: Create records, edit own records, view all records and analytics

### Viewer Account
- **Username**: `bhanu`
- **Password**: `viewer123`
- **Permissions**: View all records and analytics (read-only)

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Live Deployment](#live-deployment)
3. [Features](#features)
4. [Technology Stack](#technology-stack)
5. [Local Setup](#local-setup)
6. [API Endpoints](#api-endpoints)
7. [Access Control](#access-control)
8. [Testing](#testing)
9. [Deployment](#deployment)

---

## 🎯 Overview

Finance Dashboard Backend is a complete solution for managing financial records with:
- **User Management**: Admin, Analyst, and Viewer roles
- **Financial Records**: Full CRUD with role-based restrictions
- **Analytics**: Dashboard summaries, trends, and statistics
- **Access Control**: Enforced at both view and object levels
- **Data Validation**: Comprehensive input validation
- **Persistent Storage**: PostgreSQL database

---

## 🚀 Live Deployment

**Status**: ✅ **LIVE ON RENDER**

**API Base URL**: `https://zrovyn-finance-backend.onrender.com`

**Admin Panel**: `https://zrovyn-finance-backend.onrender.com/admin/`

All endpoints are fully functional and tested.

---

## ✨ Features

### 1. User & Role Management
- ✅ Three predefined roles (Viewer, Analyst, Admin)
- ✅ User status management (active, inactive, suspended)
- ✅ UUID-based user identification
- ✅ Token authentication for API access

### 2. Financial Records Management
- ✅ Create, read, update, delete operations
- ✅ Income and expense record types
- ✅ 10 financial categories
- ✅ Date-based filtering
- ✅ Soft delete functionality
- ✅ Bulk create support

### 3. Dashboard Analytics
- ✅ Overall financial summary (income, expenses, balance)
- ✅ Category-wise breakdown
- ✅ Monthly trends (last 12 months)
- ✅ Recent activity feed
- ✅ Statistics for date ranges
- ✅ Record count by type and category

### 4. Access Control
- ✅ Role-based permissions at view level
- ✅ Object-level permissions for record editing
- ✅ Automatic user assignment on creation
- ✅ Admin override capabilities

### 5. Additional Features
- ✅ Search and filtering
- ✅ Pagination support
- ✅ Comprehensive error handling
- ✅ API documentation
- ✅ Production logging

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | Django 4.2.8 |
| API | Django REST Framework 3.14.0 |
| Database | PostgreSQL |
| Authentication | Token-based |
| Hosting | Render |
| Server | Gunicorn |
| Reverse Proxy | Nginx (on Render) |

---

## 💻 Local Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment manager (venv)

### Installation

#### 1. Clone Repository
```bash
git clone https://github.com/reddeppareddy-27/Zrovyn.git
cd finance_backend
```

#### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env - For local development, SQLite will be used by default
# No additional configuration needed for SQLite
```

#### 5. Run Migrations
```bash
python manage.py migrate
```

#### 6. Create Superuser
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

#### 7. Create Test Users
```bash
python manage.py manage.py create_admin
```

#### 8. Start Development Server
```bash
python manage.py runserver
```

Server will run at: `http://localhost:8000`

---

## 🔌 Complete API Endpoints Reference

### Base URL
```
https://zrovyn-finance-backend.onrender.com/api/v1/
```

### 🔐 Authentication

#### Get Authentication Token
```
POST /api/v1/api-token-auth/

Body:
{
  "username": "reddy",
  "password": "analyst123"
}

Response:
{
  "token": "your-unique-token-here"
}

Usage: Include in all requests as: Authorization: Token <token>
```

---

### 👥 User Management Endpoints

#### List All Users (Admin Only)
```
GET /api/v1/users/

Headers: Authorization: Token <admin-token>
Response: List of all users with details
```

#### Create New User (Admin Only)
```
POST /api/v1/users/

Headers: Authorization: Token <admin-token>
Body:
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "password2": "SecurePassword123!",
  "first_name": "First",
  "last_name": "Last",
  "role": 1,
  "status": "active"
}
```

#### Get User Details
```
GET /api/v1/users/{user-id}/

Headers: Authorization: Token <token>
Response: User details including role and status
```

#### Get Current User Profile
```
GET /api/v1/users/me/

Headers: Authorization: Token <token>
Response: Current authenticated user's profile
```

#### Update User (Admin Only)
```
PATCH /api/v1/users/{user-id}/

Headers: Authorization: Token <admin-token>
Body:
{
  "email": "newemail@example.com",
  "first_name": "Updated",
  "role": 2,
  "status": "active"
}
```

#### Delete User (Admin Only)
```
DELETE /api/v1/users/{user-id}/

Headers: Authorization: Token <admin-token>
Response: 204 No Content (soft delete)
```

---

### 👤 Roles Endpoints

#### List All Roles
```
GET /api/v1/roles/

Headers: Authorization: Token <token>
Response: [
  {
    "name": "viewer",
    "description": "Read-only access"
  },
  {
    "name": "analyst",
    "description": "Can view and analyze"
  },
  {
    "name": "admin",
    "description": "Full access"
  }
]
```

---

### 💰 Financial Records Endpoints

#### List All Records
```
GET /api/v1/records/

Headers: Authorization: Token <token>
Query Parameters:
  - start_date=YYYY-MM-DD (filter from date)
  - end_date=YYYY-MM-DD (filter to date)
  - type=income|expense (filter by type)
  - category=salary|food|transport|... (filter by category)
  - search=text (search in description)
  - page=1 (page number)
  - page_size=20 (items per page)

Example:
GET /api/v1/records/?type=income&start_date=2024-01-01&end_date=2024-12-31
```

#### Get Specific Record by ID
```
GET /api/v1/records/{record-id}/

Headers: Authorization: Token <token>
Response: Single record with all details
```

#### Create New Record
```
POST /api/v1/records/

Headers: Authorization: Token <token>
        Content-Type: application/json

Body:
{
  "amount": "5000.00",
  "record_type": "income",
  "category": "salary",
  "date": "2024-01-15",
  "description": "Monthly salary"
}

Valid Categories: salary, bonus, investment, food, transport, utilities, 
                  entertainment, healthcare, education, other
```

#### Update Record by ID (Own Records Only)
```
PATCH /api/v1/records/{record-id}/

Headers: Authorization: Token <token>
        Content-Type: application/json

Body:
{
  "amount": "5500.00",
  "description": "Updated salary amount",
  "date": "2024-01-15"
}

Note: Only record owner or admin can update
```

#### Full Update Record by ID
```
PUT /api/v1/records/{record-id}/

Headers: Authorization: Token <token>
        Content-Type: application/json

Body: (All fields required)
{
  "amount": "5500.00",
  "record_type": "income",
  "category": "salary",
  "date": "2024-01-15",
  "description": "Updated description"
}
```

#### Delete Record by ID
```
DELETE /api/v1/records/{record-id}/

Headers: Authorization: Token <token>
Response: 204 No Content (soft delete)

Note: Only admin can delete
```

#### Create Multiple Records (Bulk)
```
POST /api/v1/records/bulk_create/

Headers: Authorization: Token <token>
        Content-Type: application/json

Body:
{
  "records": [
    {
      "amount": "5000.00",
      "record_type": "income",
      "category": "salary",
      "date": "2024-01-15",
      "description": "Salary"
    },
    {
      "amount": "100.00",
      "record_type": "expense",
      "category": "food",
      "date": "2024-01-16",
      "description": "Lunch"
    }
  ]
}
```

---

### 📊 Analytics & Dashboard Endpoints

#### Get Overall Summary
```
GET /api/v1/records/summary/

Headers: Authorization: Token <token>
Response:
{
  "total_income": 50000.00,
  "total_expenses": 15000.00,
  "net_balance": 35000.00,
  "total_records": 42,
  "records_count_by_type": {"income": 25, "expense": 17},
  "records_count_by_category": {...}
}
```

#### Get Category Breakdown
```
GET /api/v1/records/category_summary/

Headers: Authorization: Token <token>
Response: List of categories with totals and counts
```

#### Get Monthly Trends
```
GET /api/v1/records/monthly_summary/

Headers: Authorization: Token <token>
Query Parameters:
  - months=12 (number of months)

Response: Monthly income, expenses, and net for last 12 months
```

#### Get Recent Activity
```
GET /api/v1/records/recent_activity/

Headers: Authorization: Token <token>
Query Parameters:
  - limit=10 (number of records)

Response: Latest transactions with user info
```

#### Get Statistics for Date Range
```
GET /api/v1/records/statistics/?start_date=2024-01-01&end_date=2024-12-31

Headers: Authorization: Token <token>
Query Parameters: (Required)
  - start_date=YYYY-MM-DD
  - end_date=YYYY-MM-DD

Response: Statistics including totals, counts, averages for period
```

---

### 🎛️ Admin Panel

#### Django Admin Interface
```
URL: https://zrovyn-finance-backend.onrender.com/admin/

Login Credentials:
- Username: admin
- Password: admin123

Access: Full management of users, roles, and records
```

---

### 📋 Common Query Examples

#### Get Income Records from January 2024
```
GET /api/v1/records/?type=income&start_date=2024-01-01&end_date=2024-01-31
```

#### Get Food Expenses
```
GET /api/v1/records/?type=expense&category=food
```

#### Search for "bonus" in descriptions
```
GET /api/v1/records/?search=bonus
```

#### Get page 2 with 50 items per page
```
GET /api/v1/records/?page=2&page_size=50
```

#### Get statistics for Q1 2024
```
GET /api/v1/records/statistics/?start_date=2024-01-01&end_date=2024-03-31
```

#### Get last 3 months trends
```
GET /api/v1/records/monthly_summary/?months=3
```

---

## 🔐 Access Control

### Permission Matrix

| Action | Viewer | Analyst | Admin |
|--------|--------|---------|-------|
| View Records | ✅ All | ✅ All | ✅ All |
| Create Records | ❌ | ✅ | ✅ |
| Edit Own Records | ❌ | ✅ | ✅ |
| Edit Any Records | ❌ | ❌ | ✅ |
| Delete Records | ❌ | ❌ | ✅ |
| View Analytics | ✅ | ✅ | ✅ |
| Manage Users | ❌ | ❌ | ✅ |
| Access Admin Panel | ❌ | ❌ | ✅ |

### How It Works
- **Viewers**: Read-only access to all records and analytics
- **Analysts**: Can create and edit their own records, view all data
- **Admins**: Full access to everything, including user management

---

## 🧪 Testing

### Get Authentication Token
```bash
curl -X POST https://zrovyn-finance-backend.onrender.com/api/v1/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "reddy", "password": "analyst123"}'
```

### Create a Record
```bash
curl -X POST https://zrovyn-finance-backend.onrender.com/api/v1/records/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "5000.00",
    "record_type": "income",
    "category": "salary",
    "date": "2024-01-15",
    "description": "Monthly salary"
  }'
```

### Get Summary
```bash
curl -X GET https://zrovyn-finance-backend.onrender.com/api/v1/records/summary/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Get All Records
```bash
curl -X GET https://zrovyn-finance-backend.onrender.com/api/v1/records/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Run Tests Locally
```bash
# Run all tests
python manage.py test

# Run with coverage
pytest --cov=finance

# Run specific test
python manage.py test finance.tests.YourTestClass
```

---

## 📦 Deployment

### Requirements Met
- ✅ User and role management (Viewer, Analyst, Admin)
- ✅ Financial records CRUD operations
- ✅ Dashboard summary APIs
- ✅ Role-based access control
- ✅ Input validation and error handling
- ✅ Data persistence (PostgreSQL)

### Production Setup (Render)
1. Push code to GitHub
2. Create Web Service on Render
3. Configure environment variables
4. Render automatically:
   - Installs dependencies
   - Runs migrations
   - Creates admin user
   - Starts Gunicorn server

### Environment Variables
```
DEBUG=False
SECRET_KEY=<strong-secret-key>
ALLOWED_HOSTS=zrovyn-finance-backend.onrender.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=backend_intern_iql5
DB_USER=backend_intern
DB_PASSWORD=<password>
DB_HOST=<postgres-host>
DB_PORT=5432
```

---

## 📊 Project Structure

```
finance_backend/
├── finance/                          # Main application
│   ├── models.py                    # Data models
│   ├── views.py                     # API endpoints
│   ├── serializers.py               # Data serialization
│   ├── permissions.py               # Access control
│   ├── services.py                  # Business logic
│   ├── utils.py                     # Utility functions
│   ├── tests.py                     # Test suite
│   ├── urls.py                      # URL routing
│   ├── admin.py                     # Django admin config
│   └── migrations/                  # Database migrations
├── finance_backend/                  # Project settings
│   ├── settings.py                  # Django configuration
│   ├── urls.py                      # Main URL routing
│   └── wsgi.py                      # WSGI application
├── manage.py                        # Django management
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables
├── render.yaml                      # Render deployment config
├── README.md                        # This file
└── db.sqlite3                       # Local database (development)
```

---

## 🚀 Features Implemented

### Core Requirements
- ✅ **User Management**: Create, update, delete users with roles
- ✅ **Role-Based Access**: Viewer (read), Analyst (create/edit), Admin (full)
- ✅ **Financial Records**: Complete CRUD with filtering
- ✅ **Analytics**: Summary, trends, statistics APIs
- ✅ **Access Control**: Enforced at request and object levels
- ✅ **Validation**: Input validation on all endpoints
- ✅ **Error Handling**: Consistent error responses with proper status codes
- ✅ **Persistence**: PostgreSQL with proper indexing

### Additional Features
- ✅ Token authentication
- ✅ Pagination and filtering
- ✅ Search functionality
- ✅ Soft delete pattern
- ✅ Bulk operations
- ✅ Rate limiting ready
- ✅ Comprehensive logging
- ✅ API documentation

---

## 🔧 Configuration

### Database
- **Production**: PostgreSQL on Render (persistent)
- **Development**: SQLite (local)

### Authentication
- Token-based using DRF's `TokenAuthentication`
- Each login generates a unique token
- Include token in `Authorization: Token <token>` header

### Pagination
- Default: 20 items per page
- Maximum: 100 items per page
- Configurable per request

---

## 📝 API Response Examples

### Success Response
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_username": "reddy",
  "amount": "5000.00",
  "record_type": "income",
  "category": "salary",
  "description": "Monthly salary",
  "date": "2024-01-15",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Error Response
```json
{
  "error": "start_date and end_date query parameters are required."
}
```

---

## 🐛 Troubleshooting

### Database Connection Error
```
Error: could not connect to server
```
**Solution**: Ensure PostgreSQL is running and credentials in `.env` are correct.

### Permission Denied Error
```
Error: You do not have permission to update this record.
```
**Solution**: Verify your user role and ensure you're updating your own record (or are admin).

### CORS Issues
```
Error: CORS policy block
```
**Solution**: Update `CORS_ALLOWED_ORIGINS` in `.env` to include your frontend URL.

---

## 📚 Documentation

- **API Docs**: Available at `/api/v1/`
- **Admin Panel**: Available at `/admin/`
- **Source Code**: Fully commented and documented

---

## ✉️ Support

For issues or questions:
1. Check the troubleshooting section
2. Review API examples in this README
3. Check test files for usage patterns
4. Review model docstrings in `models.py`

---

## 📄 License

This project is provided as-is for assessment and educational purposes.

---

## 🎉 Summary

This is a **complete, production-ready Django REST Backend** that:
- ✅ Meets all core requirements
- ✅ Implements best practices
- ✅ Is fully tested and documented
- ✅ Is live on Render
- ✅ Ready for immediate use

**Deploy Status**: 🚀 **LIVE AND FULLY FUNCTIONAL**

---

**Created**: April 3, 2026  
**Status**: Production Ready  
**Version**: 1.0
