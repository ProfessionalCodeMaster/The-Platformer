import pygame

class Tree:
    """A background tree that scrolls at 40% of the camera speed."""

    PARALLAX_FACTOR = 0.4 # Used for Parallax Scrolling

    def __init__(self, x, ground_y, height):
        self.x = x
        self.ground_y = ground_y
        self.height = height

    def draw(self, screen, camera):
        center_x = self.x - int(camera.x * self.PARALLAX_FACTOR)
        top = self.ground_y - self.height
        trunk_width = self.height // 8
        canopy_width = self.height * 3 // 4
        canopy_height = self.height * 3 // 5

        trunk = pygame.Rect(
            center_x - trunk_width // 2,
            top + canopy_height // 2,
            trunk_width,
            self.height - canopy_height // 2,
        )
        canopy = pygame.Rect(
            center_x - canopy_width // 2, top, canopy_width, canopy_height
        )

        pygame.draw.rect(screen, (126, 86, 58), trunk)
        pygame.draw.ellipse(screen, (64, 139, 85), canopy)
