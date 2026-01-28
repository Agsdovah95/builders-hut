# =============================================================================
# Unit Tests for builders_hut/setups/db_setup.py
# =============================================================================
#
# LEARNING NOTE: Testing Delegation Patterns
# ------------------------------------------
# SetupDatabase delegates work to DatabaseFactory. We test:
# 1. Configuration is stored correctly
# 2. DatabaseFactory is called with correct arguments
# 3. The delegation happens as expected
#
# =============================================================================

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from builders_hut.setups.db_setup import SetupDatabase


# =============================================================================
# Tests for SetupDatabase
# =============================================================================


class TestSetupDatabase:
    """Tests for the SetupDatabase class."""

    def test_configure_stores_database_type_sql(self, temp_project_dir):
        """Verify configure() stores 'sql' database_type."""
        setup = SetupDatabase(temp_project_dir)
        setup.configure(database_type="sql")

        assert setup.database_type == "sql"

    def test_configure_stores_database_type_nosql(self, temp_project_dir):
        """Verify configure() stores 'nosql' database_type."""
        setup = SetupDatabase(temp_project_dir)
        setup.configure(database_type="nosql")

        assert setup.database_type == "nosql"

    def test_configure_ignores_extra_kwargs(self, temp_project_dir):
        """
        WHAT: Verify configure() accepts extra kwargs without error.
        WHY: Other setup classes may pass additional parameters.
        """
        setup = SetupDatabase(temp_project_dir)

        # Should not raise
        setup.configure(
            database_type="sql",
            name="test",
            version="1.0.0",
            extra_param="ignored",
        )

        assert setup.database_type == "sql"

    def test_create_calls_database_factory(self, temp_project_dir, mocker):
        """
        WHAT: Verify create() instantiates and calls DatabaseFactory.
        WHY: SetupDatabase delegates to DatabaseFactory.

        LEARNING NOTE: Mocking Classes
        -------------------------------
        We mock the DatabaseFactory class itself. When it's instantiated,
        it returns our mock, and we can verify setup_db() was called.
        """
        # Create a mock for DatabaseFactory
        mock_factory = MagicMock()
        mock_factory_class = mocker.patch(
            "builders_hut.setups.db_setup.DatabaseFactory",
            return_value=mock_factory,
        )

        setup = SetupDatabase(temp_project_dir)
        setup.configure(database_type="sql")
        setup.create()

        # Verify DatabaseFactory was instantiated with correct args
        mock_factory_class.assert_called_once_with("sql", temp_project_dir)

        # Verify setup_db() was called
        mock_factory.setup_db.assert_called_once()

    def test_create_passes_nosql_to_factory(self, temp_project_dir, mocker):
        """Verify 'nosql' type is passed to DatabaseFactory."""
        mock_factory = MagicMock()
        mock_factory_class = mocker.patch(
            "builders_hut.setups.db_setup.DatabaseFactory",
            return_value=mock_factory,
        )

        setup = SetupDatabase(temp_project_dir)
        setup.configure(database_type="nosql")
        setup.create()

        mock_factory_class.assert_called_once_with("nosql", temp_project_dir)

    def test_location_stored_correctly(self, temp_project_dir):
        """Verify location is stored as Path attribute."""
        setup = SetupDatabase(temp_project_dir)

        assert setup.location == temp_project_dir
        assert isinstance(setup.location, Path)


# =============================================================================
# End of test_db_setup.py
# =============================================================================
