# =============================================================================
# Unit Tests for builders_hut/setups/base_setup.py
# =============================================================================
#
# LEARNING NOTE: Testing Abstract Base Classes
# --------------------------------------------
# Abstract Base Classes (ABCs) define interfaces that subclasses must implement.
# Testing ABCs is tricky because you can't instantiate them directly.
#
# Strategies:
# 1. Create a concrete subclass for testing
# 2. Verify abstract methods raise NotImplementedError (or TypeError on instantiation)
# 3. Test any concrete methods provided by the ABC
#
# =============================================================================

from pathlib import Path

import pytest

from builders_hut.setups.base_setup import BaseSetup


# =============================================================================
# Tests for BaseSetup
# =============================================================================


class TestBaseSetup:
    """Tests for the BaseSetup abstract base class."""

    def test_cannot_instantiate_directly(self):
        """
        WHAT: Verify BaseSetup cannot be instantiated directly.
        WHY: It's an abstract class with abstract method create().

        LEARNING NOTE: Abstract Classes
        --------------------------------
        When you try to instantiate an ABC that has unimplemented abstract
        methods, Python raises TypeError. This enforces the contract that
        subclasses MUST implement the abstract methods.
        """
        with pytest.raises(TypeError) as exc_info:
            BaseSetup("some/path")  # type: ignore

        # The error message should mention the abstract method
        assert "create" in str(exc_info.value).lower()

    def test_location_converted_to_path_from_string(self, temp_project_dir):
        """
        WHAT: Verify location is converted from string to Path.
        WHY: The constructor accepts both str and Path for convenience.
        """

        # Create a concrete subclass for testing
        class ConcreteSetup(BaseSetup):
            def create(self):
                pass

        # Pass a string path
        string_path = str(temp_project_dir)
        setup = ConcreteSetup(string_path)

        # Should be converted to Path
        assert isinstance(setup.location, Path)
        assert setup.location == temp_project_dir

    def test_location_preserved_when_path_object(self, temp_project_dir):
        """Verify Path object is used directly without conversion."""

        class ConcreteSetup(BaseSetup):
            def create(self):
                pass

        setup = ConcreteSetup(temp_project_dir)

        assert setup.location is temp_project_dir

    def test_configure_is_optional_hook(self, temp_project_dir):
        """
        WHAT: Verify configure() can be called without implementation.
        WHY: configure() is an optional hook, not an abstract method.

        LEARNING NOTE: Optional Hooks vs Abstract Methods
        --------------------------------------------------
        - Abstract methods (@abstractmethod) MUST be implemented by subclasses
        - Optional hooks have a default implementation (often empty/pass)
        - Subclasses can override optional hooks but don't have to
        """

        class ConcreteSetup(BaseSetup):
            def create(self):
                pass

        setup = ConcreteSetup(temp_project_dir)

        # Should not raise - configure has a default empty implementation
        setup.configure(key="value", another="param")

    def test_configure_accepts_arbitrary_kwargs(self, temp_project_dir):
        """Verify configure accepts any keyword arguments."""

        class ConcreteSetup(BaseSetup):
            def create(self):
                pass

        setup = ConcreteSetup(temp_project_dir)

        # Should accept any kwargs without error
        setup.configure(
            name="test",
            version="1.0.0",
            custom_param=123,
            nested={"key": "value"},
        )

    def test_subclass_must_implement_create(self):
        """
        WHAT: Verify subclass without create() implementation raises TypeError.
        WHY: create() is abstract and must be implemented.
        """

        class IncompleteSetup(BaseSetup):
            # Deliberately not implementing create()
            pass

        with pytest.raises(TypeError):
            IncompleteSetup("some/path")

    def test_subclass_with_create_can_be_instantiated(self, temp_project_dir):
        """Verify subclass with create() implementation can be instantiated."""

        class CompleteSetup(BaseSetup):
            def create(self):
                pass

        # Should not raise
        setup = CompleteSetup(temp_project_dir)

        assert setup.location == temp_project_dir


# =============================================================================
# End of test_base_setup.py
# =============================================================================
