# =============================================================================
# Unit Tests for builders_hut/setups/git_setup.py
# =============================================================================
#
# LEARNING NOTE: Mocking External Commands
# ----------------------------------------
# SetupGithub runs 'git init' via subprocess. In tests, we mock this because:
#
# 1. Speed: Real git operations are slow
# 2. Isolation: Tests shouldn't depend on git being installed
# 3. Control: We can simulate success/failure scenarios
#
# We mock run_subprocess() instead of subprocess.run() because:
# - It's the direct dependency of SetupGithub
# - It's easier to verify the correct arguments are passed
#
# =============================================================================

from pathlib import Path
import subprocess

import pytest

from builders_hut.setups.git_setup import SetupGithub


# =============================================================================
# Tests for SetupGithub
# =============================================================================


class TestSetupGithub:
    """Tests for the SetupGithub class."""

    def test_calls_git_init(self, temp_project_dir, mocker):
        """
        WHAT: Verify SetupGithub calls 'git init'.
        WHY: Core functionality - must initialize git repository.

        LEARNING NOTE: mocker.patch()
        -----------------------------
        mocker.patch() replaces a function/method with a mock.
        The path must be where the function is USED, not where it's defined.
        SetupGithub imports run_subprocess from builders_hut.utils,
        so we patch 'builders_hut.setups.git_setup.run_subprocess'.
        """
        mock_run = mocker.patch("builders_hut.setups.git_setup.run_subprocess")

        setup = SetupGithub(temp_project_dir)
        setup.create()

        # Verify run_subprocess was called with correct arguments
        mock_run.assert_called_once_with(temp_project_dir, "git init")

    def test_uses_correct_location(self, temp_project_dir, mocker):
        """Verify git init runs in the correct directory."""
        mock_run = mocker.patch("builders_hut.setups.git_setup.run_subprocess")

        setup = SetupGithub(temp_project_dir)
        setup.create()

        # Check the location argument
        call_args = mock_run.call_args[0]  # Positional arguments
        assert call_args[0] == temp_project_dir

    def test_raises_runtime_error_on_failure(self, temp_project_dir, mocker):
        """
        WHAT: Verify RuntimeError is raised when git init fails.
        WHY: User should know if git initialization failed.

        LEARNING NOTE: side_effect
        --------------------------
        Setting side_effect on a mock makes it raise an exception
        when called, instead of returning a value.
        """
        # Configure mock to raise an exception
        mocker.patch(
            "builders_hut.setups.git_setup.run_subprocess",
            side_effect=subprocess.CalledProcessError(1, "git init"),
        )

        setup = SetupGithub(temp_project_dir)

        with pytest.raises(RuntimeError) as exc_info:
            setup.create()

        assert "Could Not Initialize Git" in str(exc_info.value)

    def test_handles_generic_exception(self, temp_project_dir, mocker):
        """Verify any exception is wrapped in RuntimeError."""
        mocker.patch(
            "builders_hut.setups.git_setup.run_subprocess",
            side_effect=Exception("Something went wrong"),
        )

        setup = SetupGithub(temp_project_dir)

        with pytest.raises(RuntimeError) as exc_info:
            setup.create()

        assert "Could Not Initialize Git" in str(exc_info.value)

    def test_location_stored_correctly(self, temp_project_dir):
        """Verify location is stored as Path attribute."""
        setup = SetupGithub(temp_project_dir)

        assert setup.location == temp_project_dir
        assert isinstance(setup.location, Path)

    def test_configure_is_optional(self, temp_project_dir, mocker):
        """
        WHAT: Verify configure() can be called without error.
        WHY: SetupGithub doesn't need configuration, but the method exists.
        """
        mocker.patch("builders_hut.setups.git_setup.run_subprocess")

        setup = SetupGithub(temp_project_dir)
        setup.configure(some_param="value")  # Should not raise
        setup.create()  # Should still work


# =============================================================================
# End of test_git_setup.py
# =============================================================================
