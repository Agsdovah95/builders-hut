from textwrap import dedent

ENV_FILE_CONTENT = dedent("""
# IMPORTANT: Change these values before deployment

# Project
TITLE="{title}"
DESCRIPTION="{description}"
VERSION="{version}"

# Debugging
DEBUG=True

# Server
PORT=8000
HOST="0.0.0.0"

# Database
DB_USER="{db_user}"
DB_PASS="{db_pass}"
DB_HOST="{db_host}"
DB_PORT={db_port}
DB_NAME="{db_name}"
DB_TYPE="{db_type}"
""")
