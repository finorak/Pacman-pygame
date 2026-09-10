SCREEN_SIZE = 1280, 720

NORTH: int = 0b0001
SOUTH: int = 0b0100
WEST: int = 0b1000
EAST: int = 0b0010

# SUPPOSED CELL SIZE
CELL_SIZE: int = 34
GUM_PADDING: int = 2

GHOST_ESCAPE_TIME: int = 30 # second
RADIUS_UPGRAD_PER_LEVEL: int = 5

TARGET_DIRECTION: dict[tuple[int, int], str] = {
    (-1, 0): "left",
    (1, 0): "right",
    (0, 1): "down",
    (0, -1): "up",
}

GHOST_START_SETTING: dict[tuple[int, int], str] = {
        (18, 18): "red",
        (0, 0): "blue",
        (18, 0): "yello",
        (0, 18): "pink"
        }
