class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in an active state
        self.game_active = False

        # High score should never be reset
        with open(self.settings.all_time_high_score_file) as file:
            self.high_score = int(file.readline())

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = 3
        self.score = 0
        self.destroyed_fleets = 0
        self.level = 1

    def write_high_score(self, new_score):
        """Writes the new all time high score into file"""
        with open(self.settings.all_time_high_score_file, "w") as file:
            file.write(new_score)