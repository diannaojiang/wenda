set "WINPYDIR=%~dp0\WPy64-38100\python-3.8.10.amd64"
IF EXIST %WINPYDIR% (
echo ��⵽���ɻ�����ʹ������Python������
set "PATH=%WINPYDIR%\;%WINPYDIR%\DLLs;%WINPYDIR%\Scripts;%PATH%;"
set "PYTHON=%WINPYDIR%\python.exe "
goto end
) 
IF EXIST python (
echo δ��⵽���ɻ�����ʹ��ϵͳPython������
)ELSE (
)
:end