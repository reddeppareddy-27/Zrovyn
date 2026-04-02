# Design Decisions and Architecture

This document outlines the key design decisions, architectural patterns, and trade-offs made in the Finance Backend system.

## Architecture Overview

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

## Key Design Decisions

### 1. Custom User Model (CustomUser)

**Decision**: Extended Django's built-in `User` model with `AbstractUser`

**Rationale**:
- Added UUID primary key for better distributed system support
- Added `role` field for role-based access control
- Added `status` field for user lifecycle management (active, inactive, suspended)
- Provides flexibility for future customizations
- Standard practice in professional Django projects

**Trade-offs**:
- ✅ Flexibility for custom fields and behaviors
- ✅ UUID provides better scalability
- ❌ Must be set up before creating any other models
- ❌ More complex than using default User model

### 2. Role-Based Access Control (RBAC)

**Decision**: Implemented separate `Role` model with permission classes

**Rationale**:
- Decouples roles from users, allowing easier role management
- Provides three clear roles: Viewer, Analyst, Admin
- Uses Django REST Framework's permission classes for enforcement
- Easy to extend with additional roles or permissions

**Implementation**:
- `Role` model defines available roles
- `CustomUser` has FK to `Role`
- Permission classes check user's role in `has_permission()` and `has_object_permission()`

**Example Permission Class**:
```python
class IsAnalystOrHigher(IsActive):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.user.role.name in ['analyst', 'admin']
```

### 3. Service Layer Pattern

**Decision**: Created `FinancialSummaryService` for business logic

**Rationale**:
- Separates business logic from HTTP concerns
- Makes complex operations (summaries, analytics) testable without HTTP
- Reusable across multiple views or APIs
- Easier to maintain and understand

**Benefits**:
- Testable independently
- Reusable methods
- Cleaner views
- Single responsibility principle

### 4. Soft Delete Pattern

**Decision**: Used `is_deleted` field instead of actual deletion

**Rationale**:
- Allows data recovery if deleted accidentally
- Maintains referential integrity
- Supports audit trails
- Soft deletes are restored by applying `is_deleted=True` flag
- Hard delete would be database operation

**Implementation**:
```python
class FinancialRecord(models.Model):
    is_deleted = models.BooleanField(default=False)
```

All queries filter with `is_deleted=False` automatically in views.

### 5. UUID Primary Keys

**Decision**: Used UUID for both `CustomUser` and `FinancialRecord`

**Rationale**:
- Better for distributed systems
- Harder to guess or enumerate
- Provides better privacy
- Standard for microservices architecture
- Reduces reliance on sequential IDs

**Trade-offs**:
- ✅ Better security and scalability
- ✅ Globally unique across systems
- ❌ Slightly larger database storage (16 bytes vs 4-8 bytes)
- ❌ Slightly slower for some index operations

### 6. Serializer Pattern

**Decision**: Separate serializers for create/update vs. read operations

**Rationale**:
- `FinancialRecordSerializer`: Read-only fields, display helper fields
- `FinancialRecordCreateUpdateSerializer`: Input validation only
- Prevents over-exposure of data
- Input validation separate from output representation

**Example**:
```python
class FinancialRecordCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['amount', 'record_type', 'category', 'description', 'date']
        # No user field - assigned by view

class FinancialRecordSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    # Display enums and metadata
```

### 7. Pagination Strategy

**Decision**: Used `PageNumberPagination` with configurable page size

**Rationale**:
- Standard approach for REST APIs
- Client can control page size within limits
- Reduces memory usage for large datasets
- Improves API response times

**Configuration**:
```python
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
```

### 8. Error Handling Strategy

**Decision**: Custom exception handler for consistent error responses

**Rationale**:
- Consistent error format across all endpoints
- Structured error information
- Client can parse errors reliably
- Logging for debugging

**Response Format**:
```json
{
  "success": false,
  "message": "Human-readable error message",
  "errors": {"field": ["error details"]},
  "status_code": 400
}
```

### 9. Database Indexes

**Decision**: Applied composite indexes on frequently queried fields

**Rationale**:
- Improves query performance for filtering and sorting
- Especially important for financial data where date/user queries are common

**Indexes Created**:
```python
indexes = [
    models.Index(fields=['user', '-date']),      # For date filtering
    models.Index(fields=['user', 'record_type']), # For type filtering
    models.Index(fields=['user', 'category']),    # For category filtering
    models.Index(fields=['is_deleted']),          # For soft delete queries
]
```

### 10. Token Authentication

**Decision**: Used Django REST Framework's built-in `TokenAuthentication`

**Rationale**:
- Simple and straightforward for REST APIs
- Stateless (no server-side session storage)
- Standard approach
- Easy to refresh tokens if needed

**Alternative Considered**: JWT
- More complex
- Better for distributed systems
- Could be added as additional auth method

## API Design Decisions

### 1. RESTful Endpoints

**Decision**: Followed REST conventions for endpoints

**Structure**:
- `GET /records/` - List
- `POST /records/` - Create
- `GET /records/{id}/` - Retrieve
- `PUT /records/{id}/` - Update
- `DELETE /records/{id}/` - Delete

**Custom Actions** (using `@action` decorator):
- `GET /records/summary/` - Dashboard summary
- `GET /records/category_summary/` - Category breakdown
- `GET /records/monthly_summary/` - Trends
- `POST /records/bulk_create/` - Batch operations

### 2. Query Parameters

**Decision**: Used query parameters for filtering and pagination

**Examples**:
```
GET /records/?start_date=2024-01-01&end_date=2024-01-31&type=income&page=1&page_size=20
```

**Parameters**:
- `start_date`, `end_date`: Date range filtering
- `type`: Income/expense filtering
- `category`: Category filtering
- `search`: Text search
- `page`, `page_size`: Pagination
- `ordering`: Sort order

### 3. Response Status Codes

**Decision**: Used appropriate HTTP status codes

**Mapping**:
- `200 OK`: Successful GET, PUT
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `207 Multi-Status`: Partial success in bulk operations

## Data Model Decisions

### 1. Record Type and Category as Enums

**Decision**: Used `CharField` with `choices` instead of separate tables

**Rationale**:
- Fixed, predefined values
- Simpler queries and indexes
- Avoids join operations
- Categories unlikely to change frequently

**Trade-off**:
- ✅ Simpler schema
- ✅ Better performance
- ❌ Adding new categories requires migration
- ❌ Cannot user-define categories

### 2. Single User-Record Relationship

**Decision**: Each record belongs to exactly one user

**Rationale**:
- Clear ownership model
- Efficient access control (check owner = current user)
- Simplifies analytics per user
- Supports multi-tenant architecture pattern

**Alternative Considered**: Shared records between users
- Would need addition shared/permission table
- More complex access control logic
- Not required for current use case

### 3. Decimal for Currency

**Decision**: Used `DecimalField` for amounts

**Rationale**:
- Proper currency representation (not float!)
- Avoids floating-point precision errors
- Django best practice for financial data
- Maintains accuracy for calculations

**Configuration**:
```python
amount = models.DecimalField(max_digits=15, decimal_places=2)
```

## Security Decisions

### 1. Token Authentication Only

**Decision**: No username/password authentication in API

**Rationale**:
- Prevents password transmission over API
- Tokens can be revoked independently
- Better for third-party integrations
- Reduces session management complexity

**Initial Setup**:
- Users created via Django admin with password
- Tokens generated via Django shell or admin
- User shares token, not password

### 2. Permission Classes Enforcement

**Decision**: All APIs require authentication and use permission classes

**Rationale**:
- Prevents accidental exposure
- Explicit is better than implicit
- Enforces access control at view level

**Every ViewSet has**:
```python
permission_classes = [IsAuthenticated]  # Minimum requirement
```

### 3. Status-Based Access Control

**Decision**: Added user `status` field to prevent access for suspended users

**Rationale**:
- Allows quick user lockout without deletion
- Preserved user data and history
- Reversible action
- Three states: active, inactive, suspended

### 4. No Password Changes via API

**Decision**: Password management only through Django admin

**Rationale**:
- Reduces complexity
- Better security (no password change endpoints to secure)
- Prevents brute force attacks on password endpoints
- Can be added later if needed

## Testing Strategy

### 1. Unit Tests for Models

**Decision**: Test models with `TestCase`

**Content**:
- Model creation and field validation
- Business logic (clean methods)
- Soft delete behavior

### 2. API Integration Tests

**Decision**: Test API endpoints with `APITestCase` and `APIClient`

**Content**:
- Authentication requirements
- Permission enforcement per role
- Valid and invalid inputs
- Pagination and filtering

### 3. Service Tests

**Decision**: Test business logic independently

**Benefits**:
- Test complex calculations without HTTP overhead
- Reusable test data
- Fast execution

## Logging and Monitoring

### 1. Structured Logging

**Decision**: Custom exception handler logs all errors

**Content**:
- Error type and message
- Request context
- Stack trace for debugging

### 2. Multiple Output Targets

**Decision**: Log to both console and file

**Rationale**:
- Console: Development visibility
- File: Production archiving and compliance
- Different levels for different components

## Future Scalability Considerations

### 1. Caching Layer

**Future Enhancement**: Add Redis for caching
- Dashboard summaries (computed expensive, change infrequently)
- User roles (loaded frequently)
- Category list

### 2. Background Jobs

**Future Enhancement**: Celery tasks for:
- Generating monthly reports
- Sending email notifications
- Data cleanup/archival

### 3. Read Replicas

**Future Enhancement**: Database read replicas for:
- Dashboard queries (high volume, read-only)
- Analytics endpoints
- Admin dashboards

### 4. API Versioning

**Current**: All endpoints under `/api/v1/`

**Future**: Support multiple versions for backward compatibility
```
/api/v1/records/
/api/v2/records/  (with enhanced features)
```

### 5. Microservices Decomposition

**Future**: Split into microservices:
- Auth Service
- Records Service
- Analytics Service
- User Management Service

**Current monolithic approach supports this evolution**

## Trade-offs and Reasoning

| Decision | Pros | Cons | Reasoning |
|----------|------|------|-----------|
| Custom User Model | Flexibility, UUID | Setup complexity | Standard in professional projects |
| Soft Deletes | Recovery, Audit trail | Schema complexity | Financial data needs history |
| Separate Services | Testable, Reusable | Extra abstraction | Maintainability > simplicity |
| Token Auth | Stateless, Simple | No session mgmt | Good for REST APIs |
| Decimal for Currency | Accurate, Safe | More storage | Correctness is critical |
| UUID Primary Keys | Distributed-ready, Secure | Larger indexes | Future-proofs the system |
| Enum Categories | Simple, Fast | Less flexible | Categories are stable |
| Pagination by Default | Scalable, Efficient | More complex queries | Prevents memory overload |

## Conclusion

The design favors **clarity, maintainability, and correctness** over simplicity. Each decision was made with consideration for:

1. **Current Requirements**: All core features effectively implemented
2. **Future Growth**: Scalable architecture supporting microservices
3. **Best Practices**: Following Django and REST conventions
4. **Security**: Role-based access control and input validation
5. **Quality**: Comprehensive testing and error handling

The codebase is organized to be understandable, maintainable, and extensible while remaining pragmatic and not over-engineered for the current scope.
