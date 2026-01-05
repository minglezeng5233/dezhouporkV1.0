#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
德州扑克3 - 游戏试运行脚本
快速测试游戏功能和界面
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_functionality():
    """测试基本功能"""
    print("德州扑克3 - 功能测试")
    print("=" * 50)
    
    try:
        # 测试模块导入
        print("1. 测试模块导入...")
        from main import Card, Suit, Rank, Player, PokerTable
        print("   ✅ 基础类导入成功")
        
        # 测试卡牌创建
        print("2. 测试卡牌创建...")
        card = Card(Suit.HEARTS, Rank.ACE)
        assert str(card) == "A♥", f"卡牌显示错误: {card}"
        print("   ✅ 卡牌创建成功")
        
        # 测试玩家创建
        print("3. 测试玩家创建...")
        player = Player("测试玩家", is_human=True, chips=1000)
        assert player.name == "测试玩家"
        assert player.chips == 1000
        assert player.is_human == True
        print("   ✅ 玩家创建成功")
        
        # 测试牌桌创建
        print("4. 测试牌桌创建...")
        table = PokerTable()
        assert len(table.deck) == 52
        print("   ✅ 牌桌创建成功")
        
        # 测试发牌
        print("5. 测试发牌功能...")
        card1 = table.deal_card()
        card2 = table.deal_card()
        assert card1 != card2, "发牌重复"
        print("   ✅ 发牌功能正常")
        
        # 测试音效管理器
        print("6. 测试音效管理器...")
        from sound_manager import SoundManager
        sound_manager = SoundManager()
        assert sound_manager.sound_enabled == True
        assert sound_manager.music_enabled == True
        print("   ✅ 音效管理器正常")
        
        # 测试资源管理器
        print("7. 测试资源管理器...")
        from resource_manager import ResourceManager
        resource_manager = ResourceManager()
        print("   ✅ 资源管理器正常")
        
        print("\n🎉 所有基础功能测试通过！")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ui_components():
    """测试UI组件"""
    print("\n8. 测试UI组件...")
    
    try:
        # 测试UI动画
        from ui_animations import AnimationManager
        anim_manager = AnimationManager()
        print("   ✅ 动画管理器正常")
        
        # 测试设置界面
        from settings_screen import SettingsScreen
        print("   ✅ 设置界面组件正常")
        
        print("   ✅ UI组件测试通过")
        return True
        
    except Exception as e:
        print(f"   ❌ UI组件测试失败: {e}")
        return False

def test_game_logic():
    """测试游戏逻辑"""
    print("\n9. 测试游戏逻辑...")
    
    try:
        from main import TexasHoldemGame
        
        # 创建游戏实例
        game = TexasHoldemGame()
        
        # 测试玩家数量
        assert len(game.players) == 5, f"玩家数量错误: {len(game.players)}"
        
        # 测试人类玩家
        human_players = [p for p in game.players if p.is_human]
        assert len(human_players) == 1, "人类玩家数量错误"
        
        # 测试手牌
        for player in game.players:
            assert len(player.hand) == 2, "手牌数量错误"
        
        # 测试底池
        assert game.table.pot >= 0, "底池不能为负"
        
        print("   ✅ 游戏逻辑测试通过")
        return True
        
    except Exception as e:
        print(f"   ❌ 游戏逻辑测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("德州扑克3 - 完整功能测试")
    print("=" * 50)
    
    # 运行所有测试
    tests = [
        ("基础功能", test_basic_functionality),
        ("UI组件", test_ui_components),
        ("游戏逻辑", test_game_logic)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 运行{test_name}测试...")
        result = test_func()
        results.append((test_name, result))
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    
    success_count = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            success_count += 1
    
    print(f"\n总测试: {len(results)}")
    print(f"通过: {success_count}")
    print(f"失败: {len(results) - success_count}")
    
    if success_count == len(results):
        print("\n🎉 所有测试通过！游戏可以正常运行。")
        print("\n📱 运行游戏命令: python3 main.py")
        print("📱 构建APK命令: ./local_build.sh")
    else:
        print("\n⚠️  部分测试失败，请检查错误信息。")
    
    return success_count == len(results)

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)