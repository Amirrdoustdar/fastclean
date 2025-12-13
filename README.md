# 🚀 FastAPI Clean CLI

**The Ultimate CLI tool for scaffolding FastAPI projects with Clean Architecture principles.**

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi-clean-cli)](https://pypi.org/project/fastapi-clean-cli/)
[![PyPI version](https://badge.fury.io/py/fastapi-clean-cli.svg)](https://pypi.org/project/fastapi-clean-cli/)
[![Downloads](https://pepy.tech/badge/fastapi-clean-cli)](https://pepy.tech/project/fastapi-clean-cli)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

---

## 📋 Table of Contents

- [Introduction](#-introduction)
- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Commands](#-commands)
- [Project Structure](#-project-structure)
- [Examples](#-examples)
- [Production Ready](#-production-ready)
- [Contributing](#-contributing)
- [Changelog](#-changelog)
- [Acknowledgments](#-acknowledgments)

---

## 📖 Introduction

**FastAPI Clean CLI** is a powerful command-line interface designed to streamline the development of FastAPI applications. It enforces **Clean Architecture** (Uncle Bob's architecture) and SOLID principles, allowing you to focus on business logic rather than boilerplate code.

### 🎯 Why FastAPI Clean CLI?

- ⚡ **Save Hours**: Generate production-ready projects in seconds
- 🏗️ **Best Practices**: Clean Architecture, SOLID principles, DDD patterns
- 🔧 **Batteries Included**: Docker, Tests, CI/CD, Monitoring out of the box
- 📚 **Learn by Example**: Educational reference implementation
- 🚀 **Production Ready**: Enterprise-grade structure from day one

---

## ✨ Features

### 🏗️ **Robust Architecture**
- ✅ **4-Layer Clean Architecture**: Domain → Application → Infrastructure → Presentation
- ✅ **Domain-Driven Design**: Entity-centric business logic
- ✅ **Dependency Injection**: Built-in IoC container
- ✅ **Repository Pattern**: Abstract data access
- ✅ **Use Case Pattern**: Single responsibility business operations

### ⚡ **Instant Scaffolding**
- ✅ **Multiple Databases**: PostgreSQL, MySQL, SQLite, MongoDB (coming soon)
- ✅ **Authentication**: JWT, OAuth2, API Key support
- ✅ **Caching**: Redis, Memcached integration
- ✅ **Background Jobs**: Celery with Redis/RabbitMQ
- ✅ **Object Storage**: MinIO/S3 client integration
- ✅ **Monitoring**: Prometheus & Grafana configs

### 🛠️ **Developer Experience**
- ✅ **CRUD Generator**: Full vertical slice in one command
- ✅ **Async/Await**: Native async support throughout
- ✅ **Type Hints**: Complete type safety
- ✅ **Auto Tests**: Unit and integration tests generated
- ✅ **CI/CD Ready**: GitHub Actions workflows included
- ✅ **Docker Ready**: Complete containerization setup
- ✅ **API Documentation**: Auto-generated Swagger/OpenAPI

---

## 🏛️ Architecture

FastAPI Clean CLI follows the **Dependency Rule**: source code dependencies can only point inwards.

```
┌──────────────────────────────────────────────────┐
│  Presentation Layer (API, CLI, Schemas)          │ ← Frameworks & Drivers
├──────────────────────────────────────────────────┤
│  Infrastructure Layer (DB, Cache, Queue, Auth)   │ ← Interface Adapters
├──────────────────────────────────────────────────┤
│  Application Layer (Use Cases, DTOs, Ports)      │ ← Application Business Rules
├──────────────────────────────────────────────────┤
│  Domain Layer (Entities, Value Objects)          │ ← Enterprise Business Rules
└──────────────────────────────────────────────────┘
```

### **Key Principles**
- 🎯 **Independence of Frameworks**: Business logic doesn't depend on FastAPI
- 🧪 **Testability**: Each layer can be tested independently
- 🔄 **Independence of Database**: Switch databases without changing business logic
- 🎨 **Independence of UI**: API can be swapped with GraphQL, CLI, etc.

---

## 📦 Installation

### **From PyPI (Recommended)**

```bash
pip install fastapi-clean-cli
```

### **From Source**

```bash
git clone https://github.com/Amirrdoustdar/fastclean.git
cd fastclean
pip install -e .
```

### **Verify Installation**

```bash
fastapi-clean --version
fastapi-clean --help
```

---

## 🚀 Quick Start

### **1. Create Your First Project**

```bash
# Simple project
fastapi-clean init --name=my_api

# With PostgreSQL and Docker
fastapi-clean init --name=my_api --db=postgresql --docker

# Enterprise setup
fastapi-clean init \
  --name=my_api \
  --db=postgresql \
  --cache=redis \
  --auth=jwt \
  --docker
```

### **2. Navigate and Install**

```bash
cd my_api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### **3. Run the Application**

```bash
# Development
uvicorn src.main:app --reload

# Or with Docker
docker-compose up
```

### **4. Access Documentation**

Open your browser at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 🎮 Commands

### **1️⃣ `init` - Create New Project**

Initialize a new FastAPI project with customizable options.

#### **Basic Usage**

```bash
fastapi-clean init --name=blog_api
```

#### **Full Options**

```bash
fastapi-clean init \
  --name=enterprise_app \
  --path=~/projects \
  --db=postgresql \
  --cache=redis \
  --queue=celery \
  --auth=jwt \
  --storage=minio \
  --monitoring=prometheus \
  --ci=github-actions \
  --docker
```

#### **Available Options**

| Option | Description | Choices | Default |
|--------|-------------|---------|---------|
| `--name` | Project name | Any valid identifier | Required |
| `--path` | Project directory | Any valid path | `.` |
| `--db` | Database | `postgresql`, `mysql`, `sqlite`, `mongodb` | `postgresql` |
| `--cache` | Caching system | `redis`, `memcached`, `none` | `none` |
| `--queue` | Task queue | `celery`, `arq`, `none` | `none` |
| `--auth` | Authentication | `jwt`, `oauth2`, `api_key`, `none` | `none` |
| `--storage` | File storage | `minio`, `s3`, `local` | `local` |
| `--monitoring` | Monitoring | `prometheus`, `elk`, `none` | `none` |
| `--docker` | Include Docker | Flag | `False` |
| `--ci` | CI/CD | `github-actions`, `gitlab-ci`, `none` | `none` |
| `--no-tests` | Skip tests | Flag | `False` |

---

### **2️⃣ `crud` - Generate CRUD Operations**

Generate a complete vertical slice for any entity with one command.

#### **Usage**

```bash
fastapi-clean crud EntityName --fields="field1:type1,field2:type2"
```

#### **Example**

```bash
fastapi-clean crud Product --fields="name:str,price:float,stock:int,is_active:bool,description:str"
```

#### **What Gets Generated**

```
✓ src/domain/entities/product.py                      # Domain Entity
✓ src/domain/repositories/product_repository.py       # Repository Interface
✓ src/infrastructure/database/models/product_model.py # SQLAlchemy Model
✓ src/infrastructure/database/repositories/product_repository.py # Repository Impl
✓ src/application/usecases/product/create_product.py  # Create Use Case
✓ src/application/usecases/product/get_product.py     # Get Use Case
✓ src/application/usecases/product/update_product.py  # Update Use Case
✓ src/application/usecases/product/delete_product.py  # Delete Use Case
✓ src/application/usecases/product/list_products.py   # List Use Case
✓ src/interfaces/api/v1/routes/product.py            # API Routes
✓ src/interfaces/schemas/product.py                  # Pydantic Schemas
✓ tests/unit/test_product_usecase.py                 # Unit Tests
✓ tests/integration/test_product_api.py              # Integration Tests
```

#### **Supported Field Types**

- `str` - String
- `int` - Integer
- `float` - Float/Decimal
- `bool` - Boolean
- `datetime` - DateTime
- `date` - Date
- `Optional[type]` - Optional field

---

### **3️⃣ `feature` - Add Features**

Add features to an existing project.

#### **Usage**

```bash
fastapi-clean feature FEATURE_NAME --type=TYPE
```

#### **Examples**

```bash
# Add JWT Authentication
fastapi-clean feature auth --type=jwt

# Add Redis Caching
fastapi-clean feature cache --type=redis

# Add Celery Background Jobs
fastapi-clean feature queue --type=celery

# Add Prometheus Monitoring
fastapi-clean feature monitoring --type=prometheus
```

---

## 📁 Project Structure

Generated projects follow a strict Clean Architecture layout:

```
my_project/
│
├── src/
│   ├── domain/                      # 🎯 Enterprise Business Rules
│   │   ├── entities/               # Business entities
│   │   ├── repositories/           # Repository interfaces (Ports)
│   │   └── value_objects/          # Value objects
│   │
│   ├── application/                 # 🔧 Application Business Rules
│   │   ├── usecases/               # Use case implementations
│   │   │   ├── user/
│   │   │   │   ├── create_user.py
│   │   │   │   ├── get_user.py
│   │   │   │   └── list_users.py
│   │   └── interfaces/             # Input/Output ports
│   │
│   ├── infrastructure/              # 🏗️ Frameworks & Drivers
│   │   ├── config/                 # Configuration
│   │   │   └── settings.py
│   │   ├── database/               # Database implementation
│   │   │   ├── database.py
│   │   │   ├── models/             # SQLAlchemy models
│   │   │   └── repositories/       # Repository implementations
│   │   ├── security/               # JWT, OAuth2 handlers
│   │   ├── worker/                 # Celery app
│   │   └── external_services/      # MinIO, S3, etc.
│   │
│   ├── interfaces/                  # 🌐 Interface Adapters
│   │   ├── api/
│   │   │   ├── dependencies.py     # FastAPI dependencies
│   │   │   └── v1/
│   │   │       └── routes/         # API endpoints
│   │   │           ├── user.py
│   │   │           └── health.py
│   │   └── schemas/                # Pydantic DTOs
│   │       └── user.py
│   │
│   └── main.py                      # FastAPI application
│
├── tests/
│   ├── conftest.py                  # Pytest configuration
│   ├── unit/                        # Unit tests
│   │   └── test_create_user_usecase.py
│   └── integration/                 # Integration tests
│       └── test_user_api.py
│
├── docker-compose.yml               # Multi-service orchestration
├── Dockerfile                       # Container definition
├── .env.example                     # Environment variables template
├── .gitignore
├── requirements.txt                 # Python dependencies
├── pytest.ini                       # Pytest configuration
└── README.md
```

---

## 💡 Examples

### **Example 1: E-Commerce API**

```bash
# Initialize project
fastapi-clean init \
  --name=shop_api \
  --db=postgresql \
  --cache=redis \
  --auth=jwt \
  --docker

cd shop_api

# Generate entities
fastapi-clean crud Product --fields="name:str,price:float,stock:int,category:str"
fastapi-clean crud Order --fields="user_id:int,total:float,status:str,created_at:datetime"
fastapi-clean crud Customer --fields="email:str,name:str,phone:str"

# Run
docker-compose up
```

### **Example 2: Blog API**

```bash
# Initialize
fastapi-clean init --name=blog_api --db=postgresql --auth=jwt

cd blog_api

# Generate
fastapi-clean crud Post --fields="title:str,content:str,author_id:int,published:bool"
fastapi-clean crud Comment --fields="post_id:int,user_id:int,content:str"
fastapi-clean crud Category --fields="name:str,slug:str"

# Run
uvicorn src.main:app --reload
```

### **Example 3: Microservice**

```bash
# Initialize with monitoring
fastapi-clean init \
  --name=user_service \
  --db=postgresql \
  --cache=redis \
  --monitoring=prometheus \
  --docker

cd user_service
docker-compose up

# Metrics available at: http://localhost:9090
```

---

## 🏭 Production Ready

When you use the `--docker` flag, FastAPI Clean CLI generates a complete `docker-compose.yml` that orchestrates:

### **Services Included**

| Service | Description | Port |
|---------|-------------|------|
| **API** | FastAPI with Uvicorn | 8000 |
| **Database** | PostgreSQL/MySQL | 5432/3306 |
| **Redis** | Caching & Message Broker | 6379 |
| **Celery Worker** | Background Jobs | - |
| **MinIO** | S3-compatible Storage | 9000 |
| **Prometheus** | Metrics Collection | 9090 |
| **Grafana** | Metrics Visualization | 3000 |

### **One Command Deploy**

```bash
docker-compose up --build
```

### **Environment Variables**

All sensitive data is managed via `.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@db:5432/mydb

# Redis
REDIS_URL=redis://redis:6379/0

# JWT
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256

# MinIO
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=password
```

---

## 🧪 Testing

Generated projects include comprehensive test suites.

### **Run Tests**

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# With coverage
pytest --cov=src --cov-report=html
```

### **Test Structure**

```python
# tests/unit/test_create_user_usecase.py
import pytest
from src.application.usecases.user.create_user import CreateUserUseCase

@pytest.mark.asyncio
async def test_create_user_success(mock_user_repository):
    usecase = CreateUserUseCase(mock_user_repository)
    user = await usecase.execute("test@example.com", "testuser")
    assert user.email == "test@example.com"
```

---

## 📊 Benchmarks

| Metric | Value |
|--------|-------|
| **Project Generation** | < 5 seconds |
| **CRUD Generation** | < 2 seconds |
| **Files Generated (init)** | 40+ files |
| **Lines of Code (init)** | 1,500+ LOC |
| **Test Coverage** | 80%+ (goal) |

---

## 🤝 Contributing

Contributions are what make the open-source community amazing! Any contributions you make are **greatly appreciated**.

### **How to Contribute**

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### **Development Setup**

```bash
git clone https://github.com/Amirrdoustdar/fastclean.git
cd fastclean
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pre-commit install
pytest
```

---

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed release notes.

### **Latest Release: v1.0.0**
- ✅ Initial stable release
- ✅ Complete Clean Architecture implementation
- ✅ CRUD generator
- ✅ Multiple database support
- ✅ Docker integration
- ✅ JWT authentication
- ✅ Redis caching

---

## 🐛 Known Issues

- ⚠️ MongoDB support is experimental (coming in v1.1.0)
- ⚠️ GraphQL templates not yet available (planned for v1.2.0)

Report bugs at: [GitHub Issues](https://github.com/Amirrdoustdar/fastclean/issues)

---

## 🗺️ Roadmap

### **v1.1.0** (Next Release)
- [ ] MongoDB full support
- [ ] GraphQL generator
- [ ] Interactive CLI mode
- [ ] WebSocket templates
- [ ] More database option

### **v1.2.0**
- [ ] Kubernetes manifests generator
- [ ] gRPC support
- [ ] Event sourcing templates
- [ ] CQRS pattern implementation

### **v2.0.0**
- [ ] Multi-tenancy support
- [ ] Advanced monitoring (OpenTelemetry)
- [ ] Service mesh integration
- [ ] Serverless deployment templates

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Special thanks to:

- **[Robert C. Martin (Uncle Bob)](https://en.wikipedia.org/wiki/Robert_C._Martin)** - For Clean Architecture principles
- **[FastAPI](https://fastapi.tiangolo.com/)** - Amazing Python framework
- **[HiDjango](https://github.com/parsarezaee/HiDjango)** - Inspiration for CLI design
- **Open Source Community** - For continuous support and contributions

---

## 📧 Contact & Support

- **Author**: Amir Doustdar
- **Email**: amirrdoustdar1@gmail.com
- **GitHub**: [@Amirrdoustdar](https://github.com/Amirrdoustdar)
- **Issues**: [GitHub Issues](https://github.com/Amirrdoustdar/fastclean/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Amirrdoustdar/fastclean/discussions)

---

## 🔗 Links

- **PyPI**: https://pypi.org/project/fastapi-clean-cli/
- **GitHub**: https://github.com/Amirrdoustdar/fastclean
- **Documentation**: [Coming Soon]
- **Blog Post**: [Coming Soon]

---

## ⭐ Star History

If this project helped you, please consider giving it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=Amirrdoustdar/fastclean&type=Date)](https://star-history.com/#Amirrdoustdar/fastclean&Date)

---

## 💖 Sponsors

Become a sponsor and get your logo here! [Sponsor this project](https://github.com/sponsors/Amirrdoustdar)

---

**Made with ❤️ and Clean Architecture principles**

*FastAPI Clean CLI - From zero to production in minutes*
