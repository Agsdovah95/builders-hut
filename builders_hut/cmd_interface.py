import shutil
from pathlib import Path

from builders_hut.setups import SetupEnv, SetupFiles, SetupFileWriter, SetupStructure
from builders_hut.utils import setup_project


def interface():
    try:
        current_path = Path(__name__).resolve().parent

        current_path = Path(current_path) / "demo"

        project_location = current_path

        if project_location.exists():
            """ clear existing """
            shutil.rmtree(project_location)

        setup_to_do = [SetupStructure, SetupFiles, SetupEnv, SetupFileWriter]

        name = input("Enter project title: ").strip()
        if not name:
            name = current_path.name.split("/")[-1]

        description = input("Enter project description: ").strip()
        if not description:
            description = "A new project"

        version = input("Enter project version (default: 0.1.0): ").strip()
        if not version:
            version = "0.1.0"

        for setup in setup_to_do:
            setup_project(
                project_location,
                setup,
                name=name,
                description=description,
                version=version,
            )

        print("Project setup completed successfully.")
    except Exception as e:
        print(f"Project setup failed: {e}")
