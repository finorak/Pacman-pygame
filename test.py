import pygame


class Pacman:
    def __init__(self, x, y, speed=2):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = (1, 0)  # Current moving direction
        self.next_direction = (1, 0)  # Queued direction change
        self.radius = 10

    def set_next_direction(self, keys):
        """Queue direction changes from user input"""
        if keys[pygame.K_UP]:
            self.next_direction = (0, -1)
        elif keys[pygame.K_DOWN]:
            self.next_direction = (0, 1)
        elif keys[pygame.K_LEFT]:
            self.next_direction = (-1, 0)
        elif keys[pygame.K_RIGHT]:
            self.next_direction = (1, 0)

    def update(self, maze, grid_size=20):
        """Update position and handle collisions"""
        # Try to move in queued direction
        if self.can_move(self.next_direction, maze, grid_size):
            self.direction = self.next_direction

        # Move in current direction
        if self.can_move(self.direction, maze, grid_size):
            self.x += self.direction[0] * self.speed
            self.y += self.direction[1] * self.speed

    def can_move(self, direction, maze, grid_size):
        """Check if next position is valid (not a wall)"""
        next_x = self.x + direction[0] * self.speed
        next_y = self.y + direction[1] * self.speed

        grid_x = next_x // grid_size
        grid_y = next_y // grid_size

        return (
            0 <= grid_x < len(maze[0])
            and 0 <= grid_y < len(maze)
            and maze[grid_y][grid_x] != 1
        )

    def draw(self, surface):
        """Draw Pacman circle"""
        pygame.draw.circle(
            surface, (255, 255, 0), (int(self.x), int(self.y)), self.radius
        )

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
# Main game loop
pacman = Pacman(100, 100)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    pacman.set_next_direction(keys)
    pacman.update([
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1]
    ])
    pacman.draw(screen)

    pygame.display.flip()
