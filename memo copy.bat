@echo off
:: 设置 Python 执行器路径（如已配置好环境变量，可用 python）
set PYTHON_EXEC=python

:: 设置 memo.py 所在路径
set MEMO_PATH=F:\MyProject\memo_tool\memo.py

:: 调用 Python 脚本并传入所有参数
%PYTHON_EXEC% %MEMO_PATH% %*

