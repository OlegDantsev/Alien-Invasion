import pygame
import sys
from bullet import Bullet
from alien import Alien


def check_keydown(event, ai_settings, screen, ship, bullets):

    if event.key == pygame.K_RIGHT:
        ship.moving_rigth = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):

    # Создание новой пули и ограничение количества пуль
    if len(bullets) < ai_settings.bullets_allowed:
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

        # Перемещение корабля вправо
        elif event.type == pygame.KEYDOWN:
            check_keydown(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup(event, ship)


def update_screen(ai_settings, screen, ship, aliens, bullets):

    # При каждом переходе цикла отрисовывается новый экран с фоном
    screen.fill(ai_settings.bg_color)

    # Все пули выводятся позади корабля и пришельцев
    for bullet in bullets:
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Отображение последнего нарисованного экрана
    pygame.display.flip()


def update_bullet(bullets):

    # Обновляет позицию пуль и уничтожает старые пули
    bullets.update()

    # Удаление пуль вышедших за пределы экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def get_number_aliens_x(ai_settings, alien_width):

    # Вычисление количества пришельцев в ряду
    avaliable_space_x = int(ai_settings.screen_width - 2 * alien_width)
    number_aliens_x = int(avaliable_space_x / (2 * alien_width))

    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number):

    # Создает пришельца и размещает его в ряду
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width

    # Создание первого ряда пришельцев
    # Создание пришельца и его размещение в ряду
    alien = Alien(ai_settings, screen)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    aliens.add(alien)

def create_fleet(ai_settings, screen, aliens):

    # Создает флот пришельцев
    # Создание пришельца и вычисление количества пришельцев в одном ряду
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)

    # Создание первого ряда
    for alien_number in range(number_aliens_x):
        create_alien(ai_settings, screen, aliens, alien_number)