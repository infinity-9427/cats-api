# 🐱 Cats API - Backend Application

REST API developed with **Python FastAPI** and **MongoDB** to manage cat breed information and users, integrated with [The Cat API](https://thecatapi.com/).

## 📋 Project Requirements

This project implements a BackEnd with **2 main controllers**:

### 🐱 **Cats Controller**
Connected to the public API https://thecatapi.com/ with the following actions:
- `GET /breeds` - List of cat breeds
- `GET /breeds/:breed_id` - Specific breed by ID
- `GET /breeds/search` - Search breeds by parameters

### 👤 **Users Controller** 
User management with MongoDB with the following actions:
- `GET /user` - List of users
- `POST /user` - Create user (auto-generated unique username)
- `GET /login` - Login validation against MongoDB
- `POST /login` - Login with JSON body (REST standard)

### 🔐 **Authentication System**
Complete JWT-based authentication system:
- **JWT Token Generation** - Automatic token creation on login
- **Token Validation** - Secure token verification
- **Protected Endpoints** - Authentication dependencies ready for use
- **Utility Endpoints** - Token verification and user information
- **Security Features** - Password hashing, token expiration, error handling

## 🔧 Technical Features

- **Framework**: Python FastAPI
- **Database**: MongoDB
- **Architecture**: Clean Architecture, SOLID, Repository Pattern
- **Security**: Hashed passwords with bcrypt, JWT tokens
- **Authentication**: Complete JWT system with Bearer token support
- **Testing**: Unit tests with pytest + custom Make commands
- **Containerization**: Docker and Docker Compose
- **Documentation**: Automatic Swagger UI + Authentication Guide

## 🔑 The Cat API Key
```
your_api_key
```

## 📋 Prerequisites

- **Docker** (recommended)
- **Docker Compose** (recommended)
- Python 3.11+ (for local development)

## 🚀 Installation and Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd cats-api
```

### 2. Run with Docker Compose (Recommended)
```bash
# Build and run all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f cats-api

# Stop services
docker-compose down
```

### 3. Access services
- **API**: http://localhost:8000
- **Swagger Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

### 4. Quick Test (Optional)
```bash
# Verify everything works - choose your preferred method
make test-quick    # Custom command (recommended)
./run_tests.sh     # Shell script (alternative)
```

## 📊 Useful Docker Commands

```bash
# View active containers
docker ps

# View logs of a specific service
docker-compose logs -f mongodb

# Access MongoDB container
docker exec -it cats-api-mongodb mongosh cats_api

# Rebuild only the API
docker-compose build cats-api

# Restart a service
docker-compose restart cats-api

# Clean volumes (⚠️ deletes data)
docker-compose down -v
```

## 👥 Default Users

The system includes pre-configured test users:

### Admin User
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@example.com`

### Test User
- **Username**: `john.doe`
- **Password**: `password123`
- **Email**: `john.doe@example.com`

## 🔐 Password Security

- Passwords are stored **hashed** using **bcrypt**
- **Never** store passwords in plain text
- Hash is generated automatically when creating users
- Hash example: `$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewVyLrId4Qa8/8IS`

## 📚 API Endpoints

### 🏠 General Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page |
| GET | `/health` | API health status |

### 🐱 Cats Controller (`/api/v1/breeds`)

#### 1. GET /breeds - List of breeds
```bash
curl -X GET "http://localhost:8000/api/v1/breeds"
```

**Successful response (200)**:
```json
[
  {
    "id": "abys",
    "name": "Abyssinian",
    "description": "The Abyssinian is easy to care for...",
    "temperament": "Active, Energetic, Independent",
    "origin": "Egypt",
    "life_span": "14 - 15"
  }
]
```

#### 2. GET /breeds/:breed_id - Specific breed
```bash
curl -X GET "http://localhost:8000/api/v1/breeds/abys"
```

**Successful response (200)**:
```json
{
  "id": "abys",
  "name": "Abyssinian",
  "description": "The Abyssinian is easy to care for...",
  "temperament": "Active, Energetic, Independent",
  "origin": "Egypt"
}
```

#### 3. GET /breeds/search - Search breeds
```bash
curl -X GET "http://localhost:8000/api/v1/breeds/search?q=persian&limit=5"
```

**Parameters**:
- `q` (string): Search term
- `limit` (int): Result limit

### 👤 Users Controller (`/api/v1`)

#### 1. GET /user - List of users
```bash
curl -X GET "http://localhost:8000/api/v1/user"
```

**Successful response (200)**:
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "first_name": "John",
    "last_name": "Doe",
    "username": "john.doe",
    "email": "john.doe@example.com",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

#### 2. POST /user - Create user
```bash
curl -X POST "http://localhost:8000/api/v1/user" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "María",
    "last_name": "García",
    "password": "mipassword123",
    "email": "maria.garcia@example.com"
  }'
```

**Successful response (201)**:
```json
{
  "id": "507f1f77bcf86cd799439012",
  "first_name": "María",
  "last_name": "García",
  "username": "maria.garcia",
  "email": "maria.garcia@example.com",
  "created_at": "2024-01-15T10:35:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

> **📝 Note**: The `username` is automatically generated as `firstname.lastname` and guaranteed to be unique. If it already exists, a number is added (e.g., `maria.garcia1`).

#### 3. Login Endpoints

##### GET /login - Login validation (Query Parameters)
```bash
curl -X GET "http://localhost:8000/api/v1/login?username=maria.garcia&password=mipassword123"
```

##### POST /login - Login validation (JSON Body - Recommended)
```bash
curl -X POST "http://localhost:8000/api/v1/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "maria.garcia", "password": "mipassword123"}'
```

**Successful response (200)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "507f1f77bcf86cd799439012",
    "first_name": "María",
    "last_name": "García",
    "username": "maria.garcia",
    "email": "maria.garcia@example.com"
  }
}
```

**Error response (401)**:
```json
{
  "detail": "Invalid username or password"
}
```

### 🔐 Authentication Endpoints (`/api/v1/auth`)

#### Token Verification (Optional Auth)
```bash
# With token
curl -H "Authorization: Bearer <your-token>" "http://localhost:8000/api/v1/auth/verify"

# Without token
curl "http://localhost:8000/api/v1/auth/verify"
```

#### Get Current User (Requires Auth)
```bash
curl -H "Authorization: Bearer <your-token>" "http://localhost:8000/api/v1/auth/me"
```

#### Token Information
```bash
curl -H "Authorization: Bearer <your-token>" "http://localhost:8000/api/v1/auth/token-info"
```

> **📚 For complete authentication documentation, see [AUTHENTICATION.md](AUTHENTICATION.md)**
```

## 🧪 Testing

### 🚀 Custom Commands (Recommended)
```bash
# Full test suite with coverage
make test

# Quick tests (faster, no coverage)
make test-quick

# Detailed coverage report
make test-cov

# Show all available commands
make help
```

### 🔧 Alternative Commands
```bash
# Shell script (traditional approach)
./run_tests.sh

# Direct pytest commands
pytest tests/ --cov=app --cov-report=term-missing

# Docker testing
docker-compose exec cats-api pytest tests/

# Quick tests only
pytest tests/

# Run specific test file
pytest tests/test_user_service.py -v
```

### ✅ Expected Output
```bash
Running tests...
84 passed in ~22s

Coverage Report:
TOTAL: 497 statements, 92% coverage
✅ Tests complete - workspace clean!
```

### � What's Tested
- **84 tests total** covering all endpoints
- **User management** (creation, authentication)
- **Cat breeds** (external API integration)
- **JWT authentication** (token generation/validation)
- **Error handling** and edge cases
- **Database operations** (MongoDB)

**Note**: Tests avoid generating HTML reports to keep workspace clean.

### 📚 Quick Reference
| Command | Purpose | Time |
|---------|---------|------|
| `make test` | Full test suite + coverage | ~23s |
| `make test-quick` | Quick tests only | ~18s |
| `make test-cov` | Detailed coverage report | ~25s |
| `./run_tests.sh` | Shell script alternative | ~23s |
| `pytest tests/test_user_service.py -v` | Specific test file | ~3s |

## 🔧 Troubleshooting

### Problem: API doesn't respond
```bash
# Check that containers are running
docker ps

# Review API logs
docker-compose logs cats-api

# Restart services
docker-compose restart
```

### Problem: MongoDB connection error
```bash
# Check MongoDB status
docker-compose logs mongodb

# Check connectivity
docker exec -it cats-api-mongodb mongosh --eval "db.adminCommand('ping')"

# Restart MongoDB
docker-compose restart mongodb
```

### Problem: 500 error on user endpoints
- **Common cause**: Problem with ObjectId to string conversion
- **Solution**: Verify that the `_id` field is converted correctly in the repository

### Problem: Tests fail
```bash
# Clean Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +

# Reinstall dependencies
pip install -r requirements.txt

# Run tests with more detail
pytest -v -s
```

### Problem: Ports occupied
```bash
# Check what's using port 8000
lsof -i :8000

# Change port in docker-compose.yml
# ports:
#   - "8001:8000"  # host_port:container_port
```

## 📋 Complete Usage Examples

### 1. Complete user workflow
```bash
# 1. Create a new user
curl -X POST "http://localhost:8000/api/v1/user" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Ana",
    "last_name": "Martínez", 
    "password": "mipassword456",
    "email": "ana.martinez@email.com"
  }'

# Response: {"id":"...","username":"ana.martinez",...}

# 2. Login with the created user
curl -X GET "http://localhost:8000/api/v1/login?username=ana.martinez&password=mipassword456"

# Response: {"access_token":"...","user":{...}}

# 3. List all users
curl -X GET "http://localhost:8000/api/v1/user"
```

### 2. Explore cat breeds
```bash
# 1. View all available breeds
curl -X GET "http://localhost:8000/api/v1/breeds"

# 2. Search for a specific breed
curl -X GET "http://localhost:8000/api/v1/breeds/search?q=maine"

# 3. Get breed details
curl -X GET "http://localhost:8000/api/v1/breeds/mcoo"  # Maine Coon
```

### 3. Authentication testing
```bash
# Correct login
curl -X GET "http://localhost:8000/api/v1/login?username=admin&password=admin123"

# Incorrect login (should return 401)
curl -X GET "http://localhost:8000/api/v1/login?username=admin&password=wrong"
```

## 🏗️ Project Architecture

The project follows **Clean Architecture** and **SOLID** principles:

```
app/
├── controllers/         # REST controllers
│   ├── cat_controller.py      # 🐱 Cats controller
│   └── user_controller.py     # 👤 Users controller
├── services/           # Business logic
│   ├── cat_service.py         # Cats service (TheCatAPI)
│   └── user_service.py        # Users service
├── repositories/       # Data access
│   ├── user_repository.py     # MongoDB repository
│   └── user_repository_interface.py
├── models/             # Data models
│   ├── cat.py                 # Cat models
│   └── user.py                # User models
├── schemas/            # Pydantic schemas
│   ├── cat.py                 # REST cat schemas
│   └── user.py                # REST user schemas
└── core/               # Configuration and utilities
    ├── config.py              # Configuration
    ├── database.py            # MongoDB connection
    └── security.py            # Password hash, JWT
```

## 🔐 Security Details

### Password Hashing
- **Algorithm**: bcrypt with automatic salt
- **Rounds**: 12 (configurable)
- **Hash example**: `$2b$12$LQv3c1yqBWVHxkd0LHAkCO...`

### JWT Tokens
- **Algorithm**: HS256
- **Expiration**: 30 minutes (configurable)
- **Claims**: username in `sub` field

### Username Generation
- **Format**: `firstname.lastname`
- **Normalization**: No accents, lowercase letters only
- **Unique**: If exists, number is added (`juan.perez1`)

## 📱 Documentation Access

Once the API is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json



