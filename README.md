# 截图拼 PDF

一个极简的 Windows 小工具：用全局热键连续截屏，按一下键就把所有截图合成一个 PDF。
适合把网页、电子书、PPT 等「只能看不能下载」的内容翻页截图后导出成 PDF。

## 安装

需要 Python 3.x。

```bash
pip install -r requirements.txt
```

## 使用

```bash
python screenshot_to_pdf.py
```

运行后程序在后台监听热键（窗口可最小化，热键全局生效）：

| 热键 | 作用 |
| --- | --- |
| `S` | 截取当前整个屏幕 |
| `Z` | 撤销上一张截图 |
| `1` | 结束并生成 PDF |
| `Q` | 放弃退出（不生成 PDF） |

生成的 PDF 会保存在脚本同目录下，文件名形如 `output_20260531_120000.pdf`。

## 说明

- 截图临时存放在 `_shots/` 目录；放弃退出时截图会保留，方便手动处理。
- 默认截取主屏幕，多显示器可把 `ImageGrab.grab()` 改为 `ImageGrab.grab(all_screens=True)`。
- `keyboard` 库在 Windows 上注册全局热键通常需要管理员权限运行。
