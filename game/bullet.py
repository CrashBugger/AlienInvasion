import pygame
from pygame.sprite import Sprite

from game.settings import Settings
from game.ship import Ship


class Bullet(Sprite):
    def __init__(self, ai_settings: Settings, screen, ship: Ship):
        """在飞船所在位置创建子弹"""
        super().__init__()
        self.screen = screen
        # 在（0.0）处创建一个子弹矩形
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        # 修改位置
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # 存储小数表示位置
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor


    def update(self):
        """向上移动子弹"""
        # 更新y坐标
        self.y -= self.speed_factor
        # 覆盖
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
