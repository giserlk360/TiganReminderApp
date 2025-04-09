import tkinter as tk
from tkinter import messagebox
import threading
import time
import random

class TiganReminderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("提肛提醒器 🍑")
        self.master.geometry("300x240")
        self.master.resizable(False, False)

        self.interval = tk.IntVar(value=60)

        # 提示语列表
        self.messages = [
            "快提一下菊花，坚持就是胜利 💪🍑",
            "系统检测你坐太久了，是时候提一提了 🕵️",
            "核心力量从“臀”开始，现在，提起来！🔥",
            "你的菊花提醒上线了～ 快动一动～ 😄",
            "放下鼠标，提一提，然后继续战斗！🧘‍♂️",
            "提肛一分钟，通畅一整天 🌈",
            "姿势不变，肌肉在练！🏋️",
            "每小时提一下，痔疮远离你家！🚽",
            "来，跟我一起：吸～ 提～ 呼～ ☯️",
            "提升战斗力，从这一提开始 🚀"
        ]

        tk.Label(master, text="提肛提醒时间间隔（分钟）").pack(pady=10)
        self.interval_entry = tk.Entry(master, textvariable=self.interval, width=10, justify='center')
        self.interval_entry.pack()

        self.status_label = tk.Label(master, text="状态：未启动")
        self.status_label.pack(pady=10)

        self.start_btn = tk.Button(master, text="开始提醒", command=self.start_timer)
        self.start_btn.pack(pady=5)

        self.stop_btn = tk.Button(master, text="停止提醒", command=self.stop_timer, state=tk.DISABLED)
        self.stop_btn.pack(pady=5)

        self.running = False
        self.thread = None

    def start_timer(self):
        if not self.running:
            self.running = True
            self.status_label.config(text="状态：运行中...")
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.thread = threading.Thread(target=self.run_timer, daemon=True)
            self.thread.start()

    def stop_timer(self):
        self.running = False
        self.status_label.config(text="状态：已停止")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def run_timer(self):
        while self.running:
            try:
                minutes = int(self.interval.get())
            except ValueError:
                minutes = 60
            time.sleep(minutes * 60)
            if self.running:
                self.show_reminder()

    def show_reminder(self):
        msg = random.choice(self.messages)
        messagebox.showinfo("提肛提醒！", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = TiganReminderApp(root)
    root.mainloop()
