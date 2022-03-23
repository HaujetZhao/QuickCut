pyinstaller --noconfirm  -i "../QuickCut/misc/icon.ico" "../QuickCut/QuickCut.py"

echo d | xcopy /y /s .\\rely .\dist\QuickCut

pause


