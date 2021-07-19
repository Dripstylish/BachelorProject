from PySide6.QtWidgets import QLabel

from PySide6Extended.widget.layout_widget import LayoutBoxVertical
from PySide6Extended.widget.layout import QBoxHorizontal
from PySide6Extended.widget.widget import Widget


class Scaffold(Widget):
    """
    A widget used to build a standard layout in an application
    """

    def __init__(self, appbar=None, sidemenu=None, page=None):
        scaffold_list = []

        if sidemenu is not None:
            scaffold_list.append(sidemenu)

        if appbar is not None or page is not None:
            self.main = LayoutBoxVertical()
            if appbar is not None:
                self.main.addWidget(appbar)
            if page is not None:
                self.main.addWidget(page)
            else:
                self.main.addWidget(QLabel("Error: Empty Page"))
            scaffold_list.append(self.main)

        super().__init__(QBoxHorizontal(), scaffold_list)
