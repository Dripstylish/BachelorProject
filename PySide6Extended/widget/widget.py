from PySide6.QtWidgets import QWidget

from PySide6Extended.core import app
from PySide6Extended.widget.layout import QBoxVertical


class Widget(QWidget):
    """
    An extension of QWidget, that allows functionality closer to Flutter or Kivy
    """

    def __init__(self, layout=None, children=None, background=None):
        super().__init__()

        if layout is None:
            self.layout = QBoxVertical()
        else:
            self.layout = layout

        if children is None:
            self.children = []
        else:
            self.children = children
            for child in children:
                self.layout.addWidget(child)

        self.setLayout(self.layout)

        if background is None:
            app.theme.change_window_color(self, app.theme.window_color)
        else:
            app.theme.change_window_color(self, background)

    # Functions for handling widgets:

    def addWidget(self, widget):
        self.children.append(widget)
        self.layout.addWidget(widget)

    def insertWidget(self, index, widget):
        self.children.insert(index, widget)
        self.layout.insertWidget(index, widget)

    def removeWidget(self, widget):
        self.children.remove(widget)
        self.layout.removeWidget(widget)

    def replaceWidget(self, old_widget, new_widget):
        index = self.indexOf(old_widget)
        self.children.remove(index)
        self.children.insert(index, new_widget)
        self.layout.replaceWidget(old_widget, new_widget)

    def getWidgetAt(self, index):
        return self.children[index]

    def indexOf(self, widget):
        return self.layout.indexOf(widget)

    def exists(self, widget):
        if self.indexOf(widget) is not None and self.indexOf(widget) != -1:
            return True
        else:
            return False

    def deleteAll(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        self.children = []

    # Other functions:

    def addStretch(self):
        self.layout.addStretch()

    def addSeparator(self):
        self.layout.addSeparator()
