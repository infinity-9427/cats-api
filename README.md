# 🐱 Cats API - Backend Application

Una API REST desarrollada con FastAPI para gestionar información de razas de gatos y usuarios, integrada con [The Cat API](https://thecatapi.com/) y base de datos MongoDB.

## 🚀 Características

- **API RESTful** con FastAPI
- **Base de datos MongoDB** para gestión de usuarios
- **Integración con The Cat API** para información de razas
- **Autenticación JWT** para usuarios
- **Arquitectura limpia** siguiendo principios SOLID
- **Pruebas unitarias** con pytest
- **Contenerización** con Docker y Docker Compose
- **Documentación automática** con Swagger UI

## 🛠️ Tecnologías Utilizadas

### Backend Framework
- **FastAPI** - Framework web moderno y rápido para Python
- **Uvicorn** - Servidor ASGI para FastAPI
- **Pydantic** - Validación de datos y serialización

### Base de Datos
- **MongoDB** - Base de datos NoSQL
- **Motor** - Driver asíncrono de MongoDB para Python
- **PyMongo** - Driver oficial de MongoDB

### Autenticación y Seguridad
- **JWT (JSON Web Tokens)** - Para autenticación
- **bcrypt** - Para hash de contraseñas
- **python-jose** - Para manejo de JWT

### Integración Externa
- **httpx** - Cliente HTTP asíncrono para integración con The Cat API

### Testing
- **pytest** - Framework de testing
- **pytest-asyncio** - Para testing asíncrono

### Containerización
- **Docker** - Para contenerización
- **Docker Compose** - Para orquestación de servicios

## 📋 Requisitos Previos

- Docker
- Docker Compose
- Python 3.11+ (para desarrollo local)

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd cats-api
```

### 2. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

### 3. Ejecutar con Docker Compose
```bash
# Construir y ejecutar todos los servicios
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f cats-api
```

### 4. Acceder a los servicios
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **MongoDB Express**: http://localhost:8081 (admin/admin)

## 📚 Endpoints de la API

### 🏠 General
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Página de inicio |
| GET | `/health` | Estado de salud de la API |

### 🐱 Controlador de Gatos

#### Obtener todas las razas
```http
GET /breeds
```

**Respuesta exitosa (200)**:
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

#### Obtener raza por ID
```http
GET /breeds/{breed_id}
```

**Parámetros**:
- `breed_id` (string): ID de la raza

**Ejemplo**:
```bash
curl -X GET "http://localhost:8000/breeds/abys"
```

**Respuesta exitosa (200)**:
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

#### Buscar razas
```http
GET /breeds/search
```

**Parámetros de consulta**:
- `q` (string): Término de búsqueda
- `limit` (int, opcional): Límite de resultados (default: 10)
- `page` (int, opcional): Página de resultados (default: 0)

**Ejemplo**:
```bash
curl -X GET "http://localhost:8000/breeds/search?q=persian&limit=5"
```

**Respuesta exitosa (200)**:
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

### 👤 Controlador de Usuarios

#### Obtener todos los usuarios
```http
GET /users
```

**Headers requeridos**:
- `Authorization: Bearer <token>`

**Respuesta exitosa (200)**:
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

#### Crear usuario
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

**Respuesta exitosa (201)**:
```json
{
  "id": "64a1234567890abcdef12345",
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2023-07-10T10:30:00Z",
  "message": "Usuario creado exitosamente"
}
```

#### Iniciar sesión
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

**Respuesta exitosa (200)**:
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

## 🔧 Configuración

### Variables de Entorno

```env
# Base de datos
DATABASE_URL=mongodb://admin:password123@mongodb:27017/cats_api?authSource=admin

# API Externa
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

## 🧪 Pruebas

### Ejecutar pruebas unitarias
```bash
# Con Docker
docker-compose exec cats-api pytest

# Local
pytest tests/

# Con cobertura
pytest --cov=app tests/
```

### Ejemplos de pruebas
```bash
# Probar endpoint de salud
curl -X GET "http://localhost:8000/health"

# Probar creación de usuario
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"test@example.com","password":"test123"}'

# Probar login
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"test_user","password":"test123"}'
```

## 🏗️ Arquitectura

El proyecto sigue principios de **Clean Architecture** y **SOLID**:

```
app/
├── controllers/          # Controladores REST
│   ├── cats_controller.py
│   └── users_controller.py
├── services/            # Lógica de negocio
│   ├── cats_service.py
│   ├── users_service.py
│   └── auth_service.py
├── models/              # Modelos de datos
│   ├── cat_models.py
│   └── user_models.py
├── repositories/        # Acceso a datos
│   ├── cats_repository.py
│   └── users_repository.py
├── utils/              # Utilidades
│   ├── database.py
│   └── security.py
└── main.py             # Punto de entrada
```

## 📊 Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | Éxito |
| 201 | Recurso creado |
| 400 | Solicitud incorrecta |
| 401 | No autorizado |
| 403 | Prohibido |
| 404 | Recurso no encontrado |
| 409 | Conflicto (usuario duplicado) |
| 500 | Error interno del servidor |

## 🐛 Troubleshooting

### Problemas comunes

1. **Error de conexión a MongoDB**:
   ```bash
   docker-compose down
   docker-compose up mongodb
   # Esperar a que MongoDB esté listo
   docker-compose up cats-api
   ```

2. **Puerto ya en uso**:
   ```bash
   # Cambiar puertos en docker-compose.yml
   ports:
     - "8001:8000"  # En lugar de 8000:8000
   ```

3. **Regenerar contenedores**:
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```



