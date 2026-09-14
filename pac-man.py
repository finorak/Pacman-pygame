import sys

from codes.core.app import Rendering
from codes.setting import SCREEN_SIZE
from codes.utilities.error_handling import error_handler


@error_handler
def main() -> None:
    if len(sys.argv) != 2:
        print("[ERROR] Invalid arguments.", file=sys.stderr)
        print(f"[USAGE] python3 {sys.argv[0]} <config>", file=sys.stderr)
        sys.exit(1)
    app = Rendering(SCREEN_SIZE, sys.argv[1])
    app.run()


if __name__ == "__main__":
    main()
