# -*- coding: utf-8 -*-
"""
德州扑克3 - 界面动画效果
增强游戏视觉效果和用户体验
"""

from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Rotate, PushMatrix, PopMatrix
import random

class AnimationManager:
    """动画管理器"""
    
    def __init__(self):
        pass
    
    def fade_in(self, widget, duration=0.5):
        """淡入动画"""
        widget.opacity = 0
        anim = Animation(opacity=1, duration=duration)
        anim.start(widget)
    
    def fade_out(self, widget, duration=0.5):
        """淡出动画"""
        anim = Animation(opacity=0, duration=duration)
        anim.start(widget)
    
    def bounce(self, widget, scale_to=1.2, duration=0.3):
        """弹跳动画 - 需要组件支持 scale 属性"""
        if hasattr(widget, 'scale'):
            original_scale = widget.scale
            anim = Animation(scale=scale_to, duration=duration/2) + \
                   Animation(scale=original_scale, duration=duration/2)
            anim.start(widget)
    
    def shake(self, widget, intensity=10, duration=0.3):
        """震动动画"""
        original_pos = widget.pos[:]
        
        def shake_step(dt):
            widget.pos = (
                original_pos[0] + random.randint(-intensity, intensity),
                original_pos[1] + random.randint(-intensity, intensity)
            )
        
        def reset_pos(dt):
            widget.pos = original_pos
        
        Clock.schedule_interval(shake_step, 0.05)
        Clock.schedule_once(lambda dt: Clock.unschedule(shake_step), duration)
        Clock.schedule_once(reset_pos, duration)

    def deal_card_animation(self, card_widget, target_pos, duration=0.5):
        """发牌动画"""
        anim = Animation(
            pos=target_pos,
            duration=duration,
            transition='out_quad'
        )
        anim.start(card_widget)
        return anim

class ParticleEffect(Widget):
    """粒子效果"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (10, 10)
        self.particles = []
    
    def create_confetti(self, count=20, duration=2.0):
        """创建五彩纸屑效果"""
        colors = [
            (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1),
            (1, 1, 0, 1), (1, 0, 1, 1),
        ]
        
        for i in range(count):
            particle = Widget()
            particle.size = (random.randint(5, 15), random.randint(5, 15))
            particle.pos = (
                self.center_x - particle.width/2,
                self.center_y - particle.height/2
            )
            
            with particle.canvas:
                Color(*random.choice(colors))
                Rectangle(pos=particle.pos, size=particle.size)
            
            anim = Animation(
                x=particle.x + random.randint(-200, 200),
                y=particle.y + random.randint(-200, 200),
                opacity=0,
                duration=duration * random.uniform(0.8, 1.2)
            )
            anim.start(particle)
            
            self.particles.append(particle)
            self.add_widget(particle)
        
        Clock.schedule_once(self._clear_particles, duration + 0.5)
    
    def _clear_particles(self, dt):
        self.clear_widgets()
        self.particles.clear()

class CardFlipAnimation:
    """卡牌翻转动画"""
    
    def flip_card(self, card_widget, duration=0.4):
        """翻转卡牌 - 需要组件支持 rotation_y 属性"""
        if not hasattr(card_widget, 'rotation_y'):
            return
            
        anim1 = Animation(rotation_y=90, duration=duration/2)
        
        def flip_face(instance, value):
            card_widget.card.face_up = not card_widget.card.face_up
            # 翻转属性值到 270 继续完成动画
            card_widget.rotation_y = 270
            anim2 = Animation(rotation_y=360, duration=duration/2)
            anim2.start(card_widget)
            
        anim1.bind(on_complete=flip_face)
        anim1.start(card_widget)
