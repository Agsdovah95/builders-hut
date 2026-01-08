import shutil
from pathlib import Path


from builders_hut.setups.files_setup import SetupFiles
from builders_hut.setups.structure_setup import SetupStructure
from builders_hut.setups.base_setup import BaseSetup
from builders_hut.setups.env_setup import EnvSetup


def setup_project(location: Path, setup_cls: type[BaseSetup], **config) -> None:
    """Setup the project."""
    setup = setup_cls(location)
    setup.configure(**config)
    setup.create()


if __name__ == "__main__":
    try:
        project_location = (
            "C:/Users/User/OneDrive/Documents/work/personal/builders-hut/demo"
        )

        project_location = Path(project_location)

        if project_location.exists():
            shutil.rmtree(project_location)

        setup_to_do = [SetupStructure, SetupFiles, EnvSetup]

        for setup in setup_to_do:
            setup_project(project_location, setup, package_manager="uv")

        print("Project setup completed successfully.")
    except Exception as e:
        print(f"Project setup failed: {e}")
