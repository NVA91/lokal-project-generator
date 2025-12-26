# Phase 1 Implementation Guide

## 🎯 Ziel

Aufbau eines professionellen Scaffolding-Tools mit:
- **Hook-System** (async, vor/nach Generierung)
- **Config-Management** (global + template-spezifisch)
- **Template-System** (Jinja2-Rendering)
- **CLI** (Click-basiert mit voller Validierung)
- **Tests** (TDD, Unit + Integration)

---

## 📦 Modul-Übersicht

### Core Modules (`src/lokal/core/`)

#### 1. **exceptions.py**
```python
# Custom exception hierarchy
LokalException
├── TemplateError
│   ├── TemplateNotFound
│   └── InvalidTemplate
├── ConfigError
├── HookExecutionError
└── RemoteTemplateError
```

✅ **Status:** Complete

#### 2. **config.py**
```python
@dataclass
class GlobalConfig:
    """~/.lokal/config.json"""
    author: str
    email: str
    license: str
    default_project_path: str
    template_paths: list
    remote_template_sources: list
    verbose: bool

@dataclass
class TemplateConfig:
    """template.json in template directory"""
    name: str
    description: str
    version: str
    dependencies: dict
    hooks: dict
    variables: dict
```

**Methods:**
- `from_file()` - Load from JSON
- `save()` - Persist to JSON
- `to_dict()` - Serialization

✅ **Status:** Complete

#### 3. **template.py**
```python
@dataclass
class Template:
    path: Path
    config: TemplateConfig

    @classmethod
    def from_path(template_path: Path) -> Template
    
    def render_file(file_path: Path, variables: dict) -> str
    
    def validate() -> bool
    
    def get_files() -> Generator[Path]
```

**Features:**
- Jinja2 template rendering
- File filtering (ignore patterns)
- Validation

✅ **Status:** Complete

#### 4. **hooks.py** ⭐ (PRIORITÄT 1)
```python
class HookStage(Enum):
    PRE_GENERATE = "pre_generate"
    POST_GENERATE = "post_generate"
    POST_INSTALL = "post_install"

class Hook:
    async def execute(context: dict) -> bool
    @staticmethod
    def _interpolate(command: str, context: dict) -> str

class HookManager:
    def register(hook: Hook) -> None
    async def execute_stage(stage: HookStage, context: dict) -> bool
    def load_from_config(config: dict) -> None
```

**Beispiel:**
```json
{
  "hooks": {
    "post_generate": [
      "git init",
      "git add .",
      "python -m venv .venv"
    ],
    "post_install": [
      "source .venv/bin/activate && pip install -r requirements.txt"
    ]
  }
}
```

**Features:**
- ✅ Async execution
- ✅ Variable interpolation (`{{project_name}}`, `{{project_path}}`)
- ✅ Multiple hook stages
- ✅ Error handling

✅ **Status:** Complete

#### 5. **generator.py**
```python
class Generator:
    def __init__(template: Template, project_name: str, output_path: Path, variables: dict)
    
    def _setup_variables() -> None
    
    def generate(dry_run: bool = False) -> Generator[Path]
```

**Funktionalität:**
- Datei-Kopierung
- Jinja2-Rendering für Text-Dateien
- Binary-Dateien "as-is" kopieren
- Dry-Run Modus (Preview ohne Dateien)
- Dateinamen-Rendering

✅ **Status:** Complete

---

### CLI Module (`src/lokal/cli/`)

#### **main.py** - CLI Entry Point
```bash
lokal --help
lokal --verbose
lokal --config ~/.lokal/config.json
```

**Context-Management:**
```python
ctx.obj = {
    'global_config': GlobalConfig,
    'config_path': Path,
    'verbose': bool
}
```

✅ **Status:** Complete

#### **commands/generate.py**
```bash
lokal generate <template_path> <project_name>
lokal generate ./templates/python my-app
lokal generate ./templates/python my-app -o ~/projects
lokal generate ./templates/python my-app --skip-hooks
lokal generate ./templates/python my-app --dry-run
```

**Features:**
- ✅ Template validation
- ✅ Path validation
- ✅ Hook execution
- ✅ Progress bar
- ✅ Colored output

✅ **Status:** Complete

#### **commands/list_cmd.py**
```bash
lokal list
lokal list --path ./templates
```

**Output:**
```
Found 3 template(s):
Name               Description              Version  Author
-----------------  -------------------------  --------  ---------
python-project     Python project template  1.0.0    Your Name
fastapi-service    FastAPI microservice     1.0.0    Your Name
react-app          React frontend           1.0.0    Your Name
```

✅ **Status:** Complete

#### **commands/preview.py**
```bash
lokal preview ./templates/python-project
```

**Output:**
```
Template: python-project
Description: Python project template
Version: 1.0.0
Author: Your Name

Files in template:
  - README.md
  - main.py
  - requirements.txt

Hooks:
  post_generate:
    - git init
    - git add .
  post_install:
    - pip install -r requirements.txt
```

✅ **Status:** Complete

#### **commands/config_cmd.py**
```bash
lokal config show
lokal config set author "Your Name"
lokal config set license "Apache-2.0"
lokal config reset
```

✅ **Status:** Complete

#### **utils/validators.py**
- `validate_project_name()` - Regex-basiert (alphanumeric, hyphens, underscores)
- `validate_path()` - Path existence check

✅ **Status:** Complete

#### **utils/formatters.py**
- `format_success()` - Grüne Ausgabe
- `format_error()` - Rote Ausgabe
- `format_info()` - Cyan Ausgabe
- `format_warning()` - Gelbe Ausgabe

✅ **Status:** Complete

---

### Testing (`src/tests/`)

#### **Unit Tests**

**test_template.py** ✅
- ✅ `test_load_valid_template()`
- ✅ `test_load_nonexistent_template()`
- ✅ `test_load_template_without_config()`
- ✅ `test_validate_valid_template()`
- ✅ `test_render_file_with_variables()`
- ✅ `test_render_multiple_variables()`
- ✅ `test_get_files()`
- ✅ `test_get_files_excludes_template_json()`

**test_config.py** ✅
- ✅ `test_default_config()`
- ✅ `test_save_config()`
- ✅ `test_load_config()`
- ✅ `test_load_nonexistent_config()`
- ✅ `test_load_invalid_json()`
- ✅ `test_template_config_with_hooks()`

**test_hooks.py** ✅
- ✅ `test_hook_creation()`
- ✅ `test_execute_simple_command()`
- ✅ `test_hook_variable_interpolation()`
- ✅ `test_hook_command_interpolation()`
- ✅ `test_register_hook()`
- ✅ `test_load_hooks_from_config()`
- ✅ `test_execute_stage_with_hooks()`

**test_validators.py** ✅
- ✅ Parametrized tests für Project-Namen
- ✅ Path validation tests

#### **Integration Tests**

**test_e2e_generation.py** ✅
- ✅ `test_generate_project_from_template()`
- ✅ `test_dry_run_generation()`
- ✅ `test_generation_with_hooks()`
- ✅ `test_render_variables_in_files()`

---

## 🛠️ Development Workflow

### 1. Setup
```bash
cd lokal-project-generator
make dev  # Install dev dependencies
```

### 2. Write Tests First (TDD)
```python
# src/tests/unit/test_my_feature.py
def test_my_feature():
    # Arrange
    # Act
    # Assert
    pass
```

### 3. Implement Feature
```python
# src/lokal/core/my_module.py
class MyFeature:
    pass
```

### 4. Run Tests
```bash
make test              # All tests
make test-cov         # With coverage
make test-unit        # Unit only
```

### 5. Check Quality
```bash
make lint             # Code style
make format           # Auto-format
make type             # Type checking
```

---

## 📋 Checklist für Phase 1

### Core Modules
- [x] exceptions.py
- [x] config.py (GlobalConfig + TemplateConfig)
- [x] template.py (Template class)
- [x] hooks.py (Hook + HookManager)
- [x] generator.py (Generator class)

### CLI
- [x] main.py (Click group + context)
- [x] generate.py (generate command)
- [x] list_cmd.py (list command)
- [x] preview.py (preview command)
- [x] config_cmd.py (config command)
- [x] validators.py (input validation)
- [x] formatters.py (output formatting)

### Testing
- [x] conftest.py (fixtures)
- [x] test_template.py (8+ tests)
- [x] test_config.py (10+ tests)
- [x] test_hooks.py (7+ tests)
- [x] test_validators.py (parametrized tests)
- [x] test_e2e_generation.py (integration tests)

### Infrastructure
- [x] pyproject.toml (Poetry config)
- [x] Makefile (dev commands)
- [x] .gitignore
- [x] README.md (user guide)
- [x] This document

---

## 🚀 Beispiel Template erstellen

### 1. Template-Verzeichnis
```bash
mkdir -p templates/python-project/src
cd templates/python-project
```

### 2. template.json
```json
{
  "name": "python-project",
  "description": "Python project with setuptools",
  "version": "1.0.0",
  "author": "Your Name",
  "dependencies": {
    "python": ">=3.8"
  },
  "hooks": {
    "post_generate": [
      "git init",
      "git add ."
    ]
  }
}
```

### 3. Beispiel-Dateien
```bash
# README.md
echo '# {{project_name}}' > README.md

# src/main.py
echo 'print("Hello {{project_name}}!")' > src/main.py

# requirements.txt
echo 'click>=8.0' > requirements.txt
```

### 4. Template testen
```bash
lokal preview ./templates/python-project
lokal generate ./templates/python-project my-awesome-app
```

---

## 📊 Code Coverage Target

- **Unit Tests:** >90%
- **Integration Tests:** >80%
- **Overall:** >85%

```bash
make test-cov  # Generates htmlcov/index.html
```

---

## 🔄 Git Workflow

```bash
# Feature branch
git checkout -b feature/my-feature develop

# Commit
git add .
git commit -m 'feat: Add my feature'

# Push
git push origin feature/my-feature

# Pull Request
# Create PR from feature/my-feature → develop

# After merge
git checkout develop
git pull origin develop
```

---

## 📚 Phase 2 Preview

### Remote Templates
```bash
lokal generate github.com/user/template-repo my-app
```

### GUI (Tkinter)
```bash
lokal gui  # Opens graphical interface
```

### Specialized Stacks
- FastAPI microservice
- React frontend
- ESP32 IoT project
- Docker containerization

---

**Status: Phase 1 ✅ COMPLETE**

Ready for Phase 2! 🚀
