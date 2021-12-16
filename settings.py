class Settings:
    # Class foe keeping settings

    def __init__(self):
        # Inicializing game setting
        # Screen settings
        self.screen_width = 1200
        self.screen_hight = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed_factor = 1.5

        # Параметры пули
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
