import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group


def run_game():

    # Создает объект экрана и запускает игру
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_hight)
    )
    pygame.display.set_caption("Alien Invasion")

    # Вывод коробля на экран
    ship = Ship(screen, ai_settings)

    # Создание группы для хранения пуль и пришельцев
    bullets = Group()
    aliens = Group()

    # Создание флота пришельцев
    gf.create_fleet(ai_settings, screen, aliens)

    # Запуск основного цикла игры
    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullet(bullets)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)

run_game()
