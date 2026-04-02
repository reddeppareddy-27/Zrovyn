# Quick Start Guide

Get the Finance Backend up and running in 5 minutes.

## Prerequisites

- Python 3.8+
- PostgreSQL (or SQLite for testing)
- Git

## Installation (5 minutes)

### 1. Clone and Navigate

```bash
cd finance_backend
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure for Development

```bash
# Copy environment template
cp .env.example .env

# For development with SQLite (no PostgreSQL needed):
# Edit .env and change DB_ENGINE to:
# DB_ENGINE=django.db.backends.sqlite3
# DB_NAME=db.sqlite3
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Roles and Users

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
Role.objects.get(name='admin')
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

### 7. Start Server

```bash
python manage.py runserver
```

Server runs at: `http://localhost:8000`

## Quick API Test

### Get Authentication Token

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

### Test the API

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

## Using Django Admin

1. Go to `http://localhost:8000/admin/`
2. Login with `admin` / `admin123`
3. Manage users, roles, and records via the admin interface

## Project Structure

```
finance_backend/
├── manage.py              # Django management
├── requirements.txt       # Dependencies
├── .env.example          # Configuration template
│
├── finance_backend/      # Django settings
│   ├── settings.py       # Configuration
│   └── urls.py          # URL routing
│
├── finance/              # Main app
│   ├── models.py        # Data models
│   ├── views.py         # API endpoints
│   ├── serializers.py   # Data validation
│   ├── permissions.py   # Access control
│   ├── services.py      # Business logic
│   ├── tests.py         # Unit tests
│   └── urls.py          # App URLs
│
├── README.md            # Full documentation
├── API_USAGE_GUIDE.md   # API examples
└── DESIGN_DECISIONS.md  # Architecture docs
```

## Available Roles and Permissions

| Role | Create Records | View Records | Delete Records | Manage Users |
|------|----------------|--------------|----------------|-------------|
| Viewer | ❌ | ✅ Own | ❌ | ❌ |
| Analyst | ✅ | ✅ Own | ❌ | ❌ |
| Admin | ✅ | ✅ All | ✅ | ✅ |

## API Endpoints Quick Reference

### Records
- `GET /api/v1/records/` - List your records
- `POST /api/v1/records/` - Create (Analyst+)
- `GET /api/v1/records/{id}/` - View
- `PUT /api/v1/records/{id}/` - Update (Analyst+)
- `DELETE /api/v1/records/{id}/` - Delete (Admin)

### Analytics
- `GET /api/v1/records/summary/` - Dashboard summary
- `GET /api/v1/records/category_summary/` - By category
- `GET /api/v1/records/monthly_summary/` - Monthly trends
- `GET /api/v1/dashboard/overview/` - Complete overview
- `GET /api/v1/dashboard/insights/` - Financial insights

### Users (Admin)
- `GET /api/v1/users/` - List users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/me/` - Your profile
- `PUT /api/v1/users/{id}/` - Update

## Running Tests

```bash
# Run all tests
python manage.py test

# Run with pytest
pytest

# Run specific test
python manage.py test finance.tests.FinancialRecordTestCase
```

## Common Tasks

### Create Test Data

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
    date=date.today(),
    description='Test salary'
)
```

### Reset Database

```bash
# Delete all data (keeping migrations)
python manage.py flush

# Or completely reset (for SQLite)
rm db.sqlite3
python manage.py migrate
```

### Create Another Admin

```bash
python manage.py createsuperuser
```

## Troubleshooting

### Reset for PostgreSQL

```bash
# If using PostgreSQL and something breaks
dropdb finance_db
createdb finance_db
python manage.py migrate
```

### Port Already in Use

```bash
# Run on different port
python manage.py runserver 8001
```

### ModuleNotFoundError

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Database Locked (SQLite)

```bash
# Restart server - SQLite releases locks automatically
```

## Next Steps

1. **Read Full Documentation**: See [README.md](README.md)
2. **Learn the API**: Check [API_USAGE_GUIDE.md](API_USAGE_GUIDE.md)
3. **Architecture Overview**: See [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md)
4. **Deploy**: See [DEPLOYMENT.md](DEPLOYMENT.md)

## Example: Complete Workflow

```bash
# 1. Activate environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Start server
python manage.py runserver

# 3. In another terminal, get token
TOKEN=$(python manage.py shell << EOF
from rest_framework.authtoken.models import Token
from finance.models import CustomUser
user = CustomUser.objects.get(username='analyst')
token = Token.objects.get_or_create(user=user)[0]
print(token.key)
EOF
)

# 4. Create a record
curl -X POST http://localhost:8000/api/v1/records/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "1500.00",
    "record_type": "expense",
    "category": "food",
    "date": "2024-01-15"
  }'

# 5. View summary
curl -X GET http://localhost:8000/api/v1/records/summary/ \
  -H "Authorization: Token $TOKEN"
```

## Key Files to Understand

1. **models.py**: Core data models (User, Role, Record)
2. **views.py**: All API endpoints
3. **permissions.py**: Role-based access control
4. **serializers.py**: Data validation and representation
5. **services.py**: Business logic for analytics

## Support

- Check [README.md](README.md) for detailed documentation
- Review [API_USAGE_GUIDE.md](API_USAGE_GUIDE.md) for examples
- Check test cases in [tests.py](finance/tests.py) for usage patterns
- Review [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) for architecture

Happy coding! 🚀
