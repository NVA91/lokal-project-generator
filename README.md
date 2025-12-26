# Lokal Project Generator

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Professional scaffolding tool for standardized project setup.**

🚀 Eliminate boilerplate. Generate consistent projects. Automate everything.

## Features

✨ **Core Features:**
- 🖥️ **CLI Interface** - Powerful command-line interface via `click`
- 📦 **Template-Based Generation** - Create projects from structured templates
- 🎨 **Jinja2 Rendering** - Dynamic variables in your templates
- 🔗 **Hook System** - Execute custom scripts before/after generation
- ⚙️ **JSON Config** - Template and global configuration
- 🧪 **Fully Tested** - Comprehensive unit + integration tests (TDD)
- 🔐 **Type-Safe** - Python 3.8+ with type hints

## Quick Start

### Installation

```bash
git clone https://github.com/NVA91/lokal-project-generator.git
cd lokal-project-generator
make dev  # or: poetry install --with dev
```

### Usage

```bash
# Generate project from template
lokal generate ./templates/python-project my-awesome-app

# List available templates
lokal list --path ./templates

# Preview template structure
lokal preview ./templates/python-project

# Manage global config
lokal config show
lokal config set author \"Your Name\"
```

## Development

### Running Tests

```bash
make test              # Run all tests
make test-cov         # With coverage
make test-unit        # Unit tests only
make test-int         # Integration tests only
```

### Code Quality

```bash
make lint             # Check code style
make format           # Format code
make type             # Type checking
```

## Documentation

See [README_PHASE1.md](./README_PHASE1.md) for detailed Phase 1 architecture and implementation guide.

## License

MIT License - see LICENSE file for details

---

**Made with ❤️ for developers who love automation**
