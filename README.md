# 防止屏幕休眠工具 (Prevent Sleep Tool)

一个简单的工具，用于防止电脑屏幕进入休眠状态。通过定期移动鼠标来保持系统活动状态，适用于某些限制屏幕休眠的工作环境。

## 功能特点

- 简洁的图形界面
- 可随时启动/停止监控
- 实时显示操作日志
- 最小化系统托盘运行
- 鼠标移动幅度小，不影响正常工作

## 下载和使用

### 方式一：直接使用

1. 从 [Releases](../../releases) 页面下载最新的 `防止睡眠工具.exe`
2. 双击运行即可，无需安装
3. 点击"不要睡觉"按钮开始防止屏幕休眠
4. 点击"停止监听"按钮停止程序
5. 关闭窗口即可完全退出程序

### 方式二：从源码运行

1. 克隆仓库：
   ```bash
   git clone https://github.com/snailuu/prevent-sleep.git
   cd prevent-sleep
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

3. 运行程序：
   ```bash
   python src/prevent_sleep.py
   ```

## 打包方式

如果您想自己打包程序：

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 运行打包脚本：
   ```bash
   python build.py
   ```

3. 打包后的程序位于 `dist` 目录下

## 注意事项

- 由于程序使用了鼠标模拟操作，某些杀毒软件可能会报警，这是正常现象
- 程序仅通过移动鼠标来保持系统活动，不会修改任何系统设置
- 建议在使用前先测试程序是否适合您的工作环境

## 开发相关

- Python 3.6+
- tkinter 用于GUI界面
- pyautogui 用于鼠标控制
- PyInstaller 用于打包

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
