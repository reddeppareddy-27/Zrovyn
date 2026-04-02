# API Usage Guide

This guide provides practical examples for using the Finance Backend API.

## Getting Started

### 1. Start the Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/v1/`

### 2. Access Django Admin

Navigate to `http://localhost:8000/admin/` and log in with your superuser credentials.

## Authentication

The API uses Token Authentication. You need to get a token before making API requests.

### Get Token

First, create a user through Django admin or use the create user endpoint.

To get the token:

```bash
curl -X POST http://localhost:8000/api-auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

Or through Django shell:

```bash
python manage.py shell

from rest_framework.authtoken.models import Token
from finance.models import CustomUser

user = CustomUser.objects.get(username='your_username')
token, created = Token.objects.get_or_create(user=user)
print(token.key)
```

Use this token in all subsequent API requests:

```bash
-H "Authorization: Token <your-token>"
```

## Practical Examples

### Example 1: Complete Workflow for Analytics User

```bash
# Variables
TOKEN="<your-analyst-token>"
API_URL="http://localhost:8000/api/v1"

# 1. Get your profile
curl -X GET "$API_URL/users/me/" \
  -H "Authorization: Token $TOKEN"

# Response:
# {
#   "id": "...",
#   "username": "analyst1",
#   "email": "analyst@example.com",
#   "role": "analyst",
#   "status": "active"
# }

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

# Response (201 Created):
# {
#   "id": "550e8400-e29b-41d4-a716-446655440000",
#   "user_username": "analyst1",
#   "amount": "5000.00",
#   "record_type": "income",
#   "record_type_display": "Income",
#   "category": "salary",
#   "category_display": "Salary",
#   "description": "Monthly salary",
#   "date": "2024-01-15",
#   "created_at": "2024-01-15T10:30:00Z",
#   "updated_at": "2024-01-15T10:30:00Z"
# }

# 3. Create an expense record
curl -X POST "$API_URL/records/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "150.50",
    "record_type": "expense",
    "category": "food",
    "date": "2024-01-15",
    "description": "Lunch at restaurant"
  }'

# 4. View all records
curl -X GET "$API_URL/records/" \
  -H "Authorization: Token $TOKEN"

# 5. Filter records by date
curl -X GET "$API_URL/records/?start_date=2024-01-01&end_date=2024-01-31" \
  -H "Authorization: Token $TOKEN"

# 6. Get dashboard summary
curl -X GET "$API_URL/records/summary/" \
  -H "Authorization: Token $TOKEN"

# Response:
# {
#   "total_income": "5000.00",
#   "total_expenses": "150.50",
#   "net_balance": "4849.50",
#   "total_records": 2,
#   "records_count_by_type": {
#     "income": 1,
#     "expense": 1
#   },
#   "records_count_by_category": {
#     "salary": 1,
#     "food": 1
#   }
# }

# 7. Get category wise breakdown
curl -X GET "$API_URL/records/category_summary/" \
  -H "Authorization: Token $TOKEN"

# 8. Get monthly trends for past 6 months
curl -X GET "$API_URL/records/monthly_summary/?months=6" \
  -H "Authorization: Token $TOKEN"

# 9. Get recent activity (last 5 transactions)
curl -X GET "$API_URL/records/recent_activity/?limit=5" \
  -H "Authorization: Token $TOKEN"

# 10. Get comprehensive dashboard overview
curl -X GET "$API_URL/dashboard/overview/" \
  -H "Authorization: Token $TOKEN"

# 11. Get financial insights
curl -X GET "$API_URL/dashboard/insights/" \
  -H "Authorization: Token $TOKEN"
```

### Example 2: Admin Managing Users

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

# Note: Get the role ID from /roles/ endpoint

# 3. Get list of roles
curl -X GET "$API_URL/roles/" \
  -H "Authorization: Token $ADMIN_TOKEN"

# Response:
# [
#   {"name": "viewer", "description": "Read-only access"},
#   {"name": "analyst", "description": "Can view and analyze"},
#   {"name": "admin", "description": "Full access"}
# ]

# 4. List inactive users
curl -X GET "$API_URL/users/inactive_users/" \
  -H "Authorization: Token $ADMIN_TOKEN"

# 5. Update user status
curl -X PUT "$API_URL/users/<user-id>/" \
  -H "Authorization: Token $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "suspended"
  }'

# 6. View specific user's records
curl -X GET "$API_URL/records/?user=<user-id>" \
  -H "Authorization: Token $ADMIN_TOKEN"

# Note: Admin can view any user's records
```

### Example 3: Bulk Create Records

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
      },
      {
        "amount": "25.00",
        "record_type": "expense",
        "category": "transport",
        "date": "2024-01-10",
        "description": "Uber"
      },
      {
        "amount": "100.00",
        "record_type": "expense",
        "category": "entertainment",
        "date": "2024-01-11",
        "description": "Movie tickets"
      }
    ]
  }'

# Response:
# {
#   "created_count": 3,
#   "error_count": 0,
#   "created_records": [...]
# }
```

### Example 4: Advanced Filtering and Statistics

```bash
TOKEN="<your-viewer-token>"
API_URL="http://localhost:8000/api/v1"

# 1. Filter by record type (only income)
curl -X GET "$API_URL/records/?type=income" \
  -H "Authorization: Token $TOKEN"

# 2. Filter by category
curl -X GET "$API_URL/records/?category=food" \
  -H "Authorization: Token $TOKEN"

# 3. Filter by date range
curl -X GET "$API_URL/records/?start_date=2024-01-01&end_date=2024-01-31" \
  -H "Authorization: Token $TOKEN"

# 4. Search in description
curl -X GET "$API_URL/records/?search=salary" \
  -H "Authorization: Token $TOKEN"

# 5. Pagination
curl -X GET "$API_URL/records/?page=1&page_size=10" \
  -H "Authorization: Token $TOKEN"

# 6. Sort by date
curl -X GET "$API_URL/records/?ordering=-date" \
  -H "Authorization: Token $TOKEN"

# 7. Get statistics for specific period
curl -X GET "$API_URL/records/statistics/?start_date=2024-01-01&end_date=2024-01-31" \
  -H "Authorization: Token $TOKEN"

# Response:
# {
#   "start_date": "2024-01-01",
#   "end_date": "2024-01-31",
#   "total_records": 15,
#   "total_income": "5000.00",
#   "total_expenses": "1500.00",
#   "net_balance": "3500.00",
#   "average_per_record": "433.33"
# }
```

### Example 5: Permission Testing

```bash
# Variables
VIEWER_TOKEN="<viewer-token>"
ANALYST_TOKEN="<analyst-token>"
ADMIN_TOKEN="<admin-token>"
API_URL="http://localhost:8000/api/v1"

# 1. VIEWER trying to create record (should fail with 403)
curl -X POST "$API_URL/records/" \
  -H "Authorization: Token $VIEWER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "100.00",
    "record_type": "income",
    "category": "salary",
    "date": "2024-01-15"
  }'

# Response (403 Forbidden):
# {
#   "success": false,
#   "message": "You must be an Analyst or higher to create records.",
#   "status_code": 403
# }

# 2. ANALYST can create record (should succeed with 201)
curl -X POST "$API_URL/records/" \
  -H "Authorization: Token $ANALYST_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "100.00",
    "record_type": "income",
    "category": "salary",
    "date": "2024-01-15"
  }'

# 3. VIEWER trying to delete record (should fail with 403)
curl -X DELETE "$API_URL/records/<record-id>/" \
  -H "Authorization: Token $VIEWER_TOKEN"

# Response (403 Forbidden):
# {
#   "success": false,
#   "message": "You must be an Admin to delete records.",
#   "status_code": 403
# }

# 4. ADMIN can delete record (should succeed with 204)
curl -X DELETE "$API_URL/records/<record-id>/" \
  -H "Authorization: Token $ADMIN_TOKEN"
```

### Example 6: Error Handling

```bash
TOKEN="<your-token>"
API_URL="http://localhost:8000/api/v1"

# 1. Invalid amount (must be positive)
curl -X POST "$API_URL/records/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "-100.00",
    "record_type": "income",
    "category": "salary",
    "date": "2024-01-15"
  }'

# Response (400 Bad Request):
# {
#   "success": false,
#   "message": "Invalid input provided.",
#   "errors": {
#     "amount": ["Amount must be greater than 0."]
#   },
#   "status_code": 400
# }

# 2. Missing required field
curl -X POST "$API_URL/records/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "100.00",
    "record_type": "income",
    "date": "2024-01-15"
  }'

# Response (400 Bad Request):
# {
#   "success": false,
#   "message": "Invalid input provided.",
#   "errors": {
#     "category": ["This field is required."]
#   },
#   "status_code": 400
# }

# 3. Invalid date format
curl -X POST "$API_URL/records/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "100.00",
    "record_type": "income",
    "category": "salary",
    "date": "15-01-2024"
  }'

# Response (400 Bad Request):
# {
#   "success": false,
#   "message": "Invalid input provided.",
#   "errors": {
#     "date": ["Date has wrong format. Use one of these formats instead: YYYY-MM-DD"]
#   },
#   "status_code": 400
# }

# 4. No authentication
curl -X GET "$API_URL/records/"

# Response (401 Unauthorized):
# {
#   "success": false,
#   "message": "Authentication required.",
#   "status_code": 401
# }

# 5. Invalid token
curl -X GET "$API_URL/records/" \
  -H "Authorization: Token invalid-token"

# Response (401 Unauthorized):
# {
#   "success": false,
#   "message": "Authentication required.",
#   "status_code": 401
# }
```

## Using Python Requests

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"
TOKEN = "<your-token>"

headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

# 1. Create a record
record_data = {
    "amount": "5000.00",
    "record_type": "income",
    "category": "salary",
    "date": "2024-01-15",
    "description": "Monthly salary"
}

response = requests.post(
    f"{BASE_URL}/records/",
    headers=headers,
    json=record_data
)

if response.status_code == 201:
    print("Record created:", response.json())
else:
    print("Error:", response.json())

# 2. Get dashboard summary
response = requests.get(
    f"{BASE_URL}/records/summary/",
    headers=headers
)

if response.status_code == 200:
    summary = response.json()
    print(f"Total Income: ${summary['total_income']}")
    print(f"Total Expenses: ${summary['total_expenses']}")
    print(f"Net Balance: ${summary['net_balance']}")

# 3. Get monthly trends
response = requests.get(
    f"{BASE_URL}/records/monthly_summary/?months=6",
    headers=headers
)

if response.status_code == 200:
    for month in response.json():
        print(f"{month['year']}-{month['month']:02d}: " +
              f"Income=${month['income']}, Expenses=${month['expenses']}")

# 4. Filter records
params = {
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "type": "expense",
    "page": 1,
    "page_size": 20
}

response = requests.get(
    f"{BASE_URL}/records/",
    headers=headers,
    params=params
)

if response.status_code == 200:
    data = response.json()
    print(f"Total records: {data['count']}")
    for record in data['results']:
        print(f"  {record['category']}: ${record['amount']}")
```

## Tips and Best Practices

1. **Always include the Authorization header** with your token
2. **Use appropriate date format**: `YYYY-MM-DD` for dates, ISO 8601 for timestamps
3. **Handle pagination** for large result sets
4. **Use filtering** to reduce data transfer
5. **Check response status codes** to handle errors properly
6. **Use the correct HTTP methods**: GET (read), POST (create), PUT (update), DELETE (remove)
7. **Batch operations** when creating multiple records to save requests
8. **Monitor rate limits** (if configured)
9. **Cache dashboard summaries** if fetched frequently
10. **Use appropriate pagination sizes** (default 20, max 100)

## Common Scenarios

### Scenario 1: Get Monthly Budget Report

```python
import requests
from datetime import date
from dateutil.relativedelta import relativedelta

TOKEN = "<your-token>"
BASE_URL = "http://localhost:8000/api/v1"
headers = {"Authorization": f"Token {TOKEN}"}

# Get monthly data for current year
today = date.today()
start_date = today.replace(month=1, day=1)
end_date = date(today.year, 12, 31)

response = requests.get(
    f"{BASE_URL}/records/",
    headers=headers,
    params={
        "start_date": str(start_date),
        "end_date": str(end_date),
        "page_size": 100
    }
)

# Process data and create report
if response.status_code == 200:
    all_records = response.json()["results"]
    # Group by month and calculate totals
```

### Scenario 2: Track Spending by Category

```python
import requests

TOKEN = "<your-token>"
BASE_URL = "http://localhost:8000/api/v1"
headers = {"Authorization": f"Token {TOKEN}"}

response = requests.get(
    f"{BASE_URL}/records/category_summary/",
    headers=headers
)

if response.status_code == 200:
    summary = response.json()["results"]
    
    # Get top spending categories
    expenses = [item for item in summary if item["type"] == "expense"]
    sorted_expenses = sorted(expenses, key=lambda x: float(x["total_amount"]), reverse=True)
    
    print("Top Spending Categories:")
    for item in sorted_expenses[:5]:
        print(f"  {item['category_display']}: ${item['total_amount']}")
```

## Troubleshooting

- **401 Unauthorized**: Check your token is valid and included in header
- **403 Forbidden**: Your role doesn't have permission for this action
- **404 Not Found**: The resource doesn't exist or has been deleted
- **400 Bad Request**: Check your request payload and query parameters
- **500 Internal Server Error**: Check server logs for details
