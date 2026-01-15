from textwrap import dedent

ENV_FILE_CONTENT = dedent("""
TITLE="{title}"
DESCRIPTION="{description}"
VERSION="{version}"
DEBUG=True
PORT=8000
HOST="0.0.0.0"
""")
