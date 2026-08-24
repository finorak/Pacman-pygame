import sys

from codes.core.app import App


def main() -> None:
    if len(sys.argv) < 1:
        print("Pleas provde argument", file=sys.stderr)
        sys.exit(1)
    app = App(sys.argv[1], (950, 950))
    app.run()


if __name__ == "__main__":
    main()
