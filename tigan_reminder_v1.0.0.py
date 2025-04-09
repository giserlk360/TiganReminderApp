import tkinter as tk
from tkinter import messagebox
import threading
import time

class TiganReminderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("提肛提醒器 🍑")
        self.master.geometry("300x200")
        self.master.resizable(False, False)

        self.interval = tk.IntVar(value=60)

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
        messagebox.showinfo("提肛时间到啦！", "快提一下菊花，坚持就是胜利 💪🍑")

if __name__ == "__main__":
    root = tk.Tk()
    app = TiganReminderApp(root)
    root.mainloop()
