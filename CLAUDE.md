# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目简介

一个 Windows 小工具:通过全局热键连续截取整屏,最后合成一个 PDF。用于把「只能看不能下载」的内容(网页、电子书、PPT 等)翻页截图后导出为 PDF。提供图形界面版和命令行版两个入口。

## 命令

```bash
pip install -r requirements.txt   # 运行依赖:keyboard、pillow、img2pdf
python app.py                     # 图形界面版(推荐)
python screenshot_to_pdf.py       # 命令行版;会阻塞在全局热键循环里
build.bat                         # 用 PyInstaller 打包成单文件 exe,产物在 dist\
```

发布:exe **不进 git**(`dist/` 已 gitignore),通过 GitHub Releases 分发。附件用 **ASCII 名**(`screenshot-to-pdf.exe`)上传——中文文件名经 Windows 控制台传给 `gh` 时会被编码吃掉,只剩 `PDF.exe`。流程:`Copy-Item dist\截图拼PDF.exe dist\screenshot-to-pdf.exe` 后 `gh release upload <tag> dist\screenshot-to-pdf.exe --clobber`。仓库远程是 `feixiangliao0208/screenshot-to-pdf`。

没有测试、lint;唯一的"构建"是 `build.bat`(打包 exe,额外需要 pyinstaller,仅打包时用)。

## 架构

核心逻辑与两个入口分离:

- **`core.py`** — `ScreenshotSession` 类,纯逻辑,不含 UI 也不含热键:`capture()` / `undo()` / `build_pdf()` / `clear()`,`shots` 列表是 PDF 页序的唯一来源。命令行版和界面版都复用它。
- **`app.py`** — tkinter 界面入口。主按钮「快捷截图转 PDF」启动一轮会话,期间注册全局热键 + 启用窗口按钮。
- **`screenshot_to_pdf.py`** — 命令行入口,`keyboard.add_hotkey` + `while` 轮询(每 0.1s)阻塞。

## 关键实现要点

- **热键全局且阻塞**:两个入口都注册全局热键(`s` 截图 / `z` 撤销 / `f` 生成 PDF / `q` 放弃),窗口不在前台也能触发。命令行版会卡住任何非交互 shell;**不要**用工具调用去启动它并期待返回。`keyboard` 在沙盒里 import 也会挂起(它要挂钩系统输入),验证语法用 `python -m py_compile`,不要直接 import keyboard。
- **管理员权限**:`keyboard` 注册全局热键在 Windows 上通常需要管理员权限;打包脚本用 `--uac-admin` 让 exe 运行时自动提权。
- **tkinter 线程**:`keyboard` 的热键回调在它自己的线程触发,而 tkinter 只能在主线程动 UI。`app.py` 里所有热键回调都用 `self.root.after(0, ...)` 把动作转回主线程,不要在回调里直接改控件。
- **打包后的路径**:`core.app_dir()` 处理了 PyInstaller 冻结的情况——冻结时 `__file__` 指向临时解包目录,改用 `sys.executable` 所在目录,保证 `_shots/` 和输出 PDF 落在用户看得到的地方。新增需要写文件的逻辑请走 `app_dir()`,别用 `__file__`。
- **截图缓存**:`_shots/` 下的 PNG(已 gitignore),文件名序号取自 `len(shots)+1`;撤销会从列表弹出并删除文件。界面版生成 PDF 后调用 `clear()` 清理;命令行版和"放弃"都保留截图。
- **合成用 img2pdf**:`build_pdf()` 用 `img2pdf.convert(shots)` 直接写 PDF(不是 Pillow 的 save_all)。界面版用文件对话框让用户选保存位置;命令行版用时间戳 `output_<YYYYMMDD_HHMMSS>.pdf`。
- 多显示器:`core.py` 里 `ImageGrab.grab()` 只截主屏,需改为 `ImageGrab.grab(all_screens=True)`。
