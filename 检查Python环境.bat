@echo off
chcp 65001 > nul
echo ======================================
echo      Python 环境检测工具
echo ======================================
echo.

set PYTHON_FOUND=0

:: 检查PATH中是否有Python
echo 正在检查 PATH 中的 Python...
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_EXEC=py
    set PYTHON_FOUND=1
    echo [√] 找到 Python 启动器 (py)
    echo.
    echo 版本信息:
    py --version
    echo.
    goto PYTHON_CHECK_COMPLETE
)

where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_EXEC=python
    set PYTHON_FOUND=1
    echo [√] 找到 Python 解释器 (python)
    echo.
    echo 版本信息:
    python --version
    echo.
    goto PYTHON_CHECK_COMPLETE
)

:: 检查常见安装路径
echo 正在检查常见安装路径...

if exist "%ProgramFiles%\Python*\python.exe" (
    for /d %%i in ("%ProgramFiles%\Python*") do (
        set PYTHON_EXEC="%%i\python.exe"
        set PYTHON_FOUND=1
        echo [√] 找到 Python 安装: %%i
        echo.
        echo 但它未添加到 PATH 环境变量中。
        goto PYTHON_CHECK_COMPLETE
    )
)

if exist "%ProgramFiles(x86)%\Python*\python.exe" (
    for /d %%i in ("%ProgramFiles(x86)%\Python*") do (
        set PYTHON_EXEC="%%i\python.exe"
        set PYTHON_FOUND=1
        echo [√] 找到 Python 安装: %%i
        echo.
        echo 但它未添加到 PATH 环境变量中。
        goto PYTHON_CHECK_COMPLETE
    )
)

if exist "%LOCALAPPDATA%\Programs\Python\Python*\python.exe" (
    for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
        set PYTHON_EXEC="%%i\python.exe"
        set PYTHON_FOUND=1
        echo [√] 找到 Python 安装: %%i
        echo.
        echo 但它未添加到 PATH 环境变量中。
        goto PYTHON_CHECK_COMPLETE
    )
)

:: 如果没有找到Python
if %PYTHON_FOUND% EQU 0 (
    echo [×] 未找到 Python 安装。
    echo.
    echo 请安装 Python 或确保其在 PATH 中。
    echo 您可以从 https://www.python.org/downloads/ 下载并安装Python。
    echo.
    echo 安装时请勾选 "Add Python to PATH" 选项。
    goto END
)

:PYTHON_CHECK_COMPLETE
if %PYTHON_FOUND% EQU 1 (
    echo ======================================
    echo 检测结果:
    if "%PYTHON_EXEC%"=="py" (
        echo [√] Python 环境正常，可以使用 memo.bat 和 memo_gui.bat
    ) else if "%PYTHON_EXEC%"=="python" (
        echo [√] Python 环境正常，可以使用 memo.bat 和 memo_gui.bat
    ) else (
        echo [!] Python 已安装但未添加到 PATH 环境变量中
        echo.
        echo 建议操作:
        echo 1. 按照 安装指南.md 中的步骤添加 Python 到 PATH
        echo 2. 或者修改 memo.bat 和 memo_gui.bat 文件，将 PYTHON_EXEC 设置为:
        echo    set PYTHON_EXEC=%PYTHON_EXEC%
    )
)

:END
echo.
echo ======================================
echo 按任意键退出...
pause > nul