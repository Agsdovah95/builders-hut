# =============================================================================
# Unit Tests for builders_hut/setups/database/factory.py
# =============================================================================
#
# LEARNING NOTE: Testing Factory Patterns
# ---------------------------------------
# The Factory pattern creates objects based on parameters.
# DatabaseFactory creates different database setups based on database_type.
#
# We test:
# 1. SQL setup writes correct files and runs Alembic
# 2. NoSQL setup is a no-op (currently)
# 3. Invalid type raises an error
#
# =============================================================================

from pathlib import Path

import pytest

from builders_hut.setups.database.factory import DatabaseFactory
from builders_hut.setups.structure_setup import SetupStructure
from builders_hut.setups.files_setup import SetupFiles


# =============================================================================
# Tests for DatabaseFactory
# =============================================================================


class TestDatabaseFactory:
    """Tests for the DatabaseFactory class."""

    @pytest.fixture
    def project_with_files(self, temp_project_dir):
        """Creates directory structure and empty files."""
        SetupStructure(temp_project_dir).create()
        SetupFiles(temp_project_dir).create()
        return temp_project_dir

    def test_init_stores_database_type(self, temp_project_dir):
        """Verify __init__ stores the database_type attribute."""
        factory = DatabaseFactory("sql", temp_project_dir)

        assert factory.database_type == "sql"

    def test_init_stores_location(self, temp_project_dir):
        """Verify __init__ stores the location attribute."""
        factory = DatabaseFactory("sql", temp_project_dir)

        assert factory.location == temp_project_dir

    def test_sql_writes_session_py(self, project_with_files, mocker):
        """
        WHAT: Verify SQL setup writes session.py.
        WHY: session.py contains database connection logic.
        """
        # Mock run_subprocess to avoid running Alembic
        mocker.patch("builders_hut.setups.database.factory.run_subprocess")

        # Need to create migrations directory and env.py for the test
        (project_with_files / "migrations").mkdir()
        (project_with_files / "migrations" / "env.py").touch()

        factory = DatabaseFactory("sql", project_with_files)
        factory.setup_db()

        session_file = project_with_files / "app" / "database" / "session.py"
        content = session_file.read_text()

        # Should contain database session code
        assert len(content) > 0

    def test_sql_writes_database_init(self, project_with_files, mocker):
        """Verify SQL setup writes database __init__.py."""
        mocker.patch("builders_hut.setups.database.factory.run_subprocess")
        (project_with_files / "migrations").mkdir()
        (project_with_files / "migrations" / "env.py").touch()

        factory = DatabaseFactory("sql", project_with_files)
        factory.setup_db()

        init_file = project_with_files / "app" / "database" / "__init__.py"
        content = init_file.read_text()

        # Should contain exports or imports
        assert len(content) > 0

    def test_sql_runs_alembic_init(self, project_with_files, mocker):
        """
        WHAT: Verify SQL setup runs 'alembic init'.
        WHY: Alembic manages database migrations.
        """
        mock_run = mocker.patch("builders_hut.setups.database.factory.run_subprocess")
        (project_with_files / "migrations").mkdir()
        (project_with_files / "migrations" / "env.py").touch()

        factory = DatabaseFactory("sql", project_with_files)
        factory.setup_db()

        # Find the alembic init call
        calls = [str(call) for call in mock_run.call_args_list]
        alembic_call_found = any("alembic init" in call for call in calls)

        assert alembic_call_found, "alembic init was not called"

    def test_sql_uses_async_template(self, project_with_files, mocker):
        """Verify SQL setup uses async Alembic template."""
        mock_run = mocker.patch("builders_hut.setups.database.factory.run_subprocess")
        (project_with_files / "migrations").mkdir()
        (project_with_files / "migrations" / "env.py").touch()

        factory = DatabaseFactory("sql", project_with_files)
        factory.setup_db()

        # Check for async template flag
        calls = [str(call) for call in mock_run.call_args_list]
        async_template_found = any("-t async" in call for call in calls)

        assert async_template_found, "Async template flag not used"

    def test_sql_writes_migrations_env(self, project_with_files, mocker):
        """
        WHAT: Verify SQL setup writes migrations/env.py.
        WHY: Custom env.py is needed for async SQLAlchemy.
        """
        mocker.patch("builders_hut.setups.database.factory.run_subprocess")

        # Create migrations directory (normally created by alembic init)
        migrations_dir = project_with_files / "migrations"
        migrations_dir.mkdir()
        (migrations_dir / "env.py").touch()  # Create empty file

        factory = DatabaseFactory("sql", project_with_files)
        factory.setup_db()

        env_file = migrations_dir / "env.py"
        content = env_file.read_text()

        # Should contain custom migration env code
        assert len(content) > 0

    def test_nosql_is_noop(self, project_with_files):
        """
        WHAT: Verify NoSQL setup does nothing.
        WHY: NoSQL support is not yet implemented.

        LEARNING NOTE: Testing No-ops
        -----------------------------
        To test that nothing happens, we verify:
        1. No errors are raised
        2. No files are modified
        """
        # Get initial state of a file
        session_file = project_with_files / "app" / "database" / "session.py"
        original_content = session_file.read_text()

        factory = DatabaseFactory("nosql", project_with_files)
        factory.setup_db()  # Should not raise

        # Verify file was not modified
        assert session_file.read_text() == original_content

    def test_invalid_type_raises_error(self, temp_project_dir):
        """
        WHAT: Verify invalid database type raises RuntimeError.
        WHY: Only 'sql' and 'nosql' are valid types.

        LEARNING NOTE: Testing Error Messages
        -------------------------------------
        It's good practice to verify error messages are helpful.
        Users will see these when something goes wrong.
        """
        factory = DatabaseFactory("invalid", temp_project_dir)

        with pytest.raises(RuntimeError) as exc_info:
            factory.setup_db()

        assert "Invalid Database Type" in str(exc_info.value)

    def test_random_type_raises_error(self, temp_project_dir):
        """Verify random database type raises RuntimeError."""
        factory = DatabaseFactory("mongodb_cloud", temp_project_dir)

        with pytest.raises(RuntimeError):
            factory.setup_db()


# =============================================================================
# Tests for SQL Database Setup Details
# =============================================================================


class TestSqlDatabaseSetup:
    """Detailed tests for SQL database setup."""

    @pytest.fixture
    def project_with_migrations(self, temp_project_dir):
        """Creates project structure including migrations directory."""
        SetupStructure(temp_project_dir).create()
        SetupFiles(temp_project_dir).create()
        (temp_project_dir / "migrations").mkdir()
        (temp_project_dir / "migrations" / "env.py").touch()
        return temp_project_dir

    def test_session_contains_async_engine(self, project_with_migrations, mocker):
        """Verify session.py contains async engine setup."""
        mocker.patch("builders_hut.setups.database.factory.run_subprocess")

        factory = DatabaseFactory("sql", project_with_migrations)
        factory.setup_db()

        session_file = project_with_migrations / "app" / "database" / "session.py"
        content = session_file.read_text()

        # Should reference async SQLAlchemy
        assert "async" in content.lower() or "AsyncSession" in content

    def test_uses_correct_python_file_path(self, project_with_migrations, mocker):
        """
        WHAT: Verify correct venv Python path is used.
        WHY: Alembic must run in the project's venv.
        """
        mock_run = mocker.patch("builders_hut.setups.database.factory.run_subprocess")
        mocker.patch(
            "builders_hut.setups.database.factory.get_python_file",
            return_value=".venv/bin/python -m",
        )

        factory = DatabaseFactory("sql", project_with_migrations)
        factory.setup_db()

        # Check that the command includes the venv path
        calls = [str(call) for call in mock_run.call_args_list]
        venv_used = any(".venv" in call for call in calls)

        assert venv_used, "venv Python was not used"


# =============================================================================
# End of test_database_factory.py
# =============================================================================
