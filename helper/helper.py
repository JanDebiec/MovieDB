class ManagedFile:
    def __init__(self, name, mode):
        self._name = name
        self._mode = mode

    def __enter__(self):
        self._file = open(self._name,self._mode)
        return self._file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file:
            self._file.close()