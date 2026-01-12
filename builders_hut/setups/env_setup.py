import subprocess
from rich import print

from builders_hut.setups.base_setup import BaseSetup
from builders_hut.utils import get_platform, write_pyproject

PACKAGES = [
    "fastapi",
    "python-dotenv",
    "email-validator",
    "tzdata",
    "pydantic-settings",
    "scalar-fastapi",
    "uvicorn",
    "jinja2"
]

DEV_PACKAGES = ["pytest"]


class SetupEnv(BaseSetup):
    """Create Env and Install Base Packages"""

    def create(self):
        try:
            platform = get_platform()

            print(
                f"Working On: [bold green]{platform[0].upper()}{platform[1:]}[/bold green]"
            )

            print(f"Working Directory: {self.location}")

            print("Updating pyproject file...")

            write_pyproject(
                path=(self.location / "pyproject.toml"),
                name=self.name,
                description=self.description,
                version=self.version,
                dependencies=PACKAGES,
                dev_dependencies=DEV_PACKAGES,
            )

            print("Creating Environment...")

            subprocess.run(
                "python -m venv .venv",
                cwd=self.location,
                shell=True,
                check=True,
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
            )

            print("Installing Packages...")

            command = "pip install -e ."
            python_file = (
                ".venv/bin/python -m"
                if platform == "linux"
                else ".venv\\Scripts\\python.exe -m"
            )

            full_command = f"{python_file} {command}"

            subprocess.run(
                full_command,
                cwd=self.location,
                shell=True,
                check=True,
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
            )

            print("[bold green]Done [/bold green]")

        except Exception as e:
            print(str(e))
            raise RuntimeError("Failed to create environment") from e

    def configure(self, name: str, description: str, version: str):
        self.name = name
        self.description = description
        self.version = version
