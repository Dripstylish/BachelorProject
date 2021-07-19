from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton


class Button(QPushButton):
    def __init__(self, text=None, icon=None, click_event=None):
        super().__init__()
        self.setAutoFillBackground(True)

        if text is not None:
            self.setText(text)

        if icon is not None:
            self.setIcon(QIcon(icon))
            self.setIconSize(QSize(11, 11))

        if click_event is not None:
            self.clicked.connect(click_event)