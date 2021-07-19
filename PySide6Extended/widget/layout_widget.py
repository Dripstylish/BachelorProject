from PySide6Extended.widget.layout import QBoxHorizontal, QBoxVertical
from PySide6Extended.widget.widget import Widget


class Layout(Widget):
    """
    The default layout widget class
    """

    def __init__(self, layout=None, children=None, background=None):
        super().__init__(layout, children, background)


class LayoutBoxHorizontal(Layout):
    """
    A widget containing the QBoxHorizontal layout
    """

    def __init__(self, children=None, background=None):
        super().__init__(QBoxHorizontal(), children, background)


class LayoutBoxVertical(Layout):
    """
    A widget containing the QBoxVertical layout
    """

    def __init__(self, children=None, background=None):
        super().__init__(QBoxVertical(), children, background)
