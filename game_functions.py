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


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):

    # Проверка попаданий в пришельцев
    # При обнаружении попадания удалить пулю
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # Проверка того, что флот пришельцев уничтожен и создание нового
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def update_bullet(ai_settings, screen, ship, aliens, bullets):

    # Обновляет позицию пуль и уничтожает старые пули
    bullets.update()

    # Удаление пуль вышедших за пределы экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)


def get_number_aliens_x(ai_settings, alien_width):

    # Вычисление количества пришельцев в ряду
    avaliable_space_x = int(ai_settings.screen_width - 2 * alien_width)
    number_aliens_x = int(avaliable_space_x / (2 * alien_width))

    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):

    # Определяет количество рядов
    available_space_y = (ai_settings.screen_height -
                         (10 * alien_height - ship_height))
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):

    # Создает пришельца и размещает его в ряду
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width

    # Создание первого ряда пришельцев
    # Создание пришельца и его размещение в ряду
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):

    # Создает флот пришельцев
    # Создание пришельца и вычисление количества пришельцев в одном ряду
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # Создание флота пришельцев
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)


def check_fleet_edges(ai_settings, aliens):

    # Реагирует на достижение пришельцом правого края
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    # Опускает весь флот и меняет направление флота
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, aliens):

    # Проверяет достиг ли пришелец края экрана, после чего обновляет позицию
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
