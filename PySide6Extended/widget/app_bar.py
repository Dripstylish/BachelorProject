from PySide6Extended.core import app
from PySide6Extended.widget.container import Container
from PySide6Extended.widget.layout import QBoxHorizontal
from PySide6Extended.widget.widget import Widget


class AppBar(Widget):
    """
    A class to build an application top bar
    """

    def __init__(self, left=None, center=None, right=None):
        super().__init__(QBoxHorizontal(), [])
        self.setAutoFillBackground(True)
        self.setFixedHeight(50)
        app.theme.change_window_color(self, app.theme.primary_color)

        if left is not None:
            padding = Container()
            padding.setFixedWidth(15)
            self.addWidget(padding)
            for child in left:
                self.addWidget(child)
        else:
            self.addWidget(Container())

        self.addStretch()

        if center is not None:
            for child in center:
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
