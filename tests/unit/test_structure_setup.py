# =============================================================================
# Unit Tests for builders_hut/setups/structure_setup.py
# =============================================================================
#
# LEARNING NOTE: Testing File System Operations
# ---------------------------------------------
# When testing code that creates directories/files, we have two options:
#
# 1. Use real file system (temp directories) - Tests actual behavior
# 2. Mock the file system calls - Tests logic without I/O
#
# Here we use temp directories (Option 1) because:
# - It's more realistic
# - Cleanup is handled by fixtures
# - We can verify the actual structure
#
# =============================================================================

from pathlib import Path

import pytest

from builders_hut.setups.structure_setup import SetupStructure


# =============================================================================
# Tests for SetupStructure
# =============================================================================


class TestSetupStructure:
    """Tests for the SetupStructure class."""

    def test_creates_app_directory(self, temp_project_dir):
        """
        WHAT: Verify SetupStructure creates the 'app' directory.
        WHY: 'app' is the main application directory.
        """
        setup = SetupStructure(temp_project_dir)
        setup.create()

        app_dir = temp_project_dir / "app"
        assert app_dir.exists()
        assert app_dir.is_dir()

    def test_creates_tests_directory(self, temp_project_dir):
        """Verify SetupStructure creates the 'tests' directory."""
        setup = SetupStructure(temp_project_dir)
        setup.create()

        tests_dir = temp_project_dir / "tests"
        assert tests_dir.exists()
        assert tests_dir.is_dir()

    def test_creates_all_subdirectories(self, temp_project_dir, expected_app_directories):
        """
        WHAT: Verify all expected subdirectories are created.
        WHY: The project structure must be complete.

        LEARNING NOTE: Fixture Dependencies
        -----------------------------------
        This test uses the 'expected_app_directories' fixture from conftest.py.
        This keeps the expected structure in one place for easy updates.
        """
        setup = SetupStructure(temp_project_dir)
        setup.create()

        for dir_path in expected_app_directories:
            full_path = temp_project_dir / dir_path
            assert full_path.exists(), f"Directory {dir_path} was not created"
            assert full_path.is_dir(), f"{dir_path} is not a directory"

    def test_creates_api_directory(self, temp_project_dir):
        """Verify 'app/api' directory is created."""
        setup = SetupStructure(temp_project_dir)
        setup.create()

        assert (temp_project_dir / "app" / "api").exists()

    def test_creates_api_v1_directory(self, temp_project_dir):
        """Verify 'app/api/v1' directory is created."""
        setup = SetupStructure(temp_project_dir)
        setup.create()

        assert (temp_project_dir / "app" / "api" / "v1").exists()

    def test_creates_database_directory(self, temp_project_dir):
        """Verify 'app/database' directory is created."""
        setup = SetupStructure(temp_project_dir)
        setup.create()

        assert (temp_project_dir / "app" / "database").exists()

    def test_creates_schemas_directory(self, temp_project_dir):
        """Verify 'app/schemas' directory is created."""
        setup = SetupStructure(temp_project_dir)
        setup.create()

        assert (temp_project_dir / "app" / "schemas").exists()

    def test_creates_services_directory(self, temp_project_dir):
        """Verify 'app/services' directory is created."""
        setup = SetupStructure(temp_project_dir)
        setup.create()

        assert (temp_project_dir / "app" / "services").exists()

    def test_creates_repositories_directory(self, temp_project_dir):
        """Verify 'app/repositories' directory is created."""
        setup = SetupStructure(temp_project_dir)
        setup.create()

        assert (temp_project_dir / "app" / "repositories").exists()

    def test_creates_core_directory(self, temp_project_dir):
        """Verify 'app/core' directory is created."""
        setup = SetupStructure(temp_project_dir)
        setup.create()

        assert (temp_project_dir / "app" / "core").exists()

    def test_creates_models_directory(self, temp_project_dir):
        """Verify 'app/models' directory is created."""
        setup = SetupStructure(temp_project_dir)
        setup.create()

        assert (temp_project_dir / "app" / "models").exists()

    def test_creates_workers_directory(self, temp_project_dir):
        """Verify 'app/workers' directory is created."""
        setup = SetupStructure(temp_project_dir)
        setup.create()

        assert (temp_project_dir / "app" / "workers").exists()

    def test_creates_utils_directory(self, temp_project_dir):
        """Verify 'app/utils' directory is created."""
        setup = SetupStructure(temp_project_dir)
        setup.create()

        assert (temp_project_dir / "app" / "utils").exists()

    def test_creates_templates_directory(self, temp_project_dir):
        """Verify 'app/templates' directory is created."""
        setup = SetupStructure(temp_project_dir)
        setup.create()

        assert (temp_project_dir / "app" / "templates").exists()

    def test_idempotent_creation(self, temp_project_dir):
        """
        WHAT: Verify running create() twice doesn't cause errors.
        WHY: Idempotent operations can be safely retried.

        LEARNING NOTE: Idempotency
        --------------------------
        An idempotent operation produces the same result whether executed
        once or multiple times. This is important for reliability.
        """
        setup = SetupStructure(temp_project_dir)

        # First creation
        setup.create()

        # Second creation should not raise
        setup.create()

        # Structure should still be valid
        assert (temp_project_dir / "app").exists()
        assert (temp_project_dir / "tests").exists()

    def test_all_dirs_class_attribute(self):
        """
        WHAT: Verify ALL_DIRS contains expected directories.
        WHY: This is the source of truth for directory structure.
        """
        expected = [
            "api",
            "api/v1",
            "database",
            "schemas",
            "services",
            "repositories",
            "core",
            "models",
            "workers",
            "utils",
            "templates",
        ]

        assert SetupStructure.ALL_DIRS == expected

    def test_location_stored_correctly(self, temp_project_dir):
        """Verify location is stored as Path attribute."""
        setup = SetupStructure(temp_project_dir)

        assert setup.location == temp_project_dir
        assert isinstance(setup.location, Path)


# =============================================================================
# End of test_structure_setup.py
# =============================================================================
