# =============================================================================
# Unit Tests for builders_hut/utils.py
# =============================================================================
#
# LEARNING NOTE: Anatomy of a Test File
# -------------------------------------
# A well-organized test file typically has:
# 1. Imports at the top
# 2. Tests grouped by the function/class they test
# 3. Clear, descriptive test names that explain what's being tested
#
# Test naming convention: test_<function_name>_<scenario>_<expected_outcome>
# Example: test_write_file_when_file_missing_raises_error
#
# =============================================================================

from pathlib import Path
from unittest.mock import MagicMock
import subprocess

import pytest
import tomlkit

from builders_hut.utils import (
    get_platform,
    get_python_file,
    make_file,
    make_folder,
    run_subprocess,
    setup_project,
    write_file,
    write_pyproject,
)
from builders_hut.setups.base_setup import BaseSetup


# =============================================================================
# Tests for get_platform()
# =============================================================================
#
# LEARNING NOTE: Testing Platform-Dependent Code
# -----------------------------------------------
# get_platform() returns different values on different operating systems.
# We can test this by mocking the platform.system() function to return
# specific values, allowing us to test all code paths on any machine.
#


class TestGetPlatform:
    """Tests for the get_platform() function."""

    def test_get_platform_returns_lowercase(self, mocker):
        """
        WHAT: Verify get_platform() returns lowercase OS name.
        WHY: The function uses .lower() to normalize the output.
        HOW: Mock platform.system() to return 'Windows' (capitalized).
        """
        # Arrange: Mock platform.system to return a capitalized value
        mocker.patch("builders_hut.utils.platform.system", return_value="Windows")

        # Act: Call the function
        result = get_platform()

        # Assert: Result should be lowercase
        assert result == "windows"

    def test_get_platform_linux(self, mocker):
        """Test that 'Linux' system returns 'linux'."""
        mocker.patch("builders_hut.utils.platform.system", return_value="Linux")
        assert get_platform() == "linux"

    def test_get_platform_darwin(self, mocker):
        """Test that macOS ('Darwin') returns 'darwin'."""
        mocker.patch("builders_hut.utils.platform.system", return_value="Darwin")
        assert get_platform() == "darwin"


# =============================================================================
# Tests for get_python_file()
# =============================================================================
#
# LEARNING NOTE: Testing Functions with Dependencies
# --------------------------------------------------
# get_python_file() calls get_platform() internally. We mock get_platform()
# to control its return value and test both code paths.
#


class TestGetPythonFile:
    """Tests for the get_python_file() function."""

    def test_get_python_file_linux(self, mocker):
        """
        WHAT: Verify Linux returns Unix-style venv path.
        WHY: Linux uses forward slashes and 'bin' directory.
        """
        mocker.patch("builders_hut.utils.get_platform", return_value="linux")

        result = get_python_file()

        assert result == ".venv/bin/python -m"

    def test_get_python_file_windows(self, mocker):
        """
        WHAT: Verify Windows returns Windows-style venv path.
        WHY: Windows uses backslashes and 'Scripts' directory.
        """
        mocker.patch("builders_hut.utils.get_platform", return_value="windows")

        result = get_python_file()

        assert result == ".venv\\Scripts\\python.exe -m"

    def test_get_python_file_other_os_uses_linux_path(self, mocker):
        """
        WHAT: Verify non-Linux OS (like macOS) falls through to else branch.
        WHY: The code only checks for 'linux', everything else uses Windows path.
        NOTE: This might be a bug in the original code - macOS should use Unix path.
        """
        mocker.patch("builders_hut.utils.get_platform", return_value="darwin")

        result = get_python_file()

        # Current behavior: non-linux returns Windows path
        # This tests the ACTUAL behavior, not necessarily the desired behavior
        assert result == ".venv\\Scripts\\python.exe -m"


# =============================================================================
# Tests for make_folder()
# =============================================================================
#
# LEARNING NOTE: Testing File System Operations
# ---------------------------------------------
# For file system tests, we use the temp_project_dir fixture which gives us
# a real temporary directory. This is better than mocking because:
# 1. We test real behavior
# 2. The fixture handles cleanup automatically
# 3. Tests are more reliable
#


class TestMakeFolder:
    """Tests for the make_folder() function."""

    def test_make_folder_creates_directory(self, temp_project_dir):
        """
        WHAT: Verify make_folder creates a new directory.
        WHY: Core functionality - must create directories.
        """
        # Arrange: Define path for new directory
        new_dir = temp_project_dir / "new_folder"
        assert not new_dir.exists()  # Precondition check

        # Act: Create the folder
        make_folder(new_dir)

        # Assert: Directory now exists
        assert new_dir.exists()
        assert new_dir.is_dir()

    def test_make_folder_creates_nested_directories(self, temp_project_dir):
        """
        WHAT: Verify make_folder creates parent directories.
        WHY: Uses parents=True, so deep paths should work.
        """
        deep_path = temp_project_dir / "a" / "b" / "c" / "d"

        make_folder(deep_path)

        assert deep_path.exists()
        assert deep_path.is_dir()

    def test_make_folder_existing_directory_no_error(self, temp_project_dir):
        """
        WHAT: Verify make_folder doesn't raise error if directory exists.
        WHY: Uses exist_ok=True, so this should be idempotent.
        """
        existing_dir = temp_project_dir / "existing"
        existing_dir.mkdir()  # Create it first

        # Act & Assert: Should not raise
        make_folder(existing_dir)

        assert existing_dir.exists()


# =============================================================================
# Tests for make_file()
# =============================================================================


class TestMakeFile:
    """Tests for the make_file() function."""

    def test_make_file_creates_file(self, temp_project_dir):
        """Verify make_file creates a new file."""
        new_file = temp_project_dir / "test.txt"

        make_file(new_file)

        assert new_file.exists()
        assert new_file.is_file()

    def test_make_file_creates_empty_file(self, temp_project_dir):
        """Verify created file is empty."""
        new_file = temp_project_dir / "empty.txt"

        make_file(new_file)

        assert new_file.read_text() == ""

    def test_make_file_existing_file_no_error(self, temp_project_dir):
        """Verify make_file doesn't fail on existing file."""
        existing_file = temp_project_dir / "existing.txt"
        existing_file.write_text("original content")

        # Should not raise
        make_file(existing_file)

        # Content should be preserved (touch doesn't overwrite)
        assert existing_file.read_text() == "original content"


# =============================================================================
# Tests for write_file()
# =============================================================================
#
# LEARNING NOTE: Testing Error Conditions
# ---------------------------------------
# It's important to test that functions fail correctly when given bad input.
# Use pytest.raises() to verify the correct exception is raised.
#


class TestWriteFile:
    """Tests for the write_file() function."""

    def test_write_file_writes_content(self, temp_project_dir):
        """Verify write_file writes content to existing file."""
        test_file = temp_project_dir / "test.txt"
        test_file.touch()  # File must exist first

        write_file(test_file, "Hello, World!")

        assert test_file.read_text() == "Hello, World!"

    def test_write_file_overwrites_existing_content(self, temp_project_dir):
        """Verify write_file replaces existing content."""
        test_file = temp_project_dir / "test.txt"
        test_file.write_text("old content")

        write_file(test_file, "new content")

        assert test_file.read_text() == "new content"

    def test_write_file_missing_file_raises_error(self, temp_project_dir):
        """
        WHAT: Verify write_file raises FileNotFoundError for missing files.
        WHY: The function requires the file to exist first.

        LEARNING NOTE: pytest.raises()
        ------------------------------
        pytest.raises() is a context manager that:
        1. Expects the code inside to raise an exception
        2. Fails the test if no exception is raised
        3. Allows inspection of the raised exception
        """
        missing_file = temp_project_dir / "does_not_exist.txt"

        with pytest.raises(FileNotFoundError) as exc_info:
            write_file(missing_file, "content")

        # Verify error message contains the file path
        assert "does_not_exist.txt" in str(exc_info.value)

    def test_write_file_handles_unicode(self, temp_project_dir):
        """Verify write_file handles unicode content correctly."""
        test_file = temp_project_dir / "unicode.txt"
        test_file.touch()
        unicode_content = "Hello, 世界! 🎉 Привет мир!"

        write_file(test_file, unicode_content)

        assert test_file.read_text(encoding="utf-8") == unicode_content


# =============================================================================
# Tests for run_subprocess()
# =============================================================================
#
# LEARNING NOTE: Mocking External Commands
# ----------------------------------------
# We mock subprocess.run to avoid actually running shell commands.
# This makes tests:
# 1. Fast (no real command execution)
# 2. Reliable (no dependency on external tools)
# 3. Safe (no side effects)
#


class TestRunSubprocess:
    """Tests for the run_subprocess() function."""

    def test_run_subprocess_calls_subprocess_run(self, mocker, temp_project_dir):
        """
        WHAT: Verify run_subprocess calls subprocess.run correctly.
        WHY: Ensure the wrapper function passes correct arguments.
        """
        mock_run = mocker.patch("builders_hut.utils.subprocess.run")

        run_subprocess(temp_project_dir, "echo hello")

        # Verify subprocess.run was called with expected arguments
        mock_run.assert_called_once_with(
            "echo hello",
            cwd=temp_project_dir,
            shell=True,
            check=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )

    def test_run_subprocess_uses_correct_working_directory(self, mocker, temp_project_dir):
        """Verify the command runs in the specified directory."""
        mock_run = mocker.patch("builders_hut.utils.subprocess.run")

        run_subprocess(temp_project_dir, "ls")

        # Check the cwd parameter
        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["cwd"] == temp_project_dir

    def test_run_subprocess_propagates_error(self, mocker, temp_project_dir):
        """
        WHAT: Verify subprocess errors are propagated.
        WHY: check=True means CalledProcessError should be raised on failure.
        """
        # Configure mock to raise an exception
        mocker.patch(
            "builders_hut.utils.subprocess.run",
            side_effect=subprocess.CalledProcessError(1, "bad_command"),
        )

        with pytest.raises(subprocess.CalledProcessError):
            run_subprocess(temp_project_dir, "bad_command")


# =============================================================================
# Tests for write_pyproject()
# =============================================================================
#
# LEARNING NOTE: Testing File Generation
# --------------------------------------
# When testing functions that generate files, we:
# 1. Call the function with known inputs
# 2. Read the generated file
# 3. Verify the content matches expectations
#


class TestWritePyproject:
    """Tests for the write_pyproject() function."""

    def test_write_pyproject_creates_valid_toml(self, temp_project_dir):
        """
        WHAT: Verify generated pyproject.toml is valid TOML.
        WHY: Invalid TOML would break project setup.
        """
        pyproject_path = temp_project_dir / "pyproject.toml"

        write_pyproject(
            pyproject_path,
            name="test-project",
            version="1.0.0",
            description="Test description",
        )

        # Parse the generated file - will raise if invalid TOML
        content = pyproject_path.read_text()
        parsed = tomlkit.parse(content)

        assert "project" in parsed

    def test_write_pyproject_sets_project_name(self, temp_project_dir):
        """Verify project name is set correctly."""
        pyproject_path = temp_project_dir / "pyproject.toml"

        write_pyproject(pyproject_path, name="my-awesome-project")

        parsed = tomlkit.parse(pyproject_path.read_text())
        assert parsed["project"]["name"] == "my-awesome-project"

    def test_write_pyproject_sets_version(self, temp_project_dir):
        """Verify version is set correctly."""
        pyproject_path = temp_project_dir / "pyproject.toml"

        write_pyproject(pyproject_path, name="test", version="2.5.0")

        parsed = tomlkit.parse(pyproject_path.read_text())
        assert parsed["project"]["version"] == "2.5.0"

    def test_write_pyproject_default_version(self, temp_project_dir):
        """Verify default version is 0.1.0."""
        pyproject_path = temp_project_dir / "pyproject.toml"

        write_pyproject(pyproject_path, name="test")

        parsed = tomlkit.parse(pyproject_path.read_text())
        assert parsed["project"]["version"] == "0.1.0"

    def test_write_pyproject_sets_description(self, temp_project_dir):
        """Verify description is set when provided."""
        pyproject_path = temp_project_dir / "pyproject.toml"

        write_pyproject(
            pyproject_path, name="test", description="A wonderful project"
        )

        parsed = tomlkit.parse(pyproject_path.read_text())
        assert parsed["project"]["description"] == "A wonderful project"

    def test_write_pyproject_omits_empty_description(self, temp_project_dir):
        """Verify empty description is not included."""
        pyproject_path = temp_project_dir / "pyproject.toml"

        write_pyproject(pyproject_path, name="test", description="")

        parsed = tomlkit.parse(pyproject_path.read_text())
        assert "description" not in parsed["project"]

    def test_write_pyproject_sets_python_version(self, temp_project_dir):
        """Verify Python version requirement is set."""
        pyproject_path = temp_project_dir / "pyproject.toml"

        write_pyproject(pyproject_path, name="test", python=">=3.11")

        parsed = tomlkit.parse(pyproject_path.read_text())
        assert parsed["project"]["requires-python"] == ">=3.11"

    def test_write_pyproject_sets_dependencies(self, temp_project_dir):
        """Verify dependencies are included."""
        pyproject_path = temp_project_dir / "pyproject.toml"
        deps = ["fastapi", "uvicorn", "sqlalchemy"]

        write_pyproject(pyproject_path, name="test", dependencies=deps)

        parsed = tomlkit.parse(pyproject_path.read_text())
        assert parsed["project"]["dependencies"] == deps

    def test_write_pyproject_empty_dependencies_default(self, temp_project_dir):
        """Verify empty dependencies list when none provided."""
        pyproject_path = temp_project_dir / "pyproject.toml"

        write_pyproject(pyproject_path, name="test")

        parsed = tomlkit.parse(pyproject_path.read_text())
        assert parsed["project"]["dependencies"] == []

    def test_write_pyproject_sets_dev_dependencies(self, temp_project_dir):
        """Verify dev dependencies are in optional-dependencies."""
        pyproject_path = temp_project_dir / "pyproject.toml"
        dev_deps = ["pytest", "black", "mypy"]

        write_pyproject(pyproject_path, name="test", dev_dependencies=dev_deps)

        parsed = tomlkit.parse(pyproject_path.read_text())
        assert parsed["project"]["optional-dependencies"]["dev"] == dev_deps

    def test_write_pyproject_includes_scripts(self, temp_project_dir):
        """Verify project scripts are included."""
        pyproject_path = temp_project_dir / "pyproject.toml"

        write_pyproject(pyproject_path, name="test")

        parsed = tomlkit.parse(pyproject_path.read_text())
        scripts = parsed["project"]["scripts"]
        assert "run_dev_server" in scripts
        assert "run_prod_server" in scripts

    def test_write_pyproject_overwrites_existing(self, temp_project_dir):
        """Verify existing file is overwritten."""
        pyproject_path = temp_project_dir / "pyproject.toml"
        pyproject_path.write_text("old content")

        write_pyproject(pyproject_path, name="new-project")

        parsed = tomlkit.parse(pyproject_path.read_text())
        assert parsed["project"]["name"] == "new-project"


# =============================================================================
# Tests for setup_project()
# =============================================================================
#
# LEARNING NOTE: Testing with Mock Classes
# ----------------------------------------
# To test setup_project(), we create a mock setup class that tracks
# whether configure() and create() were called with correct arguments.
#


class TestSetupProject:
    """Tests for the setup_project() function."""

    def test_setup_project_instantiates_setup_class(self, temp_project_dir):
        """
        WHAT: Verify setup_project creates an instance of the setup class.
        WHY: The function should instantiate the class with the location.
        """

        # Create a mock setup class
        class MockSetup(BaseSetup):
            instances = []

            def __init__(self, location):
                super().__init__(location)
                MockSetup.instances.append(self)

            def create(self):
                pass

        MockSetup.instances = []  # Reset

        setup_project(temp_project_dir, MockSetup)

        assert len(MockSetup.instances) == 1
        assert MockSetup.instances[0].location == temp_project_dir

    def test_setup_project_calls_configure(self, temp_project_dir):
        """Verify setup_project calls configure() with kwargs."""
        configure_calls = []

        class MockSetup(BaseSetup):
            def configure(self, **kwargs):
                configure_calls.append(kwargs)

            def create(self):
                pass

        setup_project(
            temp_project_dir,
            MockSetup,
            name="test",
            version="1.0.0",
        )

        assert len(configure_calls) == 1
        assert configure_calls[0] == {"name": "test", "version": "1.0.0"}

    def test_setup_project_calls_create(self, temp_project_dir):
        """Verify setup_project calls create() method."""
        create_called = []

        class MockSetup(BaseSetup):
            def create(self):
                create_called.append(True)

        setup_project(temp_project_dir, MockSetup)

        assert len(create_called) == 1

    def test_setup_project_calls_configure_before_create(self, temp_project_dir):
        """
        WHAT: Verify configure() is called before create().
        WHY: Configuration must be set before creation.
        """
        call_order = []

        class MockSetup(BaseSetup):
            def configure(self, **kwargs):
                call_order.append("configure")

            def create(self):
                call_order.append("create")

        setup_project(temp_project_dir, MockSetup, some_config="value")

        assert call_order == ["configure", "create"]


# =============================================================================
# End of test_utils.py
# =============================================================================
