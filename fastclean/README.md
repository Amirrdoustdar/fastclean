# fastclean

🚀 CLI tool for creating FastAPI projects with Clean Architecture

## Quick Start

```bash
# Install
pip install -e .

# Create templates
make templates

# Create a new project
fastclean init --name=my_api --db=postgresql --docker

# Generate CRUD
fastclean crud Product --fields="name:str,price:float"
```

## Features

- ✅ Clean Architecture (4 layers)
- ✅ Async/Await support
- ✅ Multiple databases (PostgreSQL, MySQL, SQLite)
- ✅ Docker ready
- ✅ Auto-generated tests
- ✅ JWT Authentication
- ✅ Redis caching

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/fastclean.git
cd fastclean

# Install dependencies
pip install -e ".[dev]"

# Create templates
make templates

# Run tests
make test
```

## Documentation

See [ARCHITECTURE.md](ARCHITECTURE.md) for architecture details.

## License

MIT License
