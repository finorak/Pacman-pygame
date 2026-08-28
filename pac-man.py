import sys

from codes.core import App


def main() -> None:
    if len(sys.argv) != 2:
        print("[ERROR] Invalid arguments.", file=sys.stderr)
        print(f"[USAGE] python3 {sys.argv[0]} <config>", file=sys.stderr)
        sys.exit(1)
    app = App(sys.argv[1], (950, 950))
    app.run()


if __name__ == "__main__":
    main()
