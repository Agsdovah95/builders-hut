from builders_hut.setups.base_setup import BaseSetup
import subprocess


class EnvSetup(BaseSetup):
    def create(self):
        if self.package_manager == "pip":
            subprocess.run(["python", "-m", "venv", "env"], cwd=self.location)

    def configure(self, package_manager="pip", **_):
        self.package_manager = package_manager
