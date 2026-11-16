import pygame

class Enemy:

    """A gray square that patrols its platform and damages the player."""
    def __init__(self, x, y, platform, size=30, damage=10, speed=2):
        if platform.rect.width < size:
            raise ValueError("The platform must be wide enough for the enemy")

        self.rect = pygame.Rect(x, y, size, size)
        self.platform = platform
        self.rect.bottom = platform.rect.top
        self.rect.x = max(platform.rect.left, min(self.rect.x, platform.rect.right - size))
        self.speed = speed  # Pixels per frame, matching the player's movement.
        self.direction = 1
        self.damage = damage
        self.damage_cooldown = 750  # Milliseconds between contact hits.

    def update(self, player):

        """Patrol without crossing platform edges, then apply contact damage."""
        self.rect.x += self.speed * self.direction

        if self.rect.right >= self.platform.rect.right:
            self.rect.right = self.platform.rect.right
            self.direction = -1
        elif self.rect.left <= self.platform.rect.left:
            self.rect.left = self.platform.rect.left
            self.direction = 1

        now = pygame.time.get_ticks()
        if (
            self.rect.colliderect(player.rect)
            and player.health > 0
            and now >= player.next_enemy_damage_time
        ):
            player.take_damage(self.damage)
            player.next_enemy_damage_time = now + self.damage_cooldown

    def draw(self, screen, camera):
        draw_rect = self.rect.move(-camera.x, 0)
        pygame.draw.rect(screen, (128, 128, 128), draw_rect)
