# -*- coding: utf-8 -*-
"""截图拼 PDF 的核心逻辑(不含 UI、不含热键)。

命令行版(screenshot_to_pdf.py)和图形界面版(app.py)都复用这里。
"""

import os
import sys
import datetime

from PIL import ImageGrab
import img2pdf


def app_dir():
    """返回程序所在目录。

    打包成 exe(PyInstaller)后,__file__ 指向临时解包目录,不适合存文件;
    此时改用可执行文件所在目录,保证 _shots 和 PDF 落在用户看得到的地方。
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


class ScreenshotSession:
    """管理一轮截图:缓存截图文件、撤销、合成 PDF。"""

    def __init__(self, shots_dir=None):
        self.shots_dir = shots_dir or os.path.join(app_dir(), "_shots")
        os.makedirs(self.shots_dir, exist_ok=True)
        self.shots = []  # 已截图片的文件路径,顺序即 PDF 页序

    @property
    def count(self):
        return len(self.shots)

    def capture(self):
        """截当前整屏,存盘并记入列表,返回当前张数。"""
        img = ImageGrab.grab()  # 仅主屏;多显示器可改 all_screens=True
        idx = len(self.shots) + 1
        path = os.path.join(self.shots_dir, f"shot_{idx:03d}.png")
        img.save(path)
        self.shots.append(path)
        return self.count

    def undo(self):
        """撤销最后一张,返回剩余张数;没有截图时返回 0。"""
        if not self.shots:
            return 0
        path = self.shots.pop()
        try:
            os.remove(path)
        except OSError:
            pass
        return self.count

    def build_pdf(self, out_path=None):
        """把所有截图合成 PDF。

        out_path 为空时用时间戳在程序目录生成。没有截图时返回 None,
        否则返回生成的 PDF 路径。
        """
        if not self.shots:
            return None
        if out_path is None:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = os.path.join(app_dir(), f"output_{ts}.pdf")
        with open(out_path, "wb") as f:
            f.write(img2pdf.convert(self.shots))
        return out_path

    def clear(self):
        """删除所有缓存截图并清空列表。"""
        for path in self.shots:
            try:
                os.remove(path)
            except OSError:
                pass
        self.shots = []
