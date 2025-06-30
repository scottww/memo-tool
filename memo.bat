@echo off
:: 切换到 bat 所在目录
cd /d %~dp0

:: 设置 Python 执行器（自动检测 Python 版本）
set PYTHON_FOUND=0

:: 检查PATH中是否有Python
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_EXEC=py
    set PYTHON_FOUND=1
    goto PYTHON_READY
)

where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_EXEC=python
    set PYTHON_FOUND=1
    goto PYTHON_READY
)

:: 检查常见安装路径
if exist "%ProgramFiles%\Python*\python.exe" (
    for /d %%i in ("%ProgramFiles%\Python*") do (
        set PYTHON_EXEC="%%i\python.exe"
        set PYTHON_FOUND=1
        goto PYTHON_READY
    )
)

if exist "%ProgramFiles(x86)%\Python*\python.exe" (
    for /d %%i in ("%ProgramFiles(x86)%\Python*") do (
        set PYTHON_EXEC="%%i\python.exe"
        set PYTHON_FOUND=1
        goto PYTHON_READY
    )
)

if exist "%LOCALAPPDATA%\Programs\Python\Python*\python.exe" (
    for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
        set PYTHON_EXEC="%%i\python.exe"
        set PYTHON_FOUND=1
        goto PYTHON_READY
    )
)

:: 如果没有找到Python
if %PYTHON_FOUND% EQU 0 (
    echo Python 未安装或未找到。
    echo 请安装 Python 或确保其在 PATH 中。
    echo 您可以从 https://www.python.org/downloads/ 下载并安装Python。
    pause
    exit /b 1
)

:PYTHON_READY

:: 执行 memo.py 并传参
%PYTHON_EXEC% memo.py %*

:: 如果发生错误，显示错误信息并暂停
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 执行过程中出现错误，错误代码: %ERRORLEVEL%
    pause
)
