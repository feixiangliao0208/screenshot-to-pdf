# -*- coding: utf-8 -*-
"""
截图拼 PDF 工具
用法：在浏览器里翻页，按热键截图，截够了按结束键自动生成 PDF。

热键：
  S  —— 截一张当前整个屏幕
  Z  —— 撤销上一张（截错了可删掉）
  1  —— 结束并生成 PDF
  Q  —— 放弃退出（不生成）
"""

import os
import sys
import time
import datetime
import keyboard
from PIL import ImageGrab

# 截图临时存放目录
SHOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_shots")
os.makedirs(SHOTS_DIR, exist_ok=True)

shots = []          # 已截图片的文件路径列表
done = {"finish": False, "abort": False}


def capture():
    img = ImageGrab.grab()  # 整个屏幕（多显示器可改 all_screens=True）
    idx = len(shots) + 1
    path = os.path.join(SHOTS_DIR, f"shot_{idx:03d}.png")
    img.save(path)
    shots.append(path)
    print(f"  ✓ 已截第 {idx} 张")


def undo():
    if shots:
        path = shots.pop()
        try:
            os.remove(path)
        except OSError:
            pass
        print(f"  ↩ 已撤销，剩 {len(shots)} 张")
    else:
        print("  （还没有截图，无法撤销）")


def finish():
    done["finish"] = True


def abort():
    done["abort"] = True


def build_pdf():
    if not shots:
        print("没有任何截图，未生成 PDF。")
        return
    import img2pdf
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"output_{ts}.pdf")
    with open(out, "wb") as f:
        f.write(img2pdf.convert(shots))
    print(f"\n✅ 已生成 PDF（共 {len(shots)} 页）：\n{out}")


def main():
    print(__doc__)
    print("=" * 50)
    print("开始监听热键…（窗口可以最小化，热键全局生效）\n")

    keyboard.add_hotkey("s", capture)
    keyboard.add_hotkey("z", undo)
    keyboard.add_hotkey("1", finish)
    keyboard.add_hotkey("q", abort)

    while not done["finish"] and not done["abort"]:
        time.sleep(0.1)

    keyboard.unhook_all()

    if done["abort"]:
        print("\n已放弃，未生成 PDF。截图仍保留在 _shots 目录。")
    else:
        try:
            build_pdf()
        except Exception as e:
            import traceback
            print("\n❌ 生成 PDF 出错：")
            traceback.print_exc()
            print(f"\n截图仍保留在：{SHOTS_DIR}")

    input("\n按回车键关闭窗口…")


if __name__ == "__main__":
    main()
