#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
德州扑克3 - 核心游戏逻辑测试
不依赖Kivy框架，专门测试游戏核心功能
"""

import sys
import os
import random
from enum import Enum
from collections import defaultdict

# 游戏常量定义
class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦" 
    CLUBS = "♣"
    SPADES = "♠"

class Rank(Enum):
    TWO = ("2", 2)
    THREE = ("3", 3)
    FOUR = ("4", 4)
    FIVE = ("5", 5)
    SIX = ("6", 6)
    SEVEN = ("7", 7)
    EIGHT = ("8", 8)
    NINE = ("9", 9)
    TEN = ("10", 10)
    JACK = ("J", 11)
    QUEEN = ("Q", 12)
    KING = ("K", 13)
    ACE = ("A", 14)
    
    @property
    def symbol(self):
        return self.value[0]
    
    @property
    def value_num(self):
        return self.value[1]

class HandType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

# 扑克牌类
class Card:
    """扑克牌类"""
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank
        self.face_up = True
        
    def __str__(self):
        return f"{self.rank.symbol}{self.suit.value}"
    
    def __repr__(self):
        return self.__str__()
    
    def get_color(self):
        """获取花色颜色"""
        return "red" if self.suit in [Suit.HEARTS, Suit.DIAMONDS] else "black"

# 牌桌类
class PokerTable:
    """牌桌类"""
    def __init__(self):
        self.pot = 0
        self.current_bet = 0
        self.small_blind = 100
        self.big_blind = 200
        self.community_cards = []
        self.deck = self._create_deck()
    
    def _create_deck(self):
        """创建一副牌"""
        deck = []
        for suit in Suit:
            for rank in Rank:
                deck.append(Card(suit, rank))
        random.shuffle(deck)
        return deck
    
    def reset_deck(self):
        """重置牌堆"""
        self.deck = self._create_deck()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
    
    def deal_card(self):
        """发一张牌"""
        if len(self.deck) == 0:
            self.reset_deck()
        return self.deck.pop()
    
    def deal_community(self, count):
        """发公共牌"""
        cards = []
        for _ in range(count):
            cards.append(self.deal_card())
        self.community_cards.extend(cards)
        return cards

# 玩家类
class Player:
    """玩家类"""
    def __init__(self, name, is_human=False, chips=1000):
        self.name = name
        self.is_human = is_human
        self.chips = chips
        self.hand = []
        self.current_bet = 0
        self.folded = False
        self.all_in = False
        self.position = 0
        self.is_active = False
    
    def reset_hand(self):
        """重置手牌状态"""
        self.hand = []
        self.current_bet = 0
        self.folded = False
        self.all_in = False
        self.is_active = False
    
    def bet(self, amount):
        """下注"""
        if amount >= self.chips:
            amount = self.chips
            self.all_in = True
        
        self.chips -= amount
        self.current_bet += amount
        return amount
    
    def fold(self):
        """弃牌"""
        self.folded = True
    
    def can_act(self):
        """是否可以行动"""
        return not self.folded and not self.all_in and self.chips > 0

# 游戏逻辑类
class TexasHoldemGame:
    """德州扑克游戏逻辑类"""
    def __init__(self):
        self.table = PokerTable()
        self.players = self._create_players()
        
        # 游戏状态
        self.game_state = "preflop"  # preflop, flop, turn, river, showdown, finished
        self.current_player_idx = 0
        self.is_hand_active = False
        self.winners = []
        
        # UI状态
        self.feedback = ""
        self.is_waiting = False
        self.wait_until = 0
        self.hand_count = 1
        
        # 开始游戏
        self.start_new_hand()
    
    def _create_players(self):
        """创建玩家"""
        players = []
        
        # 人类玩家（底部）
        human = Player("玩家", is_human=True, chips=10000)
        human.position = 4  # 底部位置
        
        # AI玩家
        ai_data = [
            ("AI玩家1", 5000),
            ("AI玩家2", 8000),
            ("AI玩家3", 6000),
            ("AI玩家4", 7000),
        ]
        
        for i, (name, chips) in enumerate(ai_data):
            player = Player(name, is_human=False, chips=chips)
            player.position = i
            players.append(player)
        
        # 将人类玩家添加到末尾（底部位置）
        players.append(human)
        
        return players
    
    def start_new_hand(self):
        """开始新的一手牌"""
        self.table.reset_deck()
        self.game_state = "preflop"
        self.current_player_idx = 0
        self.winners = []
        self.feedback = ""
        self.is_waiting = False
        
        # 重置玩家状态
        for player in self.players:
            player.reset_hand()
            # 发两张手牌
            player.hand = [self.table.deal_card(), self.table.deal_card()]
            # 人类玩家手牌正面，AI玩家背面
            player.hand[0].face_up = player.is_human
            player.hand[1].face_up = player.is_human
        
        # 下盲注
        self._post_blinds()
        
        self.is_hand_active = True
        self.hand_count += 1
    
    def _post_blinds(self):
        """下盲注"""
        # 简化：前两个玩家下盲注
        small_blind = min(self.players[0].chips, self.table.small_blind)
        big_blind = min(self.players[1].chips, self.table.big_blind)
        
        self.players[0].bet(small_blind)
        self.players[1].bet(big_blind)
        
        self.table.pot = small_blind + big_blind
        self.table.current_bet = self.table.big_blind
        
        # 从大盲后开始行动
        self.current_player_idx = 2 % len(self.players)
    
    def handle_player_action(self, action):
        """处理玩家行动"""
        if not self.is_hand_active:
            return False
        
        player = self.players[self.current_player_idx]
        if not player.is_human:
            return False
        
        if action == "fold":
            player.fold()
            self.feedback = f"{player.name} 弃牌"
            self._advance_game()
            
        elif action == "check":
            if self.table.current_bet > player.current_bet:
                self.feedback = "不能过牌，需要跟注"
                return False
            else:
                self.feedback = f"{player.name} 过牌"
                self._advance_game()
                
        elif action == "call":
            call_amount = self.table.current_bet - player.current_bet
            if call_amount > 0:
                amount = player.bet(call_amount)
                self.table.pot += amount
                self.feedback = f"{player.name} 跟注 {amount:,}"
            else:
                self.handle_player_action("check")
                return True
                
            self._advance_game()
            
        elif action == "raise":
            # 简化加注：加注到当前下注的2倍
            raise_to = max(self.table.current_bet * 2, self.table.big_blind * 2)
            raise_amount = raise_to - player.current_bet
            
            if raise_amount > player.chips:
                return self.handle_player_action("all_in")
            
            amount = player.bet(raise_amount)
            self.table.pot += amount
            self.table.current_bet = raise_to
            self.feedback = f"{player.name} 加注到 {raise_to:,}"
            
            self._advance_game()
            
        elif action == "all_in":
            all_in_amount = player.chips
            amount = player.bet(all_in_amount)
            self.table.pot += amount
            if player.current_bet > self.table.current_bet:
                self.table.current_bet = player.current_bet
            
            self.feedback = f"{player.name} 全下 {all_in_amount:,}"
            self._advance_game()
        
        return True
    
    def _advance_game(self):
        """推进游戏到下一状态"""
        # 找到下一个可以行动的玩家
        start_idx = self.current_player_idx
        while True:
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
            player = self.players[self.current_player_idx]
            
            if player.can_act():
                break
            
            if self.current_player_idx == start_idx:
                # 所有玩家都已行动，进入下一阶段
                self._next_street()
                return
        
        # 如果是AI玩家，设置等待时间
        current_player = self.players[self.current_player_idx]
        if not current_player.is_human:
            self.is_waiting = True
            self.wait_until = 0  # 简化：不使用时间
    
    def _next_street(self):
        """进入下一阶段"""
        if self.game_state == "preflop":
            self.game_state = "flop"
            self.table.deal_community(3)
            self.feedback = "翻牌发出"
            
        elif self.game_state == "flop":
            self.game_state = "turn"
            self.table.deal_community(1)
            self.feedback = "转牌发出"
            
        elif self.game_state == "turn":
            self.game_state = "river"
            self.table.deal_community(1)
            self.feedback = "河牌发出"
            
        elif self.game_state == "river":
            self.game_state = "showdown"
            self._determine_winner()
            return
        
        # 重置下注轮
        self.table.current_bet = 0
        for player in self.players:
            player.current_bet = 0
        
        # 找到第一个未弃牌的玩家开始行动
        for i, player in enumerate(self.players):
            if not player.folded:
                self.current_player_idx = i
                break
    
    def _determine_winner(self):
        """确定赢家（简化版）"""
        active_players = [p for p in self.players if not p.folded]
        
        if len(active_players) == 1:
            winner = active_players[0]
            winner.chips += self.table.pot
            self.winners = [winner]
        else:
            # 简化：随机选择一个赢家
            winner = random.choice(active_players)
            winner.chips += self.table.pot
            self.winners = [winner]
        
        # 显示所有手牌
        for player in self.players:
            for card in player.hand:
                card.face_up = True
        
        self.game_state = "finished"
        self.is_hand_active = False
        self.feedback = f"{self.winners[0].name} 赢得 {self.table.pot:,}"
        
        # 设置自动开始下一局的计时
        self.is_waiting = True
        self.wait_until = 0  # 简化：不使用时间

def test_basic_functionality():
    """测试基本功能"""
    print("德州扑克3 - 核心游戏逻辑测试")
    print("=" * 50)
    
    try:
        # 测试卡牌创建
        print("1. 测试卡牌创建...")
        card = Card(Suit.HEARTS, Rank.ACE)
        assert str(card) == "A♥", f"卡牌显示错误: {card}"
        print("   ✅ 卡牌创建成功")
        
        # 测试玩家创建
        print("2. 测试玩家创建...")
        player = Player("测试玩家", is_human=True, chips=1000)
        assert player.name == "测试玩家"
        assert player.chips == 1000
        assert player.is_human == True
        print("   ✅ 玩家创建成功")
        
        # 测试牌桌创建
        print("3. 测试牌桌创建...")
        table = PokerTable()
        assert len(table.deck) == 52
        print("   ✅ 牌桌创建成功")
        
        # 测试发牌
        print("4. 测试发牌功能...")
        card1 = table.deal_card()
        card2 = table.deal_card()
        assert card1 != card2, "发牌重复"
        print("   ✅ 发牌功能正常")
        
        print("   ✅ 基础功能测试通过")
        return True
        
    except Exception as e:
        print(f"   ❌ 基础功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_game_logic():
    """测试游戏逻辑"""
    print("\n5. 测试游戏逻辑...")
    
    try:
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
        
        # 测试游戏状态
        assert game.game_state == "preflop", "初始游戏状态错误"
        
        print("   ✅ 游戏逻辑测试通过")
        return True
        
    except Exception as e:
        print(f"   ❌ 游戏逻辑测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_player_actions():
    """测试玩家行动"""
    print("\n6. 测试玩家行动...")
    
    try:
        # 创建游戏实例
        game = TexasHoldemGame()
        
        # 找到人类玩家
        human_player = next(p for p in game.players if p.is_human)
        
        # 测试弃牌
        initial_chips = human_player.chips
        result = game.handle_player_action("fold")
        assert result == True, "弃牌操作失败"
        assert human_player.folded == True, "玩家未弃牌"
        
        # 测试下注
        game2 = TexasHoldemGame()
        human_player2 = next(p for p in game2.players if p.is_human)
        initial_chips2 = human_player2.chips
        
        result = game2.handle_player_action("call")
        assert result == True, "跟注操作失败"
        assert human_player2.chips < initial_chips2, "筹码未减少"
        
        print("   ✅ 玩家行动测试通过")
        return True
        
    except Exception as e:
        print(f"   ❌ 玩家行动测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("德州扑克3 - 核心功能测试（不依赖Kivy）")
    print("=" * 50)
    
    # 运行所有测试
    tests = [
        ("基础功能", test_basic_functionality),
        ("游戏逻辑", test_game_logic),
        ("玩家行动", test_player_actions)
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
        print("\n🎉 所有核心功能测试通过！")
        print("\n💡 说明：")
        print("• 核心游戏逻辑已通过测试")
        print("• 如需运行完整游戏，需要安装Kivy框架")
        print("• 可以使用虚拟环境安装: python3 -m venv venv && source venv/bin/activate && pip install kivy==2.2.1")
    else:
        print("\n⚠️  部分测试失败，请检查错误信息。")
    
    return success_count == len(results)

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)