import PyInstaller.__main__

PyInstaller.__main__.run([
    'src/prevent_sleep.py',
    '--name=防止睡眠工具',
    '--windowed',
    '--onefile',
    '--icon=assets/icon.ico',  # 如果您有图标的话
    '--add-data=README.md;.',
]) 