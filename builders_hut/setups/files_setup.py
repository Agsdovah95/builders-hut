from builders_hut.setups.base_setup import BaseSetup
from rich import print

FILES_TO_CREATE = [
    # Main application file
    "app/main.py",
    # Core configuration and logger files
    "app/core/config.py",
    "app/core/logger.py",
    # __init__.py files for package initialization
    "app/models/__init__.py",
    "app/schemas/__init__.py",
    "app/services/__init__.py",
    "app/repositories/__init__.py",
    "app/utils/__init__.py",
    "app/database/__init__.py",
    "app/workers/__init__.py",
    "app/api/__init__.py",
    # Test initialization file
    "tests/__init__.py",
    # Script files
    "scripts/dev.py",
    "scripts/prod.py",
]


class SetupFiles(BaseSetup):
    """Setup all the required files for the project."""

    def create(self):
        for file_path in FILES_TO_CREATE:
            full_path = self.location / file_path
            full_path.touch(exist_ok=True)
            print(f"[bold green]Created file:[/bold green] {file_path.split('/')[-1]}")
