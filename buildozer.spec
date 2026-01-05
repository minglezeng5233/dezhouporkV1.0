[app]

# 应用标题
title = 德州扑克3

# 包名（必须唯一）
package.name = texasholdem3

# 域名（反转的包名）
package.domain = org.poker

# 源代码目录
source.dir = .

# 主程序文件
source.main = main.py

# 支持的安卓版本
android.api = 33
android.minapi = 21
android.ndk = 25b

# SDK和NDK路径配置 - 移除硬编码路径，让Buildozer在构建时自动下载或从环境变量读取
# android.sdk_path = /home/runner/.buildozer/android/platform/android-sdk
# android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b
# android.ant_path = /usr/share/ant

# 权限要求
android.permissions = INTERNET,VIBRATE

# 屏幕方向（竖屏优化）
orientation = portrait

# 全屏模式
fullscreen = 1

# 包含的模块
requirements = python3,kivy==2.2.1,openssl,requests,pyjnius

# 包含的文件模式 - 确保包含音效文件
include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf,json,wav,mp3

# 排除的文件模式
exclude_exts = .pyc,.pyo,.git,.gitignore,.DS_Store

# 图标文件
icon.filename = %(source.dir)s/icon.png

# 启动画面
presplash.filename = %(source.dir)s/splash.png

# 资源文件配置
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf,json,wav,mp3
source.include_patterns = *,sounds/*

# 应用版本
version = 3.0.0
version.code = 1

author = Poker Developer
description = 德州扑克3 - 专业手游版，基于Kivy框架的移动端优化版本

log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
# 包含的架构
android.arch = armeabi-v7a,arm64-v8a
android.theme = @android:style/Theme.NoTitleBar.Fullscreen
android.touchscreen_type = finger
android.screen_size = normal,large,xlarge
android.screen_density = mdpi,hdpi,xhdpi,xxhdpi
android.app_category = game
android.multiwindow_mode = none
