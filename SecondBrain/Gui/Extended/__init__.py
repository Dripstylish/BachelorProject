from PySide6.QtGui import QPalette, QAction
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QFrame, QMenu

from SecondBrain.Gui.Application import app

class Builder:
    """
    A class used to initialise the main Application screen easily
    """

    def __init__(self, main, root):
        main.setCentralWidget(root)


class QBoxVertical(QVBoxLayout):
    """
    An extention of QVBoxLayout that fully stretches across the screen
    """

    def __init__(self, ):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)


class QBoxHorizontal(QHBoxLayout):
    """
    An extention of QHBoxLayout that fully stretches across the screen
    """

    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)


class Widget(QWidget):
    """
    An extention of QWidget, that allows functionality closer to Flutter or Kivy
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

        palette = self.palette()
        if background is None:
            palette.setColor(QPalette.Window, app.theme.window_color)
        else:
            palette.setColor(QPalette.Window, background)
        self.setPalette(palette)

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

    def getChildAt(self, index):
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

    def addStretch(self):
        self.layout.addStretch()

class ScrollArea(QScrollArea):
    def __init__(self, layout=None, children=None, background=None, stretch_buttom=False):
        super().__init__()
        self.setAutoFillBackground(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setWidgetResizable(True)

        palette = self.palette()
        if background is None:
            palette.setColor(QPalette.Window, app.theme.window_color)
        else:
            palette.setColor(QPalette.Window, background)
        self.setPalette(palette)

        if layout is None:
            self.root = LayoutBoxVertical(children, background=background, stretch_buttom=stretch_buttom)
        else:
            self.root = layout
        self.setWidget(self.root)


class LayoutBoxHorizontal(Widget):
    """
    A widget, that contains the QBoxHorizontal layout
    """

    def __init__(self, children=None):
        super().__init__(QBoxHorizontal(), children)


class LayoutBoxVertical(Widget):
    """
    A widget, that contains the QBoxVertical layout
    """

    def __init__(self, children=None, stretch_top=False, stretch_buttom=False, background=None):

        layout = QBoxVertical()
        if stretch_top:
            layout.addStretch()
        if children is not None:
            for child in children:
                layout.addWidget(child)
        if stretch_buttom:
            layout.addStretch()

        super().__init__(layout, None, background)


class Scaffold(Widget):
    """
    A widget used as the main scaffold of an Application
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
                for child in page:
                    self.main.addWidget(child)
            else:
                self.main.addWidget(QLabel("Error: Empty Page"))
            scaffold_list.append(self.main)
        super().__init__(QBoxHorizontal(), scaffold_list)


class AppBar(Widget):
    def __init__(self, left=None, right=None):
        super().__init__(QBoxHorizontal(), [])
        self.setAutoFillBackground(True)
        self.setFixedHeight(50)
        app.theme.change_window_color(self, app.theme.window_color)

        if left is not None:
            padding = Container()
            padding.setFixedWidth(15)
            self.addWidget(padding)
            for child in left:
                self.addWidget(child)
        else:
            self.addWidget(Container())
        self.addStretch()
        if right is not None:
            for child in right:
                self.addWidget(child)
            padding = Container()
            padding.setFixedWidth(15)
            self.addWidget(padding)
        else:
            self.addWidget(Container())


class Container(Widget):
    """
    A simple container widget
    """
    def __init__(self, layout=None, children=None, background=None):
        super().__init__(layout, children, background)


class Button(QPushButton):
    def __init__(self, text, icon=None, click_event=None):
        super().__init__(text)
        if icon is not None:
            self.setIcon(icon)

        if click_event is not None:
            self.clicked.connect(click_event)


class PopUpMenu(QMenu):
    def __init__(self, parent=None):
        super(PopUpMenu, self).__init__(parent)

        app.theme.change_window_color(self, app.theme.window_color)
        app.theme.change_text_color(self, app.theme.text_color)


class PopUpMenuAction(QAction):
    def __init__(self, text=None, icon=None, click_event=None):
        super(PopUpMenuAction, self).__init__()

        if text is not None:
            self.setText(text)

        if icon is not None:
            self.setIcon(icon)

        if click_event is not None:
            self.triggered.connect(click_event)