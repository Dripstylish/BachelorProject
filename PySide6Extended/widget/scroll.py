from PySide6.QtWidgets import QScrollArea, QFrame

from PySide6Extended.widget.widget import Widget


class ScrollArea(QScrollArea):
    """
    A class used to create a scroll area with a widget inside of it to handle nesting
    """

    def __init__(self, layout=None, children=None, background=None):
        super().__init__()
        self.setAutoFillBackground(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setWidgetResizable(True)
        self.root = Widget(layout, children, background)
        self.setWidget(self.root)

    def addWidget(self, widget):
        self.root.addWidget(widget)

    def insertWidget(self, index, widget):
        self.root.insertWidget(index, widget)

    def removeWidget(self, widget):
        self.root.removeWidget(widget)

    def replaceWidget(self, old_widget, new_widget):
        self.replaceWidget(old_widget, new_widget)

    def getWidgetAt(self, index):
        return self.root.getWidgetAt(index)

    def indexOf(self, widget):
        return self.root.indexOf(widget)

    def exists(self, widget):
        return self.root.exists(widget)

    def deleteAll(self):
        self.root.deleteAll()
