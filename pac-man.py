import sys

from codes.core.app import Rendering
from codes.setting import SCREEN_SIZE


def main() -> None:
    if len(sys.argv) != 2:
        print("[ERROR] Invalid arguments.", file=sys.stderr)
        print(f"[USAGE] python3 {sys.argv[0]} <config>", file=sys.stderr)
        sys.exit(1)
    app = Rendering(SCREEN_SIZE)
    app.run()


if __name__ == "__main__":
    main()
