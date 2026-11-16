import pygame
from game_platform import Platform

# This class inherits from the Platform class
class Goal(Platform):

    """A yellow platform that completes the level when landed on."""
    def draw(self, screen, camera):
        pygame.draw.rect(screen, (255, 255, 0), self.rect.move(-camera.x, 0))

    def update(self, player, previous_rect):
        """Return True for a living player landing on the top from above."""
        return (
            player.health > 0
            and player.on_ground
            and player.velocity_y >= 0
            and previous_rect.bottom <= self.rect.top
            and player.rect.bottom == self.rect.top
            and player.rect.right > self.rect.left
            and player.rect.left < self.rect.right
        )
