class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 5

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.queen_bullet_color = (255, 0, 0)
        self.queen_bullet_speed = 1.5
        self.queen_bullet_fire_time = 1000

        # Alien settings
        self.fleet_drop_speed = 10
        self.super_alien_chance = 0.1
        self.queen_alien_chance = 0.25

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed = 0.75
        self.bullet_speed = 1.5
        self.bullets_allowed = 3
        self.alien_speed = 0.5
        self.fleet_direction = 1  # 1: represents right; -1 represents left

        # Scoring
        self.alien_points = 50
        self.super_alien_points = 150
        self.queen_alien_points = 500

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self. speedup_scale
        self.alien_points = int(self.score_scale * self.alien_points)
        self.super_alien_points = int(self.score_scale * self.super_alien_points)
        self.queen_alien_points = int(self.score_scale * self.queen_alien_points)
