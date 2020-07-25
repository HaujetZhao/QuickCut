pyinstaller --hidden-import pkg_resources.py2_warn --noconfirm -w -i icon.ico QuickCut.py

echo d | xcopy /y /s .\dist\rely .\dist\QuickCut

del /F /Q QuickCut_compiles_by_pyinstaller.7z

7z a -t7z QuickCut_compiles_by_pyinstaller.7z .\dist\QuickCut -mx=9 -ms=200m -mf -mhc -mhcf  -mmt -r

nuitka --mingw64 --windows-disable-console --standalone --show-progress --show-memory --plugin-enable=qt-plugins --plugin-enable=pylint-warnings --plugin-enable=numpy --recurse-all --recurse-not-to=numpy,jinja2 --windows-icon=icon.ico --nofollow-imports --assume-yes-for-downloads --output-dir=out QuickCut.py

echo d | xcopy /y /s .\out\rely .\out\QuickCut.dist

del /F /Q QuickCut_compiles_by_nuitka.7z

7z a -t7z QuickCut_compiles_by_nuitka.7z .\out\QuickCut.dist -mx=9 -ms=200m -mf -mhc -mhcf -mmt -r

pause