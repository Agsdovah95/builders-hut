from builders_hut.cmd_interface import interface


def main():
    try:
        interface()
    except Exception as e:
        print(f"Project setup failed: {e}")


if __name__ == "__main__":
    main()
