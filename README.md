# 提肛提醒器小助手 🍑

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-1.0.2-orange.svg)

一个简单的桌面应用程序，旨在提醒长时间坐着的用户进行提肛运动。

</div>

## 📋 功能特点

- ⏰ **定时提醒**：按设定间隔（默认 1 小时）弹出提醒窗口
- 🎯 **自定义间隔**：允许用户修改提醒的时间间隔
- 💬 **自定义提示语**：支持添加/编辑自己的提示语，并保存到本地
- 🔔 **提示音**：播放提示音增强提醒效果
- 🔄 **随机显示**：每次提醒时随机选择一条提示语
- 🔲 **最小化运行**：支持将窗口最小化到系统托盘
- 🖥️ **托盘图标**：使用系统托盘图标，支持显示/隐藏窗口及退出程序
- 👤 **关于作者**：显示作者相关信息

## 🚀 版本历史

### v1.0.2 (当前版本 - Pro 版)

**新增功能:**

* ✅ **自定义提示语:** 支持添加/编辑自己的提示语，并保存到本地 `messages.json` 文件
* ✅ **系统托盘图标:** 使用 `pystray` 和 `Pillow` 实现系统托盘图标，支持显示/隐藏窗口及退出程序
* ✅ **提示音:** 使用 `playsound` 播放提示音 (`ding.mp3`)
* ✅ **窗口图标:** 为应用程序窗口设置单独的图标 (`icon.ico`)
* ✅ **关于作者:** 添加了"关于作者"按钮显示相关信息
* **打包改进:** 优化了打包配置，确保资源文件能被正确包含和访问

### v1.0.1

* **自定义提示语:** 引入了从外部文件加载提示语的功能
* **随机显示:** 每次提醒时随机选择一条提示语

### v1.0.0

* **基本提醒:** 实现按设定间隔（默认 1 小时）弹出提醒窗口
* **最小化运行:** 支持将窗口最小化
* **自定义间隔:** 允许用户修改提醒的时间间隔
* **基础退出:** 提供退出程序的功能

## 🔧 环境要求

* **Python:** 推荐 Python 3.8 或更高版本
* **依赖库:**
  * `pystray`: 用于创建系统托盘图标
  * `Pillow`: `pystray` 的依赖，用于处理图像文件
  * `playsound`: 用于播放提示音

你可以使用 pip 安装这些库：
```bash
pip install pystray Pillow playsound
```

*注意:* 如果在国内环境安装速度慢，可以考虑使用镜像源，例如：
```bash
pip install pystray Pillow playsound -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 🏃‍♂️ 如何运行

1. 确保你已经安装了 Python 和上述依赖库
2. 将项目代码（包括 `.py` 文件和 `icon.png`, `icon.ico`, `ding.mp3`, `messages.json` 文件）放在同一个目录下
3. 在命令行中，切换到该目录
4. 运行主程序脚本：
   ```bash
   python tigan_reminder_v1.0.2.py
   ```

## 📦 打包为 .exe (Windows)

如果你想创建一个独立的可执行文件，方便在没有 Python 环境的 Windows 电脑上运行：

1. **安装 PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **执行打包命令:**
   在包含所有文件（`.py`, `.png`, `.ico`, `.mp3`, `.json`）的目录下，打开命令行并运行：
   ```bash
   pyinstaller --noconfirm --onefile --windowed --add-data "icon.png;." --add-data "icon.ico;." --add-data "ding.mp3;." --add-data "messages.json;." --icon="icon.ico" tigan_reminder_v1.0.2.py
   ```

   * `--onefile`: 生成单个可执行文件
   * `--windowed`: 运行时不显示命令行控制台
   * `--add-data "文件;."`: 将资源文件添加到包中。注意 Windows 使用分号 `;`，macOS/Linux 使用冒号 `:`
   * `--icon="icon.ico"`: 设置生成 `.exe` 文件的图标

3. **查找结果:** 打包成功后，可在生成的 `dist` 目录下找到 `tigan_reminder_v1.0.2.exe` 文件

## 🔄 设置开机自启 (Windows 手动方式)

1. 按下 `Win + R` 组合键，打开"运行"对话框
2. 输入 `shell:startup` 并按回车，会打开系统的"启动"文件夹
3. 将打包好的 `.exe` 文件（或它的快捷方式）复制或拖动到这个"启动"文件夹中
4. 下次开机时，程序就会自动运行了

## 📝 许可证

本项目采用 MIT 许可证。详情请参阅 LICENSE 文件。

## 👨‍💻 作者

- **作者:** 李康
- **Github:** [https://github.com/giserlk360/TiganReminderApp](https://github.com/giserlk360/TiganReminderApp)

---

<div align="center">
感谢使用提肛提醒器小助手！希望它能帮助你保持健康的工作习惯。
</div>


