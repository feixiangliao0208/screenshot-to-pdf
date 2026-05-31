# 截图拼 PDF

一个极简的 Windows 小工具：用全局热键连续截屏，按一下键就把所有截图合成一个 PDF。
适合把网页、电子书、PPT 等「只能看不能下载」的内容翻页截图后导出成 PDF。

提供两种用法：**图形界面版**(`app.py`，推荐)和**命令行版**(`screenshot_to_pdf.py`)。

## 直接下载使用（无需安装 Python）

到本仓库右侧的 [**Releases**](https://github.com/Pleasecallmealex/PythonProject5/releases/latest) 页面，下载 `截图拼PDF.exe`，双击即可运行（首次会弹出管理员授权，点「是」）。对方电脑**不需要装 Python 或任何库**。

> 想自己改代码 / 自己打包，再看下面的「安装」和「打包」。

## 安装

需要 Python 3.x。

```bash
pip install -r requirements.txt
```

依赖只有三个第三方库：`keyboard`、`pillow`、`img2pdf`（界面用的 `tkinter` 是 Python 自带的）。

## 使用

### 图形界面版（推荐）

```bash
python app.py
```

打开后点击「快捷截图转 PDF」按钮进入截图模式，然后翻页截图。窗口上的按钮和全局热键都能用：

| 热键 | 按钮 | 作用 |
| --- | --- | --- |
| `S` | 截图 | 截取当前整个屏幕 |
| `Z` | 撤销 | 撤销上一张截图 |
| `F` | 生成 PDF | 结束并选择位置保存 PDF |
| `Q` | 放弃 | 放弃本次（不生成 PDF） |

生成时会弹出保存对话框让你选择 PDF 位置；生成成功后会自动清理本次的临时截图。

### 命令行版

```bash
python screenshot_to_pdf.py
```

运行后在后台监听热键（窗口可最小化，热键全局生效），热键同上。生成的 PDF 保存在脚本同目录下，文件名形如 `output_20260531_120000.pdf`。

## 打包成 exe（发给别人用）

双击运行 `build.bat`，会自动安装依赖并用 PyInstaller 把界面版打包成单文件 exe，产物在 `dist\截图拼PDF.exe`。

把这个 exe 单独发给别人即可，**对方电脑无需安装 Python 或任何库**。exe 已自带一个隔离的 Python 运行时，不会和对方已有的 Python 冲突。

> exe 用 `--uac-admin` 打包，运行时会自动请求管理员权限（`keyboard` 注册全局热键需要）。

## 说明

- 截图临时存放在 `_shots/` 目录；命令行版放弃退出、界面版放弃时，截图都会保留，方便手动处理。
- 默认截取主屏幕，多显示器可把 `core.py` 里的 `ImageGrab.grab()` 改为 `ImageGrab.grab(all_screens=True)`。
- `keyboard` 库在 Windows 上注册全局热键通常需要管理员权限运行。

## 文件结构

| 文件 | 作用 |
| --- | --- |
| `core.py` | 核心逻辑：截图、撤销、合成 PDF（被下面两个复用） |
| `app.py` | 图形界面版入口（tkinter） |
| `screenshot_to_pdf.py` | 命令行版入口 |
| `build.bat` | 一键打包成 exe |
