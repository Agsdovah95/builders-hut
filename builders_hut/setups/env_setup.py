from builders_hut.setups.base_setup import BaseSetup
import subprocess


class EnvSetup(BaseSetup):
    PACKAGE_MANAGERS = {
        "pip": "python -m venv env",
        "uv": "uv init",
        "poetry": "poetry init --no-interaction",
    }

    def create(self):
        try:
            subprocess.run(
                self.PACKAGE_MANAGERS[self.package_manager],
                cwd=self.location,
                shell=True,
                check=True,
            )
        except KeyError:
            raise ValueError(
                f"Unsupported package manager: {self.package_manager}"
            ) from None

        except Exception as e:
            raise RuntimeError(
                f"Failed to create environment with {self.package_manager}"
            ) from e

    def configure(self, package_manager="pip", **_):
        self.package_manager = package_manager
