from textwrap import dedent

DEV_FILE_CONTENT = dedent("""
import uvicorn


def main():
    uvicorn.run("app.main:app", reload=True, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
""")
