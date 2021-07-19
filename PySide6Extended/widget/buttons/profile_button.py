from PySide6.QtCore import QSize
from PySide6Extended.widget import Button


class ProfileButton(Button):
    def __init__(self, text=None, icon=None, click_event=None):
        super().__init__(text, icon, click_event)
        self.setIconSize(QSize(30, 30))
