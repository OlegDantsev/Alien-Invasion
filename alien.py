import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    # Класс создающий одного пришельца

    def __init__(self, ai_settings, screen):

        # Инициализирует пришельца и задает его начальное положение
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображение и определение атрибута rect
        self.image = pygame.image.load('images/alien_1.bmp')
        self.rect = self.image.get_rect()

        # Каждый новый пришелец появляется в верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение позиции пришельца в float
        self.x = float(self.rect.x)

    def blitme(self):
        # Выводит пришельца в текущем положении
        self.screen.blit(self.image, self.rect)
