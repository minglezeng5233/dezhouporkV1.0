#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
德州扑克3 - 界面布局测试脚本
测试界面组件的位置和布局合理性
"""

import sys
import os
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

class LayoutTestWidget(BoxLayout):
    """布局测试界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        
        # 测试信息
        self.add_widget(Label(text="=== 界面布局测试 ===", font_size=20))
        
        # 测试不同屏幕尺寸
        test_sizes = [
            (360, 640, "小屏手机"),
            (720, 1280, "标准手机"),
            (1080, 1920, "高清手机"),
            (600, 800, "平板竖屏")
        ]
        
        for width, height, desc in test_sizes:
            Window.size = (width, height)
            screen_adapter._update_screen_state()
            
            layout_config = screen_adapter.get_optimal_layout_config()
            
            # 检查布局合理性
            status_bar_ratio = layout_config['status_bar_height'] / height
            game_area_ratio = layout_config['game_area_height'] / height
            button_area_ratio = layout_config['button_area_height'] / height
            
            info_text = f"{desc} ({width}x{height}):\n"
            info_text += f"  状态栏: {status_bar_ratio:.1%} ({layout_config['status_bar_height']:.0f}px)\n"
            info_text += f"  游戏区: {game_area_ratio:.1%} ({layout_config['game_area_height']:.0f}px)\n"
            info_text += f"  按钮区: {button_area_ratio:.1%} ({layout_config['button_area_height']:.0f}px)\n"
            
            # 检查卡牌尺寸是否合理
            card_width_ratio = layout_config['card_width'] / width
            info_text += f"  卡牌宽: {card_width_ratio:.1%} ({layout_config['card_width']:.0f}px)\n"
            
            # 检查玩家卡片尺寸
            player_card_width_ratio = layout_config['player_card_width'] / width
            player_card_height_ratio = layout_config['player_card_height'] / height
            info_text += f"  玩家卡: {player_card_width_ratio:.1%}x{player_card_height_ratio:.1%}\n"
            
            # 布局合理性评估
            issues = []
            if status_bar_ratio < 0.05:
                issues.append("状态栏太小")
            if game_area_ratio < 0.6:
                issues.append("游戏区域太小")
            if button_area_ratio < 0.15:
                issues.append("按钮区域太小")
            if card_width_ratio < 0.05:
                issues.append("卡牌太小")
            
            if issues:
                info_text += f"  ⚠️ 问题: {', '.join(issues)}"
            else:
                info_text += "  ✅ 布局合理"
            
            self.add_widget(Label(text=info_text, font_size=12))
        
        # 恢复默认尺寸
        Window.size = (720, 1280)

class LayoutTestApp(App):
    """布局测试应用"""
    
    def build(self):
        self.title = "界面布局测试"
        return LayoutTestWidget()

if __name__ == '__main__':
    print("启动界面布局测试...")
    LayoutTestApp().run()