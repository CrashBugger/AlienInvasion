import pygame
from pygame import Surface
from pygame.sprite import Group

from game.game_status import GameStatus
from game.settings import Settings
from game.ship import Ship


class Scoreboard():
    """显示得分信息的类"""

    def __init__(self, ai_settings: Settings, screen: Surface, status: GameStatus):
        """初始化得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.status = status
        # 显示得分时的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # 准备初始得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分转换为渲染图像"""
        # 将得分圆整
        rounded_score = int(round(self.status.score, -1))
        score_str = "{:,}".format(rounded_score)
        # score_str = str(self.status.score)删去
        self.score_image = self.font.render(score_str, True, self.text_color)
        # 将得分显示在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """将最高得分转换为渲染的图像"""
        high_score = int(round(self.status.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)
        # 将最高得分显示在屏幕中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """将等级渲染为图像"""
        self.level_image = self.font.render(str(self.status.level), True, self.text_color, self.ai_settings.bg_color)
        """将等级放在得分下方"""
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示还剩下多少飞船"""
        self.ships = Group()
        for ship_number in range(self.status.ships_left):
            ship = Ship(self.screen, self.ai_settings)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
