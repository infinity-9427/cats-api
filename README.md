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
- `POST /login` - Login with JSON body

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
- **Testing**: **100% Real Data Integration Tests** - No mocks, real MongoDB and Cat API
- **Containerization**: Docker and Docker Compose
- **Documentation**: Automatic Swagger UI + Authentication Guide

## � Quick Start for Contributors

Perfect for developers who want to **test everything quickly** with real data:

### Prerequisites
- Python 3.11+
- Docker & Docker Compose

### 1. Clone and Setup
```bash
git clone <repository>
cd cats-api
```

### 2. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your Cat API key
# Get your free API key from: https://thecatapi.com/signup
```

### 3. Install Dependencies
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install all dependencies using modern Python packaging
make install
```

### 4. Start Real Database
```bash
# Start MongoDB in Docker (fresh environment)
docker-compose up mongodb -d
```

### 5. Run All Tests (100% Real Data)
```bash
# Run all tests with real MongoDB and Cat API
make test-quick
```

**✅ Expected Result**: All tests pass in ~10 seconds using:
- **Real MongoDB** for user operations 
- **Real Cat API** for breed data
- **No mocks or dummy data**

### 6. Run with Coverage
```bash
# Run tests with coverage report
make test
```

## 🧪 Testing Philosophy

This project uses **100% Real Data Integration Testing**:

### ✅ What We Test
- **Real MongoDB Operations**: Create, read, authenticate users in actual database
- **Real Cat API Integration**: Fetch breeds, search, handle errors from live API
- **Real HTTP Endpoints**: All API routes tested via FastAPI TestClient
- **Real Data Validation**: Pydantic schemas, password hashing, JWT tokens
- **Real Error Handling**: 404s, 401s, validation errors with actual API responses

### ❌ What We Don't Use
- **No Mocks**: No mocked services or fake responses
- **No Dummy Data**: No hardcoded or simulated data
- **No Unit Tests**: Focus on integration and end-to-end testing

### 📊 Test Coverage
- **All Tests**: Integration tests with real data
- **~10 seconds**: Fast execution time
- **High Coverage**: Focuses on critical business logic

### 🔄 Test Environment
- **Fresh Database**: Cleaned before/after each test
- **Isolated Tests**: No test dependencies or shared state
- **Production-like**: Same code paths as production environment

**⚡ Fast Local Testing**: Quick setup for immediate feedback and development.

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

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your Cat API key
# Get your free API key from: https://thecatapi.com/signup
```

### 3. Run with Docker Compose (Recommended)
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

### 4. Access services
- **API**: http://localhost:8000
- **Swagger Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

### 5. Local Development (Alternative)
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
make install

# Start MongoDB only
docker-compose up mongodb -d

# Run tests
make test-quick    # Quick tests without coverage
make test          # Full tests with coverage
make test-cov      # Detailed coverage report

# Start development server
make dev           # Auto-reload server
```

## 📊 Available Commands

```bash
# View all available commands
make help

# Available commands:
make install      # Install dependencies from pyproject.toml
make test-quick   # Run tests without coverage (fastest)
make test         # Run all tests with coverage
make test-cov     # Run tests with detailed coverage report
make clean        # Clean cache files and build artifacts
make dev          # Start development server
make help         # Show help message
```

## � Docker Commands

```bash
# View active containers
docker ps

# View logs of a specific service
docker-compose logs -f mongodb

# Access MongoDB container
docker exec -it cats-api-mongodb mongosh cats_api

# Access MongoDB with authentication
docker-compose exec mongodb mongosh --username admin --password password123 --authenticationDatabase admin

# Rebuild only the API
docker-compose build cats-api

# Restart a service
docker-compose restart cats-api

# Clean volumes (⚠️ deletes data and recreates default users)
docker-compose down -v
```

## 👥 Default Users

The system automatically creates pre-configured test users during MongoDB initialization:

### Admin User
- **Username**: `admin`
- **Password**: `password123`
- **Email**: `admin@example.com`

### Test User
- **Username**: `john.doe`
- **Password**: `password123`
- **Email**: `john.doe@example.com`

> **🔧 Note**: These users are created automatically when the MongoDB container starts with an empty database via the `init-mongo.js` script.

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

#### 3. Login Endpoint

##### POST /login - User Authentication
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

## 🧪 Testing

> **� Docker-First Testing**: Tests run in containers for consistency and ease of setup.

### 🚀 Recommended Commands (Docker-based)
```bash
# Quick Docker-based tests (recommended for new clones)
make test-quick

# Docker tests with coverage reports
make test-docker

# Show all available commands
make help
```

### � How it works
- **No local setup required**: Tests run in Docker containers
- **MongoDB included**: Automatic test database setup
- **Clean environment**: Fresh containers for each test run
- **Cross-platform**: Works on Linux, macOS, and Windows

### �🔧 Alternative Commands (Local Development)
```bash
# Local testing (requires Python environment setup)
make test           # Full test suite
make test-cov       # With coverage

# Shell script (traditional approach)
./run_tests.sh

# Direct pytest commands (requires local environment)
pytest tests/ --cov=app --cov-report=term-missing
```

### ⚙️ Testing Architecture
- **Test Database**: `cats_api_test` (isolated from main database)
- **Environment**: Uses `.env` configuration
- **MongoDB**: Automatically started with Docker Compose
- **Clean State**: Database cleaned between test runs

### ✅ Expected Output
```bash
🐳 Running Cats API Tests in Docker...
📦 Starting MongoDB...
⏳ Waiting for MongoDB to be ready...
🧪 Running tests...
================================= test session starts =================================
collected 48 items

tests/test_cat_service.py ....                                      [ 8%]
tests/test_user_service.py ................                        [ 41%]
...
==================== XX passed, X failed, X warnings ==================
✅ Tests completed!
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
| `make test-quick` | Fast tests without coverage | ~5-8s |
| `make test` | Full test suite + coverage | ~8-12s |
| `make test-cov` | Detailed coverage + HTML report | ~10-15s |
| `./run_tests.sh` | Shell script alternative | ~8-12s |
| `pytest tests/test_user_service.py -v` | Specific test file | ~2-3s |

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



