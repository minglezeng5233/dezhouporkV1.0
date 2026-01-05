# 德州扑克3 - Android APK构建指南

## 快速开始

### 方法一：GitHub Actions自动构建（推荐）

1. 确保你的仓库包含 `.github/workflows/build-apk.yml` 文件
2. 推送代码到main/master分支
3. 在GitHub仓库的"Actions"标签页查看构建进度
4. 构建完成后，在"Releases"页面下载APK

### 方法二：本地构建

```bash
# 1. 克隆仓库
git clone [你的仓库URL]
cd 德州扑克3

# 2. 设置Python环境（推荐Python 3.11）
python3.11 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install buildozer cython

# 4. 构建APK
buildozer -v android debug

# 5. 生成的APK在 bin/ 目录
```

### 方法三：使用Docker构建

```bash
# 使用官方Kivy构建镜像
docker run --rm -v $(pwd):/src kivy/buildozer android debug
```

## 构建要求

- Python 3.8-3.11（不支持3.12+）
- Java JDK 8或11
- 至少5GB可用磁盘空间
- 稳定的网络连接

## 项目结构

```
德州扑克3/
├── main.py              # 主程序
├── buildozer.spec       # 构建配置
├── requirements.txt     # Python依赖
├── assets/             # 资源文件
├── .github/workflows/  # GitHub Actions
└── bin/               # 生成的APK
```

## 常见问题

### Q: 构建失败怎么办？
A: 检查Python版本是否为3.11或更早版本

### Q: 如何更新版本？
A: 修改 buildozer.spec 中的 version 和 version.code

### Q: APK太大怎么办？
A: 优化资源文件，排除不必要的模块

## 联系方式

如有问题，请在GitHub Issues中反馈。