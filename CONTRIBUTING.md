# Contributing to FastClean

First off, thank you for considering contributing to FastClean! 🎉

It's people like you that make FastClean such a great tool. We welcome contributions from everyone, whether you're fixing a typo, adding a feature, or improving documentation.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Project Structure](#project-structure)

---

## 📜 Code of Conduct

This project and everyone participating in it is governed by our commitment to providing a welcoming and inspiring community for all. By participating, you are expected to uphold this standard.

**Expected Behavior:**
- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

**Unacceptable Behavior:**
- Harassment, trolling, or discriminatory language
- Public or private harassment
- Publishing others' private information
- Any conduct which could reasonably be considered inappropriate

---

## 🤝 How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check the [existing issues](https://github.com/Amirrdoustdar/fastclean/issues) to avoid duplicates.

When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the behavior
- **Expected behavior** vs **actual behavior**
- **Environment details** (OS, Python version, FastClean version)
- **Error messages or logs** (if applicable)
- **Screenshots** (if helpful)

**Bug Report Template:**
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Run command '...'
2. See error

**Expected behavior**
What you expected to happen.

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.11]
- FastClean: [e.g., 1.0.0]

**Additional context**
Any other context about the problem.
```

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the proposed feature
- **Explain why this enhancement would be useful**
- **List any alternatives** you've considered
- **Include examples or mockups** if applicable

### 📝 Improving Documentation

Documentation improvements are always welcome! This includes:

- Fixing typos or unclear wording
- Adding examples or tutorials
- Improving API documentation
- Translating documentation
- Creating video tutorials or blog posts

### 🔧 Contributing Code

We love code contributions! Here's what we're particularly interested in:

**High Priority:**
- Bug fixes
- Performance improvements
- Test coverage improvements
- Documentation improvements

**Feature Requests:**
- New database support (MongoDB, etc.)
- New authentication methods
- Additional template generators
- CI/CD pipeline templates
- Monitoring integrations

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- pip and virtualenv
- Basic understanding of FastAPI and Clean Architecture

### Fork the Repository

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/fastclean.git
   cd fastclean
   ```

3. Add the original repository as upstream:
   ```bash
   git remote add upstream https://github.com/Amirrdoustdar/fastclean.git
   ```

---

## 🛠️ Development Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Development Dependencies

```bash
pip install -e ".[dev]"
```

This installs FastClean in editable mode with all development dependencies:
- pytest (testing)
- black (code formatting)
- flake8 (linting)
- mypy (type checking)
- pre-commit (git hooks)

### 3. Install Pre-commit Hooks

```bash
pre-commit install
```

This ensures code quality checks run automatically before each commit.

### 4. Verify Installation

```bash
# Check if fastapi-clean command works
fastapi-clean --version

# Run tests
pytest

# Check code style
black --check .
flake8 .
mypy fastclean/
```

---

## 🔄 Pull Request Process

### 1. Create a Branch

Create a feature branch from `main`:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
# or
git checkout -b docs/your-documentation-update
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test improvements
- `chore/` - Maintenance tasks

### 2. Make Your Changes

- Write clear, readable code
- Follow the [coding standards](#coding-standards)
- Add tests for new features
- Update documentation as needed
- Keep commits focused and atomic

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=fastclean --cov-report=html

# Run specific tests
pytest tests/test_cli.py

# Run linting
black .
flake8 .
mypy fastclean/
```

### 4. Commit Your Changes

Follow the [commit message guidelines](#commit-message-guidelines):

```bash
git add .
git commit -m "feat: add PostgreSQL connection pooling"
```

### 5. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 6. Create Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your feature branch
4. Fill out the PR template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## How Has This Been Tested?
Describe the tests you ran

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass locally
```

### 7. Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, your PR will be merged! 🎉

### 8. After Merge

```bash
# Update your local main branch
git checkout main
git pull upstream main

# Delete your feature branch
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

---

## 📏 Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

**Line Length:**
- Maximum 100 characters (not 79)

**Imports:**
```python
# Standard library
import os
import sys

# Third-party
import click
from jinja2 import Template

# Local
from fastclean.core import Generator
from fastclean.utils import format_name
```

**Type Hints:**
Always use type hints for function arguments and return values:

```python
def create_project(name: str, path: Path, options: Dict[str, Any]) -> bool:
    """Create a new FastAPI project.
    
    Args:
        name: Project name
        path: Project directory path
        options: Additional options
        
    Returns:
        True if successful, False otherwise
    """
    pass
```

**Docstrings:**
Use Google-style docstrings:

```python
def generate_crud(entity: str, fields: List[str]) -> None:
    """Generate CRUD operations for an entity.
    
    This function creates all necessary files for CRUD operations
    including models, repositories, use cases, and API routes.
    
    Args:
        entity: Name of the entity (e.g., "User", "Product")
        fields: List of field definitions (e.g., ["name:str", "age:int"])
        
    Raises:
        ValueError: If entity name is invalid
        FileExistsError: If entity already exists
        
    Example:
        >>> generate_crud("Product", ["name:str", "price:float"])
    """
    pass
```

**Code Formatting:**
```bash
# Format code with black
black fastclean/

# Check formatting
black --check fastclean/
```

**Linting:**
```bash
# Run flake8
flake8 fastclean/

# With configuration
flake8 --max-line-length=100 --exclude=venv,__pycache__
```

**Type Checking:**
```bash
# Run mypy
mypy fastclean/
```

---

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── unit/                    # Unit tests
│   ├── test_generator.py
│   ├── test_templates.py
│   └── test_utils.py
└── integration/             # Integration tests
    ├── test_cli.py
    └── test_project_generation.py
```

### Writing Tests

**Unit Tests:**
```python
import pytest
from fastclean.core.generator import ProjectGenerator

def test_validate_project_name():
    """Test project name validation."""
    generator = ProjectGenerator()
    
    # Valid names
    assert generator.validate_name("my_project") is True
    assert generator.validate_name("MyProject") is True
    
    # Invalid names
    assert generator.validate_name("123project") is False
    assert generator.validate_name("my-project!") is False

@pytest.mark.parametrize("name,expected", [
    ("user", "User"),
    ("product_item", "ProductItem"),
    ("API_KEY", "ApiKey"),
])
def test_format_entity_name(name, expected):
    """Test entity name formatting."""
    from fastclean.utils import format_entity_name
    assert format_entity_name(name) == expected
```

**Integration Tests:**
```python
import pytest
from click.testing import CliRunner
from fastclean.cli import cli

def test_init_command(tmp_path):
    """Test project initialization command."""
    runner = CliRunner()
    result = runner.invoke(cli, [
        'init',
        '--name', 'test_project',
        '--path', str(tmp_path),
        '--db', 'postgresql'
    ])
    
    assert result.exit_code == 0
    assert (tmp_path / 'test_project').exists()
    assert (tmp_path / 'test_project' / 'src').exists()
```

**Fixtures:**
```python
# conftest.py
import pytest
from pathlib import Path

@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary project directory."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    return project_dir

@pytest.fixture
def sample_config():
    """Sample configuration for tests."""
    return {
        "name": "test_project",
        "db": "postgresql",
        "auth": "jwt"
    }
```

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/unit/test_generator.py

# Specific test
pytest tests/unit/test_generator.py::test_validate_project_name

# With coverage
pytest --cov=fastclean --cov-report=html

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Run only failed tests
pytest --lf
```

### Test Coverage

We aim for 80%+ test coverage. Check coverage with:

```bash
pytest --cov=fastclean --cov-report=html
open htmlcov/index.html  # View in browser
```

---

## 💬 Commit Message Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

### Examples

```bash
# Feature
git commit -m "feat(cli): add MongoDB support to init command"

# Bug fix
git commit -m "fix(generator): resolve template rendering issue with special characters"

# Documentation
git commit -m "docs: add examples for CRUD generation"

# Breaking change
git commit -m "feat(api)!: change authentication method

BREAKING CHANGE: JWT tokens now require 'Bearer ' prefix"
```

### Best Practices

- Use present tense ("add feature" not "added feature")
- Use imperative mood ("move cursor to..." not "moves cursor to...")
- First line should be 50 characters or less
- Reference issues and PRs when relevant (#123)
- Explain "what" and "why" not "how"

---

## 🏗️ Project Structure

Understanding the project structure helps you navigate and contribute:

```
fastclean/
├── fastclean/                    # Main package
│   ├── __init__.py
│   ├── cli.py                   # CLI commands (Click)
│   ├── core/                    # Core functionality
│   │   ├── generator.py         # Project generator
│   │   ├── crud_generator.py    # CRUD generator
│   │   └── template_engine.py   # Template processing
│   ├── templates/               # Jinja2 templates
│   │   ├── project/             # Project structure templates
│   │   ├── crud/                # CRUD templates
│   │   └── features/            # Feature templates
│   └── utils/                   # Utility functions
│       ├── file_utils.py
│       ├── string_utils.py
│       └── validators.py
├── tests/                       # Test suite
├── docs/                        # Documentation
├── .github/                     # GitHub specific files
│   └── workflows/               # CI/CD workflows
├── pyproject.toml              # Project metadata
├── setup.py                    # Setup configuration
└── README.md                   # Main documentation
```

### Key Files

**`cli.py`** - CLI command definitions
```python
@click.command()
@click.option('--name', required=True, help='Project name')
def init(name: str):
    """Initialize a new FastAPI project."""
    pass
```

**`core/generator.py`** - Main project generation logic

**`templates/`** - Jinja2 templates for code generation

**`tests/`** - Comprehensive test suite

---

## 🎯 What to Work On

### Good First Issues

Look for issues labeled `good first issue`:
- Documentation improvements
- Simple bug fixes
- Adding examples
- Writing tests

### Areas Needing Help

- **MongoDB Support**: Complete implementation
- **GraphQL Templates**: Add GraphQL support
- **More Examples**: Real-world project examples
- **Documentation**: Video tutorials, blog posts
- **Testing**: Increase coverage to 90%+
- **Performance**: Optimize template rendering

---

## 🆘 Getting Help

### Questions?

- **GitHub Discussions**: [Ask questions](https://github.com/Amirrdoustdar/fastclean/discussions)
- **Issues**: [Report bugs](https://github.com/Amirrdoustdar/fastclean/issues)
- **Email**: amirrdoustdar1@gmail.com

### Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Click Documentation](https://click.palletsprojects.com/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)

---

## 🏆 Recognition

Contributors will be:
- Listed in the README
- Credited in release notes
- Given shout-outs on social media
- Added to the GitHub Contributors page

---

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Your contributions make FastClean better for everyone. Whether you're fixing a typo or adding a major feature, we appreciate your effort!

**Happy coding!** 🚀

---

<div align="center">

**Questions? Reach out to [@Amirrdoustdar](https://github.com/Amirrdoustdar)**

Made with ❤️ by the FastClean community

</div>
