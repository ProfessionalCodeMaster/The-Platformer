import pygame
from player import Player
from game_platform import Platform
from camera import Camera
from health_bar import HealthBar
from enemy import Enemy
from spikes import Spikes
from goal import Goal
from tree import Tree
from cloud import Cloud

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

LEVEL_WIDTH = 3000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Platformer")

clock = pygame.time.Clock()

# Fill the level with floating platforms, including the small platform, and the ground.
small_platform = Platform(2350, 400, 100, 30)

platforms = [
    Platform(0, 550, LEVEL_WIDTH, 50),  # Ground
    Platform(300, 450, 200, 30),
    Platform(700, 400, 200, 30),
    Platform(1100, 350, 200, 30),
    Platform(1500, 450, 250, 30),
    Platform(1950, 350, 200, 30),
    small_platform,
    Platform(2650, 350, 200, 30),
]

# Fill the ground gaps between neighboring floating platforms with spikes.
spikes = [
    Spikes(left.rect.right, platforms[0].rect.top,
           (right.rect.left - left.rect.right) // 25)
    for left, right in zip(platforms[1:], platforms[2:])
]

# Fill the sky with clouds.
clouds = [
    Cloud(75, 105, 145),
    Cloud(330, 65, 185),
    Cloud(645, 135, 130),
    Cloud(875, 80, 175),
    Cloud(1165, 115, 155),
    Cloud(1370, 55, 165),
]

# Fill the background with trees.
trees = [
    Tree(x, platforms[0].rect.top, height * 115 // 100)
    for x, height in (
        (40, 165), (205, 200), (385, 155), (555, 215), (740, 175),
        (910, 195), (1090, 155), (1255, 205), (1440, 170), (1620, 215),
        (1790, 180),
    )
]

# Place the goal at the end of a level.
goal = Goal(LEVEL_WIDTH - 125, platforms[0].rect.top - 20, 100, 20)
# Keep the goal separate from the floating platforms used to place hazards.
landing_platforms = [goal] + platforms

def new_game():
    """Create fresh player, health bar, camera, and enemies for a new run."""
    new_player = Player(100, 400)
    new_health_bar = HealthBar(20, 20, max_health=new_player.max_health)
    new_camera = Camera(SCREEN_WIDTH, LEVEL_WIDTH)
    new_enemies = [
        Enemy(spawn_platform.rect.centerx - 15, spawn_platform.rect.top - 30, spawn_platform)
        for spawn_platform in platforms[1:]
        if spawn_platform is not small_platform
    ]
    return new_player, new_health_bar, new_camera, new_enemies


player, health_bar, camera, enemies = new_game()
game_over = False
level_won = False

# All the game fonts and buttons
title_font = pygame.font.Font(None, 80)
button_font = pygame.font.Font(None, 36)
game_over_text = title_font.render("Game Over", True, (255, 255, 255))
restart_text = button_font.render("Press R to Restart", True, (255, 255, 255))
win_text = title_font.render("You Win!", True, (255, 255, 0))
play_again_text = button_font.render("Press P to Play Again", True, (255, 255, 255))
restart_button = pygame.Rect(0, 0, restart_text.get_width() + 40, 60)
restart_button.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
play_again_button = pygame.Rect(0, 0, play_again_text.get_width() + 40, 60)
play_again_button.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
overlay.fill((0, 0, 0, 180))

running = True

while running:

    jump_pressed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue

        if game_over or level_won:
            active_button = play_again_button if level_won else restart_button
            restart_key = pygame.K_p if level_won else pygame.K_r
            restart_pressed = event.type == pygame.KEYDOWN and event.key == restart_key
            restart_clicked = (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and active_button.collidepoint(event.pos)
            )
            if restart_pressed or restart_clicked:
                player, health_bar, camera, enemies = new_game()
                game_over = False
                level_won = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    if not running:
        break

    if not game_over and not level_won:
        previous_player_rect = player.rect.copy()
        player.move(landing_platforms, LEVEL_WIDTH, jump_pressed)

        for enemy in enemies:
            enemy.update(player)

        for spike_row in spikes:
            spike_row.update(player, previous_player_rect)

        camera.update(player)
        game_over = player.health <= 0
        level_won = goal.update(player, previous_player_rect)

    screen.fill((100, 180, 255)) # Sky Blue Color

    for cloud in clouds:
        cloud.draw(screen, camera)

    for tree in trees:
        tree.draw(screen, camera)

    for platform in platforms:
        platform.draw(screen, camera)
    goal.draw(screen, camera)

    for spike_row in spikes:
        spike_row.draw(screen, camera)

    player.draw(screen, camera)
    for enemy in enemies:
        enemy.draw(screen, camera)

    health_bar.update(player.health)
    health_bar.draw(screen)

    if game_over or level_won:
        screen.blit(overlay, (0, 0))
        result_text = win_text if level_won else game_over_text
        action_text = play_again_text if level_won else restart_text
        active_button = play_again_button if level_won else restart_button
        screen.blit(result_text, result_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
        ))
        button_color = (100, 100, 100) if active_button.collidepoint(
            pygame.mouse.get_pos()
        ) else (65, 65, 65)
        pygame.draw.rect(screen, button_color, active_button)
        screen.blit(action_text, action_text.get_rect(center=active_button.center))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
