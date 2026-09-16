"""Program entry point module."""

import sys

from codes import Rendering
from codes.setting import SCREEN_SIZE
from codes.utilities.error_handling import error_handler


@error_handler
def main() -> None:
    """Program entry point.

    This function is used as the entry point of our implementation.
    """
    if len(sys.argv) != 2:
        print("[ERROR] Invalid arguments.", file=sys.stderr)
        print(f"[USAGE] python3 {sys.argv[0]} <config>", file=sys.stderr)
        sys.exit(1)
    app = Rendering(SCREEN_SIZE, sys.argv[1])
    app.run()


if __name__ == "__main__":
    main()
