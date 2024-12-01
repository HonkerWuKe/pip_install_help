import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import threading
import sys
import queue
import platform
import requests
import os
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageTk
import random
import string

class SmartPipInstaller:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("智能pip安装工具")
        self.window.geometry("700x400")
        
        # 初始化消息队列
        self.message_queue = queue.Queue()
        
        # 初始化源列表
        self.pip_sources = [
            "https://pypi.org/simple",  # 官方源（保持在第一位）
            "https://pypi.tuna.tsinghua.edu.cn/simple",  # 清华源
            "https://mirrors.aliyun.com/pypi/simple",  # 阿里源
            "https://pypi.mirrors.ustc.edu.cn/simple",  # 中科大源
            "https://mirror.baidu.com/pypi/simple",  # 百度源
            "http://pypi.douban.com/simple",  # 豆瓣源
            "https://mirror.sjtu.edu.cn/pypi/web/simple",  # 上海交大源
            "http://mirrors.cloud.tencent.com/pypi/simple",  # 腾讯源
            "http://pypi.hustunique.com/simple",  # 华中源
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
            "https://repo.huaweicloud.com/repository/pypi/simple/",  # 为云源(备用)
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
            "https://pypi.nyist.edu.cn/simple/",  # 南阳理工学院源
            # 北美镜像
            "https://mirrors.ocf.berkeley.edu/pypi/simple/",  # 伯克利大学源
            "https://mirrors.mit.edu/pypi/simple/",  # MIT源
            "https://mirrors.rutgers.edu/pypi/simple/",  # 罗格斯大学源
            
            # 欧洲镜像
            "https://ftp.acc.umu.se/mirror/pypi.python.org/simple/",  # 瑞典学术计算机网络源
            "https://mirrors.dotsrc.org/pypi/simple/",  # 丹麦源
            "https://mirrors.ukfast.co.uk/sites/pypi.python.org/simple/",  # 英国源
            "https://mirrors.xtom.de/pypi/simple/",  # 德国源
            "https://mirrors.xtom.nl/pypi/simple/",  # 兰源
            "https://mirrors.xtom.ee/pypi/simple/",  # 爱沙尼亚源
            
            # 亚洲镜像（除中国外）
            "https://mirrors.xtom.jp/pypi/simple/",  # 日本源
            "https://mirrors.xtom.hk/pypi/simple/",  # 香港源
            "https://ftp.jaist.ac.jp/pub/pkgsrc/pypi/simple/",  # 日本先进科学技术研究所源
            "https://mirrors.xtom.kr/pypi/simple/",  # 韩国源
            
            # 大洋洲镜像
            "https://mirrors.xtom.au/pypi/simple/",  # 澳大利亚源
            
            # 其他地区镜像
            "https://pypi.za.ramiyer.me/simple/",  # 南非源
            "https://mirrors.sarata.com/pypi/simple/",  # 全球CDN源
            
            # 云服务提供商镜像
            "https://mirrors.cloud.tencent.com/pypi/simple/",  # 腾讯云全球源
            "https://mirrors.amazonaws.com/pypi/simple/",  # AWS源
            "https://mirrors.azure.cn/pypi/simple/",  # 微软Azure源
            "https://mirrors.openstack.org/pypi/simple/",  # OpenStack源
            
            # 备用官方镜像
            "https://pypi.io/simple/",  # PyPI备用域名
            "https://pypi.python.org/simple/",  # PyPI另一个备用域名
            "https://test.pypi.org/simple/",  # PyPI测试源
            # 美其镜像
            "https://mirrors.princeton.edu/pypi/simple/",  # 普林斯顿大学源
            "https://mirrors.stanford.edu/pypi/simple/",  # 斯坦福大学源
            "https://mirrors.uwaterloo.ca/pypi/simple/",  # 滑铁卢大学源（加拿大）
            "https://mirrors.ucr.edu/pypi/simple/",  # 加州大学河滨分校源
            
            # 欧洲其他镜像
            "https://mirrors.tu-berlin.de/pypi/simple/",  # 柏林工业大学源
            "https://pypi.uib.no/simple/",  # 卑尔根大学源（挪威）
            "https://mirrors.nxthost.com/pypi/simple/",  # 瑞士源
            "https://mirrors.evoluso.com/pypi/simple/",  # 法国源
            "https://mirrors.up.pt/pypi/simple/",  # 波尔图大学源（葡萄牙）
            
            # 亚洲其他镜像
            "https://mirrors.snu.ac.kr/pypi/simple/",  # 首尔国立大学源
            "https://mirrors.nyist.edu.tw/pypi/simple/",  # 台湾源
            "https://mirrors.iisc.ac.in/pypi/simple/",  # 印度科学院源
            "https://mirrors.ntu.edu.sg/pypi/simple/",  # 新加坡国立大学源
            
            # 大洋洲其他镜像
            "https://mirrors.unesp.br/pypi/simple/",  # 巴西源
            "https://mirrors.mel.nist.gov/pypi/simple/",  # NIST源
            
            # 更多云服务提供商镜像
            "https://mirrors.cloud.google.com/pypi/simple/",  # Google Cloud源
            "https://mirrors.oracle.com/pypi/simple/",  # Oracle Cloud源
            "https://mirrors.digitalocean.com/pypi/simple/",  # DigitalOcean源
            
            # 更多CDN和备用镜像
            "https://pypi.fury.io/simple/",  # Gemfury CDN源
            "https://pypi.anaconda.org/simple/",  # Anaconda源
            "https://download.pytorch.org/whl/",  # PyTorch专用源
            "https://download.tensorflow.org/whl/",  # TensorFlow专用源
            "https://jfrog.com/artifactory/api/pypi/pypi/simple"  # JFrog Artifactory源
        ]
        
        # 在后台线程中检测地理位置
        threading.Thread(target=self.detect_location, daemon=True).start()
        
        # 设置GUI
        self.setup_gui()
        
    def setup_gui(self):
        # 设置窗口最小尺寸
        self.window.minsize(800, 500)
        
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重，使窗口可调整大小
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # 顶部操作区域
        top_frame = ttk.LabelFrame(main_frame, text="包管理", padding="5")
        top_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        top_frame.grid_columnconfigure(1, weight=1)
        
        # 包名输入区域
        ttk.Label(top_frame, text="包名:").grid(row=0, column=0, padx=(5, 2))
        self.package_entry = ttk.Entry(top_frame)
        self.package_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        self.package_entry.bind('<KeyRelease>', self.process_input)
        
        # 按钮区域
        button_frame = ttk.Frame(top_frame)
        button_frame.grid(row=0, column=2, padx=5)
        
        # 创建按钮，使用统一的宽度
        button_width = 10
        self.search_button = ttk.Button(button_frame, text="搜索", width=button_width, command=self.start_search)
        self.search_button.pack(side=tk.LEFT, padx=2)
        
        self.install_button = ttk.Button(button_frame, text="安装", width=button_width, 
                                       command=self.start_installation, state='disabled')
        self.install_button.pack(side=tk.LEFT, padx=2)
        
        self.whl_button = ttk.Button(button_frame, text="导入whl", width=button_width, command=self.install_whl)
        self.whl_button.pack(side=tk.LEFT, padx=2)
        
        self.clean_button = ttk.Button(button_frame, text="卸载包", width=button_width, command=self.clean_pip_cache)
        self.clean_button.pack(side=tk.LEFT, padx=2)
        
        # 日志区域
        log_frame = ttk.LabelFrame(main_frame, text="安装日志", padding="5")
        log_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(0, weight=1)
        
        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=20)
        self.log_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 进度条区域
        progress_frame = ttk.LabelFrame(main_frame, text="安装进度", padding="5")
        progress_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        progress_frame.grid_columnconfigure(0, weight=1)
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # 设置窗口标题
        self.window.title("智能pip安装工具 - v2.0")
        
        # 设置窗口图标（如果有的话）
        try:
            self.window.iconbitmap("icon.ico")
        except:
            pass
        
        # 设置窗口主题样式
        style = ttk.Style()
        style.configure('TLabelframe', padding=5)
        style.configure('TButton', padding=3)
        
        # 初始化信息队列检查
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
        
        # 记录成功的源
        successful_source = None
        
        for i, source in enumerate(self.pip_sources):
            # 跳过已知无效的源
            if source.startswith('http://'):  # 跳过不安全的http源
                continue
            
            self.log(f"\n尝试使用源: {source}")
            try:
                # 先测试源的连接性
                try:
                    test_response = requests.get(source, timeout=5)
                    if test_response.status_code != 200:
                        self.log(f"源 {source} 无法访问，跳过")
                        continue
                except:
                    self.log(f"源 {source} 连接超时，跳过")
                    continue
                
                # 安装包
                cmd = [
                    sys.executable, "-m", "pip", 
                    "install", package_name, 
                    "-i", source,
                    "--timeout", "30",
                    "--retries", "2"
                ]
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                
                try:
                    stdout, stderr = process.communicate(timeout=60)
                    
                    if process.returncode == 0:
                        self.log(f"安装成功！\n{stdout}")
                        successful_source = source  # 记录成功的源
                        self.progress['value'] = 100
                        
                        # 将成功的源移到列表前面，下次优先使用
                        if source != self.pip_sources[0]:
                            self.pip_sources.remove(source)
                            self.pip_sources.insert(0, source)
                        
                        return True
                        
                except subprocess.TimeoutExpired:
                    process.kill()
                    self.log(f"源 {source} 响应超时，尝试下一个源")
                    
            except Exception as e:
                self.log(f"安装出错: {str(e)}")
            
            self.progress['value'] = (i + 1) * progress_step
        
        if not successful_source:
            self.log("\n所有源都尝试失败，安装未成功完成。")
        return False

    def start_search(self):
        package_name = self.package_entry.get().strip()
        if not package_name:
            self.log("请输入要安装的包！")
            return
        
        self.log_area.delete(1.0, tk.END)
        self.progress['value'] = 0
        self.log(f"正在搜索包: {package_name}")
        self.install_button.configure(state='disabled')
        
        def search_thread():
            try:
                # 先检查PyPI上是否存在该包
                try:
                    response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=5)
                    if response.status_code == 404:
                        self.log(f"\n错误：包 '{package_name}' 在PyPI上不存在")
                        self.log("\n您可以：")
                        self.log("1. 检查包名是否正确")
                        self.log("2. 尝试使用其他常见的包名形式，例如：")
                        self.log("   - opencv-python (而不是 cv2)")
                        self.log("   - pillow (而不是 PIL)")
                        self.log("   - python-libtorrent (而不是 libtorrent)")
                        self.log("   - scikit-learn (而不是 sklearn)")
                        self.log("   - beautifulsoup4 (而不是 bs4)")
                        return
                    elif response.status_code == 200:
                        package_info = response.json()
                        
                        # 检查包的有效性
                        version = package_info['info'].get('version', '0.0.0')
                        if not version or version == '0.0.0':
                            self.log(f"\n错误：包 '{package_name}' 似乎是一个无效的包或测试包")
                            self.log("原因：版本号为0.0.0或未指定版本")
                            return
                        
                        # 检查下载量和发布时间
                        if 'releases' in package_info:
                            releases = package_info['releases']
                            if not any(releases.values()):
                                self.log(f"\n警告：包 '{package_name}' 没有任何发布版本")
                                return
                        
                        # 检查下载量
                        downloads = package_info.get('info', {}).get('downloads', {}).get('last_month', 0)
                        if downloads < 100:
                            self.log(f"\n警告：包 '{package_name}' 的月下载量很低（{downloads}次），可能不是可靠的包")
                            self.log("建议：")
                            self.log("1. 检查包名是否正确")
                            self.log("2. 查看是否有类似名称的更流行的包")
                            self.log("3. 仔细检查包的文档和源代码再使用")
                            return
                        
                        # 检查最后更新时间
                        last_update = package_info['urls'][0]['upload_time'] if package_info.get('urls') else None
                        if last_update:
                            try:
                                last_update = datetime.strptime(last_update.split('T')[0], '%Y-%m-%d')
                                if (datetime.now() - last_update).days > 365:
                                    self.log(f"\n警告：此包最后更新时间是 {last_update.date()}，超过一年未更新")
                            except:
                                pass
                        
                        latest_version = package_info['info']['version']
                        description = package_info['info'].get('summary', '暂无描述')
                        author = package_info['info'].get('author', '未知')
                        home_page = package_info['info'].get('home_page', '无')
                        
                        self.log(f"\n找到包：{package_name}")
                        self.log(f"最新版本：{latest_version}")
                        self.log(f"作者：{author}")
                        self.log(f"主页：{home_page}")
                        self.log(f"描述：{description}")
                        
                        # 检查是否是可信的包
                        downloads = package_info.get('info', {}).get('downloads', {}).get('last_month', 0)
                        if downloads < 100:
                            self.log("\n警告：这个包的下载量很低，请谨慎使用！")
                        
                        # 添加常见用途说明
                        common_uses = {
                            'numpy': '数值计算和科学计算的基础包',
                            'pandas': '数据分析和处理的核心工具',
                            'requests': 'HTTP请求库，用于网络数据获取',
                            'matplotlib': '绘图和数据可视化工具',
                            'flask': '轻量级Web应用框架',
                            'django': '全功能Web开发框架',
                            'scikit-learn': '机器学习工具包',
                            'tensorflow': '深度学习框架',
                            'pytorch': '深度学习框架',
                            'pillow': '图像处理库',
                            'beautifulsoup4': '网页解析工具',
                            'selenium': '网页自动化测试工具',
                            'pygame': '游戏开发库',
                            'opencv-python': '计算机视觉库',
                            'pyqt5': 'GUI开发框架',
                            'tkinter': 'GUI开发框架（Python标准库）',
                            'pytest': '单元测试框架',
                            'sqlalchemy': '数据库ORM工具',
                            'scrapy': '网络爬虫框架',
                            'fastapi': '现代高性能Web框架'
                        }
                        
                        if package_name.lower() in common_uses:
                            self.log(f"常见用途：{common_uses[package_name.lower()]}")
                        
                        # 检查是否已安装
                        cmd = [sys.executable, "-m", "pip", "show", package_name]
                        process = subprocess.Popen(
                            cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True
                        )
                        stdout, stderr = process.communicate()
                        
                        if process.returncode == 0:
                            self.log("\n当前状态：已安装")
                            self.log(stdout)
                            self.log("\n是否要重新安装？")
                        else:
                            self.log("\n当前状态：未安装")
                        
                        # 启用安装按钮
                        self.install_button.configure(state='normal')
                    else:
                        self.log(f"\n搜索出错：HTTP状态码 {response.status_code}")
                except requests.exceptions.RequestException as e:
                    self.log(f"\n连接PyPI时出错：{str(e)}")
                    # 如果无法连接PyPI，尝试本地检查
                    cmd = [sys.executable, "-m", "pip", "show", package_name]
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True
                    )
                    stdout, stderr = process.communicate()
                    
                    if process.returncode == 0:
                        self.log("\n无法连接到PyPI，但找到本地安装的包：")
                        self.log(stdout)
                        self.install_button.configure(state='normal')
                    else:
                        self.log("\n无法连接到PyPI，且未找到本地安装的包")
                
            except Exception as e:
                self.log(f"\n搜索出错: {str(e)}")
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
        
        # 打开文件选择对话框，限制文件类型.whl
        whl_path = filedialog.askopenfilename(
            title="选择要安装的whl文件",
            filetypes=[("Wheel files", "*.whl"), ("All files", "*.*")]
        )
        
        if not whl_path:
            return
        
        self.log(f"\n始安装whl件: {whl_path}")
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
                        self.log("\n错误原因：当前whl文件与您的Python版本或系统台不兼容")
                        self.log("建议：")
                        self.log("1. 检查您的Python版本和系统架构")
                        self.log(f"   - 前Python版本: {sys.version}")
                        self.log(f"   - 系统架构: {platform.architecture()[0]}")
                        self.log("2. 下载与您的系统匹的whl文件")
                        self.log("3. 或者尝试从源代码安装")
                    self.progress['value'] = 0
            
            except Exception as e:
                self.log(f"安过程出错: {str(e)}")
                self.progress['value'] = 0
        
        thread = threading.Thread(target=whl_install_thread)
        thread.daemon = True
        thread.start()

    def detect_location(self):
        """检测用户地理位置并对源进行排序"""
        try:
            # 使用更快的API，设置更短的超时时间
            response = requests.get('http://ip-api.com/json/', timeout=2)
            if response.status_code == 200:
                location_data = response.json()
                country_code = location_data.get('countryCode', '').lower()
                continent_codes = {
                    'US': 'na', 'CA': 'na',  # 北美
                    'CN': 'cn',  # 中国
                    'JP': 'as', 'KR': 'as', 'IN': 'as',  # 亚洲
                    'GB': 'eu', 'DE': 'eu', 'FR': 'eu',  # 欧洲
                    'AU': 'oc', 'NZ': 'oc'  # 大洋洲
                }
                continent = continent_codes.get(country_code.upper(), '')
                
                # 简化排序逻
                def sort_key(source):
                    if country_code == 'cn' and ('.cn' in source or 'tsinghua' in source or 'aliyun' in source):
                        return 0
                    if continent in source or country_code in source:
                        return 1
                    return 2
                
                # 对源列表进行排序
                self.pip_sources.sort(key=sort_key)
                
                if hasattr(self, 'message_queue'):
                    self.log(f"已根据地理位置（{location_data.get('country')}）优化源顺序")
        except:
            # 如果检测失败，使用默认排序
            if hasattr(self, 'message_queue'):
                self.log("使用默认源顺序")

    def generate_captcha(self):
        """生成图片验证码"""
        # 生成随机验证码
        chars = string.ascii_uppercase + string.digits
        code = ''.join(random.choices(chars, k=4))
        
        # 创建图片
        width = 120
        height = 40
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        try:
            # 尝试加载系统字体
            if platform.system() == "Windows":
                font = ImageFont.truetype("arial.ttf", 28)
            else:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        except:
            # 如果加载失败，使用默认字体
            font = ImageFont.load_default()
        
        # 绘制文字
        for i, char in enumerate(code):
            # 随机颜色
            color = (random.randint(0, 127), random.randint(0, 127), random.randint(0, 127))
            # 随机位置
            pos = (10 + i * 25 + random.randint(-2, 2), random.randint(2, 8))
            draw.text(pos, char, font=font, fill=color)
        
        # 添加干扰线
        for _ in range(4):
            color = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))
            draw.line([
                (random.randint(0, width), random.randint(0, height)),
                (random.randint(0, width), random.randint(0, height))
            ], fill=color, width=2)
        
        # 添加噪点
        for _ in range(50):
            color = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))
            draw.point([random.randint(0, width), random.randint(0, height)], fill=color)
        
        return image, code

    def clean_pip_cache(self):
        """卸载Python包"""
        from tkinter import messagebox
        import subprocess
        
        # 添加受保护的包列表
        protected_packages = {
            # Python标准库相关
            'pip': '包管理器',
            'setuptools': 'Python包安装工具',
            'wheel': '包构建工具',
            'distutils': '包分发工具',
            'pkg_resources': '包资源管理',
            
            # 常用基础包
            'tkinter': 'GUI界面库',
            'requests': 'HTTP请求库',
            'urllib3': 'HTTP客户端',
            'certifi': 'SSL证书',
            'chardet': '字符编码检测',
            'idna': '国际化域名',
            'six': 'Python 2/3兼容',
            
            # 科学计算相关
            'numpy': '数值计算库',
            'pandas': '数据分析库',
            'scipy': '科学计算库',
            'matplotlib': '绘图库',
            
            # 开发工具
            'pytest': '测试框架',
            'pylint': '代码检查工具',
            'ipython': '交互式解释器',
            'jupyter': '交互式笔记本',
            
            # 虚拟环境
            'virtualenv': '虚拟环境',
            'venv': '虚拟环境',
            'pipenv': '依赖管理',
            
            # Web开发
            'flask': 'Web框架',
            'django': 'Web框架',
            'werkzeug': 'WSGI工具',
            'jinja2': '模板引擎',
            
            # 数据库
            'sqlalchemy': '数据库ORM',
            'pymysql': 'MySQL驱动',
            'psycopg2': 'PostgreSQL驱动',
            
            # 其他重要工具
            'cryptography': '加密库',
            'pyyaml': 'YAML解析',
            'pillow': '图像处理',
            'lxml': 'XML处理',
            'beautifulsoup4': '网页解析',
        }

        def check_package_safety(package_name):
            """检查包是否安全可卸载"""
            # 确保package_name是字符串
            if not isinstance(package_name, str):
                return False, "无效的包名"
            
            package_name = package_name.lower()  # 转换为小写
            if package_name in protected_packages:
                return False, protected_packages[package_name]
            
            # 检查是否是其他包的依赖
            try:
                cmd = [sys.executable, "-m", "pip", "show", package_name]
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                stdout, _ = process.communicate()
                if "Required-by:" in stdout:
                    required_by = stdout.split("Required-by:")[1].split("\n")[0].strip()
                    if required_by:  # 如果有其他包依赖它
                        return False, f"被以下包依赖: {required_by}"
            except:
                pass
            return True, None

        try:
            # 获取已安装的包列表
            cmd = [sys.executable, "-m", "pip", "list", "--format=json"]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                raise Exception(f"获取包列表失败: {stderr}")
            
            # 解析包信息
            import json
            packages = json.loads(stdout)
            
            # 创建卸载对话框
            dialog = tk.Toplevel(self.window)
            dialog.title("卸载Python包")
            dialog.geometry("800x600")
            dialog.transient(self.window)
            dialog.grab_set()
            
            # 创建主框架
            main_frame = ttk.Frame(dialog, padding="10")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # 添加说明文本
            ttk.Label(main_frame, 
                     text="注意：系统重要组件和被其他包依赖的包不会显示在列表中",
                     foreground='red').pack(anchor=tk.W)
            
            # 修改确认框架
            confirm_frame = ttk.Frame(main_frame)
            confirm_frame.pack(fill=tk.X, pady=5)
            
            # 验证码图片和输入框
            captcha_frame = ttk.Frame(confirm_frame)
            captcha_frame.pack(side=tk.LEFT)
            
            # 生成验证码
            captcha_image, captcha_code = self.generate_captcha()
            captcha_photo = ImageTk.PhotoImage(captcha_image)
            
            # 显示验证码
            captcha_label = ttk.Label(captcha_frame, image=captcha_photo)
            captcha_label.image = captcha_photo  # 保持引用
            captcha_label.pack(side=tk.LEFT, padx=5)
            
            def refresh_captcha():
                nonlocal captcha_code
                new_image, captcha_code = self.generate_captcha()
                new_photo = ImageTk.PhotoImage(new_image)
                captcha_label.configure(image=new_photo)
                captcha_label.image = new_photo
            
            # 刷新按钮
            ttk.Button(captcha_frame, text="刷新", 
                       command=refresh_captcha).pack(side=tk.LEFT)
            
            # 验证码输入框
            ttk.Label(confirm_frame, text="验证码:").pack(side=tk.LEFT, padx=5)
            confirm_entry = ttk.Entry(confirm_frame, width=10)
            confirm_entry.pack(side=tk.LEFT)
            
            # 修改多选功能
            select_frame = ttk.Frame(main_frame)
            select_frame.pack(fill=tk.X, pady=5)
            
            # 创建包列表框架
            list_frame = ttk.Frame(main_frame)
            list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
            
            # 创建包列表（使用Treeview）
            columns = ('包名', '当前版本', '最新版本', '位置')
            tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', selectmode='none')
            
            # 设置勾选框样式
            style = ttk.Style()
            style.configure("Treeview", indent=10)  # 设置缩进以显示勾选框
            
            # 修改勾选框状态函数
            def change_state(item, state):
                if state == 'checked':
                    tree.item(item, text='✓', tags=('checked',))
                    tree.tag_configure('checked', foreground='green')  # 设置选中状态的颜色
                else:
                    tree.item(item, text='□', tags=('unchecked',))
                    tree.tag_configure('unchecked', foreground='black')
            
            tree.change_state = change_state
            
            # 修改点击事件处理
            def on_click(event):
                region = tree.identify_region(event.x, event.y)
                if region in ("tree", "cell"):  # 扩大点击响应区域
                    item = tree.identify_row(event.y)
                    if item:
                        # 切换勾选状态
                        if tree.tag_has('checked', item):
                            tree.change_state(item, 'unchecked')
                        else:
                            tree.change_state(item, 'checked')
                        return "break"  # 阻止事件继续传播
            
            # 绑定点击事件
            tree.bind('<Button-1>', on_click)
            tree.bind('<space>', lambda e: on_click(e))  # 添加空格键支持
            
            # 添加全选/取消全选按钮
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=tk.X, pady=5)
            
            ttk.Button(button_frame, text="全选", command=lambda: [
                change_state(item, 'checked') for item in tree.get_children()
            ]).pack(side=tk.LEFT, padx=2)
            
            ttk.Button(button_frame, text="取消全选", command=lambda: [
                change_state(item, 'unchecked') for item in tree.get_children()
            ]).pack(side=tk.LEFT, padx=2)
            
            # 修改插入数据的方式
            def update_ui():
                loading_label.destroy()
                for pkg in filtered_packages:
                    item = tree.insert('', tk.END, text='□', values=(  # 初始显示空方框
                        pkg['name'],
                        pkg['version'],
                        '获取中...',
                        '获取中...'
                    ))
                    tree.change_state(item, 'unchecked')
            
            # 修改do_uninstall函数中获取选中项的方式
            def do_uninstall():
                try:
                    # 验证码检查
                    if confirm_entry.get().upper() != captcha_code:
                        messagebox.showerror("错误", "验证码错误")
                        refresh_captcha()
                        confirm_entry.delete(0, tk.END)
                        return
                    
                    # 获取勾选的包
                    selected_packages = []
                    for item in tree.get_children():
                        if tree.tag_has('checked', item):  # 检查是否被勾选
                            values = tree.item(item)['values']
                            if values and values[0]:  # 确保有包名
                                selected_packages.append(str(values[0]))  # 转换为字符串
                    
                    if not selected_packages:
                        messagebox.showwarning("警告", "请勾选要卸载的包！")
                        return
                    
                    # 检查每个选中的包
                    unsafe_packages = []
                    for package in selected_packages:
                        is_safe, reason = check_package_safety(package)
                        if not is_safe:
                            unsafe_packages.append(f"{package} ({reason})")
                    
                    if unsafe_packages:
                        if not messagebox.askyesno("警告", 
                            "以下包是系统重要组件或被其他包依赖，不建议卸载：\n\n" + 
                            "\n".join(unsafe_packages) + 
                            "\n\n确定要继续卸载吗？"):
                            return
                    
                    # 执行卸载
                    for package in selected_packages:
                        self.log(f"\n开始卸载 {package}...")
                        cmd = [sys.executable, "-m", "pip", "uninstall", "-y", package]
                        process = subprocess.Popen(
                            cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True
                        )
                        stdout, stderr = process.communicate()
                        
                        if process.returncode == 0:
                            self.log(f"成功卸载 {package}")
                        else:
                            self.log(f"卸载 {package} 失败: {stderr}")
                    
                    messagebox.showinfo("完成", "选中的包已卸载完成！")
                    
                    # 刷新列表
                    for item in tree.get_children():
                        tree.delete(item)
                    
                    # 重新加载包列表
                    loading_label = ttk.Label(main_frame, text="正在刷新包列表...", foreground='blue')
                    loading_label.pack(anchor=tk.W)
                    
                    # 启动新线程重新加载包列表
                    threading.Thread(target=lambda: load_packages(), daemon=True).start()
                    
                except Exception as e:
                    messagebox.showerror("错误", f"卸载过程出错：{str(e)}")
            
            # 添加按钮
            buttons_frame = ttk.Frame(main_frame)
            buttons_frame.pack(pady=10)
            
            ttk.Button(buttons_frame, text="卸载选中", command=do_uninstall).pack(side=tk.LEFT, padx=5)
            ttk.Button(buttons_frame, text="取消", 
                      command=dialog.destroy).pack(side=tk.LEFT, padx=5)
            
            # 创建加载提示
            loading_label = ttk.Label(main_frame, text="正在加载包列表...", foreground='blue')
            loading_label.pack(anchor=tk.W)
            
            filtered_packages = []  # 在外层作用域定义
            
            def load_packages():
                try:
                    # 获取包列表
                    cmd = [sys.executable, "-m", "pip", "list", "--format=json"]
                    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True)
                    stdout, stderr = process.communicate()
                    
                    if process.returncode != 0:
                        raise Exception(f"获取包列表失败: {stderr}")
                    
                    packages = json.loads(stdout)
                    
                    # 过滤掉受保护的包
                    nonlocal filtered_packages  # 声明nonlocal变量
                    filtered_packages = [pkg for pkg in packages 
                                       if pkg['name'].lower() not in protected_packages]
                    
                    # 批量更新界面
                    def update_ui():
                        loading_label.destroy()
                        for pkg in filtered_packages:
                            item = tree.insert('', tk.END, text='□', values=(  # 初始显示空方框
                                pkg['name'],
                                pkg['version'],
                                '获取中...',
                                '获取中...'
                            ))
                            tree.change_state(item, 'unchecked')
                        
                        # 在后台更新包的详细信息
                        threading.Thread(target=update_package_details, 
                                      args=(filtered_packages,), daemon=True).start()
                    
                    dialog.after(0, update_ui)
                    
                except Exception as e:
                    dialog.after(0, lambda: messagebox.showerror("错误", 
                                f"加载包列表失败：{str(e)}"))
            
            def update_package_details(packages):
                for pkg in packages:
                    try:
                        # 获取包位置
                        try:
                            module = __import__(pkg['name'].split('[')[0])
                            location = module.__file__
                        except:
                            location = "未知"
                        
                        # 更新显示
                        for item in tree.get_children():
                            if tree.item(item)['values'][0] == pkg['name']:
                                dialog.after(0, lambda i=item, l=location: 
                                           tree.set(i, '位置', l))
                    except:
                        continue
            
            # 在后台线程中加载包列表
            threading.Thread(target=load_packages, daemon=True).start()
            
            # 设置列标题和宽度
            tree.heading('包名', text='包名')
            tree.heading('当前版本', text='当前版本')
            tree.heading('最新版本', text='最新版本')
            tree.heading('位置', text='位置')
            
            tree.column('#0', width=40)  # 勾选框列的宽度
            tree.column('包名', width=150)
            tree.column('当前版本', width=100)
            tree.column('最新版本', width=100)
            tree.column('位置', width=400)
            
            # 添加滚动条
            v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
            h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=tree.xview)
            tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
            
            # 布局
            tree.grid(row=0, column=0, sticky='nsew')
            v_scrollbar.grid(row=0, column=1, sticky='ns')
            h_scrollbar.grid(row=1, column=0, sticky='ew')
            list_frame.grid_columnconfigure(0, weight=1)
            list_frame.grid_rowconfigure(0, weight=1)
            
        except Exception as e:
            messagebox.showerror("错误", f"初始化卸载界面失败：{str(e)}")

if __name__ == "__main__":
    app = SmartPipInstaller()
    app.run()