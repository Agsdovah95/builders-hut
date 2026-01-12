import shutil
from pathlib import Path


from builders_hut.setups import SetupStructure, SetupEnv, SetupFiles, SetupFileWriter

from builders_hut.utils import setup_project


def main():
    try:
        current_path = Path(__name__).resolve().parent

        current_path = Path(current_path) / "demo"

        project_location = current_path

        if project_location.exists():
            """ clear existing """
            shutil.rmtree(project_location)

        setup_to_do = [SetupStructure, SetupFiles, SetupEnv, SetupFileWriter]

        for setup in setup_to_do:
            name = "INTest"
            description = "Lorem ipsum dolor sit amet"
            version = "0.2.0"
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


if __name__ == "__main__":
    main()
