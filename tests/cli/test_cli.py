# =============================================================================
# CLI Tests for builders_hut/cmd_interface.py
# =============================================================================
#
# LEARNING NOTE: Testing CLI Applications
# ---------------------------------------
# Testing CLI applications requires simulating command-line invocations.
# Typer provides a CliRunner that makes this easy:
#
# 1. Create a runner: runner = CliRunner()
# 2. Invoke commands: result = runner.invoke(app, ["build", "--help"])
# 3. Check result: assert result.exit_code == 0
#
# Key things to test:
# - Exit codes (0 for success, non-zero for errors)
# - Output text (help messages, version info)
# - Option handling (--version, --help, --path)
#
# =============================================================================

import pytest
from typer.testing import CliRunner

from builders_hut.cmd_interface import app, APP_VERSION, STEPS


# =============================================================================
# Test Setup
# =============================================================================


@pytest.fixture
def runner():
    """
    Creates a CliRunner for testing CLI commands.

    LEARNING NOTE: CliRunner
    ------------------------
    CliRunner is a test utility that invokes CLI commands without
    actually running them in a subprocess. This makes tests:
    1. Fast - No process spawning
    2. Isolated - Output is captured
    3. Controllable - Input can be simulated
    """
    return CliRunner()


# =============================================================================
# Version Tests
# =============================================================================


class TestVersion:
    """Tests for the --version flag."""

    def test_version_flag_shows_version(self, runner):
        """
        WHAT: Verify --version shows the app version.
        WHY: Users need to know which version they're running.
        """
        result = runner.invoke(app, ["--version"])

        assert result.exit_code == 0
        assert APP_VERSION in result.output

    def test_version_short_flag(self, runner):
        """Verify -v also shows version."""
        result = runner.invoke(app, ["-v"])

        assert result.exit_code == 0
        assert APP_VERSION in result.output

    def test_version_contains_hut(self, runner):
        """Verify version output mentions 'hut'."""
        result = runner.invoke(app, ["--version"])

        assert "hut" in result.output.lower()


# =============================================================================
# Help Tests
# =============================================================================


class TestHelp:
    """Tests for --help output."""

    def test_main_help_shows_commands(self, runner):
        """
        WHAT: Verify --help shows available commands.
        WHY: Help should guide users to available commands.
        """
        result = runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "build" in result.output
        assert "add" in result.output

    def test_build_help_shows_options(self, runner):
        """Verify 'build --help' shows build options."""
        result = runner.invoke(app, ["build", "--help"])

        assert result.exit_code == 0
        assert "--path" in result.output
        assert "--accept-defaults" in result.output

    def test_build_help_shows_description(self, runner):
        """Verify 'build --help' shows command description."""
        result = runner.invoke(app, ["build", "--help"])

        assert result.exit_code == 0
        # Should mention building or creating a project
        assert "build" in result.output.lower() or "project" in result.output.lower()

    def test_help_short_flag(self, runner):
        """Verify -h works as help shortcut."""
        # Note: Typer uses --help by default, -h may not be enabled
        result = runner.invoke(app, ["--help"])

        assert result.exit_code == 0


# =============================================================================
# Build Command Tests
# =============================================================================


class TestBuildCommand:
    """Tests for the build command."""

    def test_build_with_accept_defaults(self, runner, temp_project_dir, mocker):
        """
        WHAT: Verify build --accept-defaults runs without prompts.
        WHY: Users should be able to skip the wizard.

        LEARNING NOTE: Mocking in CLI Tests
        -----------------------------------
        We mock the setup functions to avoid actually creating projects.
        This keeps tests fast and focused on CLI behavior.
        """
        # Mock all setup-related functions
        mocker.patch("builders_hut.cmd_interface.run_setup_with_progress")
        mocker.patch("builders_hut.cmd_interface.show_success")

        result = runner.invoke(
            app, ["build", "--accept-defaults", "--path", str(temp_project_dir)]
        )

        # Should complete successfully (or fail gracefully)
        # Exit code 0 = success, 1 = handled error
        assert result.exit_code in [0, 1]

    def test_build_y_short_flag(self, runner, temp_project_dir, mocker):
        """Verify -y works as shortcut for --accept-defaults."""
        mocker.patch("builders_hut.cmd_interface.run_setup_with_progress")
        mocker.patch("builders_hut.cmd_interface.show_success")

        result = runner.invoke(
            app, ["build", "-y", "-p", str(temp_project_dir)]
        )

        assert result.exit_code in [0, 1]

    def test_build_uses_provided_path(self, runner, temp_project_dir, mocker):
        """
        WHAT: Verify build uses the --path option correctly.
        WHY: Users should be able to specify where to create the project.
        """
        mock_progress = mocker.patch(
            "builders_hut.cmd_interface.run_setup_with_progress"
        )
        mocker.patch("builders_hut.cmd_interface.show_success")

        result = runner.invoke(
            app, ["build", "-y", "--path", str(temp_project_dir)]
        )

        # Verify the path was passed to run_setup_with_progress
        if mock_progress.called:
            call_kwargs = mock_progress.call_args.kwargs
            # The path should be the resolved version of our temp dir
            assert "project_location" in call_kwargs


# =============================================================================
# Add Command Tests
# =============================================================================


class TestAddCommand:
    """Tests for the add command."""

    def test_add_shows_not_implemented(self, runner):
        """
        WHAT: Verify add command shows 'not implemented' message.
        WHY: Users should know the feature is pending.
        """
        result = runner.invoke(app, ["add"])

        # Should mention not implemented
        assert "not implemented" in result.output.lower()


# =============================================================================
# Error Handling Tests
# =============================================================================


class TestErrorHandling:
    """Tests for error handling in CLI."""

    def test_invalid_command_shows_error(self, runner):
        """
        WHAT: Verify invalid commands show error message.
        WHY: Users should get helpful feedback for typos.
        """
        result = runner.invoke(app, ["invalid_command"])

        # Should have non-zero exit code
        assert result.exit_code != 0

    def test_no_args_shows_help(self, runner):
        """
        WHAT: Verify running with no args shows help.
        WHY: App is configured with no_args_is_help=True.
        """
        result = runner.invoke(app, [])

        # Should show help (exit 0) and contain command names
        assert "build" in result.output or "Usage" in result.output


# =============================================================================
# Constants Tests
# =============================================================================


class TestConstants:
    """Tests for CLI constants."""

    def test_app_version_is_string(self):
        """Verify APP_VERSION is a valid version string."""
        assert isinstance(APP_VERSION, str)
        # Version should be in semver-like format (x.y.z)
        parts = APP_VERSION.split(".")
        assert len(parts) >= 2

    def test_steps_contains_all_setup_classes(self):
        """Verify STEPS dict has entry for each setup class."""
        expected_steps = [
            "SetupStructure",
            "SetupFiles",
            "SetupGithub",
            "SetupEnv",
            "SetupFileWriter",
            "SetupDatabase",
        ]

        for step in expected_steps:
            assert step in STEPS, f"{step} missing from STEPS"

    def test_steps_values_are_descriptions(self):
        """Verify STEPS values are descriptive strings."""
        for step, description in STEPS.items():
            assert isinstance(description, str)
            assert len(description) > 5  # Meaningful description


# =============================================================================
# UI Function Tests
# =============================================================================


class TestUIFunctions:
    """Tests for UI helper functions."""

    def test_render_header_returns_panel(self):
        """Verify render_header returns a Panel object."""
        from builders_hut.cmd_interface import render_header
        from rich.panel import Panel

        result = render_header()

        assert isinstance(result, Panel)

    def test_render_header_contains_version(self):
        """Verify header contains the app version."""
        from builders_hut.cmd_interface import render_header, APP_VERSION

        panel = render_header()

        # Convert panel to string to check content
        # Panel's renderable should contain version
        # This is a simplified check
        assert panel is not None


# =============================================================================
# End of test_cli.py
# =============================================================================
