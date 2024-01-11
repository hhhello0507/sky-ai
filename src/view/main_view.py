import tkinter as tk


class MainView:
    def __init__(self, title: str):
        self._root = None
        self._init_root(title)

    def _init_root(self, title: str):
        root = tk.Tk()
        root.title(title)
        self._root = root

    def init_view(self):
        label = tk.Label(self._root)
        label.pack()

    def get_root(self) -> tk.Tk:
        return self._root


