
from pathlib import Path


class AppointmentLogger:
    def __init__(self, filename: str = "clinic.log") -> None:
        self._path = Path(filename)
        self._stream = None
        self._entered = False

    def __enter__(self):
        if self._entered:
            raise RuntimeError("This logger context has already been entered.")
        self._stream = self._path.open("a", encoding="utf-8")
        self._entered = True
        print("[log] opened")
        return self

    def write(self, message: str) -> None:
        if self._stream is None or self._stream.closed:
            raise RuntimeError("The action journal is not open.")
        self._stream.write(message.rstrip() + "\n")
        self._stream.flush()
        print(message)

    def __exit__(self, exc_type, exc_value, traceback):
        stream, self._stream = self._stream, None
        if stream is not None and not stream.closed:
            try:
                stream.close()
                print("[log] closed")
            except OSError:
                if exc_type is None:
                    raise
                print("[log] close failed; original error preserved")
        return False
