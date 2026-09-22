"""Module that contains the frect class for the rendering."""


class Frect:
    """Rectangular class like the one that pygame has."""

    def __init__(
        self,
        pos_x: float = 0.0,
        pos_y: float = 0.0,
        width: float = 0.0,
        height: float = 0.0,
    ) -> None:
        """
        Everything starts here.

        Args:
            pos_x (float): The position x of the rect.
            pos_y (float): The position y of the rect.
            width (float): The width of the rect.
            height (float): The height of the rect.
        """
        self.x = float(pos_x)
        self.y = float(pos_y)
        self.width = float(width)
        self.height = float(height)

    def copy(self) -> "Frect":
        """Create a copy of the rect."""
        return Frect(self.x, self.y, self.width, self.height)

    @property
    def size(self) -> tuple[float, float]:
        """
        Get the size of the rect.

        Returns:
            tuple: The width, height of the rect.
        """
        return self.width, self.height

    @size.setter
    def size(self, size: tuple[float, float]) -> None:
        """
        Get the size of the rect.

        Args:
            size (tuple[float, float]): The width, height of the rect.
        """
        self.width, self.height = float(size[0]), float(size[1])

    @property
    def pos(self) -> tuple[float, float]:
        """
        Get the position of the rect.

        Returns:
            tuple: The position x, y of the rect.
        """
        return self.x, self.y

    @pos.setter
    def pos(self, pos: tuple[float, float]) -> None:
        """
        Set the position of the rect.

        Args:
            pos(tuple): The position x, y of the rect.
        """
        self.x, self.y = float(pos[0]), float(pos[1])

    @property
    def left(self) -> float:
        """
        Get the left position of the rect.

        Returns:
            float: The left pos of the rect.
        """
        return self.x

    @left.setter
    def left(self, value: float) -> None:
        """
        Set the left position of the rect.

        Args:
            value(float): The left pos of the rect.
        """
        self.x = float(value)

    @property
    def right(self) -> float:
        """
        Get the right position of the rect.

        Returns:
            float: The right pos of the rect.
        """
        return self.x + self.width

    @right.setter
    def right(self, value: float) -> None:
        """
        Set the right position of the rect.

        Args:
            value(float): The right pos of the rect.
        """
        self.x = float(value) - self.width

    @property
    def top(self) -> float:
        """
        Get the top position of the rect.

        Returns:
            float: The top pos of the rect.
        """
        return self.y

    @top.setter
    def top(self, value: float) -> None:
        """
        Set the top position of the rect.

        Args:
            value(float): The top pos of the rect.
        """
        self.y = float(value)

    @property
    def bottom(self) -> float:
        """
        Get the bottom position of the rect.

        Returns:
            float: The bottom pos of the rect.
        """
        return self.y + self.height

    @bottom.setter
    def bottom(self, value: float) -> None:
        """
        Set the bottom position of the rect.

        Args:
            value(float): The bottom pos of the rect.
        """
        self.y = float(value) - self.height

    @property
    def centerx(self) -> float:
        """
        Get the center pos x position of the rect.

        Returns:
            float: The center pos x pos of the rect.
        """
        return self.x + self.width / 2.0

    @centerx.setter
    def centerx(self, value: float) -> None:
        """
        Set the centerx position of the rect.

        Args:
            value(float): The centerx pos of the rect.
        """
        self.x = float(value) - self.width / 2.0

    @property
    def centery(self) -> float:
        """
        Get the center pos y position of the rect.

        Returns:
            float: The center pos y pos of the rect.
        """
        return self.y + self.height / 2.0

    @centery.setter
    def centery(self, value: float) -> None:
        """
        Set the centery position of the rect.

        Args:
            value(float): The centery pos of the rect.
        """
        self.y = float(value) - self.height / 2.0

    @property
    def center(self) -> tuple[float, float]:
        """
        Get the center position of the rect.

        Returns:
            tuple: The center of the rect.
        """
        return self.centerx, self.centery

    @center.setter
    def center(self, value: tuple[float, float]) -> None:
        """
        Set the center of the rect.

        Args:
            value (tuple[float, float]): the center of the rect.
        """
        self.centerx, self.centery = float(value[0]), float(value[1])

    @property
    def topleft(self) -> tuple[float, float]:
        """
        Get the topleft position of the rect.

        Returns:
            tuple: The topleft of the rect.
        """
        return self.left, self.top

    @topleft.setter
    def topleft(self, value: tuple[float, float]) -> None:
        """
        Set the topleft of the rect.

        Args:
            value (tuple[float, float]): the topleft of the rect.
        """
        self.left, self.top = float(value[0]), float(value[1])

    @property
    def bottomright(self) -> tuple[float, float]:
        """
        Get the bottomright position of the rect.

        Returns:
            tuple: The bottomright of the rect.
        """
        return self.right, self.bottom

    @bottomright.setter
    def bottomright(self, value: tuple[float, float]) -> None:
        """
        Set the bottomright of the rect.

        Args:
            value (tuple[float, float]): the bottomright of the rect.
        """
        self.right, self.bottom = float(value[0]), float(value[1])

    def collidepoint(self, pos: tuple[float, float]) -> bool:
        """
        Check if the point is in the rect.

        Args:
            pos (tuple[float, float]): The position of the point.
        Returns:
            bool: True if it collides.
        """
        px, py = pos
        return self.left <= px < self.right and self.top <= py < self.bottom
