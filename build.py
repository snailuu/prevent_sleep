import PyInstaller.__main__
import os
import shutil
import sys
import time
import psutil  # 需要先安装：pip install psutil

def is_process_running(process_name):
    """检查指定名称的进程是否在运行"""
    for proc in psutil.process_iter(['name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def force_delete_file(file_path, max_attempts=3, delay=1):
    """强制删除文件，带有重试机制"""
    for attempt in range(max_attempts):
        try:
            if os.path.exists(file_path):
                os.chmod(file_path, 0o777)  # 尝试修改文件权限
                os.remove(file_path)
            return True
        except Exception as e:
            print(f"删除文件失败 (尝试 {attempt + 1}/{max_attempts}): {e}")
            if attempt < max_attempts - 1:
                time.sleep(delay)
    return False

def cleanup():
    """清理旧的构建文件"""
    print("正在清理旧的构建文件...")
    
    # 检查程序是否在运行
    if is_process_running("防止睡眠工具.exe"):
        print("警告: 检测到防止睡眠工具正在运行，请先关闭程序！")
        sys.exit(1)
    
    paths_to_remove = ['build', 'dist', '防止睡眠工具.spec']
    for path in paths_to_remove:
        try:
            if os.path.isfile(path):
                if not force_delete_file(path):
                    print(f"无法删除文件: {path}")
                    sys.exit(1)
            elif os.path.isdir(path):
                retries = 3
                for i in range(retries):
                    try:
                        shutil.rmtree(path, ignore_errors=True)
                        break
                    except Exception as e:
                        if i == retries - 1:
                            print(f"无法删除目录 {path}: {e}")
                            sys.exit(1)
                        time.sleep(1)
        except Exception as e:
            print(f"清理 {path} 时出错: {e}")

def main():
    """主函数"""
    try:
        # 确保 assets 目录存在
        if not os.path.exists('assets'):
            os.makedirs('assets')

        # 执行清理
        cleanup()

        print("开始打包程序...")
        # 执行打包
        PyInstaller.__main__.run([
            'src/prevent_sleep.py',
            '--name=防止睡眠工具',
            '--windowed',  # 不显示控制台窗口
            '--onefile',   # 打包成单个文件
            '--clean',     # 清理临时文件
            '--noconfirm', # 不询问确认
            '--add-data=README.md;.',
        ])
        
        print("打包完成！")
        print(f"可执行文件位置: {os.path.abspath('dist/防止睡眠工具.exe')}")
        
    except Exception as e:
        print(f"打包过程中出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 