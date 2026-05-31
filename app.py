# -*- coding: utf-8 -*-
"""截图拼 PDF —— 图形界面版。

主窗口有一个「快捷截图转 PDF」按钮,按下后进入截图模式:
全局热键 S/Z/F/Q 生效,窗口上也有对应按钮,可自由翻页截图,最后合成 PDF。
"""

import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import keyboard

from core import ScreenshotSession


class App:
    def __init__(self, root):
        self.root = root
        self.session = None
        self.capturing = False
        self._hotkeys = []

        root.title("截图拼 PDF 工具")
        root.geometry("380x280")
        root.resizable(False, False)

        ttk.Label(
            root, text="截图拼 PDF 工具", font=("Microsoft YaHei", 14, "bold")
        ).pack(pady=(16, 4))
        self.hint = ttk.Label(
            root, text="按下按钮开始,翻页时用热键或按钮截图", foreground="#666"
        )
        self.hint.pack()

        self.start_btn = ttk.Button(
            root, text="快捷截图转 PDF", command=self.start
        )
        self.start_btn.pack(pady=12, ipadx=10, ipady=6)

        self.status = ttk.Label(root, text="未开始", font=("Microsoft YaHei", 11))
        self.status.pack(pady=4)

        ops = ttk.Frame(root)
        ops.pack(pady=8)
        self.cap_btn = ttk.Button(ops, text="截图 (S)", width=12, command=self.do_capture)
        self.undo_btn = ttk.Button(ops, text="撤销 (Z)", width=12, command=self.do_undo)
        self.gen_btn = ttk.Button(ops, text="生成 PDF (F)", width=12, command=self.do_generate)
        self.abort_btn = ttk.Button(ops, text="放弃 (Q)", width=12, command=self.do_abort)
        self.cap_btn.grid(row=0, column=0, padx=4, pady=4)
        self.undo_btn.grid(row=0, column=1, padx=4, pady=4)
        self.gen_btn.grid(row=1, column=0, padx=4, pady=4)
        self.abort_btn.grid(row=1, column=1, padx=4, pady=4)
        self._set_ops_state("disabled")

        root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------- 会话控制 ----------
    def start(self):
        self.session = ScreenshotSession()
        try:
            self._register_hotkeys()
        except Exception as e:
            messagebox.showerror(
                "热键注册失败",
                "无法注册全局热键,通常是权限不足。\n"
                "请关闭后右键以「管理员身份运行」本程序。\n\n"
                f"详细:{e}",
            )
            self.session = None
            return
        self.capturing = True
        self.start_btn.config(text="截图中…", state="disabled")
        self._set_ops_state("normal")
        self.hint.config(text="窗口可最小化,热键全局生效")
        self._update_status()

    def _register_hotkeys(self):
        # 热键回调在 keyboard 自己的线程触发,必须用 after 转回主线程再动 UI
        self._hotkeys = [
            keyboard.add_hotkey("s", lambda: self.root.after(0, self.do_capture)),
            keyboard.add_hotkey("z", lambda: self.root.after(0, self.do_undo)),
            keyboard.add_hotkey("f", lambda: self.root.after(0, self.do_generate)),
            keyboard.add_hotkey("q", lambda: self.root.after(0, self.do_abort)),
        ]

    def _unregister_hotkeys(self):
        for h in self._hotkeys:
            try:
                keyboard.remove_hotkey(h)
            except (KeyError, ValueError):
                pass
        self._hotkeys = []

    def _end_session(self):
        self._unregister_hotkeys()
        self.capturing = False
        self.session = None
        self.start_btn.config(text="快捷截图转 PDF", state="normal")
        self._set_ops_state("disabled")
        self.status.config(text="未开始")
        self.hint.config(text="按下按钮开始,翻页时用热键或按钮截图")

    def _set_ops_state(self, state):
        for b in (self.cap_btn, self.undo_btn, self.gen_btn, self.abort_btn):
            b.config(state=state)

    def _update_status(self):
        n = self.session.count if self.session else 0
        self.status.config(text=f"已截 {n} 张")

    # ---------- 具体操作 ----------
    def do_capture(self):
        if not self.capturing:
            return
        self.session.capture()
        self._update_status()

    def do_undo(self):
        if not self.capturing:
            return
        self.session.undo()
        self._update_status()

    def do_generate(self):
        if not self.capturing:
            return
        if self.session.count == 0:
            messagebox.showinfo("提示", "还没有任何截图,无法生成 PDF。")
            return
        default_name = "output_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".pdf"
        out = filedialog.asksaveasfilename(
            title="保存 PDF",
            defaultextension=".pdf",
            initialfile=default_name,
            filetypes=[("PDF 文件", "*.pdf")],
        )
        if not out:
            return  # 用户取消保存,会话继续,可接着截图
        try:
            self.session.build_pdf(out)
        except Exception as e:
            messagebox.showerror("生成失败", f"生成 PDF 出错:\n{e}")
            return
        self.session.clear()
        messagebox.showinfo("完成", f"已生成 PDF:\n{out}")
        self._end_session()

    def do_abort(self):
        if not self.capturing:
            return
        if self.session.count and not messagebox.askyesno(
            "放弃", "确定放弃本次截图吗?\n(已截图会保留在 _shots 目录,不生成 PDF)"
        ):
            return
        self._end_session()

    def on_close(self):
        if self.capturing and not messagebox.askyesno(
            "退出", "正在截图中,确定退出吗?(不会生成 PDF)"
        ):
            return
        self._unregister_hotkeys()
        self.root.destroy()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
