from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu

from PySide6Extended.core import app


class PopUpMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)

        app.theme.change_window_color(self, app.theme.window_color)
        app.theme.change_text_color(self, app.theme.text_color)


class PopUpMenuAction(QAction):
    def __init__(self, text=None, icon=None, click_event=None):
        super().__init__()

        if text is not None:
            self.setText(text)

        if icon is not None:
            self.setIcon(icon)

        if click_event is not None:
            self.triggered.connect(click_event)