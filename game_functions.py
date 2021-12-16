import pygame
import sys
import settings
import ship
from bullet import Bullet

def check_keydown(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_rigth = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_rigth = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, ship, bullets):
    # Отслеживание событий клавы и мыши
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #Перемещение корабля вправо
        elif event.type == pygame.KEYDOWN:
            check_keydown(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup(event, ship)


def update_screen(ai_settings, screen, ship, bullets):
    # При каждом переходе цикла отрисовывается новый экран с фоном
    screen.fill(ai_settings.bg_color)
    #Все пули выводятся позади корабля и пришельцев
    for bullet in bullets:
        bullet.draw_bullet()
    ship.blitme()

    # Отображение последнего нарисованного экрана
    pygame.display.flip()