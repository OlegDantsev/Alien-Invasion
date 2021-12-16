import pygame
import sys
import settings
import ship


def check_keydown(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_rigth = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True


def check_keyup(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_rigth = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ship):
    # Отслеживание событий клавы и мыши
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #Перемещение корабля вправо
        elif event.type == pygame.KEYDOWN:
            check_keydown(event, ship)
        elif event.type == pygame.KEYUP:
            check_keyup(event, ship)


def update_screen(ai_settings, screen, ship):
    # При каждом переходе цикла отрисовывается новый экран с фоном
    screen.fill(ai_settings.bg_color)
    ship.blitme()

    # Отображение последнего нарисованного экрана
    pygame.display.flip()