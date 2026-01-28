# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Builders Hut is a Python CLI tool that scaffolds production-ready FastAPI projects. It uses Typer for the command-line interface and Rich for beautiful terminal UI.

## Development Commands

### Setup Development Environment
```bash
# Install in editable mode
pip install -e .

# The tool becomes available as 'hut' command
hut --version
```

### Building and Publishing
```bash
# Build the package (outputs to dist/)
python -m build

# Publish to PyPI
twine upload dist/*
```

### Running the Tool
```bash
# Interactive mode (default)
hut build

# With default values
hut build --accept-defaults -y

# Specify path
hut build --path ./my-project

# Alternative invocations
python -m hut build
python -m builders_hut build
```

## Architecture

### Setup Phase System

The project scaffolding follows a **6-phase setup pattern**, executed sequentially:

1. **SetupStructure** - Creates directory structure (app/, tests/, and subdirectories)
2. **SetupFiles** - Creates empty `__init__.py` files for Python modules
3. **SetupGithub** - Initializes git repository
4. **SetupEnv** - Creates virtual environment, writes pyproject.toml, installs dependencies
5. **SetupFileWriter** - Writes template content to all files using `FILES_TO_WRITE` mapping
6. **SetupDatabase** - Configures database (SQL: Alembic setup; NoSQL: pending)

Each phase is a class inheriting from `BaseSetup` ([setups/base_setup.py](builders_hut/setups/base_setup.py)).

### BaseSetup Pattern

All setup classes follow this pattern:
```python
class SomeSetup(BaseSetup):
    def __init__(self, location: Path):
        # location is the target project directory

    def configure(self, **kwargs):
        # Store configuration from user input (optional hook)

    def create(self):
        # Execute the setup (required)
```

Setup execution happens in [utils.py:setup_project()](builders_hut/utils.py) via:
```python
setup = setup_cls(location)
setup.configure(**config)
setup.create()
```

### Template System

All template file contents live in [builders_hut/setups/file_contents/](builders_hut/setups/file_contents/):
- [app_main.py](builders_hut/setups/file_contents/app_main.py) - FastAPI main application
- [app_core.py](builders_hut/setups/file_contents/app_core.py) - Config, errors, exceptions, lifespan
- [app_api.py](builders_hut/setups/file_contents/app_api.py) - Common routes (health, docs, home)
- [app_api_v1.py](builders_hut/setups/file_contents/app_api_v1.py) - Versioned API endpoints
- [app_database.py](builders_hut/setups/file_contents/app_database.py) - Database session/connection
- [app_model.py](builders_hut/setups/file_contents/app_model.py) - Example ORM models
- [app_repository.py](builders_hut/setups/file_contents/app_repository.py) - Data access layer
- [app_services.py](builders_hut/setups/file_contents/app_services.py) - Business logic layer
- [app_schema.py](builders_hut/setups/file_contents/app_schema.py) - Pydantic schemas
- [app_templates.py](builders_hut/setups/file_contents/app_templates.py) - Jinja2 HTML templates
- [env_file.py](builders_hut/setups/file_contents/env_file.py) - Environment variables
- [run_file.py](builders_hut/setups/file_contents/run_file.py) - Server run script

The [all_writes.py](builders_hut/setups/all_writes.py) file contains `FILES_TO_WRITE`, a dict mapping Path → content string.

### Database Factory Pattern

Database setup uses a factory pattern in [setups/database/factory.py](builders_hut/setups/database/factory.py):
- **SQL databases**: Creates session.py, initializes Alembic for migrations, writes migrations/env.py
- **NoSQL databases**: Not yet implemented

## Key Files and Their Roles

- [cmd_interface.py](builders_hut/cmd_interface.py) - Typer CLI commands, wizard UI, progress display
- [__main__.py](builders_hut/__main__.py) - Entry point for `python -m builders_hut`
- [utils.py](builders_hut/utils.py) - Shared utilities: pyproject.toml writer, folder/file creation, subprocess runner
- [setups/__init__.py](builders_hut/setups/__init__.py) - Exports all setup classes
- [hut/](hut/) - Alias package enabling `python -m hut` as alternative to `python -m builders_hut`

## Generated Project Structure

Generated projects follow a **layered architecture**:
```
API Routes (app/api/)
  ↓
Services (app/services/) - Business logic
  ↓
Repositories (app/repositories/) - Data access abstraction
  ↓
Models (app/models/) + Database (app/database/) - ORM and persistence
```

Supporting layers:
- **Core** (app/core/) - Configuration, errors, exceptions, lifespan, responses
- **Schemas** (app/schemas/) - Pydantic request/response models
- **Workers** (app/workers/) - Background tasks (template only)
- **Utils** (app/utils/) - Helper functions (template only)
- **Templates** (app/templates/) - Jinja2 HTML templates

## Platform Handling

Cross-platform support in [utils.py:get_platform()](builders_hut/utils.py):
- Detects Windows vs Linux
- Adjusts virtual environment paths (`.venv\Scripts\python.exe` vs `.venv/bin/python`)
- Used by `get_python_file()` for running commands in the created venv

## Configuration Flow

User inputs collected via wizard ([cmd_interface.py:run_wizard()](builders_hut/cmd_interface.py)):
1. `name` - Project name
2. `description` - Project description
3. `version` - Initial version
4. `database_type` - "sql" or "nosql"
5. `database_provider` - "postgres", "mysql", "sqlite", or "mongodb"

These values are passed as `**kwargs` to each setup class's `configure()` method.

## UI Pattern

The CLI uses Rich for beautiful terminal output:
- **Panels** for questions and status messages
- **Progress bars** with spinners for setup phases
- **Live displays** for real-time progress updates
- **BANNER** constant for ASCII art logo

All UI logic is in [cmd_interface.py](builders_hut/cmd_interface.py).

## Adding New Features

### To add a new template file:
1. Add content as a constant in `builders_hut/setups/file_contents/`
2. Import it in [all_writes.py](builders_hut/setups/all_writes.py)
3. Add `Path → content` mapping to `FILES_TO_WRITE`

### To add a new setup phase:
1. Create class inheriting from BaseSetup in `builders_hut/setups/`
2. Implement `create()` method (and optionally `configure()`)
3. Export from [setups/__init__.py](builders_hut/setups/__init__.py)
4. Add to `setup_steps` list in [cmd_interface.py:build()](builders_hut/cmd_interface.py)
5. Add description to `STEPS` dict in [cmd_interface.py](builders_hut/cmd_interface.py)

### To add a new CLI command:
1. Add `@app.command()` decorated function in [cmd_interface.py](builders_hut/cmd_interface.py)
2. Follow Typer conventions for arguments and options

## Important Notes

- **No tests currently exist** - The tests/ directory is empty
- **Version must be updated** in both [pyproject.toml](pyproject.toml) and [cmd_interface.py](builders_hut/cmd_interface.py) APP_VERSION constant
- **Python 3.13+ required** - Specified in pyproject.toml
- Generated projects use **Scalar** for API docs (not Swagger UI)
- Generated projects include a **"Hero" example** showing the full stack pattern (model → repository → service → schema → API endpoint)
