import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import threading
import sys
import queue
import platform

class SmartPipInstaller:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("智能pip安装工具")
        self.window.geometry("700x400")
        
        # 更新pip源列表，添加更多国内镜像
        self.pip_sources = [
            "https://pypi.org/simple",  # 官方源
            "https://pypi.tuna.tsinghua.edu.cn/simple",  # 清华源
            "https://mirrors.aliyun.com/pypi/simple",  # 阿里源
            "https://pypi.mirrors.ustc.edu.cn/simple",  # 中科大源
            "https://mirror.baidu.com/pypi/simple",  # 百度源
            "http://pypi.douban.com/simple",  # 豆瓣源
            "https://mirror.sjtu.edu.cn/pypi/web/simple",  # 上海交大源
            "http://mirrors.cloud.tencent.com/pypi/simple",  # 腾讯源
            "http://pypi.hustunique.com/simple",  # 华中科大源
            "http://mirrors.sohu.com/Python/",  # 搜狐源
            "https://pypi.hustunique.com/",  # 华中理工源
            "http://pypi.sdutlinux.org/simple/",  # 山东理工源
            "https://mirror.sjtu.edu.cn/pypi/web/simple/",  # 上海交通大学源
            "http://mirrors.yun-idc.com/pypi/simple/",  # 云IDC源
            "https://mirrors.pku.edu.cn/pypi/simple/",  # 北京大学源
            "https://mirrors.zju.edu.cn/pypi/simple/",  # 浙江大学源
            "https://mirrors.hit.edu.cn/pypi/simple/",  # 哈工大源
            "https://mirrors.neusoft.edu.cn/pypi/simple/",  # 东软信息学院源
            "https://mirrors.cqu.edu.cn/pypi/simple/",  # 重庆大学源
            "https://mirrors.bfsu.edu.cn/pypi/web/simple/",  # 北京外国语大学源
            "https://mirrors.sjtug.sjtu.edu.cn/pypi/web/simple/",  # 上海交大源(SJTUG)
            "https://mirrors.nju.edu.cn/pypi/web/simple/",  # 南京大学源
            "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/",  # 清华大学源(镜像站)
            "https://mirrors.huaweicloud.com/repository/pypi/simple/",  # 华为云源
            "https://repo.huaweicloud.com/repository/pypi/simple/",  # 华为云源(备用)
            "https://mirrors.cloud.tencent.com/pypi/simple/",  # 腾讯云源
            "https://mirrors.aliyun.com/pypi/simple/",  # 阿里云源(备用)
            "https://mirrors.163.com/pypi/simple/",  # 网易源
            "https://mirrors.jlu.edu.cn/pypi/simple/",  # 吉林大学源
            "https://mirrors.dlut.edu.cn/pypi/simple/",  # 大连理工源
            "https://mirrors.nwafu.edu.cn/pypi/simple/",  # 西北农林科技大学源
            "https://mirrors.sustech.edu.cn/pypi/simple/",  # 南方科技大学源
            "https://mirrors.njupt.edu.cn/pypi/simple/",  # 南京邮电大学源
            "https://mirrors.scau.edu.cn/pypi/simple/",  # 华南农业大学源
            "https://mirrors.dgut.edu.cn/pypi/simple/",  # 东莞理工学院源
            "https://mirrors.bit.edu.cn/pypi/simple/",  # 北京理工大学源
            "https://mirrors.bupt.edu.cn/pypi/simple/",  # 北京邮电大学源
            "https://mirrors.sdu.edu.cn/pypi/simple/",  # 山东大学源
            "https://mirrors.csu.edu.cn/pypi/simple/",  # 中南大学源
            "https://mirrors.hnu.edu.cn/pypi/simple/",  # 湖南大学源
            "https://mirrors.sysu.edu.cn/pypi/simple/",  # 中山大学源
            "https://mirrors.xjtu.edu.cn/pypi/simple/",  # 西安交通大学源
            "https://mirrors.seu.edu.cn/pypi/simple/",  # 东南大学源
            "https://mirrors.nwu.edu.cn/pypi/simple/",  # 西北大学源
            "https://mirrors.cpu.edu.cn/pypi/simple/",  # 中国药科大学源
            "https://mirrors.usts.edu.cn/pypi/simple/",  # 苏州科技大学源
            "https://mirrors.gzhu.edu.cn/pypi/simple/",  # 广州大学源
            "https://mirrors.qlu.edu.cn/pypi/simple/",  # 齐鲁工业大学源
            "https://pypi.byrio.org/simple/",  # 北青源
            "https://pypi.nyist.edu.cn/simple/"  # 南阳理工学院源
        ]
        
        self.setup_gui()
        
    def setup_gui(self):
        # 包名输入框
        frame = ttk.Frame(self.window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="请输入包名:").grid(row=0, column=0, sticky=tk.W)
        self.package_entry = ttk.Entry(frame, width=40)
        self.package_entry.grid(row=0, column=1, padx=5)
        self.package_entry.bind('<KeyRelease>', self.process_input)
        
        # 按钮框架
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=0, column=2, padx=5)
        
        # 搜索按钮
        self.search_button = ttk.Button(button_frame, text="搜索", command=self.start_search)
        self.search_button.grid(row=0, column=0, padx=2)
        
        # 安装按钮
        self.install_button = ttk.Button(button_frame, text="安装", command=self.start_installation, state='disabled')
        self.install_button.grid(row=0, column=1, padx=2)
        
        # 导入whl按钮
        self.whl_button = ttk.Button(button_frame, text="导入whl", command=self.install_whl)
        self.whl_button.grid(row=0, column=2, padx=2)
        
        # 输出区域
        self.log_area = scrolledtext.ScrolledText(self.window, width=80, height=20)
        self.log_area.grid(row=1, column=0, padx=10, pady=10)
        
        # 进度条
        self.progress = ttk.Progressbar(self.window, length=680, mode='determinate')
        self.progress.grid(row=2, column=0, padx=10, pady=5)
        
        self.message_queue = queue.Queue()
        self.window.after(100, self.check_queue)

    def log(self, message):
        self.message_queue.put(message)

    def check_queue(self):
        while not self.message_queue.empty():
            message = self.message_queue.get()
            self.log_area.insert(tk.END, message + '\n')
            self.log_area.see(tk.END)
        self.window.after(100, self.check_queue)

    def install_package(self, package_name):
        total_sources = len(self.pip_sources)
        progress_step = 100 / total_sources
        
        for i, source in enumerate(self.pip_sources):
            self.log(f"\n尝试使用源: {source}")
            try:
                cmd = [sys.executable, "-m", "pip", "install", package_name, "-i", source]
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                
                stdout, stderr = process.communicate()
                
                if process.returncode == 0:
                    self.log(f"安装成功！\n{stdout}")
                    self.progress['value'] = 100
                    return True
                else:
                    self.log(f"从该源安装失败: {stderr}")
                    if "No matching distribution found" in stderr:
                        self.log("\n提示：如果您有对应的.whl文件，可以点击\"导入whl\"按钮进行安装")
                
            except Exception as e:
                self.log(f"安装出错: {str(e)}")
            
            self.progress['value'] = (i + 1) * progress_step
        
        self.log("\n所有源都尝试失败，安装未成功完成。")
        self.log("\n提示：如果您有对应的.whl文件，可以点击\"导入whl\"按钮进行安装")
        return False

    def start_search(self):
        package_name = self.package_entry.get().strip()
        if not package_name:
            self.log("请输入要安装的包名！")
            return
        
        self.log_area.delete(1.0, tk.END)
        self.progress['value'] = 0
        self.log(f"正在搜索包: {package_name}")
        self.install_button.configure(state='disabled')
        
        def search_thread():
            try:
                # 尝使用pip show命令
                cmd = [sys.executable, "-m", "pip", "show", package_name]
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                stdout, stderr = process.communicate()
                
                if process.returncode == 0:
                    self.log("\n找到包信息：")
                    self.log(stdout)
                    self.log("\n该包已经安装。是否要重新安装？")
                else:
                    # 尝试使用pip index命令
                    cmd = [sys.executable, "-m", "pip", "index", "versions", package_name]
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True
                    )
                    stdout, stderr = process.communicate()
                    
                    if process.returncode == 0 and stdout:
                        self.log("\n找到包版本信息：")
                        self.log(stdout)
                    else:
                        self.log(f"\n未找到包 '{package_name}' 的相关信息")
                        self.log("\n您可以：")
                        self.log("1. 检查包名是否正确")
                        self.log("2. 尝试使用其他常见的包名形式，例如：")
                        self.log("   - opencv-python (而不是 cv2)")
                        self.log("   - pillow (而不是 PIL)")
                        self.log("   - python-libtorrent (而不是 libtorrent)")
                        self.log("   - scikit-learn (而不是 sklearn)")
                        self.log("   - beautifulsoup4 (而不是 bs4)")
                
                # 启用安装按钮
                self.install_button.configure(state='normal')
                
            except Exception as e:
                self.log(f"搜索出错: {str(e)}")
                self.install_button.configure(state='normal')
        
        thread = threading.Thread(target=search_thread)
        thread.daemon = True
        thread.start()

    def start_installation(self):
        package_name = self.package_entry.get().strip()
        if not package_name:
            self.log("请输入要安装的包名！")
            return
        
        self.log("\n开始安装...")
        self.install_button.configure(state='disabled')
        
        def install_thread():
            self.install_package(package_name)
            self.install_button.configure(state='normal')
        
        thread = threading.Thread(target=install_thread)
        thread.daemon = True
        thread.start()

    def run(self):
        self.window.mainloop()

    def process_input(self, event):
        text = self.package_entry.get().strip()
        # 处理 "pip install package" 格式
        if text.lower().startswith('pip install '):
            package_name = text[11:].strip()
            self.package_entry.delete(0, tk.END)
            self.package_entry.insert(0, package_name)
        # 处理 "pip -i source install package" 格式
        elif text.lower().startswith('pip -i '):
            parts = text.split()
            if 'install' in parts:
                package_name = parts[parts.index('install') + 1].strip()
                self.package_entry.delete(0, tk.END)
                self.package_entry.insert(0, package_name)
        # 处理 "python -m pip install package" 格式
        elif text.lower().startswith('python -m pip'):
            parts = text.split()
            if 'install' in parts:
                package_name = parts[parts.index('install') + 1].strip()
                self.package_entry.delete(0, tk.END)
                self.package_entry.insert(0, package_name)
        # 处理 "conda install package" 格式
        elif text.lower().startswith('conda install '):
            package_name = text[13:].strip()
            self.package_entry.delete(0, tk.END)
            self.package_entry.insert(0, package_name)

    def install_whl(self):
        from tkinter import filedialog
        
        # 打开文件选择对话框，限制文件类型为.whl
        whl_path = filedialog.askopenfilename(
            title="选择要安装的whl文件",
            filetypes=[("Wheel files", "*.whl"), ("All files", "*.*")]
        )
        
        if not whl_path:
            return
        
        self.log(f"\n开始安装whl文件: {whl_path}")
        self.progress['value'] = 0
        
        def whl_install_thread():
            try:
                # 使用pip安装whl文件
                cmd = [sys.executable, "-m", "pip", "install", whl_path]
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                
                stdout, stderr = process.communicate()
                
                if process.returncode == 0:
                    self.log("whl文件安装成功！")
                    self.log(stdout)
                    self.progress['value'] = 100
                else:
                    self.log(f"whl文件安装失败: {stderr}")
                    if "is not a supported wheel on this platform" in stderr:
                        self.log("\n错误原因：当前whl文件与您的Python版本或系统平台不兼容")
                        self.log("建议：")
                        self.log("1. 检查您的Python版本和系统架构")
                        self.log(f"   - 当前Python版本: {sys.version}")
                        self.log(f"   - 系统架构: {platform.architecture()[0]}")
                        self.log("2. 下载与您的系统匹配的whl文件")
                        self.log("3. 或者尝试从源代码安装")
                    self.progress['value'] = 0
            
            except Exception as e:
                self.log(f"安装过程出错: {str(e)}")
                self.progress['value'] = 0
        
        thread = threading.Thread(target=whl_install_thread)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    app = SmartPipInstaller()
    app.run()