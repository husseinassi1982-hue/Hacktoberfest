"""Collect recognized signs within one translation session."""

class SignBuffer:
    def __init__(self):
        self._signs = []

    def add(self, sign):
        if sign:
            self._signs.append(sign)

    def get_signs(self):
        return list(self._signs)

    def clear(self):
        self._signs.clear()
