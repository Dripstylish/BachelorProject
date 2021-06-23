import sys

from PySide6.QtWidgets import QApplication

from SecondBrain.Gui.Theme.Icon import Icon
from SecondBrain.Gui.Theme import Theme

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.theme = Theme(self.app)

    def start(self):
        self.app.exec()

app = App()
icon = Icon(app.theme)
icon.load_icons()
