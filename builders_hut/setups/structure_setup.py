from builders_hut.setups.base_setup import BaseSetup
from rich import print

# Define all necessary directories for the project structure
ALL_DIRS = [
    "api",
    "database",
    "schemas",
    "services",
    "repositories",
    "core",
    "models",
    "workers",
    "utils",
]


class SetupStructure(BaseSetup):
    """Setup all the required directory structure for the project."""

    def create(self):
        print(
            f"[bold green]Creating directory structure at:[/bold green] {self.location}"
        )
        (self.location / "tests").mkdir(exist_ok=True, parents=True)
        print("[bold green]Created 'tests' directory.[/bold green]")
        (self.location / "app").mkdir(exist_ok=True, parents=True)
        print("[bold green]Created 'app' directory.[/bold green]")
        (self.location / "scripts").mkdir(exist_ok=True, parents=True)
        print("[bold green]Created 'scripts' directory inside 'app'.[/bold green]")
        for dir_name in ALL_DIRS:
            (self.location / "app" / dir_name).mkdir(exist_ok=True, parents=True)
            print(
                f"[bold green]Created '{dir_name}' directory inside 'app'.[/bold green]"
            )
