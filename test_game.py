#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
德州扑克3 - 游戏测试脚本
测试游戏功能、音效、界面和交互
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestTexasHoldemGame(unittest.TestCase):
    """德州扑克游戏测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 导入游戏模块
        from main import TexasHoldemGame, Player, Card, Suit, Rank
        
        # 创建测试游戏实例
        self.game = TexasHoldemGame()
        
    def test_game_initialization(self):
        """测试游戏初始化"""
        self.assertIsNotNone(self.game)
        self.assertEqual(len(self.game.players), 5)
        self.assertTrue(self.game.is_hand_active)
        
    def test_player_creation(self):
        """测试玩家创建"""
        players = self.game.players
        
        # 检查玩家数量
        self.assertEqual(len(players), 5)
        
        # 检查人类玩家
        human_players = [p for p in players if p.is_human]
        self.assertEqual(len(human_players), 1)
        
        # 检查AI玩家
        ai_players = [p for p in players if not p.is_human]
        self.assertEqual(len(ai_players), 4)
        
    def test_card_dealing(self):
        """测试发牌功能"""
        # 检查每个玩家都有2张牌
        for player in self.game.players:
            self.assertEqual(len(player.hand), 2)
            
        # 检查人类玩家手牌正面朝上
        human_player = next(p for p in self.game.players if p.is_human)
        for card in human_player.hand:
            self.assertTrue(card.face_up)
            
        # 检查AI玩家手牌背面朝上（除了最后阶段）
        ai_players = [p for p in self.game.players if not p.is_human]
        for player in ai_players:
            for card in player.hand:
                self.assertFalse(card.face_up)
    
    def test_player_actions(self):
        """测试玩家行动"""
        # 找到人类玩家
        human_player = next(p for p in self.game.players if p.is_human)
        
        # 测试弃牌
        initial_chips = human_player.chips
        result = self.game.handle_player_action("fold")
        self.assertTrue(result)
        self.assertTrue(human_player.folded)
        self.assertEqual(human_player.chips, initial_chips)
        
    def test_betting_actions(self):
        """测试下注行动"""
        # 找到人类玩家
        human_player = next(p for p in self.game.players if p.is_human)
        
        # 测试跟注
        initial_chips = human_player.chips
        result = self.game.handle_player_action("call")
        self.assertTrue(result)
        self.assertLess(human_player.chips, initial_chips)
        
    def test_game_advancement(self):
        """测试游戏推进"""
        initial_state = self.game.game_state
        
        # 模拟游戏推进
        self.game._next_street()
        
        # 检查游戏状态变化
        self.assertNotEqual(self.game.game_state, initial_state)
        
    def test_winner_determination(self):
        """测试赢家确定"""
        # 设置所有玩家弃牌，只剩一个
        for i, player in enumerate(self.game.players):
            if i > 0:
                player.folded = True
        
        # 确定赢家
        self.game._determine_winner()
        
        # 检查赢家
        self.assertEqual(len(self.game.winners), 1)
        self.assertEqual(self.game.winners[0].name, "玩家")

class TestSoundManager(unittest.TestCase):
    """音效管理器测试类"""
    
    def setUp(self):
        """测试前准备"""
        from sound_manager import SoundManager
        self.sound_manager = SoundManager()
    
    def test_sound_manager_initialization(self):
        """测试音效管理器初始化"""
        self.assertIsNotNone(self.sound_manager)
        self.assertTrue(self.sound_manager.sound_enabled)
        self.assertTrue(self.sound_manager.music_enabled)
        self.assertEqual(self.sound_manager.sound_volume, 0.7)
        self.assertEqual(self.sound_manager.music_volume, 0.5)
    
    def test_sound_toggle(self):
        """测试音效开关"""
        initial_state = self.sound_manager.sound_enabled
        
        # 切换音效
        new_state = self.sound_manager.toggle_sound()
        self.assertNotEqual(new_state, initial_state)
        
        # 再次切换
        final_state = self.sound_manager.toggle_sound()
        self.assertEqual(final_state, initial_state)
    
    def test_volume_settings(self):
        """测试音量设置"""
        # 测试音效音量
        self.sound_manager.set_sound_volume(0.8)
        self.assertEqual(self.sound_manager.sound_volume, 0.8)
        
        # 测试音乐音量
        self.sound_manager.set_music_volume(0.6)
        self.assertEqual(self.sound_manager.music_volume, 0.6)
        
        # 测试边界值
        self.sound_manager.set_sound_volume(1.5)  # 超过1.0
        self.assertEqual(self.sound_manager.sound_volume, 1.0)
        
        self.sound_manager.set_sound_volume(-0.5)  # 低于0.0
        self.assertEqual(self.sound_manager.sound_volume, 0.0)

class TestResourceManager(unittest.TestCase):
    """资源管理器测试类"""
    
    def test_resource_manager_import(self):
        """测试资源管理器导入"""
        try:
            from resource_manager import ResourceManager
            self.assertTrue(True)  # 导入成功
        except ImportError:
            self.fail("无法导入ResourceManager")

def run_all_tests():
    """运行所有测试"""
    print("德州扑克3 - 功能测试")
    print("=" * 50)
    
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_suite.addTest(unittest.makeSuite(TestTexasHoldemGame))
    test_suite.addTest(unittest.makeSuite(TestSoundManager))
    test_suite.addTest(unittest.makeSuite(TestResourceManager))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print(f"测试结果: {result.testsRun} 个测试运行")
    print(f"通过: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    return result.wasSuccessful()

def quick_test():
    """快速功能测试"""
    print("德州扑克3 - 快速功能测试")
    print("=" * 50)
    
    try:
        # 测试导入
        from main import TexasHoldemGame, Card, Suit, Rank
        print("✅ 模块导入成功")
        
        # 测试游戏创建
        game = TexasHoldemGame()
        print("✅ 游戏创建成功")
        
        # 测试玩家数量
        assert len(game.players) == 5, "玩家数量不正确"
        print("✅ 玩家数量正确")
        
        # 测试发牌
        for player in game.players:
            assert len(player.hand) == 2, "手牌数量不正确"
        print("✅ 发牌功能正常")
        
        # 测试音效管理器
        from sound_manager import SoundManager
        sound_manager = SoundManager()
        print("✅ 音效管理器正常")
        
        # 测试资源管理器
        from resource_manager import ResourceManager
        print("✅ 资源管理器正常")
        
        print("\n🎉 所有快速测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == '__main__':
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == 'quick':
        # 快速测试
        success = quick_test()
    else:
        # 完整测试
        success = run_all_tests()
    
    # 退出码
    sys.exit(0 if success else 1)