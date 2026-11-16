class Camera:
    def __init__(self, screen_width, level_width):

        # Camera's initial position
        self.screen_width = screen_width
        self.level_width = level_width
        self.x = 0

        # Camera starts scrolling when player reaches
        # 70% of the screen width
        self.left_follow_point = int(screen_width * 0.3)
        self.right_follow_point = int(screen_width * 0.7)

    # Update camera's position
    def update(self, player):

        # Player's position relative to the camera
        player_screen_x = player.rect.centerx - self.x

        # Follow player to the right
        if player_screen_x > self.right_follow_point:
            self.x = player.rect.centerx - self.right_follow_point

        # Follow player to the left
        elif player_screen_x < self.left_follow_point:
            self.x = player.rect.centerx - self.left_follow_point

        # Stop camera at beginning of level
        if self.x < 0:
            self.x = 0

        # Stop camera at end of level
        max_camera_x = self.level_width - self.screen_width

        if self.x > max_camera_x:
            self.x = max_camera_x