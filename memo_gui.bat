@echo off
:: 切换到 bat 所在目录
cd /d %~dp0

:: 设置 Python 执行器（自动检测 Python 版本）
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_EXEC=py
) else (
    where python >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set PYTHON_EXEC=python
    ) else (
        echo Python 未安装或未添加到 PATH 环境变量中。
        echo 请安装 Python 或确保其在 PATH 中。
        pause
        exit /b 1
    )
)

:: 执行 memo_gui.py
echo 正在启动 Memo 笔记管理器...
%PYTHON_EXEC% memo_gui.py

:: 如果发生错误，显示错误信息并暂停
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 执行过程中出现错误，错误代码: %ERRORLEVEL%
    pause
)