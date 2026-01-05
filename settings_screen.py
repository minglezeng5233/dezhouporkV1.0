# -*- coding: utf-8 -*-
"""
德州扑克3 - 设置界面
游戏设置和音效控制
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.properties import BooleanProperty, NumericProperty

class SettingsScreen(BoxLayout):
    """设置界面"""
    
    def __init__(self, sound_manager, **kwargs):
        super().__init__(**kwargs)
        self.sound_manager = sound_manager
        self.orientation = 'vertical'
        # 使用百分比padding和spacing
        self.padding = ['5%', '5%']
        self.spacing = '2%'
        
        self._create_ui()
    
    def _create_ui(self):
        """创建设置界面"""
        # 标题
        title = Label(
            text='游戏设置',
            font_size='4%',  # 使用百分比字体
            size_hint=(1, 0.1)
        )
        self.add_widget(title)
        
        # 音效设置
        sound_section = self._create_sound_section()
        self.add_widget(sound_section)
        
        # 游戏设置
        game_section = self._create_game_section()
        self.add_widget(game_section)
        
        # 按钮区域
        button_section = self._create_button_section()
        self.add_widget(button_section)
    
    def _create_sound_section(self):
        """创建音效设置区域"""
        section = BoxLayout(orientation='vertical', size_hint=(1, 0.3))
        
        # 音效标题
        sound_title = Label(text='音效设置', font_size='2.5%')  # 使用百分比字体
        section.add_widget(sound_title)
        
        # 音效开关
        sound_toggle_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        sound_toggle_layout.add_widget(Label(text='音效:', font_size='2%'))  # 使用百分比字体
        
        self.sound_toggle = ToggleButton(
            text='开启' if self.sound_manager.sound_enabled else '关闭',
            state='down' if self.sound_manager.sound_enabled else 'normal',
            font_size='2%'  # 使用百分比字体
        )
        self.sound_toggle.bind(on_press=self._toggle_sound)
        sound_toggle_layout.add_widget(self.sound_toggle)
        section.add_widget(sound_toggle_layout)
        
        # 音效音量
        sound_volume_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        sound_volume_layout.add_widget(Label(text='音效音量:', font_size='2%'))  # 使用百分比字体
        
        self.sound_slider = Slider(
            min=0, max=100, value=self.sound_manager.sound_volume * 100,
            size_hint=(0.6, 1)
        )
        self.sound_slider.bind(value=self._on_sound_volume_change)
        sound_volume_layout.add_widget(self.sound_slider)
        section.add_widget(sound_volume_layout)
        
        # 音乐开关
        music_toggle_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        music_toggle_layout.add_widget(Label(text='背景音乐:', font_size='2%'))  # 使用百分比字体
        
        self.music_toggle = ToggleButton(
            text='开启' if self.sound_manager.music_enabled else '关闭',
            state='down' if self.sound_manager.music_enabled else 'normal',
            font_size='2%'  # 使用百分比字体
        )
        self.music_toggle.bind(on_press=self._toggle_music)
        music_toggle_layout.add_widget(self.music_toggle)
        section.add_widget(music_toggle_layout)
        
        # 音乐音量
        music_volume_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        music_volume_layout.add_widget(Label(text='音乐音量:', font_size='2%'))  # 使用百分比字体
        
        self.music_slider = Slider(
            min=0, max=100, value=self.sound_manager.music_volume * 100,
            size_hint=(0.6, 1)
        )
        self.music_slider.bind(value=self._on_music_volume_change)
        music_volume_layout.add_widget(self.music_slider)
        section.add_widget(music_volume_layout)
        
        return section
    
    def _create_game_section(self):
        """创建游戏设置区域"""
        section = BoxLayout(orientation='vertical', size_hint=(1, 0.2))
        
        # 游戏设置标题
        game_title = Label(text='游戏设置', font_size='2.5%')  # 使用百分比字体
        section.add_widget(game_title)
        
        # AI难度设置
        difficulty_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.5))
        difficulty_layout.add_widget(Label(text='AI难度:', font_size='2%'))  # 使用百分比字体
        
        self.difficulty_slider = Slider(
            min=1, max=3, value=2,
            size_hint=(0.6, 1)
        )
        difficulty_layout.add_widget(self.difficulty_slider)
        section.add_widget(difficulty_layout)
        
        return section
    
    def _create_button_section(self):
        """创建按钮区域"""
        section = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        
        # 保存按钮
        save_btn = Button(text='保存设置', font_size='2.5%')  # 使用百分比字体
        save_btn.bind(on_press=self._save_settings)
        section.add_widget(save_btn)
        
        # 取消按钮
        cancel_btn = Button(text='取消', font_size='2.5%')  # 使用百分比字体
        cancel_btn.bind(on_press=self._cancel)
        section.add_widget(cancel_btn)
        
        return section
    
    def _toggle_sound(self, instance):
        """切换音效开关"""
        enabled = self.sound_manager.toggle_sound()
        instance.text = '开启' if enabled else '关闭'
    
    def _toggle_music(self, instance):
        """切换音乐开关"""
        enabled = self.sound_manager.toggle_music()
        instance.text = '开启' if enabled else '关闭'
    
    def _on_sound_volume_change(self, instance, value):
        """音效音量变化"""
        self.sound_manager.set_sound_volume(value / 100.0)
    
    def _on_music_volume_change(self, instance, value):
        """音乐音量变化"""
        self.sound_manager.set_music_volume(value / 100.0)
    
    def _save_settings(self, instance):
        """保存设置"""
        # 这里可以保存到配置文件
        print("设置已保存")
        self.parent.parent.dismiss()
    
    def _cancel(self, instance):
        """取消设置"""
        self.parent.parent.dismiss()

class SettingsPopup(Popup):
    """设置弹窗"""
    
    def __init__(self, sound_manager, **kwargs):
        super().__init__(**kwargs)
        self.title = '游戏设置'
        # 使用相对尺寸，适应不同屏幕
        self.size_hint = (0.85, 0.85)
        self.auto_dismiss = False
        
        self.content = SettingsScreen(sound_manager)

# 游戏帮助界面
class HelpPopup(Popup):
    """帮助弹窗"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = '游戏帮助'
        self.size_hint = (0.8, 0.6)
        self.auto_dismiss = True
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        help_text = """德州扑克游戏规则：

1. 每个玩家发2张底牌
2. 翻牌圈：发3张公共牌
3. 转牌圈：发第4张公共牌  
4. 河牌圈：发第5张公共牌
5. 用任意5张牌组成最好牌型

牌型大小顺序：
同花顺 > 四条 > 葫芦 > 同花 > 顺子 > 三条 > 两对 > 一对 > 高牌

操作说明：
• 弃牌：放弃当前手牌
• 过牌：不下注，保持当前状态
• 跟注：匹配当前下注额
• 加注：增加下注金额
• 全下：押上所有筹码
"""
        
        help_label = Label(
            text=help_text,
            font_size='14sp',
            text_size=(self.size[0] - 40, None),
            halign='left',
            valign='top'
        )
        content.add_widget(help_label)
        
        close_btn = Button(text='关闭', size_hint=(1, 0.1))
        close_btn.bind(on_press=lambda x: self.dismiss())
        content.add_widget(close_btn)
        
        self.content = content