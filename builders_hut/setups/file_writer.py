from builders_hut.setups import FILES_TO_WRITE, BaseSetup
from builders_hut.utils import write_file


class SetupFileWriter(BaseSetup):
    """
    Write data to the files created previously
    """

    def create(self):
        self._write_files()

    def _write_files(self) -> None:
        for path, content in FILES_TO_WRITE.items():
            if path.name == ".env":
                content = content.format(
                    title=self.name,
                    description=self.description,
                    version=self.version,
                    db_type=self.database_provider,
                    db_user=self.db_user,
                    db_pass=self.db_pass,
                    db_host=self.db_host,
                    db_port=self.db_port,
                    db_name=self.db_name,
                )
            path = self.location / path
            write_file(path, content)

    def configure(
        self,
        name: str,
        description: str,
        version: str,
        database_provider: str,
        db_user: str = "your_username",
        db_pass: str = "your_password",
        db_host: str = "database_host",
        db_port: str = "database_port",
        db_name: str = "database_name",
        **kwargs,
    ):
        self.name = name
        self.description = description
        self.version = version
        self.database_provider = database_provider
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
