#!/bin/bash
# 德州扑克3 - 本地构建脚本
# 使用虚拟环境解决外部管理的Python环境问题

echo "🚀 开始德州扑克3 Android APK本地构建..."

# 检查是否在虚拟环境中
if [ -z "$VIRTUAL_ENV" ]; then
    echo "🔧 检测到未在虚拟环境中，尝试使用内置虚拟环境..."
    
    # 检查是否已创建虚拟环境
    if [ ! -d "venv" ]; then
        echo "📦 创建Python虚拟环境..."
        python3 -m venv venv
        
        if [ $? -ne 0 ]; then
            echo "❌ 虚拟环境创建失败"
            echo "💡 尝试安装python3-venv: brew install python-tk"
            exit 1
        fi
    fi
    
    # 激活虚拟环境
    echo "🔧 激活虚拟环境..."
    source venv/bin/activate
    
    # 升级pip
    echo "⬆️  升级pip..."
    pip install --upgrade pip
fi

# 检查buildozer是否安装
if ! command -v buildozer &> /dev/null; then
    echo "❌ Buildozer未安装，正在尝试安装..."
    pip install buildozer cython
    
    # 检查安装是否成功
    if ! command -v buildozer &> /dev/null; then
        echo "❌ Buildozer安装失败，请运行修复脚本: ./fix_build.sh"
        exit 1
    fi
fi

# 检查当前目录
if [ ! -f "main.py" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

# 检查依赖文件
if [ ! -f "requirements.txt" ]; then
    echo "❌ 未找到requirements.txt文件，正在创建..."
    cat > requirements.txt << EOF
kivy==2.2.1
pyjnius
requests
EOF
fi

echo "📦 检查系统依赖..."

# 检查Android SDK和NDK（简化检查）
if [ ! -d "$HOME/.buildozer" ]; then
    echo "⚠️  首次运行，需要下载Android SDK/NDK..."
    echo "📥 这可能需要较长时间，请耐心等待..."
fi

echo "🔨 开始构建APK..."

# 清理之前的构建
if [ -d "build" ]; then
    echo "🧹 清理旧构建文件..."
    rm -rf build
fi

if [ -d ".buildozer" ]; then
    echo "🧹 清理构建缓存..."
    rm -rf .buildozer
fi

# 运行构建
echo "🏗️  开始APK构建过程..."
buildozer -v android debug

# 检查构建结果
if ls bin/*.apk 1> /dev/null 2>&1; then
    echo "✅ APK构建成功！"
    echo "📱 生成的APK文件位于: bin/"
    
    # 显示APK信息
    for apk in bin/*.apk; do
        echo "   - $(basename $apk)"
        echo "     大小: $(du -h $apk | cut -f1)"
    done
else
    echo "❌ APK构建失败，请检查错误信息"
    echo "🔧 常见问题排查:"
    echo "   1. 检查Java JDK是否安装"
    echo "   2. 检查Android SDK路径配置"
    echo "   3. 检查网络连接（需要下载依赖）"
    exit 1
fi

echo "🎉 构建完成！"
echo ""
echo "📋 安装指南:"
echo "   1. 将APK文件传输到Android设备"
echo "   2. 在设置中允许'未知来源'安装"
echo "   3. 使用文件管理器安装APK"
echo "   4. 运行德州扑克3应用"
echo ""
echo "🔧 调试信息:"
echo "   - 查看详细日志: buildozer android debug 2>&1 | tee build.log"
echo "   - 清理构建: buildozer android clean"
echo "   - 发布版本: buildozer android release"