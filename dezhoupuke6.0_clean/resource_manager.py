# -*- coding: utf-8 -*-
"""
德州扑克3 - 资源管理器
负责管理游戏中的所有资源文件
"""

import os
import kivy
from kivy.core.image import Image
from kivy.uix.image import Image as KivyImage
from kivy.properties import ObjectProperty, StringProperty
from kivy.logger import Logger

class ResourceManager(object):
    """资源管理器类"""
    
    def __init__(self):
        # 资源路径配置 - 适配精简版本，资源文件在根目录
        self.assets_path = "."
        self.images_path = "."
        
        # 预加载的资源字典
        self.textures = {}
        self.images = {}
        
        # 创建必要的目录结构
        self._create_directories()
        
        Logger.info("ResourceManager: 资源管理器初始化完成")
    
    def _create_directories(self):
        """创建必要的资源目录 - 精简版本不需要创建assets目录"""
        # 精简版本中资源文件已在根目录，不需要创建额外目录
        pass
    
    def load_texture(self, filename, key=None):
        """加载纹理资源"""
        try:
            # 构建完整文件路径 - 精简版本直接使用文件名
            filepath = filename if os.path.isabs(filename) else filename
            
            if not os.path.exists(filepath):
                Logger.warning(f"ResourceManager: 文件不存在 {filepath}")
                return None
            
            # 使用文件路径作为键（如果没有提供自定义键）
            if key is None:
                key = filename
            
            # 加载纹理
            texture = Image(filepath).texture
            self.textures[key] = texture
            
            Logger.info(f"ResourceManager: 加载纹理 {filename} -> {key}")
            return texture
            
        except Exception as e:
            Logger.error(f"ResourceManager: 加载纹理失败 {filename} - {str(e)}")
            return None
    
    def get_texture(self, key):
        """获取已加载的纹理"""
        return self.textures.get(key)
    
    def load_image(self, filename, key=None):
        """加载图像资源"""
        try:
            # 构建完整文件路径 - 精简版本直接使用文件名
            filepath = filename if os.path.isabs(filename) else filename
            
            if not os.path.exists(filepath):
                Logger.warning(f"ResourceManager: 文件不存在 {filepath}")
                return None
            
            # 使用文件路径作为键（如果没有提供自定义键）
            if key is None:
                key = filename
            
            # 加载图像
            image = KivyImage(source=filepath)
            self.images[key] = image
            
            Logger.info(f"ResourceManager: 加载图像 {filename} -> {key}")
            return image
            
        except Exception as e:
            Logger.error(f"ResourceManager: 加载图像失败 {filename} - {str(e)}")
            return None
    
    def get_image(self, key):
        """获取已加载的图像"""
        return self.images.get(key)
    
    def preload_resources(self):
        """预加载常用资源 - 精简版本适配"""
        Logger.info("ResourceManager: 开始预加载资源...")
        
        # 预加载图标和按钮 - 精简版本中资源文件在根目录
        resources_to_load = [
            "icon.png",
            "splash.png", 
            "card_back.png",
            "button.png"
        ]
        
        for resource in resources_to_load:
            if os.path.exists(resource):
                self.load_texture(resource)
            else:
                Logger.warning(f"ResourceManager: 资源文件不存在 {resource}")
        
        Logger.info("ResourceManager: 资源预加载完成")
    
    def unload_resources(self):
        """卸载所有资源"""
        self.textures.clear()
        self.images.clear()
        Logger.info("ResourceManager: 所有资源已卸载")
    
    def get_resource_path(self, filename):
        """获取资源文件的完整路径 - 精简版本适配"""
        return filename if os.path.isabs(filename) else filename
    
    def resource_exists(self, filename):
        """检查资源文件是否存在 - 精简版本适配"""
        filepath = filename if os.path.isabs(filename) else filename
        return os.path.exists(filepath)


# 全局资源管理器实例
_resource_manager = None

def get_resource_manager():
    """获取全局资源管理器实例"""
    global _resource_manager
    if _resource_manager is None:
        _resource_manager = ResourceManager()
    return _resource_manager


def load_texture(filename, key=None):
    """加载纹理（便捷函数）"""
    return get_resource_manager().load_texture(filename, key)

def get_texture(key):
    """获取纹理（便捷函数）"""
    return get_resource_manager().get_texture(key)

def load_image(filename, key=None):
    """加载图像（便捷函数）"""
    return get_resource_manager().load_image(filename, key)

def get_image(key):
    """获取图像（便捷函数）"""
    return get_resource_manager().get_image(key)

def preload_resources():
    """预加载资源（便捷函数）"""
    return get_resource_manager().preload_resources()

def get_resource_path(filename):
    """获取资源路径（便捷函数）"""
    return get_resource_manager().get_resource_path(filename)

def resource_exists(filename):
    """检查资源是否存在（便捷函数）"""
    return get_resource_manager().resource_exists(filename)


if __name__ == "__main__":
    # 测试资源管理器
    manager = ResourceManager()
    manager.preload_resources()
    
    # 测试资源是否存在
    test_files = ["icon.png", "splash.png", "card_back.png", "button.png"]
    for file in test_files:
        exists = manager.resource_exists(file)
        print(f"{file}: {'存在' if exists else '不存在'}")