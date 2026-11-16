import pygame

class Platform:

    """A green platform and floor in the game."""
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, camera):
        draw_rect = self.rect.move(-camera.x, 0)

        pygame.draw.rect(
            screen,
            (50, 180, 70),
            draw_rect
        )