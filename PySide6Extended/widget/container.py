from PySide6Extended.widget.widget import Widget


class Container(Widget):
    """
    A class for a simple container widget
    """

    def __init__(self, layout=None, children=None, background=None):
        super().__init__(layout, children, background)
