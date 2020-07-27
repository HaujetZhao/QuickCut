pyinstaller --hidden-import pkg_resources.py2_warn --noconfirm -w -i icon.ico QuickCut.py


nuitka --mingw64 --windows-disable-console --standalone --show-progress --show-memory --plugin-enable=qt-plugins --plugin-enable=pylint-warnings --plugin-enable=numpy --recurse-all --recurse-not-to=numpy,jinja2 --windows-icon=icon.ico --nofollow-imports --assume-yes-for-downloads --output-dir=out QuickCut.py



pause