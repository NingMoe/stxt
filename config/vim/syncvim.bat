rem �]�w�ӤH VIM ����
rem

goto %COMPUTERNAME%

:FRANKSHEN-PC
set src=%~dp0
set dst=C:\vim
goto pullfile

:103TT047
echo "�|�B�q��"
set src=%~dp0
set dst=C:\vim
goto pullfile

:pullfile
copy %dst% %src%_vimrc 

:end
echo "end"
