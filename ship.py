import pygame


class Ship:

    def __init__(self, screen, ai_settings):

        # Inicialization ship and start position
        self.screen = screen

        # Image download
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Every new ship startet in
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.ai_settings = ai_settings
        self.center = float(self.rect.centerx)

        # Флаг перемещения
        self.moving_rigth = False
        self.moving_left = False

    def update(self):

        # Обновляет позицию корабля с учетом флага
        # Обновляет атрибут center, не rect
        if self.moving_rigth and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Обновление атрибута rect.centerx
        self.rect.centerx = self.center

    def blitme(self):

        # Рисует корабль на текущей позиции
        self.screen.blit(self.image, self.rect)
