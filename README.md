# 🐱 Cats API - Backend Application

A REST API developed with FastAPI to manage cat breed information and users, integrated with [The Cat API](https://thecatapi.com/) and MongoDB database.

## 🚀 Features

- **RESTful API** with FastAPI
- **MongoDB database** for user management
- **The Cat API integration** for breed information
- **JWT authentication** for users
- **Clean architecture** following SOLID principles
- **Unit testing** with pytest
- **Containerization** with Docker and Docker Compose
- **Automatic documentation** with Swagger UI

## 🛠️ Technologies Used

### Backend Framework
- **FastAPI** - Modern, fast web framework for Python
- **Uvicorn** - ASGI server for FastAPI
- **Pydantic** - Data validation and serialization

### Database
- **MongoDB** - NoSQL database
- **Motor** - Async MongoDB driver for Python
- **PyMongo** - Official MongoDB driver

### Authentication and Security
- **JWT (JSON Web Tokens)** - For authentication
- **bcrypt** - For password hashing
- **python-jose** - For JWT handling

### External Integration
- **httpx** - Async HTTP client for The Cat API integration

### Testing
- **pytest** - Testing framework
- **pytest-asyncio** - For async testing

### Containerization
- **Docker** - For containerization
- **Docker Compose** - For service orchestration

## 📋 Prerequisites

- Docker
- Docker Compose
- Python 3.11+ (for local development)

## 🚀 Installation and Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd cats-api
```

### 2. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your configurations
```

### 3. Run with Docker Compose
```bash
# Build and run all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f cats-api
```

### 4. Access services
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **MongoDB Express**: http://localhost:8081 (admin/admin)

## 📚 API Endpoints

### 🏠 General
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page |
| GET | `/health` | API health status |

### 🐱 Cats Controller

#### Get all breeds
```http
GET /breeds
```

**Successful response (200)**:
```json
[
  {
    "id": "abys",
    "name": "Abyssinian",
    "description": "The Abyssinian is easy to care for, and a joy to have in your home...",
    "temperament": "Active, Energetic, Independent, Intelligent, Gentle",
    "origin": "Egypt",
    "life_span": "14 - 15",
    "weight": {
      "imperial": "7  -  10",
      "metric": "3 - 5"
    },
    "wikipedia_url": "https://en.wikipedia.org/wiki/Abyssinian_cat",
    "image": {
      "id": "0XYvRd7oD",
      "width": 1204,
      "height": 1445,
      "url": "https://cdn2.thecatapi.com/images/0XYvRd7oD.jpg"
    }
  }
]
```

#### Get breed by ID
```http
GET /breeds/{breed_id}
```

**Parameters**:
- `breed_id` (string): Breed ID

**Example**:
```bash
curl -X GET "http://localhost:8000/breeds/abys"
```

**Successful response (200)**:
```json
{
  "id": "abys",
  "name": "Abyssinian",
  "description": "The Abyssinian is easy to care for...",
  "temperament": "Active, Energetic, Independent",
  "origin": "Egypt",
  "life_span": "14 - 15",
  "weight": {
    "imperial": "7  -  10",
    "metric": "3 - 5"
  }
}
```

#### Search breeds
```http
GET /breeds/search
```

**Query parameters**:
- `q` (string): Search term
- `limit` (int, optional): Result limit (default: 10)
- `page` (int, optional): Page number (default: 0)

**Example**:
```bash
curl -X GET "http://localhost:8000/breeds/search?q=persian&limit=5"
```

**Successful response (200)**:
```json
{
  "results": [
    {
      "id": "pers",
      "name": "Persian",
      "description": "The Persian cat is a long-haired breed...",
      "temperament": "Affectionate, Loyal, Docile, Patient, Gentle, Quiet"
    }
  ],
  "total": 1,
  "page": 0,
  "limit": 5
}
```

### 👤 Users Controller

#### Get all users
```http
GET /users
```

**Required headers**:
- `Authorization: Bearer <token>`

**Successful response (200)**:
```json
[
  {
    "id": "64a1234567890abcdef12345",
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2023-07-10T10:30:00Z",
    "updated_at": "2023-07-10T10:30:00Z"
  }
]
```

#### Create user
```http
POST /users
```

**Body**:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Successful response (201)**:
```json
{
  "id": "64a1234567890abcdef12345",
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2023-07-10T10:30:00Z",
  "message": "User created successfully"
}
```

#### Login
```http
POST /login
```

**Body**:
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```

**Successful response (200)**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "64a1234567890abcdef12345",
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

## 🔧 Configuration

### Environment Variables

```env
# Database
DATABASE_URL=mongodb://admin:password123@mongodb:27017/cats_api?authSource=admin

# External API
BASE_URL=https://thecatapi.com
CATS_API_KEY=your_api_key_here

# JWT
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# MongoDB
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=password123
MONGO_INITDB_DATABASE=cats_api
```

## 🧪 Testing

### Run unit tests
```bash
# With Docker
docker-compose exec cats-api pytest

# Local
pytest tests/

# With coverage
pytest --cov=app tests/
```

### Testing examples
```bash
# Test health endpoint
curl -X GET "http://localhost:8000/health"

# Test user creation
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"test@example.com","password":"test123"}'

# Test login
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"test_user","password":"test123"}'
```

## 🏗️ Architecture

The project follows **Clean Architecture** and **SOLID** principles:

```
app/
├── controllers/          # REST controllers
│   ├── cats_controller.py
│   └── users_controller.py
├── services/            # Business logic
│   ├── cats_service.py
│   ├── users_service.py
│   └── auth_service.py
├── models/              # Data models
│   ├── cat_models.py
│   └── user_models.py
├── repositories/        # Data access
│   ├── cats_repository.py
│   └── users_repository.py
├── utils/              # Utilities
│   ├── database.py
│   └── security.py
└── main.py             # Entry point
```

## 📊 HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Resource created |
| 400 | Bad request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource not found |
| 409 | Conflict (duplicate user) |
| 500 | Internal server error |

## 🐛 Troubleshooting

### Common issues

1. **MongoDB connection error**:
   ```bash
   docker-compose down
   docker-compose up mongodb
   # Wait for MongoDB to be ready
   docker-compose up cats-api
   ```

2. **Port already in use**:
   ```bash
   # Change ports in docker-compose.yml
   ports:
     - "8001:8000"  # Instead of 8000:8000
   ```

3. **Regenerate containers**:
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```

