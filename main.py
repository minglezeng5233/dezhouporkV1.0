# -*- coding: utf-8 -*-
"""
德州扑克3 - 专业手游版 (性能优化修复版)
基于Kivy框架的移动端优化版本
"""

import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Ellipse, Line, PushMatrix, PopMatrix, Rotate
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import (
    NumericProperty, StringProperty, ListProperty, 
    BooleanProperty, ObjectProperty
)
from kivy.config import Config
from kivy.core.text import Label as CoreLabel

import random
from enum import Enum

# 导入适配器和组件
from sound_manager import SoundManager, GameSounds
from settings_screen import SettingsPopup
from ui_animations import AnimationManager
from screen_adapter import screen_adapter

# ==============================================
# 游戏常量与枚举
# ==============================================

class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦" 
    CLUBS = "♣"
    SPADES = "♠"

class Rank(Enum):
    TWO = ("2", 2); THREE = ("3", 3); FOUR = ("4", 4); FIVE = ("5", 5)
    SIX = ("6", 6); SEVEN = ("7", 7); EIGHT = ("8", 8); NINE = ("9", 9)
    TEN = ("10", 10); JACK = ("J", 11); QUEEN = ("Q", 12); KING = ("K", 13); ACE = ("A", 14)
    @property
    def symbol(self): return self.value[0]
    @property
    def value_num(self): return self.value[1]

COLORS = {
    'bg': (0.06, 0.08, 0.12, 1),
    'table': (0.1, 0.27, 0.16, 1),
    'player_card': (0.14, 0.16, 0.22, 1),
    'player_card_active': (0.22, 0.34, 0.4, 1),
    'text_white': (0.96, 0.96, 0.98, 1),
    'text_gold': (1.0, 0.84, 0.0, 1),
    'chip_gold': (1.0, 0.84, 0.0, 1),
    'pot_gold': (1.0, 0.88, 0.24, 1),
    'btn_green': (0.27, 0.75, 0.31, 1),
    'btn_red': (0.9, 0.31, 0.31, 1),
    'btn_blue': (0.31, 0.59, 0.9, 1),
    'card_red': (0.86, 0.24, 0.24, 1),
    'card_black': (0.16, 0.16, 0.16, 1),
    'card_face': (0.98, 0.98, 0.98, 1),
    'card_back': (0.31, 0.12, 0.12, 1),
}

# ==============================================
# 核心逻辑类 (保持原有逻辑，优化接口)
# ==============================================

class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank
        self.face_up = True
    def get_color(self):
        return COLORS['card_red'] if self.suit in [Suit.HEARTS, Suit.DIAMONDS] else COLORS['card_black']

class Player:
    def __init__(self, name, is_human=False, chips=10000):
        self.name = name
        self.is_human = is_human
        self.chips = chips
        self.hand = []
        self.current_bet = 0
        self.folded = False
        self.all_in = False

    def reset_hand(self):
        self.hand = []
        self.current_bet = 0
        self.folded = False
        self.all_in = False

    def bet(self, amount):
        if amount >= self.chips:
            amount = self.chips
            self.all_in = True
        self.chips -= amount
        self.current_bet += amount
        return amount

# ==============================================
# 改进的 UI 组件 (支持动画和高效渲染)
# ==============================================

class CardWidget(Widget):
    """优化后的卡牌组件：支持旋转动画，手动绘制纹理"""
    rotation_y = NumericProperty(0)
    scale = NumericProperty(1.0)
    
    def __init__(self, card, **kwargs):
        super().__init__(**kwargs)
        self.card = card
        self.size_hint = (None, None)
        self.width = Window.width * 0.08
        self.height = self.width * 1.4
        self.bind(pos=self.redraw, rotation_y=self.redraw, scale=self.redraw)
        self.redraw()

    def redraw(self, *args):
        self.canvas.before.clear()
        self.canvas.clear()
        
        with self.canvas.before:
            PushMatrix()
            Rotate(angle=self.rotation_y, axis=(0, 1, 0), origin=self.center)
            
        with self.canvas:
            if self.card.face_up:
                Color(*COLORS['card_face'])
                Rectangle(pos=self.pos, size=self.size)
                # 绘制花色点数
                color = self.card.get_color()
                Color(*color)
                # 简单绘制：这里可以用贴图优化，暂时用CoreLabel绘制
                core_lbl = CoreLabel(text=self.card.rank.symbol, font_size=20)
                core_lbl.refresh()
                Rectangle(texture=core_lbl.texture, pos=(self.x + 2, self.y + self.height - 25), size=core_lbl.texture.size)
            else:
                Color(*COLORS['card_back'])
                Rectangle(pos=self.pos, size=self.size)
                Color(1, 1, 1, 0.2)
                Line(rectangle=(self.x+2, self.y+2, self.width-4, self.height-4))

        with self.canvas.after:
            PopMatrix()

class PlayerUI(BoxLayout):
    """优化后的玩家UI：不再重复创建，仅更新数据"""
    is_active = BooleanProperty(False)
    
    def __init__(self, player, **kwargs):
        super().__init__(**kwargs)
        self.player = player
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        config = screen_adapter.get_optimal_layout_config()
        self.size = (config['player_card_width'], config['player_card_height'])
        self.padding = 5
        
        self.name_label = Label(text=player.name, font_size='14sp', halign='center')
        self.chips_label = Label(text=str(player.chips), color=COLORS['chip_gold'], font_size='16sp')
        self.status_label = Label(text="", font_size='12sp', color=COLORS['text_gold'])
        
        self.add_widget(self.name_label)
        self.add_widget(self.chips_label)
        self.add_widget(self.status_label)
        self.update_ui()

    def update_ui(self):
        # 更新背景颜色指示活跃
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*(COLORS['player_card_active'] if self.is_active else COLORS['player_card']))
            Rectangle(pos=self.pos, size=self.size)
            if self.is_active:
                Color(1, 1, 1, 1)
                Line(rectangle=(self.x, self.y, self.width, self.height), width=1.5)

        self.name_label.text = self.player.name
        self.chips_label.text = f"¥{self.player.chips:,}"
        
        status = ""
        if self.player.folded: status = "弃牌"
        elif self.player.all_in: status = "全下"
        elif self.player.current_bet > 0: status = f"下注:{self.player.current_bet}"
        self.status_label.text = status

# ==============================================
# 游戏主逻辑与视图容器
# ==============================================

class TexasHoldem3Game:
    """逻辑封装"""
    def __init__(self):
        self.players = [
            Player("AI 1", False, 5000), Player("AI 2", False, 5000),
            Player("AI 3", False, 5000), Player("AI 4", False, 5000),
            Player("我", True, 10000)
        ]
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.game_state = "preflop"
        self.current_idx = 4 # 玩家先开始或盲注后
        self.deck = []
        self._new_deck()

    def _new_deck(self):
        self.deck = [Card(s, r) for s in Suit for r in Rank]
        random.shuffle(self.deck)

    def start_hand(self):
        self._new_deck()
        self.community_cards = []
        self.pot = 0
        for p in self.players:
            p.reset_hand()
            p.hand = [self.deck.pop(), self.deck.pop()]
            p.hand[0].face_up = p.is_human
            p.hand[1].face_up = p.is_human
        self.game_state = "preflop"

class MainGameScreen(FloatLayout):
    """主游戏屏幕：负责分层管理 UI，避免全屏重绘"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = TexasHoldem3Game()
        self.anim_mgr = AnimationManager()
        
        # 1. 背景层 (静态)
        with self.canvas.before:
            Color(*COLORS['bg'])
            Rectangle(pos=(0, 0), size=(2000, 2000)) # 覆盖全屏

        # 2. 牌桌层
        self.table_widget = Widget()
        self.add_widget(self.table_widget)
        
        # 3. 玩家层
        self.player_widgets = []
        for p in self.logic.players:
            pw = PlayerUI(p)
            self.player_widgets.append(pw)
            self.add_widget(pw)
            
        # 4. 卡牌层 (动态创建/销毁)
        self.card_layer = FloatLayout()
        self.add_widget(self.card_layer)
        
        # 5. UI 按钮层
        self.ui_layer = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos_hint={'y': 0}, padding=10, spacing=10)
        self._setup_buttons()
        self.add_widget(self.ui_layer)
        
        # 6. 信息提示层
        self.info_label = Label(text="欢迎来到德州扑克3", pos_hint={'center_y': 0.15}, font_size='18sp', color=COLORS['text_gold'])
        self.add_widget(self.info_label)

        self.logic.start_hand()
        self.update_layout()
        Clock.schedule_interval(self.refresh_ui, 1.0/30.0)

    def _setup_buttons(self):
        actions = [("弃牌", "fold", COLORS['btn_red']), ("过牌", "check", COLORS['btn_blue']), ("跟注", "call", COLORS['btn_green'])]
        for text, act, color in actions:
            btn = Button(text=text, background_color=color, background_normal='')
            btn.bind(on_release=lambda x, a=act: self.process_action(a))
            self.ui_layer.add_widget(btn)

    def update_layout(self):
        # 绘制牌桌
        tw, th = Window.width * 0.8, Window.width * 0.9
        self.table_widget.canvas.clear()
        with self.table_widget.canvas:
            Color(*COLORS['table'])
            Ellipse(pos=(Window.width/2 - tw/2, Window.height/2 - th/4), size=(tw, th))
        
        # 放置玩家
        positions = screen_adapter.get_player_positions(self)
        for i, pos in enumerate(positions):
            if i < len(self.player_widgets):
                self.player_widgets[i].pos = pos

    def refresh_ui(self, dt):
        """定期刷新数据，不重建 Widget"""
        for i, pw in enumerate(self.player_widgets):
            pw.is_active = (i == self.logic.current_idx)
            pw.update_ui()
        
        # 如果卡牌层为空，创建初始手牌（示例简化逻辑）
        if not self.card_layer.children:
            self._display_cards()

    def _display_cards(self):
        # 显示公共牌和手牌 (示例)
        self.card_layer.clear_widgets()
        # 仅显示玩家自己的牌作为示例
        me = self.logic.players[4]
        for i, card in enumerate(me.hand):
            cw = CardWidget(card)
            cw.pos = (self.player_widgets[4].x + i*40, self.player_widgets[4].top + 10)
            self.card_layer.add_widget(cw)

    def process_action(self, action):
        self.info_label.text = f"你选择了: {action}"
        # 这里接入游戏逻辑逻辑推进...

class TexasHoldem3App(App):
    def build(self):
        Window.clearcolor = COLORS['bg']
        return MainGameScreen()

if __name__ == '__main__':
    TexasHoldem3App().run()
