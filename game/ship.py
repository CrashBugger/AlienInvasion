import pygame
from pygame.sprite import Sprite

from game.settings import Settings


class Ship(Sprite):
    def __init__(self, screen, ai_settings: Settings):
        """初始化飞船，并设置其起始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        # 加载飞船图像并获取外接矩形
        self.image = pygame.image.load("D:\PyCharm\Code\project\game\images\ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # 将飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # 移动标志
        self.moving_right = False
        self.moving_left = False
        # 飞船设置
        self.ai_settings = ai_settings
        # 在飞船的center属性中存储小数值
        self.center = float(self.rect.centerx)

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        # 加上边界判断
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        # 覆盖
        self.rect.centerx = self.center

    def center_ship(self):
        """让飞船居中"""
        self.center = self.screen_rect.centerx
