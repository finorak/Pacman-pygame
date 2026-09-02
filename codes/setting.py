SCREEN_SIZE = 1600, 800

NORTH: int = 0b0001
SOUTH: int = 0b0100
WEST: int = 0b1000
EAST: int = 0b0010

DIRECTION_SETTING: dict[str, dict[str, int]] = {
        "left": {
            "x": -1,
            "y": 0,
            },
        "right": {
            "x": 1,
            "y": 0,
            },
        "up": {
            "x": 0,
            "y": -1,
            },
        "down": {
            "x": 0,
            "y": 1,
            },
        }

# SUPPOSED CELL SIZE
CELL_SIZE: int = 38

TARGET_DIRECTION: dict[tuple[int, int], str] = {
        (-1, 0): "left",
        (1, 0): "right",
        (0, 1): "down",
        (0, -1): "up"
        }
