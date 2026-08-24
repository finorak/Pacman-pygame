NORTH = 0b0001
SOUTH = 0b0100
WEST = 0b1000
EAST = 0b0010

PLAYER_SPEED: int = 480

PLAYER_FRAME_SETTING: dict[str, dict[str, int]] = {
        "left": {
            "x": -1,
            "y": 0,
            "speed_x": -PLAYER_SPEED,
            "speed_y": 0,
            },
        "right": {
            "x": 1,
            "y": 0,
            "speed_x": PLAYER_SPEED,
            "speed_y": 0,
            },
        "up": {
            "x": 0,
            "y": -1,
            "speed_x": 0,
            "speed_y": -PLAYER_SPEED,
            },
        "down": {
            "x": 0,
            "y": 1,
            "speed_x": 0,
            "speed_y": PLAYER_SPEED,
            },
        }
