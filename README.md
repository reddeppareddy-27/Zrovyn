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

## 🔌 API Endpoints

### Authentication
```
POST /api/v1/api-token-auth/
  Body: {"username": "reddy", "password": "analyst123"}
  Returns: {"token": "your-token-here"}
```

### Financial Records
```
GET    /api/v1/records/                    - List all records
POST   /api/v1/records/                    - Create new record
GET    /api/v1/records/{id}/               - Get record details
PATCH  /api/v1/records/{id}/               - Update record
DELETE /api/v1/records/{id}/               - Delete record
POST   /api/v1/records/bulk_create/        - Create multiple records
```

### Analytics
```
GET /api/v1/records/summary/               - Overall summary
GET /api/v1/records/category_summary/      - Category breakdown
GET /api/v1/records/monthly_summary/       - Monthly trends
GET /api/v1/records/recent_activity/       - Recent transactions
GET /api/v1/records/statistics/            - Date range statistics
```

### Users
```
GET    /api/v1/users/                      - List users (admin only)
POST   /api/v1/users/                      - Create user (admin only)
GET    /api/v1/users/{id}/                 - Get user details
GET    /api/v1/users/me/                   - Current user profile
PATCH  /api/v1/users/{id}/                 - Update user
DELETE /api/v1/users/{id}/                 - Delete user (admin only)
```

### Roles
```
GET /api/v1/roles/                         - List all roles
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
