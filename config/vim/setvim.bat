rem �]�w�ӤH VIM ����
rem

set src=%~p0
set dst=C:\vim

copy %src%_vimrc %dst%

if not exist %dst%\vimfiles mkdir %dst%\vimfiles
copy %src%\format.vim %dst%\vimfiles
 
if not exist %dst%\vimfiles\ftdetect mkdir %dst%\vimfiles\ftdetect
 
copy %src%\ftdetect\* %dst%\vimfiles\ftdetect\
