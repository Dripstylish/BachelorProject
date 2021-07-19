from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout


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

