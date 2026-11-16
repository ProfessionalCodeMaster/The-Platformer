import pygame

class Player:

    def __init__(self, x, y):
        self.width = 50
        self.height = 70

        self.x = x
        self.y = y

        self.max_health = 100
        self.health = self.max_health
        self.next_enemy_damage_time = 0

        # Player's movement speed
        self.speed = 5

        # Gravity
        self.velocity_y = 0
        self.gravity = 0.5

        # Player's maximum jump height
        self.jump_strength = 12

        # Player doesn't start on ground
        self.on_ground = False

        # Player's collision shape - for collision detection
        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def take_damage(self, amount):
        """Reduce health without allowing damage to heal or health below zero."""
        self.health = max(0, self.health - max(0, amount))

    # Player moves through player input
    def move(self, platforms, level_width, jump_pressed):
        keys = pygame.key.get_pressed()

        # Check whether player is standing on a platform
        self.check_on_ground(platforms)

        # Jump
        if jump_pressed and self.on_ground:
            self.velocity_y = -self.jump_strength
            self.on_ground = False

        # Move left and right
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep player inside the level
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > level_width:
            self.rect.right = level_width

        # Gravity
        self.apply_gravity()

        # Player lands on a platform
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y >= 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True

    #Makes the player jump
    def jump(self):
        if self.on_ground:
            self.velocity_y = -self.jump_strength
            self.on_ground = False

    # Makes the player fall downward
    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

    def check_on_ground(self, platforms):
        self.on_ground = False

        for platform in platforms:
            if (
                    self.rect.bottom == platform.rect.top
                    and self.rect.right > platform.rect.left
                    and self.rect.left < platform.rect.right
            ):
                self.on_ground = True
                break

    # Player is drawn as a red rectangle (Placeholder)
    def draw(self, screen, camera):
        draw_rect = self.rect.move(-camera.x, 0)

        pygame.draw.rect(
            screen,
            (255, 0, 0), # Red Color
            draw_rect
        )
