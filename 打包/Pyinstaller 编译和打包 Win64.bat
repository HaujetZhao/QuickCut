pyinstaller --hidden-import pkg_resources.py2_warn --noconfirm -w -i "../QuickCut/icon.ico" "../QuickCut/QuickCut.py"

echo d | xcopy /y /s .\dist\rely .\dist\QuickCut

del /F /Q QuickCut_Win64_pyinstaller.7z

7z a -t7z QuickCut_Win64_pyinstaller.7z .\dist\QuickCut -mx=9 -ms=200m -mf -mhc -mhcf  -mmt -r

echo d | xcopy /y /s .\dist\QuickCut C:\Portable_Programes\QuickCut

pause