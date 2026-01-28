# =============================================================================
# Shared Test Fixtures (conftest.py)
# =============================================================================
#
# LEARNING NOTE: What is conftest.py?
# -----------------------------------
# conftest.py is a special pytest file that contains "fixtures" - reusable
# pieces of test setup code. Fixtures defined here are automatically available
# to ALL test files in this directory and subdirectories.
#
# Benefits of fixtures:
# 1. DRY (Don't Repeat Yourself) - Define setup once, use everywhere
# 2. Automatic cleanup - Fixtures can clean up after themselves
# 3. Dependency injection - Pytest automatically passes fixtures to tests
# 4. Scope control - Run once per test, per module, or per session
#
# =============================================================================

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest


# =============================================================================
# FIXTURE: Temporary Project Directory
# =============================================================================
#
# LEARNING NOTE: The @pytest.fixture decorator
# --------------------------------------------
# This decorator marks a function as a fixture. When a test function has a
# parameter with the same name as a fixture, pytest automatically calls
# the fixture and passes its return value to the test.
#
# The 'yield' keyword is special here:
# - Code BEFORE yield runs BEFORE the test (setup)
# - Code AFTER yield runs AFTER the test (teardown/cleanup)
#


@pytest.fixture
def temp_project_dir():
    """
    Creates a temporary directory for testing.

    This fixture:
    1. Creates a new temporary directory before each test
    2. Yields the Path to that directory for the test to use
    3. Automatically cleans up (deletes) the directory after the test

    Usage in a test:
        def test_something(temp_project_dir):
            # temp_project_dir is a Path object to an empty temp directory
            my_file = temp_project_dir / "test.txt"
            my_file.write_text("hello")
    """
    # Create a temporary directory
    # tempfile.mkdtemp() creates a unique directory that won't conflict with other tests
    temp_dir = Path(tempfile.mkdtemp(prefix="builders_hut_test_"))

    # 'yield' returns the value to the test AND pauses here until test completes
    yield temp_dir

    # CLEANUP: This code runs AFTER the test finishes (success or failure)
    # We delete all files and the directory itself
    import shutil
    if temp_dir.exists():
        shutil.rmtree(temp_dir)


# =============================================================================
# FIXTURE: Sample Configuration
# =============================================================================
#
# LEARNING NOTE: Fixtures can return any Python object
# ---------------------------------------------------
# This fixture returns a dictionary with sample configuration values.
# Tests that need a standard config can use this instead of creating their own.
#


@pytest.fixture
def sample_config():
    """
    Returns a standard configuration dictionary for testing.

    This matches the configuration structure used by setup classes.
    """
    return {
        "name": "test_project",
        "description": "A test project",
        "version": "0.1.0",
        "database_type": "sql",
        "database_provider": "postgres",
    }


# =============================================================================
# FIXTURE: Mock Subprocess
# =============================================================================
#
# LEARNING NOTE: What is Mocking?
# -------------------------------
# Mocking replaces real objects/functions with fake ones during tests.
# This is useful when:
# 1. The real function is slow (e.g., pip install)
# 2. The real function has side effects (e.g., git init creates files)
# 3. The real function requires external tools (e.g., git must be installed)
# 4. You want to test error handling (simulate failures)
#
# We use pytest-mock's 'mocker' fixture which provides a clean API for mocking.
#


@pytest.fixture
def mock_subprocess(mocker):
    """
    Mocks subprocess.run to prevent actual command execution.

    This fixture:
    1. Replaces subprocess.run with a mock that does nothing
    2. Returns the mock so tests can verify it was called correctly

    Usage in a test:
        def test_git_init(mock_subprocess, temp_project_dir):
            # Run code that calls subprocess.run
            setup = SetupGithub(temp_project_dir)
            setup.create()

            # Verify subprocess.run was called with expected arguments
            mock_subprocess.assert_called_once()
    """
    # mocker.patch replaces the target with a MagicMock
    # MagicMock is a flexible fake object that records how it was called
    mock = mocker.patch("subprocess.run")

    # Configure the mock to return a successful result by default
    mock.return_value = MagicMock(returncode=0)

    return mock


# =============================================================================
# FIXTURE: Mock for utils.run_subprocess
# =============================================================================


@pytest.fixture
def mock_run_subprocess(mocker):
    """
    Mocks the run_subprocess utility function.

    This is more specific than mock_subprocess - it mocks our wrapper function
    instead of the underlying subprocess.run.
    """
    return mocker.patch("builders_hut.utils.run_subprocess")


# =============================================================================
# FIXTURE: Expected Directory Structure
# =============================================================================


@pytest.fixture
def expected_app_directories():
    """
    Returns the list of directories that SetupStructure should create.

    This is useful for verifying the correct structure is created.
    """
    return [
        "app",
        "app/api",
        "app/api/v1",
        "app/database",
        "app/schemas",
        "app/services",
        "app/repositories",
        "app/core",
        "app/models",
        "app/workers",
        "app/utils",
        "app/templates",
        "tests",
    ]


# =============================================================================
# FIXTURE: Database Provider Configurations
# =============================================================================
#
# LEARNING NOTE: Fixtures can depend on other fixtures
# ---------------------------------------------------
# Notice how sql_providers returns a list that can be used with
# @pytest.mark.parametrize for testing multiple database configurations.
#


@pytest.fixture
def sql_providers():
    """
    Returns a list of SQL database provider configurations for parametrized tests.
    """
    return [
        {"database_provider": "postgres", "expected_deps": ["asyncpg", "psycopg2-binary"]},
        {"database_provider": "mysql", "expected_deps": ["aiomysql", "pymysql"]},
        {"database_provider": "sqlite", "expected_deps": ["aiosqlite"]},
    ]


# =============================================================================
# HELPER: Create a minimal project structure
# =============================================================================
#
# LEARNING NOTE: Not all helpers need to be fixtures
# --------------------------------------------------
# This is a regular function, not a fixture. Tests can import and call it
# directly. Use functions for utilities that don't need setup/teardown.
#


def create_minimal_project(path: Path) -> None:
    """
    Creates a minimal project structure for testing.

    Useful when you need a basic project to exist before testing
    a specific component.
    """
    # Create basic directory structure
    (path / "app").mkdir(parents=True, exist_ok=True)
    (path / "app" / "database").mkdir(parents=True, exist_ok=True)
    (path / "tests").mkdir(parents=True, exist_ok=True)

    # Create essential files
    (path / "pyproject.toml").touch()
    (path / ".env").touch()
    (path / "app" / "__init__.py").touch()


# =============================================================================
# End of conftest.py
# =============================================================================
