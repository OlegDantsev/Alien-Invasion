import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


def run_game():

    # Создает объект экрана и запускает игру
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    # Создание кнопки play
    play_button = Button(ai_settings, screen, "Play")

    # Вывод коробля на экран
    ship = Ship(screen, ai_settings)

    # Создание группы для хранения пуль и пришельцев
    bullets = Group()
    aliens = Group()

    # Создание флота пришельцев
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # Создание экземпляра GameStats и ScoreBoard
    stats = GameStats(ai_settings)
    sb = ScoreBoard(ai_settings, screen, stats)

    # Запуск основного цикла игры
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                         play_button)

        if stats.game_active:
            ship.update()
            gf.update_bullet(ai_settings, screen, stats, sb, ship, aliens,
                             bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

run_game()
