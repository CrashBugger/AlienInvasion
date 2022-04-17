class Settings():
    def __init__(self):
        """  初始化游戏时的静态设置"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # 飞船设置
        self.ship_speed_factor = 1.0
        self.ship_limit = 3
        # 子弹设置
        self.bullet_speed_factor = 0.7
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        # 限制子弹数量
        self.bullets_allowed = 3
        # 外星人设置
        self.alien_speed_factor = 0.7  # 外星人水平移动速度
        self.fleet_drop_speed = 10  # 外星人竖直移动速度
        self.fleet_direction = 1  # 移动方向： 1为向右，-1向左
        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        # 点数提高速度
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        """初始化游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 0.7
        self.alien_speed_factor = 0.7
        self.fleet_direction = 1
        # 计分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        """提高点数"""
        self.alien_points = int(self.alien_points * self.score_scale)
