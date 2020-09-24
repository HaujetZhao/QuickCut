class _BufferedReaderForFFmpeg(io.BufferedReader):
    """Method `newline` overriden to *also* treat `\\r` as a line break."""
    def readline(self, size=-1):
        if hasattr(self, "peek"):
            def nreadahead():
                readahead = self.peek(1)
                if not readahead:
                    return 1
                n = (readahead.find(b'\r') + 1) \
                    or (readahead.find(b'\n') + 1) or len(readahead)
                if size >= 0:
                    n = min(n, size)
                return n
        else:
            def nreadahead():
                return 1
        if size is None:
            size = -1
        else:
            try:
                size_index = size.__index__
            except AttributeError:
                raise TypeError(f"{size!r} is not an integer")
            else:
                size = size_index()
        res = bytearray()
        while size < 0 or len(res) < size:
            b = self.read(nreadahead())
            if not b:
                break
            res += b
            if os.linesep == '\r\n':
                # Windows
                if res.endswith(b'\r'):
                    if self.peek(1).startswith(b'\n'):
                        # \r\n encountered
                        res += self.read(1)
                    break
            else:
                # Unix
                if res.endswith(b'\r') or res.endswith(b'\n'):
                    break
        return bytes(res)

