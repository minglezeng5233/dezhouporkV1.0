# -*- coding: utf-8 -*-
"""
德州扑克3 - 音效管理器
管理游戏音效和背景音乐
"""

import os
import kivy
from kivy.core.audio import SoundLoader
from kivy.properties import BooleanProperty, NumericProperty
from kivy.clock import Clock

class SoundManager:
    """音效管理器"""
    
    def __init__(self):
        self.sound_enabled = True
        self.music_enabled = True
        self.music_volume = 0.5
        self.sound_volume = 0.7
        
        # 音效文件
        self.sounds = {}
        self.music = None
        
        # 预加载音效
        self._load_sounds()
    
    def _load_sounds(self):
        """加载音效文件"""
        sound_files = {
            'deal_card': 'deal_card.wav',
            'chip_drop': 'chip_drop.wav', 
            'button_click': 'button_click.wav',
            'win': 'win.wav',
            'lose': 'lose.wav',
            'fold': 'fold.wav',
            'raise': 'raise.wav',
            'all_in': 'all_in.wav',
            'shuffle': 'shuffle.wav'
        }
        
        # 创建默认音效（使用Kivy内置的简单音效）
        for sound_name, filename in sound_files.items():
            try:
                # 这里可以替换为实际的音效文件路径
                # 暂时使用空字符串，后续可以添加真实音效文件
                self.sounds[sound_name] = None
            except Exception as e:
                print(f"无法加载音效 {sound_name}: {e}")
    
    def play_sound(self, sound_name):
        """播放音效（优化版）"""
        if not self.sound_enabled:
            return
        
        try:
            # 尝试加载音效文件
            sound_path = f'{sound_name}.wav'
            sound = SoundLoader.load(sound_path)
            
            if sound:
                sound.volume = self.sound_volume
                sound.play()
            else:
                # 如果音效文件不存在，创建简单的提示音
                print(f"音效文件不存在: {sound_path}")
        except Exception as e:
            print(f"播放音效失败 {sound_name}: {e}")
    
    def play_system_sound(self, sound_type="click"):
        """播放系统音效（备用方案）"""
        if not self.sound_enabled:
            return
        
        # 创建简单的系统音效
        try:
            # 这里可以添加简单的音效生成逻辑
            # 暂时使用空实现，后续可以集成Kivy的简单音效
            pass
        except Exception as e:
            print(f"播放系统音效失败: {e}")
    
    def play_music(self):
        """播放背景音乐"""
        if not self.music_enabled:
            return
        
        try:
            if self.music:
                self.music.stop()
            
            # 加载背景音乐
            self.music = SoundLoader.load('bg_music.mp3')
            if self.music:
                self.music.volume = self.music_volume
                self.music.loop = True
                self.music.play()
        except Exception as e:
            print(f"播放背景音乐失败: {e}")
    
    def stop_music(self):
        """停止背景音乐"""
        if self.music:
            self.music.stop()
    
    def toggle_sound(self):
        """切换音效开关"""
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled
    
    def toggle_music(self):
        """切换音乐开关"""
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            self.play_music()
        else:
            self.stop_music()
        return self.music_enabled
    
    def set_sound_volume(self, volume):
        """设置音效音量"""
        self.sound_volume = max(0.0, min(1.0, volume))
    
    def set_music_volume(self, volume):
        """设置音乐音量"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.music:
            self.music.volume = self.music_volume

# 游戏音效事件类
class GameSounds:
    """游戏音效事件"""
    
    def __init__(self, sound_manager):
        self.sound_manager = sound_manager
    
    def deal_card(self):
        """发牌音效"""
        self.sound_manager.play_sound('deal_card')
    
    def chip_drop(self):
        """筹码掉落音效"""
        self.sound_manager.play_sound('chip_drop')
    
    def button_click(self):
        """按钮点击音效"""
        self.sound_manager.play_sound('button_click')
    
    def win(self):
        """胜利音效"""
        self.sound_manager.play_sound('win')
    
    def lose(self):
        """失败音效"""
        self.sound_manager.play_sound('lose')
    
    def fold(self):
        """弃牌音效"""
        self.sound_manager.play_sound('fold')
    
    def raise_bet(self):
        """加注音效"""
        self.sound_manager.play_sound('raise')
    
    def all_in(self):
        """全下音效"""
        self.sound_manager.play_sound('all_in')
    
    def shuffle(self):
        """洗牌音效"""
        self.sound_manager.play_sound('shuffle')