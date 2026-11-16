import pygame

class HealthBar:

    """Draw the player's health as a red rectangle on the screen."""
    def __init__(self, x, y, width=280, height=40, max_health=100):
        if max_health <= 0:
            raise ValueError("max_health must be greater than zero")

        self.rect = pygame.Rect(x, y, width, height)
        self.max_health = max_health
        self.health = max_health

    def update(self, health):

        """Set the current health, keeping it within the allowed range."""
        self.health = max(0, min(health, self.max_health))

    def draw(self, screen):

        """Draw a red bar whose width represents the remaining health."""
        health_rect = self.rect.copy()
        health_rect.width = int(self.rect.width * self.health / self.max_health)

        if health_rect.width > 0:
            pygame.draw.rect(screen, (255, 0, 0), health_rect)
