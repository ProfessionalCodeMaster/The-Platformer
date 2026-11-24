import pygame

class Cloud:
    """A white cloud that scrolls at 20% of the camera speed."""

    PARALLAX_FACTOR = 0.2 # Used for Parallax Scrolling

    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width

    def draw(self, screen, camera):
        x = self.x - int(camera.x * self.PARALLAX_FACTOR)
        y = self.y
        width = self.width
        white = (255, 255, 255)

        pygame.draw.ellipse(screen, white, (x, y + width // 5, width, width // 4))
        pygame.draw.ellipse(screen, white, (x + width // 6, y + width // 10, width // 3, width // 3))
        pygame.draw.ellipse(screen, white, (x + width // 3, y, width // 2, width * 2 // 5))
