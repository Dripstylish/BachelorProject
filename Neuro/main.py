from PySide6.QtWidgets import QMainWindow

from Neuro.client.setup import setup_app
from Neuro.portals.portal_home import HomePortal
from Neuro.portals.portal_notebooks import NotebooksPortal
from PySide6Extended.core import app
from PySide6Extended.core.application import Builder


class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Neuro")
        # self.setWindowIcon(QIcon('web.png'))  # TODO: set app logo

        setup_app()

        #self.portal = HomePortal()
        self.portal = NotebooksPortal()
        self.root = self.portal.root
        Builder(self, self.root)

    def swap_portal(self, new_portal):
        self.portal = new_portal
        self.root = self.portal.root
        Builder(self, self.root)



if __name__ == "__main__":
    app.set_home(Home)
    app.home.resize(app.screen_resolution[0] / 1.5, app.screen_resolution[1] / 1.5)
    app.start()
