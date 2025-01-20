# 防止屏幕休眠工具 (Prevent Sleep Tool)

一个简单但功能强大的工具，用于防止电脑屏幕进入休眠状态。通过系统级 API 和多种活动模拟策略来保持系统活跃，适用于需要防止屏幕休眠的工作环境。

## 更新日志

### v1.1.0 (2024-01-20)
- 新增 Windows API 系统级防睡眠支持
- 增加多种防睡眠策略：
  - 随机鼠标移动
  - 模拟按键操作（Scroll Lock）
  - 模拟滚轮操作
  - 模拟文件系统访问
- 优化活动检测间隔（30秒）
- 增强程序稳定性
- 完善异常处理机制

### v1.0.0 (2024-01-16)
- 初始版本发布
- 基础的防睡眠功能
- 图形界面支持
- 实时日志显示

## 功能特点

- 系统级防睡眠（Windows API）
- 多策略活动模拟
- 简洁的图形界面
- 可随时启动/停止监控
- 实时显示操作日志
- 智能活动检测（30秒间隔）
- 稳定可靠的运行机制

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
   # 使用国内镜像源安装依赖
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

3. 运行程序：
   ```bash
   python src/prevent_sleep.py
   ```

## 工作原理

程序通过多种机制防止系统休眠：

1. 系统级防护：
   - 使用 Windows API (SetThreadExecutionState) 
   - 直接告知系统保持活动状态

2. 活动模拟：
   - 随机鼠标移动（小幅度）
   - 模拟按键（Scroll Lock）
   - 模拟滚轮操作
   - 文件系统访问

3. 智能调度：
   - 30秒间隔的活动检测
   - 随机选择不同活动方式
   - 异常自动恢复机制

## 打包方式

如果您想自己打包程序：

1. 安装依赖：
   ```bash
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

2. 运行打包脚本：
   ```bash
   python build.py
   ```

3. 打包后的程序位于 `dist` 目录下

## 注意事项

- 由于使用系统API和模拟操作，某些杀毒软件可能会报警，这是正常现象
- 程序使用多种策略保持系统活动，但不会修改系统设置
- 建议在使用前先测试程序是否适合您的工作环境
- 程序支持随时停止，如有异常可立即关闭

## 技术栈

- Python 3.6+
- Windows API (ctypes)
- tkinter (GUI界面)
- pyautogui (鼠标控制)
- keyboard (按键模拟)
- PyInstaller (程序打包)

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 作者

[snailuu](https://github.com/snailuu)

## 鸣谢

感谢所有贡献者的支持！
