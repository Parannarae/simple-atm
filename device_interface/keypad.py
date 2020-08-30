from typing import Optional

class KeyPad:
    def __init__(self):
        self.keypad_system = None

    def read(self) -> Optional[int]:
        raise NotImplementedError