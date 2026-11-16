import pygame

class Spikes:

    """A row of upward-pointing spikes, lethal when a player touches a tip."""
    def __init__(self, x, y, count, spike_width=25, height=50):
        """Place count triangles at (x, y), where y is the row's base."""
        if not isinstance(count, int) or count < 0:
            raise ValueError("count must be a non-negative integer")
        if spike_width <= 0 or height <= 0:
            raise ValueError("Spike width and height must be positive")
        self.x = x
        self.y = y
        self.count = count
        self.spike_width = spike_width
        self.height = height

    def draw(self, screen, camera, count=None):
        """Draw the given number of triangles; default to this row's count."""
        if count is not None:
            if not isinstance(count, int) or count < 0:
                raise ValueError("count must be a non-negative integer")
            self.count = count

        for index in range(self.count):
            left = self.x + index * self.spike_width - camera.x
            pygame.draw.polygon(screen, (128, 128, 128), [
                (left, self.y),
                (left + self.spike_width // 2, self.y - self.height),
                (left + self.spike_width, self.y),
            ])

    def update(self, player, previous_rect=None):
        """Kill on tip contact, including a fall that crosses a tip this frame."""
        tip_y = self.y - self.height
        for index in range(self.count):
            tip_x = self.x + index * self.spike_width + self.spike_width // 2
            horizontally_touching = player.rect.left <= tip_x <= player.rect.right
            touching = player.rect.top <= tip_y <= player.rect.bottom
            crossed = (
                previous_rect is not None
                and previous_rect.bottom <= tip_y <= player.rect.bottom
            )
            if horizontally_touching and (touching or crossed):
                player.take_damage(player.health)
                return
