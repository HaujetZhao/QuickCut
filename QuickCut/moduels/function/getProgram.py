import os
from moduels.component.NormalValue import 常量

# 检查环境变量中是否有程序，返回可执行程序，这个方法先不用，但是他有用，所以先存着
def getProgram(program):
    """
    Return the path for a given executable.
    """
    def is_exe(file_path):
        """
        Checks whether a file is executable.
        """
        return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if 常量.platfm == 'Windows':
                exe_file += '.exe'
            if is_exe(exe_file):
                return exe_file
