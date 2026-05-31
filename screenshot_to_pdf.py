# -*- coding: utf-8 -*-
"""
截图拼 PDF 工具(命令行版)
用法：在浏览器里翻页，按热键截图，截够了按结束键自动生成 PDF。

图形界面版见 app.py。

热键：
  S  —— 截一张当前整个屏幕
  Z  —— 撤销上一张（截错了可删掉）
  F  —— 结束并生成 PDF
  Q  —— 放弃退出（不生成）
"""

import time
import keyboard

from core import ScreenshotSession

done = {"finish": False, "abort": False}


def main():
    print(__doc__)
    print("=" * 50)
    print("开始监听热键…（窗口可以最小化，热键全局生效）\n")

    session = ScreenshotSession()

    def capture():
        n = session.capture()
        print(f"  ✓ 已截第 {n} 张")

    def undo():
        if session.count:
            n = session.undo()
            print(f"  ↩ 已撤销，剩 {n} 张")
        else:
            print("  （还没有截图，无法撤销）")

    keyboard.add_hotkey("s", capture)
    keyboard.add_hotkey("z", undo)
    keyboard.add_hotkey("f", lambda: done.update(finish=True))
    keyboard.add_hotkey("q", lambda: done.update(abort=True))

    while not done["finish"] and not done["abort"]:
        time.sleep(0.1)

    keyboard.unhook_all()

    if done["abort"]:
        print("\n已放弃，未生成 PDF。截图仍保留在 _shots 目录。")
    else:
        try:
            out = session.build_pdf()
            if out:
                print(f"\n✅ 已生成 PDF（共 {session.count} 页）：\n{out}")
            else:
                print("没有任何截图，未生成 PDF。")
        except Exception:
            import traceback
            print("\n❌ 生成 PDF 出错：")
            traceback.print_exc()
            print(f"\n截图仍保留在：{session.shots_dir}")

    input("\n按回车键关闭窗口…")


if __name__ == "__main__":
    main()
