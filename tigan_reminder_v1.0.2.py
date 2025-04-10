import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import time
import json
import os
import random
# 只保留pygame音频库
import sys
import platform

# 尝试导入 pygame 用于播放声音
try:
    import pygame
    pygame_available = True
    pygame.mixer.init()
    print("成功导入 pygame")
except ImportError:
    pygame_available = False
    print("警告: pygame 模块未安装或无法加载")
except Exception as e:
    pygame_available = False
    print(f"初始化 pygame 时发生错误: {e}")

from PIL import Image
import pystray

# 函数：获取资源文件的绝对路径
def resource_path(relative_path):
    """获取资源的绝对路径，适用于开发环境和打包后的环境"""
    try:
        # PyInstaller 创建临时文件夹并将路径存储在 _MEIPASS
        base_path = sys._MEIPASS
        full_path = os.path.join(base_path, relative_path)
        print(f"打包环境资源路径: {full_path}, 文件存在: {os.path.exists(full_path)}")
        return full_path
    except Exception:
        # 如果不是通过 PyInstaller 运行，则使用脚本所在的目录
        base_path = os.path.abspath(".")
        # 特殊处理 macOS App Bundle
        if platform.system() == "Darwin" and ".app" in base_path:
             base_path = os.path.join(base_path, "Resources")

        full_path = os.path.join(base_path, relative_path)
        print(f"开发环境资源路径: {full_path}, 文件存在: {os.path.exists(full_path)}")
        return full_path

# 使用 resource_path 函数来定义文件路径
CONFIG_FILE = resource_path("messages.json")
TRAY_ICON_FILE = resource_path("icon.png") # 明确用于托盘图标
WINDOW_ICON_FILE = resource_path("icon.ico") # 明确用于窗口图标 (.ico)
SOUND_FILE = resource_path("ding.mp3")


DEFAULT_MESSAGES = [
    "快提一下菊花，坚持就是胜利 💪🍑",
    "系统检测你坐太久了，是时候提一提了 🕵️",
    "你的菊花提醒上线了～ 快动一动～ 😄",
    "放下鼠标，提一提，然后继续战斗！🧘‍♂️",
    "提肛一分钟，通畅一整天 🌈",
    "姿势不变，肌肉在练！🏋️",
    "每小时提一下，痔疮远离你家！🚽",
    "来，跟我一起：吸～ 提～ 呼～ ☯️",
    "提升战斗力，从这一提开始 🚀"
]

# 简化后的播放声音函数，只使用pygame
def play_sound(sound_file):
    """使用pygame播放声音文件"""
    # 打印声音文件信息
    print(f"尝试播放声音文件: {sound_file}")
    print(f"文件存在检查: {os.path.exists(sound_file)}")
    
    if not os.path.exists(sound_file):
        print(f"警告: 声音文件 '{sound_file}' 未找到")
        return False
    
    # 使用 pygame 播放声音
    if pygame_available:
        try:
            def play_with_pygame():
                try:
                    pygame.mixer.music.load(sound_file)
                    pygame.mixer.music.play()
                    print("使用 pygame 播放声音成功")
                except Exception as e:
                    print(f"pygame 播放声音出错: {e}")
            
            sound_thread = threading.Thread(target=play_with_pygame, daemon=True)
            sound_thread.start()
            return True
        except Exception as e:
            print(f"尝试使用 pygame 时出错: {e}")
    
    print("警告: 无法播放声音，pygame不可用")
    return False


class TiganReminderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("提肛提醒器 🍑")
        self.master.geometry("320x340")

        # 设置窗口图标 (.ico)
        try:
            # 检查窗口图标文件是否存在
            if os.path.exists(WINDOW_ICON_FILE):
                self.master.iconbitmap(WINDOW_ICON_FILE)
            else:
                print(f"警告: 窗口图标文件 '{WINDOW_ICON_FILE}' 未找到。")
        except tk.TclError:
             # TclError 通常发生在文件格式不正确或路径有问题时
             print(f"警告: 无法加载窗口图标 '{WINDOW_ICON_FILE}'。确保文件是有效的 .ico 格式且路径正确。")
        except Exception as e:
             print(f"加载窗口图标 '{WINDOW_ICON_FILE}' 时发生未知错误: {e}")


        self.master.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.interval = tk.IntVar(value=60)
        self.running = False
        self.thread = None
        self.countdown_time = tk.IntVar(value=60)  # 默认倒计时1分钟（60秒）
        self.countdown_window = None
        self.countdown_running = False

        self.messages = self.load_messages()

        # 界面 UI
        tk.Label(master, text="提醒间隔（分钟）").pack(pady=5)
        self.interval_entry = tk.Entry(master, textvariable=self.interval, width=10, justify='center')
        self.interval_entry.pack()

        tk.Label(master, text="提肛时长（秒）").pack(pady=5)
        self.countdown_entry = tk.Entry(master, textvariable=self.countdown_time, width=10, justify='center')
        self.countdown_entry.pack()

        self.status_label = tk.Label(master, text="状态：未启动")
        self.status_label.pack(pady=5)

        self.start_btn = tk.Button(master, text="开始提醒", command=self.start_timer)
        self.start_btn.pack(pady=3)

        self.stop_btn = tk.Button(master, text="停止提醒", command=self.stop_timer, state=tk.DISABLED)
        self.stop_btn.pack(pady=3)

        self.edit_btn = tk.Button(master, text="编辑提示语", command=self.edit_messages)
        self.edit_btn.pack(pady=3)

        self.author_btn = tk.Button(master, text="关于作者", command=self.show_author_info)
        self.author_btn.pack(pady=(15, 5))

        self.setup_tray_icon()

        # self.master.after(1000, self.hide_window) # 自动最小化到托盘 (暂时注释掉，方便调试)

    def load_messages(self):
        if not os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    json.dump(DEFAULT_MESSAGES, f, indent=2, ensure_ascii=False)
                return DEFAULT_MESSAGES
            except Exception as e:
                print(f"错误: 无法创建或写入默认配置文件 '{CONFIG_FILE}': {e}")
                return DEFAULT_MESSAGES # 返回默认值，即使创建失败
        else:
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    content = f.read()
                    if not content.strip():
                         raise json.JSONDecodeError("File is empty or contains only whitespace", content, 0)
                    loaded_messages = json.loads(content)
                    # 确保加载的是列表且不为空
                    if isinstance(loaded_messages, list) and loaded_messages:
                        return loaded_messages
                    else:
                        print(f"警告: '{CONFIG_FILE}' 内容不是有效的非空列表。将使用默认提示语。")
                        raise json.JSONDecodeError("Content is not a non-empty list", content, 0)

            except json.JSONDecodeError as e:
                print(f"警告: 无法加载 {CONFIG_FILE} ({e})。将使用默认提示语并尝试重置文件。")
                try:
                    with open(CONFIG_FILE, "w", encoding="utf-8") as f_reset:
                        json.dump(DEFAULT_MESSAGES, f_reset, indent=2, ensure_ascii=False)
                    return DEFAULT_MESSAGES
                except OSError as e_reset:
                     print(f"错误: 无法重置 {CONFIG_FILE}: {e_reset}。将使用默认提示语。")
                     return DEFAULT_MESSAGES
            except Exception as e:
                 print(f"错误: 读取 {CONFIG_FILE} 时发生未知错误: {e}。将使用默认提示语。")
                 return DEFAULT_MESSAGES

    def save_messages(self):
        try:
            # 在保存前确保 self.messages 是一个列表
            if not isinstance(self.messages, list):
                print(f"错误: 尝试保存非列表类型的消息: {type(self.messages)}。将使用默认消息覆盖。")
                self.messages = DEFAULT_MESSAGES # 重置为默认值以防万一
            elif not self.messages: # 确保列表不为空，如果为空则可能使用默认值（或保持空，取决于需求）
                print("警告: 尝试保存空的消息列表。")
                # 如果不允许保存空列表，可以在这里阻止或重置
                # self.messages = DEFAULT_MESSAGES

            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.messages, f, indent=2, ensure_ascii=False)
            # messagebox.showinfo("成功", "提示语已保存。") # 可以考虑添加成功提示
        except Exception as e:
             print(f"错误: 无法保存提示语到 {CONFIG_FILE}: {e}")
             messagebox.showerror("保存错误", f"无法保存提示语到 {CONFIG_FILE}: {e}", parent=self.master)

    def edit_messages(self):
        # 确保 self.messages 是列表，以防加载失败
        current_messages = self.messages if isinstance(self.messages, list) else DEFAULT_MESSAGES
        initial_val = "\n".join(current_messages)

        new_text = simpledialog.askstring("编辑提示语", "请输入多条提示语，用换行分隔：",
                                          initialvalue=initial_val, parent=self.master) # 指定 parent
        if new_text is not None:
            potential_messages = [line.strip() for line in new_text.strip().splitlines() if line.strip()]
            if potential_messages:
                self.messages = potential_messages
                self.save_messages() # save_messages 会处理错误
            else:
                 messagebox.showwarning("编辑提示", "提示语列表不能为空。", parent=self.master)


    def start_timer(self):
        if not self.running:
            try:
                interval_value = int(self.interval.get())
                if interval_value <= 0:
                    messagebox.showerror("错误", "提醒间隔必须是大于 0 的整数。", parent=self.master)
                    return
            except ValueError:
                messagebox.showerror("错误", "请输入有效的整数作为提醒间隔。", parent=self.master)
                return

            self.running = True
            self.status_label.config(text="状态：运行中")
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.interval_entry.config(state=tk.DISABLED)
            self.edit_btn.config(state=tk.DISABLED)
            # 确保旧线程不存在或已结束
            if self.thread and self.thread.is_alive():
                print("警告: 尝试启动计时器时，发现旧线程仍在运行。")
                # 可以选择等待旧线程结束，但这可能不符合用户预期
                # self.thread.join(timeout=0.5)
            self.thread = threading.Thread(target=self.run_timer, daemon=True)
            self.thread.start()


    def stop_timer(self):
        if self.running:
            self.running = False
            # 不需要手动等待线程，因为 run_timer 内部循环会检查 self.running
            self.status_label.config(text="状态：已停止")
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.interval_entry.config(state=tk.NORMAL)
            self.edit_btn.config(state=tk.NORMAL)
            print("计时器已停止。")


    def run_timer(self):
        print("计时器线程开始运行...")
        while self.running:
            interval_minutes = 60 # 默认值
            try:
                interval_minutes = int(self.interval.get())
                if interval_minutes <= 0:
                    print(f"警告: 无效的间隔值 {interval_minutes}，使用默认值 60 分钟。")
                    interval_minutes = 60
            except ValueError:
                print(f"警告: 无法解析间隔输入，使用默认值 60 分钟。")
                interval_minutes = 60 # 出错时使用默认值

            # 等待指定分钟数，每秒检查一次 self.running 状态
            sleep_seconds = interval_minutes * 60
            for i in range(sleep_seconds):
                if not self.running:
                    print("计时器线程检测到停止标志，退出等待。")
                    return # 提前退出循环和线程
                time.sleep(1)
                # 可以在这里添加调试打印，例如打印剩余秒数
                # if (sleep_seconds - i) % 60 == 0:
                #     print(f"计时器剩余 {(sleep_seconds - i) // 60} 分钟...")

            # 只有在完成整个等待周期且仍然是 running 状态时才显示提醒
            if self.running:
                print("计时器时间到，准备显示提醒...")
                self.show_reminder()
            else:
                # 如果在最后一次 sleep 后 running 变为 False，则不显示
                print("计时器时间到，但状态已变为停止，不显示提醒。")
        print("计时器线程正常结束。")


    def show_reminder(self):
        try:
            # 使用简化的 play_sound 函数
            if pygame_available:
                play_sound(SOUND_FILE)
            else:
                print(f"警告: 无法播放声音，pygame不可用")
        except Exception as e:
            print(f"播放声音 '{SOUND_FILE}' 时出错: {e}")

        # 确保 self.messages 是列表且不为空
        valid_messages = self.messages if isinstance(self.messages, list) and self.messages else DEFAULT_MESSAGES
        msg = random.choice(valid_messages)

        # 使用 after 确保在主线程中调用 messagebox
        self.master.after(0, lambda m=msg: self.show_reminder_with_countdown(m))
    
    def show_reminder_with_countdown(self, msg):
        """显示带有倒计时的提醒框"""
        if self.countdown_window and self.countdown_window.winfo_exists():
            self.countdown_window.destroy()  # 确保没有多个倒计时窗口
        
        self.countdown_window = tk.Toplevel(self.master)
        self.countdown_window.title("提肛提醒！")
        self.countdown_window.geometry("300x200")
        self.countdown_running = True
        
        try:
            # 设置窗口图标（如果有）
            if os.path.exists(WINDOW_ICON_FILE):
                self.countdown_window.iconbitmap(WINDOW_ICON_FILE)
        except Exception as e:
            print(f"设置倒计时窗口图标时出错: {e}")
        
        # 提示信息
        message_label = tk.Label(self.countdown_window, text=msg, wraplength=280, font=("", 12))
        message_label.pack(pady=15)
        
        # 获取当前设置的倒计时时间
        try:
            countdown_seconds = int(self.countdown_time.get())
            if countdown_seconds <= 0:
                countdown_seconds = 60  # 默认为60秒
        except:
            countdown_seconds = 60  # 默认为60秒
            
        # 倒计时显示
        self.countdown_label = tk.Label(self.countdown_window, text=f"倒计时: {countdown_seconds} 秒", font=("", 14))
        self.countdown_label.pack(pady=10)
        
        # 完成按钮
        self.complete_btn = tk.Button(self.countdown_window, text="完成", command=self.close_countdown, state=tk.DISABLED)
        self.complete_btn.pack(pady=10)
        
        # 开始倒计时
        self.start_countdown(countdown_seconds)
        
        # 窗口居中显示
        self.countdown_window.update_idletasks()
        width = self.countdown_window.winfo_width()
        height = self.countdown_window.winfo_height()
        x = (self.countdown_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.countdown_window.winfo_screenheight() // 2) - (height // 2)
        self.countdown_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # 窗口焦点和置顶
        self.countdown_window.focus_force()
        self.countdown_window.lift()
        self.countdown_window.attributes('-topmost', True)
        
    def start_countdown(self, seconds):
        """开始倒计时"""
        if not self.countdown_running or not self.countdown_window or not self.countdown_window.winfo_exists():
            return
            
        if seconds > 0:
            self.countdown_label.config(text=f"倒计时: {seconds} 秒")
            self.countdown_window.after(1000, lambda: self.start_countdown(seconds-1))
        else:
            self.countdown_label.config(text="完成！可以继续工作了")
            self.complete_btn.config(state=tk.NORMAL)
            self.countdown_running = False
    
    def close_countdown(self):
        """关闭倒计时窗口"""
        self.countdown_running = False
        if self.countdown_window and self.countdown_window.winfo_exists():
            self.countdown_window.destroy()


    def hide_window(self):
        self.master.withdraw()
        print("窗口已隐藏到托盘。")
        # 可以选择在这里显示一个托盘通知
        # if self.icon and hasattr(self.icon, 'notify'):
        #     self.icon.notify("程序仍在后台运行", "提肛提醒器")


    def show_window(self, icon=None, item=None):
        self.master.after(0, self.master.deiconify)
        self.master.after(10, self.master.lift)
        self.master.after(20, self.master.focus_force)
        print("窗口已显示。")


    def exit_app(self, icon=None, item=None):
        print("开始退出应用程序...")
        self.running = False # 确保计时器线程会停止

        # 停止托盘图标（如果存在且正在运行）
        # 需要注意：直接在 pystray 的菜单回调中调用 icon.stop() 可能导致死锁或异常
        # 更安全的方式是设置一个标志，让主线程来处理退出
        # 或者使用 pystray 提供的 icon.stop 方法，但确保它在合适的线程中被调用
        # 这里尝试直接调用，但要注意潜在风险
        if icon and hasattr(icon, 'stop') and icon.visible:
             print("正在停止托盘图标...")
             try:
                 icon.stop()
                 print("托盘图标已停止。")
             except Exception as e:
                 print(f"停止托盘图标时发生错误: {e}") # 记录错误但继续退出流程
        else:
             print("托盘图标不存在或已停止。")


        # 尝试等待计时器线程结束（可选，设置较短超时）
        if self.thread and self.thread.is_alive():
            print("等待计时器线程结束...")
            self.thread.join(timeout=0.5) # 等待最多 0.5 秒
            if self.thread.is_alive():
                print("警告: 计时器线程未能在超时内结束。")


        print("销毁主窗口...")
        try:
            self.master.destroy()
            print("主窗口已销毁。")
        except tk.TclError as e:
            print(f"销毁主窗口时发生 TclError (可能窗口已关闭): {e}")
        except Exception as e:
            print(f"销毁主窗口时发生未知错误: {e}")

        print("退出进程...")
        sys.exit(0) # 明确以状态码 0 退出


    def setup_tray_icon(self):
        self.icon = None # 先初始化为 None
        try:
            # 使用 TRAY_ICON_FILE (.png)
            if not os.path.exists(TRAY_ICON_FILE):
                 print(f"错误: 托盘图标文件 '{TRAY_ICON_FILE}' 未找到！")
                 return # 没有图标文件，无法设置托盘

            image = Image.open(TRAY_ICON_FILE)
            menu = pystray.Menu(
                pystray.MenuItem("显示窗口", self.show_window, default=True),
                pystray.MenuItem("退出程序", self.exit_app) # exit_app 会处理 icon.stop
            )
            self.icon = pystray.Icon("提肛提醒器", image, "提肛提醒器 🍑", menu)

            # 启动托盘图标线程
            tray_thread = threading.Thread(target=self.icon.run, name="TrayIconThread", daemon=True)
            tray_thread.start()
            print("托盘图标线程已启动。")

        except FileNotFoundError:
             print(f"错误: 打开托盘图标文件 '{TRAY_ICON_FILE}' 失败 (FileNotFoundError)。")
        except Exception as e:
             print(f"设置托盘图标时发生错误: {e}")
             self.icon = None # 确保出错时 self.icon 为 None


    def show_author_info(self):
        """显示作者信息弹窗"""
        author_info = (
            "作者：李康\n"
            "版本：v1.0.2\n"
            "Github: https://github.com/giserlk360/TiganReminderApp"
        )
        messagebox.showinfo("关于", author_info, parent=self.master) # 指定 parent


if __name__ == "__main__":
    root = tk.Tk()
    app = TiganReminderApp(root)
    # 检查托盘图标是否成功启动，如果失败，可能需要确保主窗口可见
    # if not app.icon:
    #    print("警告: 未能成功初始化托盘图标。确保主窗口可见。")
    #    root.deiconify() # 如果托盘失败，显示主窗口

    # 初始隐藏窗口到托盘 (如果需要)
    # root.withdraw() # 启动时先隐藏
    # if app.icon and hasattr(app.icon, 'notify'): # 显示启动通知
    #    app.icon.notify("已启动并在后台运行", "提肛提醒器")

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n检测到 Ctrl+C，正在退出...")
        # 尝试优雅退出
        if app:
            app.exit_app(app.icon) # 传递 icon 对象
        else:
            sys.exit(1) # 如果 app 都没初始化成功，直接退出
    finally:
        print("应用程序主循环结束。")
