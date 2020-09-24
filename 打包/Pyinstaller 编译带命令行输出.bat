pyinstaller --hidden-import pkg_resources.py2_warn --hidden-import pymediainfo --noconfirm  -i "../QuickCut/icon.ico" "../QuickCut/QuickCut.py"

echo d | xcopy /y /s .\dist\rely .\dist\QuickCut

pause