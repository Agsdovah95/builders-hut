# Builders Hut - Development Roadmap

> **Version:** 0.4.3 → 1.0.0
> **Last Updated:** February 2026
> **Goal:** Transform Builders Hut into a production-grade, feature-rich FastAPI scaffolding tool
> **Python Support:** 3.11+ (for wider community adoption)

---

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Python Version | 3.11+ | Wider adoption, more users can benefit |
| Authentication | JWT + OAuth2 | Complete auth solution for any use case |
| Task Queue | Celery | Mature, battle-tested, large community |
| Logging | Loguru | Simple API, beautiful output, zero config |

---

## Table of Contents

- [Vision](#vision)
- [Current State Analysis](#current-state-analysis)
- [Phase 0: Critical Fixes](#phase-0-critical-fixes-immediate)
- [Phase 1: Foundation & Quality](#phase-1-foundation--quality)
- [Phase 2: Feature Expansion](#phase-2-feature-expansion)
- [Phase 3: Ecosystem & Community](#phase-3-ecosystem--community)
- [Future Considerations](#future-considerations)
- [Success Metrics](#success-metrics)
- [Release Schedule](#release-schedule)

---

## Vision

**Builders Hut** aims to be the go-to CLI tool for scaffolding production-ready FastAPI applications. Like `create-react-app` for React or `rails new` for Ruby on Rails, Builders Hut should enable developers to go from zero to a fully configured, best-practices FastAPI project in under a minute.

### Core Principles

1. **Convention over Configuration** - Sensible defaults that work out of the box
2. **Production-Ready** - Generated code should be deployable immediately
3. **Extensible** - Easy to add new templates, databases, and features
4. **Developer Experience** - Beautiful CLI, clear documentation, helpful errors

---

## Current State Analysis

### What We Have (v0.4.3)

| Feature | Status | Notes |
|---------|--------|-------|
| CLI with Typer/Rich | ✅ Complete | Beautiful terminal UI |
| 6-Phase Setup System | ✅ Complete | Extensible architecture |
| SQL Database Support | ✅ Complete | PostgreSQL, MySQL, SQLite |
| NoSQL Database Support | ❌ Not Started | MongoDB placeholder only |
| Alembic Migrations | ✅ Complete | Auto-configured for SQL |
| Layered Architecture | ✅ Complete | API→Service→Repository→Model |
| Error Handling | ✅ Complete | Comprehensive exception system |
| Test Suite | ✅ Complete | ~99 tests across unit, integration, CLI |
| Documentation | ✅ Complete | README, CONTRIBUTING, CHANGELOG, CLAUDE.md |
| `hut add` Command | ❌ Not Started | Declared but not implemented |
| Authentication | ❌ Missing | No auth templates |
| Docker Support | ❌ Missing | No containerization |
| CI/CD Templates | ❌ Missing | No GitHub Actions |

### Known Issues

1. ~~**CRITICAL:** Hardcoded database credentials in `env_file.py`~~ ✅ Fixed
2. ~~**BUG:** `rich` package missing from `pyproject.toml` dependencies~~ ✅ Fixed
3. ~~**TYPO:** `file_writter.py` should be `file_writer.py`~~ ✅ Fixed
4. ~~**TYPO:** `execptions.py` should be `exceptions.py` in generated code~~ ✅ Fixed
5. **INCOMPLETE:** NoSQL/MongoDB setup not implemented
6. **INCOMPLETE:** `add` command not implemented

---

## Phase 0: Critical Fixes (Immediate) ✅

> **Timeline:** 1-2 days
> **Version:** 0.4.4
> **Priority:** CRITICAL - Do not proceed without completing these
> **Status:** ✅ COMPLETE

### 0.1 Security Fix

- [x] Remove hardcoded credentials from `builders_hut/setups/file_contents/env_file.py`
- [x] Replace with placeholder values: `DB_USER="your_username"`, `DB_PASS="your_password"`
- [x] Add warning comment: `# IMPORTANT: Change these values before deployment`

### 0.2 Dependency Fix

- [x] Add `rich` to dependencies in `pyproject.toml`
- [x] Verify all imports have corresponding dependencies
- [x] Run `pip install -e .` on fresh environment to validate

### 0.3 Typo Fixes

- [x] Rename `file_writter.py` → `file_writer.py`
- [x] Update all imports referencing the old filename
- [x] Fix `execptions.py` → `exceptions.py` in generated code templates
- [x] Search codebase for any other typos

### 0.4 Code Cleanup

- [x] Remove duplicate export in `file_contents/__init__.py`
- [x] Ensure all `__init__.py` files have proper exports

**Deliverables:**
- Clean, secure codebase
- All dependencies properly declared
- No typos in filenames or generated code

**Status: ✅ COMPLETE**

---

## Phase 1: Foundation & Quality

> **Timeline:** 2-3 weeks
> **Version:** 0.5.0 → 0.7.0
> **Goal:** Establish quality standards and complete core functionality
> **Status:** 🔶 IN PROGRESS — Tests & docs largely done, NoSQL & `hut add` remaining

### 1.1 Test Suite Implementation ✅

**Priority:** HIGH
**Version:** 0.5.0
**Status:** ~99 tests across 11 test files (unit, integration, CLI)

#### Unit Tests

- [x] Test `BaseSetup` abstract class behavior (7 tests)
- [x] Test `SetupStructure` - directory creation (14 tests)
- [x] Test `SetupFiles` - file creation with correct paths (13 tests, 34 files verified)
- [x] Test `SetupGithub` - git initialization (5 tests)
- [x] Test `SetupEnv` - virtual environment and pyproject.toml (20+ tests)
- [x] Test `SetupFileWriter` - template content writing (10 tests)
- [x] Test `SetupDatabase` - database configuration (5 tests)
- [x] Test `DatabaseFactory` - correct handler selection (14 tests)
- [x] Test `utils.py` functions: (21 tests)
  - `get_platform()`
  - `get_python_file()`
  - `run_subprocess()`
  - `write_pyproject_toml()`
  - `create_folders()`
  - `create_files()`

#### Integration Tests

- [x] Test full `hut build` workflow with defaults
- [x] Test `hut build` with each database provider (postgres, mysql, sqlite)
- [x] Test `hut build --accept-defaults` flag
- [x] Test `hut build --path` option
- [x] Test generated project structure matches expected (layered architecture validated)
- [ ] Test generated project runs successfully (`uvicorn`)

#### CLI Tests

- [x] Test `--version` flag (3 tests)
- [x] Test `--help` output (4 tests)
- [x] Test invalid input handling (2 tests)
- [ ] Test keyboard interrupt handling

**Testing Stack:**
```
pytest
pytest-cov (coverage reporting)
pytest-mock (mocking)
pytest-asyncio (async tests)
```

**Target Coverage:** 80%+

---

### 1.2 Documentation 🔶

**Priority:** HIGH
**Version:** 0.5.0
**Status:** Core docs exist (README, CONTRIBUTING, CHANGELOG). Extended docs/ folder not started.

#### README.md Overhaul

- [x] Project description and badges (PyPI, Python versions, license)
- [x] Installation instructions (pip)
- [x] Quick start guide with CLI examples
- [x] Feature list with descriptions
- [x] Generated project structure visualization
- [x] Configuration options table
- [ ] Database provider comparison
- [ ] Troubleshooting section
- [x] Contributing link
- [ ] Terminal GIF/screenshot demo
- [ ] Test/coverage badges

#### Additional Documentation

- [x] `CONTRIBUTING.md` - How to contribute
  - Development setup
  - Code style guide
  - Pull request process
  - [ ] Issue templates (`.github/ISSUE_TEMPLATE/`)
- [x] `CHANGELOG.md` - Version history (basic, needs semver format)
- [ ] `docs/` folder for extended documentation:
  - `docs/architecture.md` - How Builders Hut works
  - `docs/templates.md` - Template system explanation
  - `docs/extending.md` - How to add new features
  - `docs/generated-project.md` - Understanding generated code

---

### 1.3 Complete NoSQL Support ❌

**Priority:** MEDIUM
**Version:** 0.6.0
**Status:** Not started — `factory.py` has `case "nosql": pass`

#### MongoDB Implementation

- [ ] Create `builders_hut/setups/database/nosql_handler.py`
- [ ] Implement MongoDB connection template
- [ ] Create async MongoDB session management
- [ ] Update `DatabaseFactory` to handle NoSQL
- [ ] Create MongoDB-specific model templates
- [ ] Create MongoDB repository pattern templates
- [ ] Update `FILES_TO_WRITE` with NoSQL variants
- [ ] Add `motor` (async MongoDB driver) to generated dependencies

#### NoSQL Templates

```python
# New files needed:
builders_hut/setups/file_contents/
├── app_database_nosql.py      # MongoDB connection
├── app_model_nosql.py         # MongoDB document models
├── app_repository_nosql.py    # MongoDB repository pattern
```

#### Configuration

- [ ] Add MongoDB connection string to env template
- [ ] Handle MongoDB Atlas vs local MongoDB
- [ ] Add database name configuration

---

### 1.4 Implement `hut add` Command ❌

**Priority:** MEDIUM
**Version:** 0.7.0
**Status:** Not started — command declared but shows "not implemented yet" placeholder

The `add` command scaffolds individual components into existing projects.

#### Subcommands

```bash
# Add a new model
hut add model <name>
# Example: hut add model User
# Creates: app/models/user.py with SQLAlchemy model

# Add a new endpoint/router
hut add endpoint <name>
# Example: hut add endpoint users
# Creates: app/api/v1/users.py with CRUD endpoints

# Add a new service
hut add service <name>
# Example: hut add service UserService
# Creates: app/services/user_service.py

# Add a new repository
hut add repository <name>
# Example: hut add repository UserRepository
# Creates: app/repositories/user_repository.py

# Add a new schema
hut add schema <name>
# Example: hut add schema User
# Creates: app/schemas/user.py with Pydantic models

# Add full CRUD stack (model + repo + service + schema + endpoint)
hut add crud <name>
# Example: hut add crud Product
# Creates all layers for a new entity
```

#### Implementation

- [ ] Create `builders_hut/commands/add.py`
- [ ] Implement component detection (is this a Builders Hut project?)
- [ ] Create templates for each component type
- [ ] Handle singular/plural naming conventions
- [ ] Update imports in `__init__.py` files automatically
- [ ] Add to router registration automatically

---

### 1.5 Error Handling & DX Improvements ❌

**Priority:** LOW
**Version:** 0.7.0
**Status:** Not started

- [ ] Add Python version validation (require 3.11+)
- [ ] Improve subprocess error messages (show stdout/stderr on failure)
- [ ] Add `--verbose` flag for detailed output
- [ ] Add `--dry-run` flag to preview without creating files
- [ ] Colorize error messages (red) and success messages (green)
- [ ] Add recovery suggestions for common errors

---

## Phase 2: Feature Expansion

> **Timeline:** 4-6 weeks
> **Version:** 0.8.0 → 0.12.0
> **Goal:** Add production-essential features that differentiate Builders Hut
> **Status:** ❌ NOT STARTED

### 2.1 Authentication System

**Priority:** HIGH
**Version:** 0.8.0

> **Decision:** Support both JWT and OAuth2 for complete authentication coverage

#### 2.1.1 JWT Authentication (Core)

- [ ] Create `app/core/security.py` template
  - Password hashing with `passlib[bcrypt]`
  - JWT token creation/verification with `python-jose`
  - Access token + Refresh token pattern
  - Token blacklisting for logout
- [ ] Create `app/api/v1/auth.py` template
  - `POST /auth/register` - User registration with email verification
  - `POST /auth/login` - Login, return access + refresh tokens
  - `POST /auth/refresh` - Refresh access token
  - `POST /auth/logout` - Invalidate tokens (blacklist)
  - `GET /auth/me` - Get current user profile
  - `PUT /auth/me` - Update current user profile
  - `POST /auth/password/reset` - Request password reset
  - `POST /auth/password/reset/confirm` - Confirm password reset
- [ ] Create `app/models/user.py` template
  - User model: id, email, password_hash, is_active, is_verified, roles
  - Token blacklist model for logout
- [ ] Create `app/schemas/auth.py` template
  - `LoginRequest`, `RegisterRequest`
  - `TokenResponse` (access_token, refresh_token, token_type, expires_in)
  - `UserCreate`, `UserUpdate`, `UserResponse`
  - `PasswordResetRequest`, `PasswordResetConfirm`
- [ ] Create `app/dependencies/auth.py` template
  - `get_current_user` - Extract user from JWT
  - `get_current_active_user` - Ensure user is active
  - `require_roles(*roles)` - Role-based access control
  - `require_verified` - Ensure email is verified
- [ ] Add auth dependencies to generated pyproject.toml:
  - `python-jose[cryptography]`
  - `passlib[bcrypt]`
  - `email-validator`

#### 2.1.2 OAuth2 Providers

- [ ] Create `app/core/oauth.py` template
  - OAuth2 client configuration
  - Token exchange logic
  - User info fetching
- [ ] Create `app/api/v1/oauth.py` template
  - `GET /auth/oauth/{provider}` - Redirect to provider
  - `GET /auth/oauth/{provider}/callback` - Handle callback
- [ ] **Google OAuth2**
  - Google client configuration
  - Scope: email, profile
  - Link/unlink Google account
- [ ] **GitHub OAuth2**
  - GitHub client configuration
  - Scope: user:email
  - Link/unlink GitHub account
- [ ] **Generic OAuth2 Template**
  - Easy to add new providers
  - Documentation for adding custom providers
- [ ] Add OAuth2 dependencies:
  - `authlib`
  - `httpx`

#### CLI Integration

```bash
# Full auth system (JWT + OAuth2)
hut build --with-auth

# JWT only
hut build --with-auth jwt

# Specific OAuth providers
hut build --with-auth oauth --oauth-providers google,github

# Add to existing project
hut add auth
hut add oauth google
hut add oauth github
```

#### Generated Files Structure

```
app/
├── core/
│   ├── security.py      # JWT + password hashing
│   └── oauth.py         # OAuth2 client logic
├── api/v1/
│   ├── auth.py          # JWT endpoints
│   └── oauth.py         # OAuth2 endpoints
├── models/
│   └── user.py          # User + OAuth account models
├── schemas/
│   └── auth.py          # Auth-related schemas
└── dependencies/
    └── auth.py          # Auth dependencies
```

---

### 2.2 Docker Support

**Priority:** HIGH
**Version:** 0.9.0

#### Generated Files

- [ ] `Dockerfile` - Multi-stage build for production
  ```dockerfile
  # Build stage
  FROM python:3.11-slim as builder
  ...

  # Production stage
  FROM python:3.11-slim
  ...
  ```
- [ ] `docker-compose.yml` - Full stack setup
  ```yaml
  services:
    api:
      build: .
      ports:
        - "8000:8000"
    db:
      image: postgres:16
      ...
    redis:
      image: redis:7
      ...
  ```
- [ ] `docker-compose.dev.yml` - Development overrides
- [ ] `.dockerignore` - Exclude unnecessary files

#### CLI Integration

```bash
hut build --with-docker      # Include Docker files
hut add docker               # Add Docker to existing project
```

---

### 2.3 CI/CD Templates

**Priority:** HIGH
**Version:** 0.9.0

#### GitHub Actions

- [ ] `.github/workflows/test.yml`
  - Run tests on push/PR
  - Multiple Python versions
  - Coverage reporting
- [ ] `.github/workflows/lint.yml`
  - Ruff linting
  - Type checking with mypy
- [ ] `.github/workflows/deploy.yml`
  - Deploy to various platforms
  - Environment-specific configs

#### Templates for Different Platforms

- [ ] Railway deployment
- [ ] Render deployment
- [ ] AWS ECS deployment
- [ ] Google Cloud Run deployment
- [ ] DigitalOcean App Platform

#### CLI Integration

```bash
hut build --with-ci          # Include CI/CD workflows
hut add ci github            # Add GitHub Actions
hut add ci gitlab            # Add GitLab CI
```

---

### 2.4 Code Quality Tools

**Priority:** MEDIUM
**Version:** 0.10.0

#### Pre-commit Configuration

- [ ] `.pre-commit-config.yaml`
  ```yaml
  repos:
    - repo: https://github.com/astral-sh/ruff-pre-commit
      hooks:
        - id: ruff
        - id: ruff-format
    - repo: https://github.com/pre-commit/mirrors-mypy
      hooks:
        - id: mypy
  ```

#### Linting & Formatting

- [ ] `ruff.toml` - Ruff configuration
- [ ] `mypy.ini` - Type checking configuration
- [ ] Update pyproject.toml with tool configs

#### CLI Integration

```bash
hut build --with-lint        # Include linting setup
hut add lint                 # Add linting to existing project
```

---

### 2.5 Logging System

**Priority:** MEDIUM
**Version:** 0.10.0

> **Decision:** Use Loguru for simple API, beautiful output, and zero-config experience

#### Loguru Integration

- [ ] Create `app/core/logging.py` template
  - Loguru configuration
  - JSON serialization for production (`serialize=True`)
  - Pretty colored output for development
  - Request ID tracking via contextvars
  - Correlation ID propagation
- [ ] Create `app/middleware/logging.py` template
  - Request/response logging middleware
  - Automatic request ID generation
  - Request duration tracking
  - Error logging with stack traces
- [ ] Log configuration features:
  - Environment-based log levels (DEBUG in dev, INFO in prod)
  - Log rotation (time-based and size-based)
  - Log retention policies
  - Async file writing for performance
  - Custom log formats
- [ ] Integration with other components:
  - Database query logging
  - HTTP client request logging
  - Background task logging
  - Error tracking integration (Sentry-compatible)
- [ ] Add `loguru` to generated dependencies

#### Example Configuration

```python
# app/core/logging.py
from loguru import logger
import sys

def setup_logging(environment: str):
    logger.remove()  # Remove default handler

    if environment == "production":
        logger.add(
            "logs/app.log",
            rotation="500 MB",
            retention="10 days",
            serialize=True,  # JSON format
            level="INFO"
        )
    else:
        logger.add(
            sys.stderr,
            colorize=True,
            format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="DEBUG"
        )
```

#### CLI Integration

```bash
hut build --with-logging     # Include Loguru logging setup
hut add logging              # Add logging to existing project
```

---

### 2.6 Caching Layer

**Priority:** MEDIUM
**Version:** 0.11.0

#### Redis Integration

- [ ] Create `app/core/cache.py` template
  - Redis connection management
  - Cache decorators
  - Cache invalidation patterns
- [ ] Create `app/dependencies/cache.py`
  - Cache dependency injection
- [ ] Add `redis` and `redis-om` to dependencies

#### CLI Integration

```bash
hut build --with-cache       # Include Redis caching
hut add cache                # Add caching to existing project
```

---

### 2.7 Background Tasks

**Priority:** MEDIUM
**Version:** 0.11.0

> **Decision:** Use Celery for mature, battle-tested task queue with large community support

#### Celery Integration

- [ ] Create `app/workers/celery_app.py` template
  - Celery app configuration
  - Broker connection (Redis)
  - Result backend configuration
  - Task serialization settings
  - Error handling and retries
- [ ] Create `app/workers/tasks/` directory structure
  - `__init__.py` - Task registration
  - `email.py` - Email sending tasks
  - `notifications.py` - Notification tasks
  - `cleanup.py` - Maintenance tasks
- [ ] Create `app/workers/beat.py` template
  - Celery Beat scheduler
  - Periodic task definitions
  - Crontab scheduling
- [ ] Create example tasks:
  - `send_email_task` - Async email sending
  - `process_upload_task` - File processing
  - `generate_report_task` - Report generation
  - `cleanup_expired_tokens_task` - Periodic cleanup
- [ ] Worker configuration:
  - Concurrency settings
  - Task routing
  - Priority queues
  - Task time limits
  - Dead letter queues
- [ ] Monitoring integration:
  - Flower dashboard setup
  - Task status tracking
  - Worker health checks
- [ ] Add Celery dependencies to generated pyproject.toml:
  - `celery[redis]`
  - `flower` (optional monitoring)

#### Generated Files Structure

```
app/
└── workers/
    ├── __init__.py
    ├── celery_app.py      # Celery configuration
    ├── beat.py            # Scheduler configuration
    └── tasks/
        ├── __init__.py
        ├── email.py       # Email tasks
        ├── notifications.py
        └── cleanup.py     # Maintenance tasks
```

#### Docker Compose Addition

```yaml
services:
  worker:
    build: .
    command: celery -A app.workers.celery_app worker --loglevel=info
    depends_on:
      - redis
      - db

  beat:
    build: .
    command: celery -A app.workers.celery_app beat --loglevel=info
    depends_on:
      - redis

  flower:
    image: mher/flower
    ports:
      - "5555:5555"
    depends_on:
      - worker
```

#### CLI Integration

```bash
hut build --with-workers         # Include Celery setup
hut add worker <name>            # Add new worker task
hut add worker email             # Add email worker
hut add worker scheduled <name>  # Add scheduled/periodic task
```

---

### 2.8 API Features

**Priority:** LOW
**Version:** 0.12.0

#### Rate Limiting

- [ ] Integrate `slowapi`
- [ ] Configure rate limits per endpoint
- [ ] Redis-backed rate limiting for distributed systems

#### API Versioning

- [ ] URL path versioning (`/api/v1/`, `/api/v2/`)
- [ ] Header versioning option
- [ ] Version deprecation handling

#### Pagination

- [ ] Cursor-based pagination template
- [ ] Offset-based pagination template
- [ ] Standard pagination response schema

#### CLI Integration

```bash
hut build --with-ratelimit
hut add api-version v2
```

---

## Phase 3: Ecosystem & Community

> **Timeline:** Ongoing
> **Version:** 1.0.0+
> **Goal:** Build community and expand ecosystem
> **Status:** ❌ NOT STARTED

### 3.1 Plugin System

**Priority:** LOW
**Version:** 1.1.0

- [ ] Design plugin architecture
- [ ] Create plugin discovery mechanism
- [ ] Plugin template/cookiecutter
- [ ] Plugin registry/marketplace

```bash
hut plugin install hut-graphql
hut plugin list
hut plugin create my-plugin
```

---

### 3.2 Template Marketplace

**Priority:** LOW
**Version:** 1.2.0

- [ ] Community template repository
- [ ] Template versioning
- [ ] Template validation
- [ ] Search and discovery

```bash
hut template list
hut template install ecommerce-api
hut template publish my-template
```

---

### 3.3 GUI/TUI Enhancements

**Priority:** LOW
**Version:** 1.3.0

- [ ] Full TUI with `textual`
- [ ] Project configuration preview
- [ ] Interactive file tree
- [ ] Real-time validation

---

### 3.4 IDE Integrations

**Priority:** LOW
**Version:** 1.4.0

- [ ] VSCode extension
- [ ] PyCharm plugin
- [ ] Neovim plugin

---

## Future Considerations

These are ideas for post-1.0 development based on community feedback:

### Database Additions
- [ ] Redis (as primary store)
- [ ] Cassandra
- [ ] DynamoDB
- [ ] CockroachDB

### Framework Variations
- [ ] Litestar (FastAPI alternative)
- [ ] Starlette (minimal)
- [ ] Django REST Framework

### Advanced Features
- [ ] GraphQL support (Strawberry)
- [ ] gRPC support
- [ ] WebSocket templates
- [ ] Server-Sent Events
- [ ] Multi-tenancy patterns
- [ ] Microservices templates
- [ ] Event sourcing patterns
- [ ] CQRS patterns

### Deployment
- [ ] Kubernetes manifests
- [ ] Terraform templates
- [ ] Pulumi templates
- [ ] Serverless (AWS Lambda, Google Functions)

### Monitoring & Observability
- [ ] Prometheus metrics
- [ ] OpenTelemetry tracing
- [ ] Sentry error tracking
- [ ] Health check dashboard

---

## Success Metrics

### Quality Metrics
| Metric | Target |
|--------|--------|
| Test Coverage | > 80% |
| Documentation Coverage | 100% of public APIs |
| Issue Response Time | < 48 hours |
| PR Review Time | < 1 week |

### Community Metrics
| Metric | Target (6 months) | Target (1 year) |
|--------|-------------------|-----------------|
| GitHub Stars | 100 | 500 |
| PyPI Downloads/month | 500 | 2,000 |
| Contributors | 5 | 15 |
| Open Issues | < 20 | < 30 |

### Feature Metrics
| Metric | Target |
|--------|--------|
| Generated Project Boot Time | < 2 seconds |
| `hut build` Completion Time | < 30 seconds |
| Supported Databases | 5+ |
| CLI Commands | 10+ |

---

## Release Schedule

| Version | Milestone | Target Date |
|---------|-----------|-------------|
| 0.4.4 | Phase 0: Critical Fixes | Week 1 |
| 0.5.0 | Tests + Documentation | Week 3 |
| 0.6.0 | NoSQL Support | Week 4 |
| 0.7.0 | `hut add` Command | Week 5 |
| 0.8.0 | Authentication System | Week 7 |
| 0.9.0 | Docker + CI/CD | Week 9 |
| 0.10.0 | Code Quality + Logging | Week 11 |
| 0.11.0 | Caching + Workers | Week 13 |
| 0.12.0 | API Features | Week 15 |
| **1.0.0** | **Stable Release** | **Week 16** |

---

## How to Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Add tests for new functionality
5. Run tests: `pytest`
6. Submit a pull request

### Priority Areas for Contribution

1. **Tests** - We need test coverage! Any tests are welcome.
2. **Documentation** - Help improve docs and add examples.
3. **NoSQL Support** - MongoDB implementation needed.
4. **Templates** - New file templates and improvements.

---

*This roadmap is a living document and will be updated as the project evolves.*

*Built with love for the Python community.*
