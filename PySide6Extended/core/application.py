import sys
import pyautogui
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6Extended.core.style.theme import Theme

class App:
    """
    A class used to initialise an application
    """
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.theme = Theme(self.app)
        self.screen_resolution = pyautogui.size()

        self.home_class = QMainWindow
        self.home = QMainWindow()

    def set_home(self, home):
        self.home_class = home
        self.home = home()

    def start(self):
        self.home.show()
        self.app.exec()

    def reload(self):
        size = self.home.size()
        self.home.hide()
        self.home.deleteLater()
        self.home = self.home_class()
        self.home.resize(size)
        self.home.show()

    def swap_home(self, new_home):
        size = self.home.size()
        self.set_home(new_home)
        self.home.resize(size)
        self.reload()


class Builder:
    """
    A class used to handle application settings and start-up functions
    """

    def __init__(self, main_window, root):
        main_window.setCentralWidget(root)
