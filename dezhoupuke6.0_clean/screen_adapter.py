# -*- coding: utf-8 -*-
"""
德州扑克3 - 屏幕适配管理器
负责处理不同屏幕尺寸和方向的自适应
"""

from kivy.core.window import Window
from kivy.clock import Clock

class ScreenAdapter:
    """屏幕适配管理器"""
    
    def __init__(self):
        self.is_portrait = True
        self.base_width = 720  # 基准宽度
        self.base_height = 1280  # 基准高度
        
        # 绑定窗口大小变化事件
        Window.bind(on_resize=self._on_window_resize)
        
        # 初始化屏幕状态
        self._update_screen_state()
    
    def _on_window_resize(self, window, width, height):
        """窗口大小变化回调"""
        self._update_screen_state()
    
    def _update_screen_state(self):
        """更新屏幕状态"""
        width, height = Window.size
        self.is_portrait = height >= width
        
        # 打印调试信息
        print(f"屏幕尺寸: {width}x{height}, 方向: {'竖屏' if self.is_portrait else '横屏'}")
    
    def get_scale_factor(self):
        """获取缩放因子"""
        if self.is_portrait:
            # 竖屏模式，以高度为基准
            return min(Window.height / self.base_height, Window.width / self.base_width)
        else:
            # 横屏模式，以宽度为基准
            return min(Window.width / self.base_height, Window.height / self.base_width)
    
    def get_relative_size(self, base_size):
        """获取相对尺寸"""
        scale_factor = self.get_scale_factor()
        return base_size * scale_factor
    
    def get_percentage_size(self, percentage, reference='width'):
        """获取百分比尺寸"""
        if reference == 'width':
            return Window.width * percentage / 100
        elif reference == 'height':
            return Window.height * percentage / 100
        else:
            return min(Window.width, Window.height) * percentage / 100
    
    def get_font_size(self, base_font_size):
        """获取适配的字体大小"""
        scale_factor = self.get_scale_factor()
        return max(10, base_font_size * scale_factor)  # 最小字体大小10
    
    def get_optimal_layout_config(self):
        """获取最佳布局配置"""
        width, height = Window.size
        
        if self.is_portrait:
            # 竖屏布局配置
            return {
                'status_bar_height': height * 0.08,
                'game_area_height': height * 0.72,
                'button_area_height': height * 0.2,
                'card_width': width * 0.08,
                'card_height': width * 0.08 * 1.4,
                'player_card_width': width * 0.25,
                'player_card_height': height * 0.1,
            }
        else:
            # 横屏布局配置
            return {
                'status_bar_height': height * 0.1,
                'game_area_height': height * 0.7,
                'button_area_height': height * 0.2,
                'card_width': height * 0.1,
                'card_height': height * 0.1 * 1.4,
                'player_card_width': width * 0.15,
                'player_card_height': height * 0.15,
            }
    
    def get_player_positions(self, game_area):
        """获取玩家位置配置"""
        width, height = game_area.size
        
        if self.is_portrait:
            # 竖屏玩家位置
            card_width = width * 0.25
            card_height = height * 0.1
            
            positions = [
                # 顶部左
                (game_area.center_x - card_width * 1.2, game_area.top - card_height * 1.5),
                # 顶部右
                (game_area.center_x + card_width * 0.2, game_area.top - card_height * 1.5),
                # 右侧
                (game_area.right - card_width * 1.1, game_area.center_y - card_height/2),
                # 左侧
                (game_area.x + card_width * 0.1, game_area.center_y - card_height/2),
                # 底部
                (game_area.center_x - card_width/2, game_area.y + card_height * 0.5),
            ]
        else:
            # 横屏玩家位置
            card_width = width * 0.15
            card_height = height * 0.15
            
            positions = [
                # 左上角
                (game_area.x + card_width * 0.5, game_area.top - card_height * 1.2),
                # 右上角
                (game_area.right - card_width * 1.5, game_area.top - card_height * 1.2),
                # 右侧中间
                (game_area.right - card_width * 1.2, game_area.center_y - card_height/2),
                # 左侧中间
                (game_area.x + card_width * 0.2, game_area.center_y - card_height/2),
                # 底部中间
                (game_area.center_x - card_width/2, game_area.y + card_height * 0.5),
            ]
        
        return positions
    
    def force_portrait_mode(self):
        """强制竖屏模式"""
        # 设置窗口最小尺寸，防止横屏
        Window.minimum_width = min(Window.size[0], Window.size[1])
        Window.minimum_height = max(Window.size[0], Window.size[1])
        
        # 如果是横屏，强制切换到竖屏
        if not self.is_portrait:
            width, height = Window.size
            if width > height:
                Window.size = (height, width)
    
    def enable_orientation_change(self):
        """启用方向切换"""
        # 允许横竖屏切换
        Window.minimum_width = 400
        Window.minimum_height = 600
        
        # 自动调整窗口大小
        def auto_resize(dt):
            width, height = Window.size
            if width < 400:
                Window.size = (400, height)
            if height < 600:
                Window.size = (width, 600)
        
        Clock.schedule_interval(auto_resize, 0.1)

# 全局屏幕适配器实例
screen_adapter = ScreenAdapter()