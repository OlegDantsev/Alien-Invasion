class GameStats:

    # отслеживание статистики для игры
    def __init__(self, ai_settings):

        # Инициализирует статистику
        self.ai_settings = ai_settings
        self.reset_stats()

        # Игра запускается в активном состоянии
        self.game_active = False

    def reset_stats(self):

        # Инициализирует статистику, мееняющуюся в ходе игры
        self.ship_left = self.ai_settings.ship_limit
