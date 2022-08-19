import mmap
import os

MMAP_SIZE = 4 * 1024


class simplemmap:
    def __init__(self, file_path: str) -> None:
        self._mmap_object = None
        self.mmap_file_path = file_path
        if os.path.exists(self.mmap_file_path) == False:
            self.create_mmap_file()
        self.read_mmap_file()

    def create_mmap_file(self) -> None:
        with open(self.mmap_file_path, mode='wb') as f:
            init_byte = b'\xFF' * 8 * MMAP_SIZE
            f.write(init_byte)

    def read_mmap_file(self) -> None:
        with open(self.mmap_file_path, mode='r+b') as f:
            self._mmap_object = mmap.mmap(f.fileno(), 0)
            self._mmap_object.seek(0)

    def read_data(self) -> bytes:
        data = self._mmap_object.read()
        self._mmap_object.seek(0)
        return data.rstrip(b'\xFF')

    def write_data(self, data: bytes) -> None:
        data += b'\xFF' * 8 * (MMAP_SIZE - len(data))
        self._mmap_object.write(data)
        self._mmap_object.seek(0)

    def dispose(self, leave_file=False) -> None:
        self._mmap_object.close()
        if leave_file == False:
            try:
                os.remove(self.mmap_file_path)
            except (FileNotFoundError, PermissionError):
                pass
