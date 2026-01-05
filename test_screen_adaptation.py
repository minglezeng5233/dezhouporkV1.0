#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
德州扑克3 - 屏幕自适应测试脚本
测试游戏界面在不同屏幕尺寸下的自适应能力
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from kivy.config import Config
Config.set('graphics', 'width', '720')
Config.set('graphics', 'height', '1280')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from screen_adapter import screen_adapter

class ScreenTestWidget(BoxLayout):
    """屏幕测试界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        
        # 窗口大小信息
        self.info_label = Label(
            text=f"当前窗口: {Window.width}x{Window.height}\n方向: {'竖屏' if screen_adapter.is_portrait else '横屏'}",
            font_size=20
        )
        self.add_widget(self.info_label)
        
        # 测试不同尺寸
        self.add_widget(Label(text="测试不同尺寸的组件:", font_size=16))
        
        # 小按钮
        small_btn = Button(text="小按钮 (5%宽度)", size_hint=(0.05, 0.05))
        self.add_widget(small_btn)
        
        # 中按钮
        medium_btn = Button(text="中按钮 (15%宽度)", size_hint=(0.15, 0.1))
        self.add_widget(medium_btn)
        
        # 大按钮
        large_btn = Button(text="大按钮 (30%宽度)", size_hint=(0.3, 0.15))
        self.add_widget(large_btn)
        
        # 百分比字体测试
        self.add_widget(Label(text="2%字体大小", font_size='2%'))
        self.add_widget(Label(text="3%字体大小", font_size='3%'))
        self.add_widget(Label(text="4%字体大小", font_size='4%'))
        
        # 缩放因子信息
        scale_info = Label(
            text=f"缩放因子: {screen_adapter.get_scale_factor():.2f}\n"
                 f"基准尺寸: {screen_adapter.base_width}x{screen_adapter.base_height}",
            font_size=14
        )
        self.add_widget(scale_info)
        
        # 布局配置信息
        layout_config = screen_adapter.get_optimal_layout_config()
        layout_info = Label(
            text=f"布局配置:\n"
                 f"状态栏高度: {layout_config['status_bar_height']:.1f}\n"
                 f"游戏区域高度: {layout_config['game_area_height']:.1f}\n"
                 f"卡牌宽度: {layout_config['card_width']:.1f}",
            font_size=12
        )
        self.add_widget(layout_info)
        
        # 绑定窗口大小变化
        Window.bind(on_resize=self._on_resize)
    
    def _on_resize(self, window, width, height):
        """窗口大小变化回调"""
        self.info_label.text = f"当前窗口: {width}x{height}\n方向: {'竖屏' if screen_adapter.is_portrait else '横屏'}"

class ScreenTestApp(App):
    """屏幕测试应用"""
    
    def build(self):
        self.title = "屏幕自适应测试"
        
        # 测试不同窗口尺寸
        test_sizes = [
            (720, 1280),   # 标准手机竖屏
            (1080, 1920),  # 高清手机竖屏
            (480, 800),    # 小屏手机竖屏
            (1280, 720),   # 横屏模式
            (600, 800),    # 平板竖屏
        ]
        
        print("=== 屏幕自适应测试 ===")
        for width, height in test_sizes:
            Window.size = (width, height)
            screen_adapter._update_screen_state()
            
            scale_factor = screen_adapter.get_scale_factor()
            layout_config = screen_adapter.get_optimal_layout_config()
            
            print(f"尺寸: {width}x{height}")
            print(f"  方向: {'竖屏' if screen_adapter.is_portrait else '横屏'}")
            print(f"  缩放因子: {scale_factor:.2f}")
            print(f"  卡牌宽度: {layout_config['card_width']:.1f}")
            print(f"  状态栏高度: {layout_config['status_bar_height']:.1f}")
            print()
        
        # 恢复默认尺寸
        Window.size = (720, 1280)
        
        return ScreenTestWidget()

if __name__ == '__main__':
    print("启动屏幕自适应测试...")
    ScreenTestApp().run()