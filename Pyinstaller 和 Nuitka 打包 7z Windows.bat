echo d | xcopy /y /s .\dist\rely .\dist\QuickCut

del /F /Q QuickCut_Windows_compiled_by_pyinstaller.7z

7z a -t7z QuickCut_Windows_compiled_by_pyinstaller.7z .\dist\QuickCut -mx=9 -ms=200m -mf -mhc -mhcf  -mmt -r




echo d | xcopy /y /s .\out\rely .\out\QuickCut.dist

del /F /Q QuickCut_Windows_compiled_by_nuitka.7z

7z a -t7z QuickCut_Windows_compiled_by_nuitka.7z .\out\QuickCut.dist -mx=9 -ms=200m -mf -mhc -mhcf -mmt -r

pause