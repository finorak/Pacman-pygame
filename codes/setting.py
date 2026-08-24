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
CELL_SIZE: int = 50
