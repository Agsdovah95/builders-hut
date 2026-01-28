# =============================================================================
# Unit Tests for builders_hut/setups/files_setup.py
# =============================================================================
#
# LEARNING NOTE: Testing with Prerequisites
# -----------------------------------------
# SetupFiles requires directories to exist before creating files.
# We have two approaches:
#
# 1. Use SetupStructure to create directories first (integration-ish)
# 2. Create only needed directories manually (more isolated)
#
# We'll use approach 2 for unit tests to keep them focused and fast.
#
# =============================================================================

from pathlib import Path

import pytest

from builders_hut.setups.files_setup import SetupFiles
from builders_hut.setups.structure_setup import SetupStructure


# =============================================================================
# Tests for SetupFiles
# =============================================================================


class TestSetupFiles:
    """Tests for the SetupFiles class."""

    @pytest.fixture
    def project_with_structure(self, temp_project_dir):
        """
        Creates the directory structure before file creation.

        LEARNING NOTE: Test Fixtures
        ----------------------------
        This fixture depends on temp_project_dir (another fixture).
        Pytest handles the dependency chain automatically:
        1. Creates temp_project_dir
        2. Creates directory structure
        3. Returns the path
        4. Cleans up after test
        """
        SetupStructure(temp_project_dir).create()
        return temp_project_dir

    def test_creates_main_py(self, project_with_structure):
        """Verify main.py is created."""
        setup = SetupFiles(project_with_structure)
        setup.create()

        main_file = project_with_structure / "app" / "main.py"
        assert main_file.exists()
        assert main_file.is_file()

    def test_creates_empty_files(self, project_with_structure):
        """
        WHAT: Verify created files are empty.
        WHY: SetupFiles only creates files; content is added by SetupFileWriter.
        """
        setup = SetupFiles(project_with_structure)
        setup.create()

        main_file = project_with_structure / "app" / "main.py"
        assert main_file.read_text() == ""

    def test_creates_all_init_files(self, project_with_structure):
        """
        WHAT: Verify all __init__.py files are created.
        WHY: These make directories into Python packages.
        """
        setup = SetupFiles(project_with_structure)
        setup.create()

        init_files = [
            "app/api/__init__.py",
            "app/api/v1/__init__.py",
            "app/core/__init__.py",
            "app/database/__init__.py",
            "app/models/__init__.py",
            "app/repositories/__init__.py",
            "app/schemas/__init__.py",
            "app/services/__init__.py",
            "app/utils/__init__.py",
            "app/workers/__init__.py",
            "tests/__init__.py",
        ]

        for file_path in init_files:
            full_path = project_with_structure / file_path
            assert full_path.exists(), f"{file_path} was not created"

    def test_creates_env_file(self, project_with_structure):
        """Verify .env file is created."""
        setup = SetupFiles(project_with_structure)
        setup.create()

        env_file = project_with_structure / ".env"
        assert env_file.exists()

    def test_creates_gitignore_file(self, project_with_structure):
        """Verify .gitignore file is created."""
        setup = SetupFiles(project_with_structure)
        setup.create()

        gitignore_file = project_with_structure / ".gitignore"
        assert gitignore_file.exists()

    def test_creates_requirements_files(self, project_with_structure):
        """Verify requirements.txt and requirements_dev.txt are created."""
        setup = SetupFiles(project_with_structure)
        setup.create()

        assert (project_with_structure / "requirements.txt").exists()
        assert (project_with_structure / "requirements_dev.txt").exists()

    def test_creates_run_py(self, project_with_structure):
        """Verify run.py is created."""
        setup = SetupFiles(project_with_structure)
        setup.create()

        assert (project_with_structure / "run.py").exists()

    def test_creates_api_files(self, project_with_structure):
        """Verify API route files are created."""
        setup = SetupFiles(project_with_structure)
        setup.create()

        assert (project_with_structure / "app" / "api" / "common.py").exists()
        assert (project_with_structure / "app" / "api" / "v1" / "hero.py").exists()

    def test_creates_core_files(self, project_with_structure):
        """Verify core configuration files are created."""
        setup = SetupFiles(project_with_structure)
        setup.create()

        core_files = [
            "app/core/config.py",
            "app/core/errors.py",
            "app/core/exceptions.py",
            "app/core/lifespan.py",
            "app/core/logger.py",
            "app/core/response_helper.py",
            "app/core/responses.py",
        ]

        for file_path in core_files:
            full_path = project_with_structure / file_path
            assert full_path.exists(), f"{file_path} was not created"

    def test_creates_database_files(self, project_with_structure):
        """Verify database files are created."""
        setup = SetupFiles(project_with_structure)
        setup.create()

        assert (project_with_structure / "app" / "database" / "session.py").exists()

    def test_creates_model_files(self, project_with_structure):
        """Verify model files are created."""
        setup = SetupFiles(project_with_structure)
        setup.create()

        assert (project_with_structure / "app" / "models" / "common.py").exists()
        assert (project_with_structure / "app" / "models" / "hero.py").exists()

    def test_creates_repository_files(self, project_with_structure):
        """Verify repository files are created."""
        setup = SetupFiles(project_with_structure)
        setup.create()

        assert (project_with_structure / "app" / "repositories" / "hero.py").exists()

    def test_creates_schema_files(self, project_with_structure):
        """Verify schema files are created."""
        setup = SetupFiles(project_with_structure)
        setup.create()

        assert (project_with_structure / "app" / "schemas" / "hero.py").exists()
        assert (project_with_structure / "app" / "schemas" / "common.py").exists()

    def test_creates_service_files(self, project_with_structure):
        """Verify service files are created."""
        setup = SetupFiles(project_with_structure)
        setup.create()

        assert (project_with_structure / "app" / "services" / "hero.py").exists()

    def test_creates_template_files(self, project_with_structure):
        """Verify template files are created."""
        setup = SetupFiles(project_with_structure)
        setup.create()

        assert (project_with_structure / "app" / "templates" / "index.html").exists()

    def test_files_to_create_count(self):
        """
        WHAT: Verify expected number of files in FILES_TO_CREATE.
        WHY: Catch accidental additions or removals.

        LEARNING NOTE: Regression Testing
        ----------------------------------
        This test catches unintended changes to the file list.
        If someone adds/removes files, this test will fail and
        prompt them to verify the change was intentional.
        """
        # Count the files in the list
        file_count = len(SetupFiles.FILES_TO_CREATE)

        # Based on the current implementation, there should be 34 files
        # Update this number if files are intentionally added/removed
        assert file_count == 34, f"Expected 34 files, got {file_count}"

    def test_idempotent_creation(self, project_with_structure):
        """Verify running create() twice doesn't cause errors."""
        setup = SetupFiles(project_with_structure)

        setup.create()
        setup.create()  # Should not raise

        # Files should still exist
        assert (project_with_structure / "app" / "main.py").exists()

    def test_location_stored_correctly(self, temp_project_dir):
        """Verify location is stored as Path attribute."""
        setup = SetupFiles(temp_project_dir)

        assert setup.location == temp_project_dir
        assert isinstance(setup.location, Path)


# =============================================================================
# End of test_files_setup.py
# =============================================================================
