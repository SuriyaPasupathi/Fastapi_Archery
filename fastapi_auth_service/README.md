# FastAPI Role-Based Authentication Service

A comprehensive authentication service with a three-tier role hierarchy: Super Admin, Client Admin, and Organizer.

## Role Hierarchy

### 1. Super Admin
- **Created by**: System (automatically on startup)
- **Permissions**: 
  - Create Client Admin accounts
  - Create Organizer accounts
  - View all users
  - Manage all accounts (activate/deactivate/verify)
  - Full system access

### 2. Client Admin
- **Created by**: Super Admin only
- **Permissions**:
  - Create Organizer accounts (under their management)
  - View their own organizers
  - Manage their own profile
- **Onboarding**: Receives email with login credentials

### 3. Organizer
- **Created by**: Super Admin or Client Admin
- **Permissions**:
  - Access to organizer-specific features
  - Manage their own profile
- **Management**: Assigned to a specific Client Admin

## Features

- ✅ **Role-based access control** with three-tier hierarchy
- ✅ **Automatic Super Admin creation** on system startup
- ✅ **Email notifications** for Client Admin onboarding
- ✅ **JWT token authentication**
- ✅ **Password hashing** with bcrypt
- ✅ **User verification and activation** system
- ✅ **Comprehensive API documentation** with Swagger UI
- ✅ **Database migrations** with Alembic
- ✅ **Environment-based configuration**

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirement.txt
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/fastapi_auth

# JWT
SECRET_KEY=your-super-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email (for Client Admin notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@yourdomain.com

# Application
APP_NAME=FastAPI Auth Service
LOGIN_URL=http://localhost:3000/login

# Super Admin (default credentials)
SUPER_ADMIN_USERNAME=superadmin
SUPER_ADMIN_PASSWORD=superadmin123
SUPER_ADMIN_EMAIL=superadmin@yourdomain.com
```

### 3. Initialize Database

```bash
python init_db.py
```

This will:
- Create all database tables
- Create the Super Admin account with default credentials

### 4. Run the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Authentication

| Method | Endpoint | Description | Access |
|--------|----------|-------------|---------|
| POST | `/api/v1/auth/login` | Login for all users | Public |
| GET | `/api/v1/auth/me` | Get current user info | Authenticated |
| POST | `/api/v1/auth/change-password` | Change password | Authenticated |

### User Management (Super Admin)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/create-client-admin` | Create Client Admin account |
| GET | `/api/v1/auth/users` | Get all users |
| GET | `/api/v1/auth/users/client-admins` | Get all Client Admins |
| POST | `/api/v1/auth/users/{user_id}/verify` | Verify user account |
| POST | `/api/v1/auth/users/{user_id}/activate` | Activate user account |
| POST | `/api/v1/auth/users/{user_id}/deactivate` | Deactivate user account |

### User Management (Client Admin)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/create-organizer` | Create Organizer account |
| GET | `/api/v1/auth/users/organizers` | Get organizers (own only) |

## Usage Examples

### 1. Login as Super Admin

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "superadmin",
    "password": "superadmin123"
  }'
```

### 2. Create Client Admin (Super Admin only)

```bash
curl -X POST "http://localhost:8000/api/v1/auth/create-client-admin" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "clientadmin1",
    "email": "clientadmin@example.com",
    "password": "securepassword123",
    "role": "client_admin",
    "organization_name": "Example Organization",
    "organization_description": "A sample organization"
  }'
```

### 3. Create Organizer (Client Admin or Super Admin)

```bash
curl -X POST "http://localhost:8000/api/v1/auth/create-organizer" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "organizer1",
    "email": "organizer@example.com",
    "password": "organizerpass123",
    "role": "organizer",
    "organizer_details": "Event organizer for sports competitions"
  }'
```

## Email Notifications

When a Super Admin creates a Client Admin account, the system automatically:

1. Creates the account in the database
2. Sends an email to the Client Admin containing:
   - User ID
   - Username
   - Password
   - Secure login link
   - Security instructions

## Security Features

- **Password Hashing**: All passwords are hashed using bcrypt
- **JWT Tokens**: Secure token-based authentication
- **Role-based Access**: Strict permission control
- **Email Verification**: Client Admin accounts are automatically verified
- **Account Management**: Super Admin can activate/deactivate accounts

## Database Schema

### Users Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| username | String | Unique username |
| email | String | Email address |
| hashed_password | String | Bcrypt hashed password |
| role | Enum | User role (super_admin, client_admin, organizer) |
| is_active | Boolean | Account active status |
| is_verified | Boolean | Account verification status |
| organization_name | String | Organization name (Client Admin) |
| organization_description | Text | Organization description (Client Admin) |
| client_admin_id | Integer | Reference to Client Admin (Organizer) |
| organizer_details | Text | Organizer details |
| created_at | DateTime | Account creation timestamp |
| updated_at | DateTime | Last update timestamp |

## Development

### Project Structure

```
fastapi_auth_service/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── auth.py          # Authentication routes
│   ├── core/
│   │   ├── config.py            # Configuration settings
│   │   ├── oauth2.py            # OAuth2 authentication
│   │   └── security.py          # Security utilities
│   ├── crud/
│   │   └── user.py              # Database operations
│   ├── models/
│   │   └── user.py              # SQLAlchemy models
│   ├── schemas/
│   │   └── user_schema.py       # Pydantic schemas
│   ├── services/
│   │   ├── auth_service.py      # Authentication service
│   │   └── email_service.py     # Email service
│   ├── database.py              # Database connection
│   └── main.py                  # FastAPI application
├── alembic/                     # Database migrations
├── init_db.py                   # Database initialization
├── requirement.txt              # Python dependencies
└── README.md                    # This file
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head
```

## Production Deployment

### Environment Variables

Ensure all sensitive information is properly configured:

1. **Database**: Use a production PostgreSQL instance
2. **JWT Secret**: Use a strong, randomly generated secret key
3. **Email**: Configure production SMTP settings
4. **CORS**: Restrict allowed origins to your frontend domain

### Security Checklist

- [ ] Change default Super Admin password
- [ ] Use HTTPS in production
- [ ] Configure proper CORS origins
- [ ] Set up proper logging
- [ ] Use environment variables for all secrets
- [ ] Regular database backups
- [ ] Monitor application logs

## Support

For issues and questions:

1. Check the API documentation at `/docs`
2. Review the logs for error details
3. Ensure all environment variables are properly set
4. Verify database connectivity

## License

This project is licensed under the MIT License.
