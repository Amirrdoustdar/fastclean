# 🚀 FastAPIClean

**The Ultimate CLI tool for scaffolding FastAPI projects with Clean Architecture principles.**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

---

## 📋 Table of Contents

- [Introduction](#-introduction)
- [Features](#-features)
- [Architecture](#-Architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Commands](#-commands)
- [Project Structure](#-project-structure)
- [Production Ready](#-production-ready)
- [Contributing](#-contributing)
- [Acknowledgments](#-acknowledgments)

---

## 📖 Introduction

**FastClean** is a powerful command-line interface designed to streamline the development of FastAPI applications. It enforces **Clean Architecture** (Uncle Bob's architecture) and SOLID principles.

Forget about setting up project structures, configuring Docker, or writing boilerplate CRUD code. FastClean does it all for you.

---

## ✨ Features

### 🏗️ Robust Architecture
- Domain-Driven Design (DDD) ready structure.
- 4-Layer Architecture: Domain, Application, Infrastructure, Presentation.
- Dependency Injection: Built-in container pattern.
- Repository Pattern: Decoupled data access logic.

### ⚡ Instant Scaffolding
- Production Setup: Docker, Docker Compose, Nginx (optional).
- Background Tasks: Auto-configured Celery with Redis.
- Object Storage: Built-in MinIO/S3 client integration.
- Monitoring: Ready-to-use Prometheus & Grafana configs.

### 🛠️ Developer Experience
- CRUD Generator: Generate Entities, Use Cases, Repositories, Routes, and Tests with one command.
- Testing: Auto-generated Unit and Integration tests using `pytest`.
- CI/CD: GitHub Actions workflows included.

---

## 🏛️ 

FastClean follows the Dependency Rule: source code dependencies can only point inwards.

```
┌───────────────────────────────────────────────┐
│ Presentation (API Routes, CLI, Schemas)       │ ← Outer Layer
├───────────────────────────────────────────────┤
│ Infrastructure (DB, Celery, MinIO, Auth)      │ ← External Interfaces
├───────────────────────────────────────────────┤
│ Application (Use Cases, Interfaces, DTOs)     │ ← Application Business Rules
├───────────────────────────────────────────────┤
│ Domain (Entities, Value Objects)              │ ← Enterprise Business Rules
└───────────────────────────────────────────────┘
```
---

## 📦 Installation

### From Source (Recommended for now)

```bash
git clone https://github.com/Amirrdoustdar/fastclean.git
cd fastclean
pip install -e .
```

Verify installation:

```bash
fastclean --help
```

---

## 🚀 Quick Start

1. Initialize a Project:

```bash
fastclean init --name=my_shop_api --db=postgresql --docker
```

2. Run the Project locally:

```bash
cd my_shop_api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

3. Documentation:

Open your browser at http://localhost:8000/docs to see the auto-generated Swagger UI.

---

## 🎮 Commands

1️⃣ init - Create New Project  
The init command is highly customizable. You can choose your stack.

Basic Usage:

```bash
fastclean init --name=blog_api
```

Enterprise Usage (Full Stack):

```bash
fastclean init \
  --name=enterprise_app \
  --db=postgresql \
  --cache=redis \
  --queue=celery \
  --auth=jwt \
  --storage=minio \
  --monitoring=prometheus \
  --ci=github-actions \
  --docker
```

Options (short summary):

- --name: Project name (string)
- --db: Database (postgresql, mysql, sqlite, mongodb)
- --cache: Caching (redis, memcached, none)
- --queue: Background Workers (celery, none)
- --storage: File Storage (minio, s3, local)
- --monitoring: Metrics (prometheus, none)
- --docker: Include Docker setup (flag)

2️⃣ crud - Generate Resources  
Generate a complete vertical slice for a resource (Entity, Repository, Use Cases, API, Tests).

Usage:

```bash
fastclean crud EntityName --fields="name:type,name:type"
```

Example:

```bash
fastclean crud Product --fields="name:str,price:float,is_active:bool,description:str"
```

What gets created (example):

- src/domain/entities/product.py
- src/domain/repositories/product_repository.py
- src/application/usecases/product/* (Create, Read, Update, Delete, List)
- src/infrastructure/database/repositories/product_repository.py
- src/interfaces/api/v1/routes/product.py
- src/interfaces/schemas/product.py
- tests/unit/test_product_usecase.py
- tests/integration/test_product_api.py

---

## 📁 Project Structure

Below is an example layout for a project generated by FastClean:

```text
my_project/
│
├── src/
│   ├── domain/                  # Enterprise Rules
│   │   ├── entities/
│   │   └── repositories/        # Interfaces
│   │
│   ├── application/             # Application Rules
│   │   ├── usecases/            # Command/Query handlers
│   │   └── interfaces/          # Ports
│   │
│   ├── infrastructure/          # External Details
│   │   ├── config/
│   │   ├── database/
│   │   ├── security/            # JWT Handler
│   │   ├── worker/              # Celery App
│   │   └── external_services/   # MinIO/S3 Client
│   │
│   ├── interfaces/              # Interface Adapters
│   │   ├── api/v1/routes/
│   │   └── schemas/             # Pydantic DTOs
│   │
│   └── main.py
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── .env
├── docker-compose.yml           # Auto-generated based on flags
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🏭 Production Ready

When you use the `--docker` flag, FastClean generates a `docker-compose.yml` that orchestrates:

- API Service (Uvicorn)
- Database (PostgreSQL/MySQL)
- Redis (Caching & Message Broker)
- Celery Worker (Background Jobs)
- MinIO (S3 Compatible Storage)
- Prometheus & Grafana (Monitoring)

Run your entire stack with one command:

```bash
docker-compose up --build
```

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project  
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)  
3. Commit your Changes (git commit -m 'Add some AmazingFeature')  
4. Push to the Branch (git push origin feature/AmazingFeature)  
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments


Inspired by [HiDjango](https://github.com/parsarezaee/HiDjango)

Based on Clean Architecture by [Robert C. Martin](https://en.wikipedia.org/wiki/Robert_C._Martin)


---

## 📧 Contact

Author: Amir Doustdar  
Email: amirrdoustdar1@gmail.com  
GitHub: @amirrdoustdar  
Issues: GitHub Issues

⭐ Star History  
If this project helped you, please consider giving it a star! ⭐

Project Link: https://github.com/Amirrdoustdar/fastclean

Made with ❤️ and Clean Architecture
