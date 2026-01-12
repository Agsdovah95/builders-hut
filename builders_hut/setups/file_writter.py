from pathlib import Path
from builders_hut.setups.base_setup import BaseSetup
from builders_hut.setups.file_contents import DEV_FILE_CONTENT, MAIN_FILE_CONTENT


class SetupFileWriter(BaseSetup):
    FILES_TO_WRITE: dict[Path, str] = {
        Path("app/main.py"): MAIN_FILE_CONTENT,
        Path("app/scripts/dev.py"): DEV_FILE_CONTENT,
    }

    def create(self):
        self._write_files()

    def _write_files(self) -> None:
        for path, content in self.FILES_TO_WRITE.items():
            path = self.location / path
            self._write_file(path, content)

    @staticmethod
    def _write_file(path: Path, content: str) -> None:
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist")

        path.write_text(content, encoding="utf-8")
