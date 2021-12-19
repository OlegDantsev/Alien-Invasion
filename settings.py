class Settings:

    # Class foe keeping settings

    def __init__(self):

        # Inicializing game setting
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Настройки корабля
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Параметры пули
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 7

        # Параметры пришельцев
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 100
        # fleet_direction = 1 обозначает движение вправо, а -1 влево
        self.fleet_direction = 1
