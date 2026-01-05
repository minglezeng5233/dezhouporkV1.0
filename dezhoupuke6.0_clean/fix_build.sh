#!/bin/bash

# 德州扑克3 Android APK构建修复脚本 - 兼容性增强版
# 解决 Python 3.12+ 移除 FancyURLopener 导致的构建失败问题

echo "🚀 开始修复德州扑克3构建环境..."

# 1. 尝试寻找兼容的 Python 版本 (优先使用 3.11)
PYTHON_EXE=""
for cmd in python3.11 python3.10 python3.9 python3; do
    if command -v $cmd &> /dev/null; then
        VERSION=$($cmd --version | cut -d' ' -f2)
        # 检查版本是否小于 3.12
        MAJOR=$(echo $VERSION | cut -d. -f1)
        MINOR=$(echo $VERSION | cut -d. -f2)
        if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 12 ]; then
            PYTHON_EXE=$cmd
            echo "✅ 找到兼容的 Python 版本: $VERSION ($cmd)"
            break
        fi
    fi
done

if [ -z "$PYTHON_EXE" ]; then
    echo "⚠️  未找到 Python 3.11 或更早的稳定版本 (当前 Python 3.12+ 与 Buildozer 存在兼容性问题)"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "💡 建议执行: brew install python@3.11"
    fi
    # 如果没找到，退而求其次使用系统 python3，但可能会失败
    PYTHON_EXE="python3"
    echo "⚠️  尝试使用系统默认 Python 3，可能会遇到之前的错误..."
fi

# 2. 清理旧的虚拟环境
if [ -d "venv" ]; then
    echo "🧹 清理旧的虚拟环境..."
    rm -rf venv
fi

# 3. 创建新的虚拟环境
echo "📦 使用 $PYTHON_EXE 创建 Python 虚拟环境..."
$PYTHON_EXE -m venv venv

# 4. 激活并更新
source venv/bin/activate
echo "⬆️  升级 pip 并安装兼容版本的 buildozer..."
pip install --upgrade pip
pip install "buildozer>=1.5.0" Cython

# 5. 验证安装
if command -v buildozer &> /dev/null; then
    echo "✅ 环境修复完成！"
    echo ""
    echo "🎯 现在请运行以下命令开始构建："
    echo "source venv/bin/activate && ./local_build.sh"
else
    echo "❌ 修复失败，请确保已安装 Python 3.11 (brew install python@3.11)"
fi
