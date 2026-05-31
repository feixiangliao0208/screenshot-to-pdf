@echo off
chcp 65001 >nul
REM ============================================================
REM 把图形界面版(app.py)打包成单文件 exe。
REM 双击运行本脚本即可,产物在 dist\ 目录。
REM ============================================================

echo [1/3] 安装运行依赖...
pip install -r requirements.txt
if errorlevel 1 goto :err

echo [2/3] 安装打包工具 PyInstaller...
pip install pyinstaller
if errorlevel 1 goto :err

echo [3/3] 开始打包...
REM  --onefile   打成单个 exe
REM  --windowed  不弹黑色控制台窗口(GUI 程序)
REM  --uac-admin 运行时自动请求管理员权限(keyboard 注册全局热键需要)
REM  --name      指定 exe 名称
pyinstaller --onefile --windowed --uac-admin --name 截图拼PDF app.py
if errorlevel 1 goto :err

echo.
echo ============================================================
echo  打包完成!exe 在 dist\截图拼PDF.exe
echo  把这个 exe 单独发给别人即可,对方无需安装 Python。
echo ============================================================
pause
exit /b 0

:err
echo.
echo 出错了,请检查上面的报错信息(常见原因:没装 Python 或没联网)。
pause
exit /b 1
