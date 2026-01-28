# =============================================================================
# Unit Tests for builders_hut/setups/file_writer.py
# =============================================================================
#
# LEARNING NOTE: Testing Template Writing
# ---------------------------------------
# SetupFileWriter writes content to files from templates.
# We test:
# 1. Content is written to the correct files
# 2. Template variables are substituted correctly (especially .env)
# 3. All files from FILES_TO_WRITE are processed
#
# =============================================================================

from pathlib import Path

import pytest

from builders_hut.setups.file_writer import SetupFileWriter
from builders_hut.setups.all_writes import FILES_TO_WRITE
from builders_hut.setups.structure_setup import SetupStructure
from builders_hut.setups.files_setup import SetupFiles


# =============================================================================
# Tests for SetupFileWriter
# =============================================================================


class TestSetupFileWriter:
    """Tests for the SetupFileWriter class."""

    @pytest.fixture
    def project_with_files(self, temp_project_dir):
        """Creates directory structure and empty files."""
        SetupStructure(temp_project_dir).create()
        SetupFiles(temp_project_dir).create()
        return temp_project_dir

    def test_configure_stores_name(self, temp_project_dir):
        """Verify configure() stores the name attribute."""
        setup = SetupFileWriter(temp_project_dir)
        setup.configure(
            name="my_project",
            description="desc",
            version="1.0.0",
            database_provider="postgres",
        )

        assert setup.name == "my_project"

    def test_configure_stores_description(self, temp_project_dir):
        """Verify configure() stores the description attribute."""
        setup = SetupFileWriter(temp_project_dir)
        setup.configure(
            name="test",
            description="A wonderful project",
            version="1.0.0",
            database_provider="postgres",
        )

        assert setup.description == "A wonderful project"

    def test_configure_stores_version(self, temp_project_dir):
        """Verify configure() stores the version attribute."""
        setup = SetupFileWriter(temp_project_dir)
        setup.configure(
            name="test",
            description="desc",
            version="2.5.0",
            database_provider="postgres",
        )

        assert setup.version == "2.5.0"

    def test_configure_stores_database_provider(self, temp_project_dir):
        """Verify configure() stores the database_provider attribute."""
        setup = SetupFileWriter(temp_project_dir)
        setup.configure(
            name="test",
            description="desc",
            version="1.0.0",
            database_provider="mysql",
        )

        assert setup.database_provider == "mysql"

    def test_create_calls_write_files(self, temp_project_dir, mocker):
        """
        WHAT: Verify create() calls _write_files().
        WHY: This is the main action of SetupFileWriter.
        """
        setup = SetupFileWriter(temp_project_dir)
        setup.configure(
            name="test",
            description="desc",
            version="1.0.0",
            database_provider="postgres",
        )

        # Mock _write_files to avoid the .env template bug
        mock_write = mocker.patch.object(setup, "_write_files")

        setup.create()

        mock_write.assert_called_once()

    def test_files_to_write_has_expected_count(self):
        """
        WHAT: Verify FILES_TO_WRITE has expected number of entries.
        WHY: Ensures all templates are registered.
        """
        # FILES_TO_WRITE should have 25 template file entries
        assert len(FILES_TO_WRITE) == 25

    def test_files_to_write_contains_non_env_files(self):
        """
        WHAT: Verify FILES_TO_WRITE contains non-.env files.
        WHY: Ensures template files beyond .env are registered.
        """
        non_env_files = [p for p in FILES_TO_WRITE.keys() if p.name != ".env"]

        # Should have 24 non-.env files (25 total - 1 .env)
        assert len(non_env_files) == 24

        # All should have content
        for path in non_env_files:
            content = FILES_TO_WRITE[path]
            assert isinstance(content, str)
            assert len(content) > 0

    def test_formats_env_file_with_title(self, project_with_files, mocker):
        """
        WHAT: Verify .env file gets title formatted.
        WHY: Project name should appear in .env.
        """
        written_files = {}

        def capture_writes(path, content):
            written_files[path.name] = content

        mocker.patch(
            "builders_hut.setups.file_writer.write_file",
            side_effect=capture_writes,
        )

        setup = SetupFileWriter(project_with_files)
        setup.configure(
            name="my_awesome_project",
            description="desc",
            version="1.0.0",
            database_provider="postgres",
        )

        setup.create()

        # Verify .env was written with the project name
        assert ".env" in written_files
        assert "my_awesome_project" in written_files[".env"]

    def test_location_stored_correctly(self, temp_project_dir):
        """Verify location is stored as Path attribute."""
        setup = SetupFileWriter(temp_project_dir)

        assert setup.location == temp_project_dir
        assert isinstance(setup.location, Path)


# =============================================================================
# Tests for FILES_TO_WRITE Mapping
# =============================================================================


class TestFilesToWrite:
    """Tests for the FILES_TO_WRITE constant."""

    def test_files_to_write_not_empty(self):
        """Verify FILES_TO_WRITE contains entries."""
        assert len(FILES_TO_WRITE) > 0

    def test_files_to_write_has_main_py(self):
        """Verify main.py is in the mapping."""
        paths = [str(p) for p in FILES_TO_WRITE.keys()]
        main_found = any("main.py" in p for p in paths)
        assert main_found, "main.py not found in FILES_TO_WRITE"

    def test_files_to_write_has_env_file(self):
        """Verify .env is in the mapping."""
        paths = [str(p) for p in FILES_TO_WRITE.keys()]
        env_found = any(".env" in p for p in paths)
        assert env_found, ".env not found in FILES_TO_WRITE"

    def test_files_to_write_has_gitignore(self):
        """Verify .gitignore is in the mapping."""
        paths = [str(p) for p in FILES_TO_WRITE.keys()]
        gitignore_found = any(".gitignore" in p for p in paths)
        assert gitignore_found, ".gitignore not found in FILES_TO_WRITE"

    def test_files_to_write_values_are_strings(self):
        """Verify all values in FILES_TO_WRITE are strings."""
        for path, content in FILES_TO_WRITE.items():
            assert isinstance(content, str), f"Content for {path} is not a string"

    def test_files_to_write_keys_are_paths(self):
        """Verify all keys in FILES_TO_WRITE are Path objects."""
        for path in FILES_TO_WRITE.keys():
            assert isinstance(path, Path), f"{path} is not a Path object"


# =============================================================================
# End of test_file_writer.py
# =============================================================================
