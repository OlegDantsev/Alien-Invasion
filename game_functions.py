import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep


def ship_hit(ai_settings, screen, stats, ship, aliens, bullets):

    # Обрабатывает столкновение корабля с пришельцем
    if stats.ship_left > 0:
        # Уменьшение ship_left
        stats.ship_left = -1

        # Очистка списка пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Пауза
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


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


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets):

    # Отслеживание событий клавы и мыши
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Перемещение корабля вправо
        elif event.type == pygame.KEYDOWN:
            check_keydown(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup(event, ship)

        # Событие кнопки Play
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)



def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):

    # Запускает новую игру при нажатии кнопки
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Сброс игровых настроек
        ai_settings.initialize_dynamic_settings()
        # Указатель мыши скрывается
        pygame.mouse.set_visible(False)
        if play_button.rect.collidepoint(mouse_x, mouse_y):
            # Сброс игровой статистики
            stats.reset_stats()
            stats.game_active = True

            # Сброс изображений счета и уровня
            sb.prep_level()
            sb.prep_score()
            sb.prep_high_score()

            # Очистка списка пришельцев
            aliens.empty()
            bullets.empty()

            # Создание нового флота
            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button):

    # При каждом переходе цикла отрисовывается новый экран с фоном
    screen.fill(ai_settings.bg_color)

    # Все пули выводятся позади корабля и пришельцев
    for bullet in bullets:
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Вывод счета
    sb.show_score()

    # Кнопка "Play" отображается, когда игра неактивна
    if not stats.game_active:
        play_button.draw_button()

    # Отображение последнего нарисованного экрана
    pygame.display.flip()


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                  bullets):

    # Проверка попаданий в пришельцев
    # При обнаружении попадания удалить пулю
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)

    # Проверка того, что флот пришельцев уничтожен и создание нового
    if len(aliens) == 0:
        # Уничтожение пуль, повышение скорости, создание нового флота
        ai_settings.increase_speed()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

        # Увеличение уровня
        stats.level += 1
        sb.prep_level()


def update_bullet(ai_settings, screen, stats, sb, ship, aliens, bullets):

    # Обновляет позицию пуль и уничтожает старые пули
    bullets.update()

    # Удаление пуль вышедших за пределы экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                  bullets)


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


def check_aliens_bottom(ai_settings, screen, stats, ship, aliens, bullets):

    # Проверяет добрались ли пришельцы до нижней части экрана
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, ship, aliens, bullets)
            break


def check_high_score(stats, sb):

    # Проверяет появился ли новый рекорд
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_aliens(ai_settings, screen, stats, ship, aliens, bullets):

    # Проверяет достиг ли пришелец края экрана, после чего обновляет позицию
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Проверка пришельцев добравшихся до нижнего края экрана
    check_aliens_bottom(ai_settings, screen, stats, ship, aliens, bullets)

    # Проверка коллизий корабль-пришельцы
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, ship, aliens, bullets)
