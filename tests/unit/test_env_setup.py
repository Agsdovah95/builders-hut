# =============================================================================
# Unit Tests for builders_hut/setups/env_setup.py
# =============================================================================
#
# LEARNING NOTE: Testing Complex Setup Logic
# ------------------------------------------
# SetupEnv has multiple responsibilities:
# 1. Writing requirements files
# 2. Creating virtual environment
# 3. Installing dependencies
#
# We mock external calls (subprocess) and verify:
# - Correct packages are included for each database type
# - Files are written with correct content
# - Error handling works correctly
#
# =============================================================================

from pathlib import Path
import subprocess

import pytest

from builders_hut.setups.env_setup import (
    SetupEnv,
    PACKAGES,
    DEV_PACKAGES,
    DB_SQL_PACKAGES,
    SQL_COMMON_PACKAGE,
)
from builders_hut.setups.structure_setup import SetupStructure
from builders_hut.setups.files_setup import SetupFiles


# =============================================================================
# Tests for SetupEnv
# =============================================================================


class TestSetupEnv:
    """Tests for the SetupEnv class."""

    @pytest.fixture
    def project_with_files(self, temp_project_dir):
        """Creates directory structure and empty files."""
        SetupStructure(temp_project_dir).create()
        SetupFiles(temp_project_dir).create()
        return temp_project_dir

    @pytest.fixture
    def configured_setup(self, project_with_files):
        """Returns a configured SetupEnv instance."""
        setup = SetupEnv(project_with_files)
        setup.configure(
            name="test_project",
            description="Test description",
            version="1.0.0",
            database_type="sql",
            database_provider="postgres",
        )
        return setup

    def test_configure_stores_name(self, temp_project_dir):
        """Verify configure() stores the name attribute."""
        setup = SetupEnv(temp_project_dir)
        setup.configure(
            name="my_project",
            description="desc",
            version="1.0.0",
            database_type="sql",
            database_provider="postgres",
        )

        assert setup.name == "my_project"

    def test_configure_stores_description(self, temp_project_dir):
        """Verify configure() stores the description attribute."""
        setup = SetupEnv(temp_project_dir)
        setup.configure(
            name="test",
            description="A wonderful project",
            version="1.0.0",
            database_type="sql",
            database_provider="postgres",
        )

        assert setup.description == "A wonderful project"

    def test_configure_stores_version(self, temp_project_dir):
        """Verify configure() stores the version attribute."""
        setup = SetupEnv(temp_project_dir)
        setup.configure(
            name="test",
            description="desc",
            version="2.5.0",
            database_type="sql",
            database_provider="postgres",
        )

        assert setup.version == "2.5.0"

    def test_configure_stores_database_type(self, temp_project_dir):
        """Verify configure() stores the database_type attribute."""
        setup = SetupEnv(temp_project_dir)
        setup.configure(
            name="test",
            description="desc",
            version="1.0.0",
            database_type="nosql",
            database_provider="mongodb",
        )

        assert setup.database_type == "nosql"

    def test_configure_stores_database_provider(self, temp_project_dir):
        """Verify configure() stores the database_provider attribute."""
        setup = SetupEnv(temp_project_dir)
        setup.configure(
            name="test",
            description="desc",
            version="1.0.0",
            database_type="sql",
            database_provider="mysql",
        )

        assert setup.database_provider == "mysql"

    def test_writes_requirements_file(self, project_with_files, mocker):
        """
        WHAT: Verify requirements.txt is written with packages.
        WHY: Dependencies must be listed for installation.
        """
        # Mock subprocess to prevent actual venv creation
        mocker.patch("builders_hut.setups.env_setup.run_subprocess")

        setup = SetupEnv(project_with_files)
        setup.configure(
            name="test",
            description="desc",
            version="1.0.0",
            database_type="sql",
            database_provider="postgres",
        )
        setup.create()

        requirements_file = project_with_files / "requirements.txt"
        content = requirements_file.read_text()

        # Check base packages are included
        assert "fastapi" in content
        assert "uvicorn" in content

    def test_includes_postgres_packages_for_postgres(self, project_with_files, mocker):
        """
        WHAT: Verify PostgreSQL packages are included for postgres provider.
        WHY: Database-specific packages must be included.

        LEARNING NOTE: Parametrized Tests
        ----------------------------------
        This test could be parametrized to test multiple databases.
        See test_includes_correct_db_packages_parametrized for an example.
        """
        mocker.patch("builders_hut.setups.env_setup.run_subprocess")

        setup = SetupEnv(project_with_files)
        setup.configure(
            name="test",
            description="desc",
            version="1.0.0",
            database_type="sql",
            database_provider="postgres",
        )
        setup.create()

        requirements = (project_with_files / "requirements.txt").read_text()

        for package in DB_SQL_PACKAGES["postgres"]:
            assert package in requirements, f"{package} not in requirements"

    def test_includes_mysql_packages_for_mysql(self, project_with_files, mocker):
        """Verify MySQL packages are included for mysql provider."""
        mocker.patch("builders_hut.setups.env_setup.run_subprocess")

        setup = SetupEnv(project_with_files)
        setup.configure(
            name="test",
            description="desc",
            version="1.0.0",
            database_type="sql",
            database_provider="mysql",
        )
        setup.create()

        requirements = (project_with_files / "requirements.txt").read_text()

        for package in DB_SQL_PACKAGES["mysql"]:
            assert package in requirements

    def test_includes_sqlite_packages_for_sqlite(self, project_with_files, mocker):
        """Verify SQLite packages are included for sqlite provider."""
        mocker.patch("builders_hut.setups.env_setup.run_subprocess")

        setup = SetupEnv(project_with_files)
        setup.configure(
            name="test",
            description="desc",
            version="1.0.0",
            database_type="sql",
            database_provider="sqlite",
        )
        setup.create()

        requirements = (project_with_files / "requirements.txt").read_text()

        for package in DB_SQL_PACKAGES["sqlite"]:
            assert package in requirements

    def test_includes_sql_common_packages(self, project_with_files, mocker):
        """Verify alembic is included for SQL databases."""
        mocker.patch("builders_hut.setups.env_setup.run_subprocess")

        setup = SetupEnv(project_with_files)
        setup.configure(
            name="test",
            description="desc",
            version="1.0.0",
            database_type="sql",
            database_provider="postgres",
        )
        setup.create()

        requirements = (project_with_files / "requirements.txt").read_text()

        assert "alembic" in requirements

    def test_writes_requirements_dev_file(self, project_with_files, mocker):
        """Verify requirements_dev.txt is written."""
        mocker.patch("builders_hut.setups.env_setup.run_subprocess")

        setup = SetupEnv(project_with_files)
        setup.configure(
            name="test",
            description="desc",
            version="1.0.0",
            database_type="sql",
            database_provider="postgres",
        )
        setup.create()

        dev_requirements = project_with_files / "requirements_dev.txt"
        content = dev_requirements.read_text()

        assert "-r requirements.txt" in content
        assert "pytest" in content

    def test_creates_virtual_environment(self, project_with_files, mocker):
        """
        WHAT: Verify virtual environment is created.
        WHY: Dependencies need to be isolated in a venv.
        """
        mock_run = mocker.patch("builders_hut.setups.env_setup.run_subprocess")

        setup = SetupEnv(project_with_files)
        setup.configure(
            name="test",
            description="desc",
            version="1.0.0",
            database_type="sql",
            database_provider="postgres",
        )
        setup.create()

        # Find the call that creates the venv
        calls = [str(call) for call in mock_run.call_args_list]
        venv_call_found = any("python -m venv .venv" in call for call in calls)

        assert venv_call_found, "No call to create venv found"

    def test_installs_dependencies(self, project_with_files, mocker):
        """Verify pip install is called."""
        mock_run = mocker.patch("builders_hut.setups.env_setup.run_subprocess")

        setup = SetupEnv(project_with_files)
        setup.configure(
            name="test",
            description="desc",
            version="1.0.0",
            database_type="sql",
            database_provider="postgres",
        )
        setup.create()

        # Find the call that installs dependencies
        calls = [str(call) for call in mock_run.call_args_list]
        install_call_found = any("pip install" in call for call in calls)

        assert install_call_found, "No pip install call found"

    def test_raises_error_on_venv_creation_failure(self, project_with_files, mocker):
        """
        WHAT: Verify RuntimeError is raised when venv creation fails.
        WHY: User should know if setup failed.
        """

        def mock_subprocess(location, command):
            if "venv" in command:
                raise subprocess.CalledProcessError(1, command)

        mocker.patch(
            "builders_hut.setups.env_setup.run_subprocess",
            side_effect=mock_subprocess,
        )

        setup = SetupEnv(project_with_files)
        setup.configure(
            name="test",
            description="desc",
            version="1.0.0",
            database_type="sql",
            database_provider="postgres",
        )

        with pytest.raises(RuntimeError) as exc_info:
            setup.create()

        assert "Failed to create environment" in str(exc_info.value)

    def test_raises_error_on_pip_install_failure(self, project_with_files, mocker):
        """Verify RuntimeError is raised when pip install fails."""
        call_count = 0

        def mock_subprocess(location, command):
            nonlocal call_count
            call_count += 1
            # Fail on the pip install call (third subprocess call)
            if "pip install" in command:
                raise subprocess.CalledProcessError(1, command)

        mocker.patch(
            "builders_hut.setups.env_setup.run_subprocess",
            side_effect=mock_subprocess,
        )

        setup = SetupEnv(project_with_files)
        setup.configure(
            name="test",
            description="desc",
            version="1.0.0",
            database_type="sql",
            database_provider="postgres",
        )

        with pytest.raises(RuntimeError):
            setup.create()

    def test_location_stored_correctly(self, temp_project_dir):
        """Verify location is stored as Path attribute."""
        setup = SetupEnv(temp_project_dir)

        assert setup.location == temp_project_dir
        assert isinstance(setup.location, Path)


# =============================================================================
# Tests for Package Constants
# =============================================================================


class TestPackageConstants:
    """Tests for package list constants."""

    def test_packages_contains_fastapi(self):
        """Verify PACKAGES includes FastAPI."""
        assert "fastapi" in PACKAGES

    def test_packages_contains_uvicorn(self):
        """Verify PACKAGES includes uvicorn for running the server."""
        assert "uvicorn" in PACKAGES

    def test_dev_packages_contains_pytest(self):
        """Verify DEV_PACKAGES includes pytest."""
        assert "pytest" in DEV_PACKAGES

    def test_sql_common_package_contains_alembic(self):
        """Verify SQL_COMMON_PACKAGE includes alembic for migrations."""
        assert "alembic" in SQL_COMMON_PACKAGE

    def test_db_sql_packages_has_postgres(self):
        """Verify DB_SQL_PACKAGES has postgres configuration."""
        assert "postgres" in DB_SQL_PACKAGES
        assert "asyncpg" in DB_SQL_PACKAGES["postgres"]

    def test_db_sql_packages_has_mysql(self):
        """Verify DB_SQL_PACKAGES has mysql configuration."""
        assert "mysql" in DB_SQL_PACKAGES
        assert "aiomysql" in DB_SQL_PACKAGES["mysql"]

    def test_db_sql_packages_has_sqlite(self):
        """Verify DB_SQL_PACKAGES has sqlite configuration."""
        assert "sqlite" in DB_SQL_PACKAGES
        assert "aiosqlite" in DB_SQL_PACKAGES["sqlite"]


# =============================================================================
# End of test_env_setup.py
# =============================================================================
