import pygame
import sys
from pygame.sprite import Group

from game.button import Button
from game.game_status import GameStatus
from game.scoreboard import Scoreboard
from settings import Settings
from game.Alien import Alien
from ship import Ship
import game_functions as gf


def run_game():
    # 初始化游戏，并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Ailien Invasion")
    # 创建play按钮
    play_button = Button(ai_settings, screen, "Play")
    # 创建一艘飞船
    ship = Ship(screen, ai_settings)
    # 创建用于存储子弹的编组
    bullets = Group()
    # 创建外星人群
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # 创建一个在游戏中存储游戏统计信息的实例
    stats = GameStatus(ai_settings)
    # 创建一个记分牌
    sb = Scoreboard(ai_settings, screen, stats)
    while True:
        # 监听事件
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb)
        # 更新
        ship.update()
        # 更新子弹
        gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb)
        # 更新aliens
        gf.update_aliens(ai_settings, stats, screen, ship, bullets, aliens,sb)
        # 每次循环重置屏幕
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, sb)


if __name__ == '__main__':
    run_game()
