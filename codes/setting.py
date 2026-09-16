SCREEN_SIZE: tuple[int, int] = 1280, 720
CURRENT_SCREEN_PADDING: tuple[int, int] = 60, 5

# SUPPOSED CELL SIZE
CELL_SIZE: int = 32
GUM_PADDING: int = 2
CELL_PADDING: int = 3
PLAYER_PADDING: int = 2

GHOST_ESCAPE_TIME: int = 10  # second
RADIUS_UPGRAD_PER_LEVEL: int = 5
SUPER_GUM_COUNT: int = 4

BACKGROUND_SPEED: int = 20
FPS: int = 60

TARGET_DIRECTION: dict[tuple[int, int], str] = {
    (-1, 0): "left",
    (1, 0): "right",
    (0, 1): "down",
    (0, -1): "up",
}

DIRECTION: dict[str, tuple[int, int]] = {
    "E": (1, 0),
    "W": (-1, 0),
    "N": (0, -1),
    "S": (0, 1),
}

GHOST_START_SETTING: dict[str, dict[str, tuple[int, int]]] = {
    "blue": {"coord": (0, 0)},
    "yellow": {"coord": (18, 0)},
    "pink": {"coord": (0, 18)},
    "red": {"coord": (18, 18)},
}

UP: int = 0b0001
RIGHT: int = 0b0010
DOWN: int = 0b0100
LEFT: int = 0b1000

DIR_VEC: dict[str, tuple[int, int]] = {
    "up": (0, -1),
    "right": (1, 0),
    "down": (0, 1),
    "left": (-1, 0),
}

DIR_BIT: dict[str, int] = {
    "up": UP,
    "right": RIGHT,
    "down": DOWN,
    "left": LEFT,
}

OPPOSITE: dict[str, str] = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
}
