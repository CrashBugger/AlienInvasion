import sys
from time import sleep

import pygame
from pygame import surface
from pygame.sprite import Group, Sprite
from pygame.surface import Surface

import ship
from bullet import Bullet
from Alien import Alien
from game.button import Button
from game.game_status import GameStatus
from game.scoreboard import Scoreboard
from game.settings import Settings


def check_keydown_events(event, ai_settings: Settings, screen, ship, bullets: Bullet):
    if event.key == pygame.K_q:
        sys.exit(1)
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_settings: Settings, screen, stats: GameStatus, play_button: Button, mouse_x, mouse_y, aliens,
                      ship, bullets, sb: Scoreboard, ):
    """在玩家单击play时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏节奏
        ai_settings.initialize_dynamic_settings()
        # 让光标不可见
        pygame.mouse.set_visible(False)
        # 重置游戏并统计信息
        stats.reset_status()
        stats.game_active = True
        # 重置得分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # 清空外星人和子弹的列表
        bullets.empty()
        aliens.empty()
        # 创建外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_events(ai_settings, screen, ship, bullets, stats: GameStatus, play_button: Button, aliens, sb):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        # 用户按下键盘
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.K_SPACE:
            fire_bullets(ai_settings, )
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 若按下按钮
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, mouse_x, mouse_y, aliens, ship, bullets, sb)


def update_screen(ai_settings: Settings, screen, stats: GameStatus, ship: ship.Ship, aliens: Group, bullets: Bullet,
                  play_button: Button, sb: Scoreboard):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环重绘屏幕
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    # 绘制外星人
    aliens.draw(screen)
    # 重绘子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    if not stats.game_active:
        play_button.draw_button()
    # 显示得分
    sb.show_score()
    # 最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, aliens: Alien, bullets: Sprite, stats, sb):
    """更新子弹未位置"""
    # 更新位置
    bullets.update()
    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets, stats, sb)


def check_bullet_alien_collision(ai_settings: Settings, screen, ship, aliens, bullets, stats: GameStatus,
                                 sb: Scoreboard):
    # 检查是否有子弹击中外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # 增加分数
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    # 更新外星人
    if len(aliens) == 0:
        bullets.empty()
        # 增加游戏节奏
        ai_settings.increase_speed()
        # 如果外星人都被消灭，就提高一个等级
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullets(ai_settings: Settings, screen: surface, ship: ship.Ship, bullets: Bullet):
    # 若子弹数量小于3，创建一颗新子弹,
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings: Settings, screen, ship: ship.Ship, aliens: Group):
    """创建外星人群"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for alien_number in range(number_aliens_x):
        for alien_row in range(number_rows):
            create_alien(ai_settings, screen, aliens, alien_number, alien_row)


def get_number_aliens(ai_settings: Settings, alien_width: int) -> int:
    """获取一行容纳的外星人数量"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    # 外星人间距为外星人宽度
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens: Group, alien_number, row_number):
    """创建一个外星人并放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    # 当前x
    alien.x = alien_width + 2 * alien_width * alien_number
    # 当前y
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    aliens.add(alien)


def get_number_rows(ai_settings: Settings, ship_height, alien_height) -> int:
    """计算能容纳多少行"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def change_fleet_direction(ai_settings, aliens):
    """将外星人整体下移，并改变他们方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings: Settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def update_aliens(ai_settings, stats, screen, ship, bullets, aliens, sb):
    """检查是否有外星人位于屏幕边缘，并更新调整外星人位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检测外星人和飞船是否相撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
    # 检查外星人是否撞到底部
    check_aliens_bottom(aliens, ai_settings, stats, screen, ship, bullets, sb)


def ship_hit(ai_settings: Settings, status: GameStatus, screen, ship: ship.Ship, aliens, bullets, sb: Scoreboard):
    """响应外星人撞到飞船"""
    # 将飞船数量ship_left减一
    if status.ships_left > 0:
        status.ships_left -= 1
        # 更新记分牌
        sb.prep_ships()
        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，重置飞船
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        status.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(aliens: Alien, ai_settings: Settings, stats: GameStatus,
                        screen: Surface, ship: ship.Ship, bullets, sb):
    """检查是否有外星人到达底部"""
    screen_rect = screen.get_rect()
    for alien in aliens:
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船撞到飞船一样处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
            break


def check_high_score(stats: GameStatus, sb: Scoreboard):
    """检查是否诞生了最高分"""
    if stats.high_score < stats.score:
        stats.high_score = stats.score
        sb.prep_high_score()
