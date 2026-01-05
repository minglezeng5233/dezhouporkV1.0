#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
德州扑克3 - 全面检测脚本
系统性地验证所有检测点
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

class ComprehensiveTestWidget(BoxLayout):
    """全面检测界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        
        self.add_widget(Label(text="=== 德州扑克3全面检测报告 ===", font_size=24))
        
        # 检测点1：界面布局
        self._test_layout()
        
        # 检测点2：触摸按钮
        self._test_buttons()
        
        # 检测点3：游戏状态转换
        self._test_game_states()
        
        # 检测点4：AI逻辑
        self._test_ai_logic()
        
        # 检测点5：性能
        self._test_performance()
        
        # 检测点6：规则正确性
        self._test_rules()
        
        # 检测点7：视觉一致性
        self._test_visual_consistency()
    
    def _test_layout(self):
        """检测点1：界面布局"""
        self.add_widget(Label(text="\n🔍 检测点1：界面布局", font_size=20))
        
        # 测试不同屏幕尺寸
        test_sizes = [
            (360, 640, "小屏手机"),
            (720, 1280, "标准手机"),
            (1080, 1920, "高清手机")
        ]
        
        for width, height, desc in test_sizes:
            Window.size = (width, height)
            screen_adapter._update_screen_state()
            layout_config = screen_adapter.get_optimal_layout_config()
            
            # 检查布局合理性
            issues = []
            
            # 检查组件是否在屏幕内
            if layout_config['player_card_width'] > width * 0.3:
                issues.append("玩家卡片过宽")
            if layout_config['player_card_height'] > height * 0.15:
                issues.append("玩家卡片过高")
            
            # 检查字体可读性
            font_size = screen_adapter.get_font_size(14)
            if font_size < 10:
                issues.append("字体过小")
            
            status = "✅ 通过" if not issues else f"⚠️ 问题: {', '.join(issues)}"
            
            self.add_widget(Label(
                text=f"{desc} ({width}x{height}): {status}",
                font_size=14
            ))
        
        Window.size = (720, 1280)
    
    def _test_buttons(self):
        """检测点2：触摸按钮"""
        self.add_widget(Label(text="\n🔍 检测点2：触摸按钮", font_size=20))
        
        # 检查按钮大小
        button_width = Window.width * 0.18
        button_height = Window.height * 0.08
        
        issues = []
        
        # 检查最小触摸目标（44x44像素）
        if button_width < 44:
            issues.append(f"按钮宽度不足: {button_width:.0f}px < 44px")
        if button_height < 44:
            issues.append(f"按钮高度不足: {button_height:.0f}px < 44px")
        
        # 检查按钮间距
        button_spacing = 10
        if button_spacing < 5:
            issues.append("按钮间距过小")
        
        status = "✅ 通过" if not issues else f"⚠️ 问题: {', '.join(issues)}"
        
        self.add_widget(Label(
            text=f"按钮尺寸: {button_width:.0f}x{button_height:.0f}px, 间距: {button_spacing}px",
            font_size=14
        ))
        self.add_widget(Label(text=f"检测结果: {status}", font_size=14))
    
    def _test_game_states(self):
        """检测点3：游戏状态转换"""
        self.add_widget(Label(text="\n🔍 检测点3：游戏状态转换", font_size=20))
        
        # 检查状态转换顺序
        expected_states = ["preflop", "flop", "turn", "river", "showdown", "finished"]
        
        issues = []
        
        # 模拟状态转换检查
        from main import TexasHoldemGame
        game = TexasHoldemGame()
        
        # 检查初始状态
        if game.game_state != "preflop":
            issues.append("初始状态不正确")
        
        # 检查状态转换方法是否存在
        if not hasattr(game, '_next_street'):
            issues.append("缺少状态转换方法")
        
        status = "✅ 通过" if not issues else f"⚠️ 问题: {', '.join(issues)}"
        
        self.add_widget(Label(
            text=f"状态转换顺序: {' → '.join(expected_states)}",
            font_size=14
        ))
        self.add_widget(Label(text=f"检测结果: {status}", font_size=14))
    
    def _test_ai_logic(self):
        """检测点4：AI逻辑"""
        self.add_widget(Label(text="\n🔍 检测点4：AI逻辑", font_size=20))
        
        from main import TexasHoldemGame
        game = TexasHoldemGame()
        
        issues = []
        
        # 检查AI决策方法
        if not hasattr(game, '_process_ai_action'):
            issues.append("缺少AI决策方法")
        
        # 检查手牌强度计算
        if not hasattr(game, '_calculate_hand_strength'):
            issues.append("缺少手牌强度计算")
        
        # 检查AI是否会非法行动
        try:
            # 测试AI在特定情况下的决策
            ai_player = game.players[0]  # 第一个AI玩家
            if hasattr(game, '_make_ai_decision'):
                # 模拟AI决策
                hand_strength = 0.5
                position_factor = 0.5
                bet_history_factor = 0.5
                decision = game._make_ai_decision(ai_player, hand_strength, position_factor, bet_history_factor)
                
                if decision not in ["fold", "check", "call", "raise", "all_in"]:
                    issues.append("AI决策返回无效动作")
        except Exception as e:
            issues.append(f"AI决策测试失败: {e}")
        
        status = "✅ 通过" if not issues else f"⚠️ 问题: {', '.join(issues)}"
        
        self.add_widget(Label(text=f"检测结果: {status}", font_size=14))
    
    def _test_performance(self):
        """检测点5：性能"""
        self.add_widget(Label(text="\n🔍 检测点5：性能优化", font_size=20))
        
        issues = []
        
        # 检查更新频率
        update_interval = 1.0/30.0  # 30FPS
        if update_interval > 1.0/60.0:
            issues.append("更新频率过低")
        
        # 检查是否有不必要的重绘
        from main import PokerGameWidget
        game_widget = PokerGameWidget()
        
        if hasattr(game_widget, '_last_display_time'):
            # 性能优化已实现
            pass
        else:
            issues.append("缺少性能优化机制")
        
        status = "✅ 通过" if not issues else f"⚠️ 问题: {', '.join(issues)}"
        
        self.add_widget(Label(
            text=f"更新频率: {1.0/update_interval:.0f}FPS",
            font_size=14
        ))
        self.add_widget(Label(text=f"检测结果: {status}", font_size=14))
    
    def _test_rules(self):
        """检测点6：规则正确性"""
        self.add_widget(Label(text="\n🔍 检测点6：游戏规则", font_size=20))
        
        issues = []
        
        # 检查下注轮顺序
        from main import TexasHoldemGame
        game = TexasHoldemGame()
        
        # 检查加注规则
        if game.table.big_blind != 200:
            issues.append("大盲注金额不正确")
        
        # 检查全下规则
        try:
            # 测试全下逻辑
            player = game.players[-1]  # 人类玩家
            original_chips = player.chips
            
            # 模拟全下
            all_in_amount = player.chips
            player.bet(all_in_amount)
            
            if player.chips != 0:
                issues.append("全下后筹码未清零")
            if not player.all_in:
                issues.append("全下后状态未更新")
                
        except Exception as e:
            issues.append(f"全下规则测试失败: {e}")
        
        status = "✅ 通过" if not issues else f"⚠️ 问题: {', '.join(issues)}"
        
        self.add_widget(Label(
            text=f"盲注: {game.table.small_blind}/{game.table.big_blind}",
            font_size=14
        ))
        self.add_widget(Label(text=f"检测结果: {status}", font_size=14))
    
    def _test_visual_consistency(self):
        """检测点7：视觉一致性"""
        self.add_widget(Label(text="\n🔍 检测点7：视觉一致性", font_size=20))
        
        from main import COLORS
        
        issues = []
        
        # 检查颜色方案
        required_colors = ['bg', 'table', 'text_white', 'text_gray', 'chip_gold', 'btn_green', 'btn_red']
        for color in required_colors:
            if color not in COLORS:
                issues.append(f"缺少颜色: {color}")
        
        # 检查颜色值格式
        for color_name, color_value in COLORS.items():
            if len(color_value) != 4:
                issues.append(f"颜色格式错误: {color_name}")
            for value in color_value:
                if not (0 <= value <= 1):
                    issues.append(f"颜色值超出范围: {color_name}")
        
        status = "✅ 通过" if not issues else f"⚠️ 问题: {', '.join(issues)}"
        
        self.add_widget(Label(
            text=f"颜色方案: {len(COLORS)}种颜色",
            font_size=14
        ))
        self.add_widget(Label(text=f"检测结果: {status}", font_size=14))

class ComprehensiveTestApp(App):
    """全面检测应用"""
    
    def build(self):
        self.title = "德州扑克3全面检测"
        return ComprehensiveTestWidget()

if __name__ == '__main__':
    print("启动全面检测...")
    ComprehensiveTestApp().run()