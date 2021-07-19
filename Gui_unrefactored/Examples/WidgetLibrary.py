from PySide6 import QtGui, QtWidgets as w
from PySide6.QtWidgets import QMainWindow

from Gui_unrefactored.Application import app
from Gui_unrefactored.Extended import Builder, Scaffold, Container, Button


class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setWindowIcon(QtGui.QIcon('web.png'))

        self.root = Scaffold(
            page=[
                Container(
                    children=[
                        w.QLabel("Label"),
                        Button("PushButton"),
                        w.QComboBox(),
                        w.QDateTimeEdit(),
                        w.QTimeEdit(),
                        w.QDateEdit(),
                        w.QDial(),
                        w.QFontComboBox(),
                        w.QLineEdit(),
                        w.QProgressBar()
                    ]
                ),
                Container(
                    children=[
                        w.QCheckBox("Checkbox"),
                        w.QRadioButton("RadioButton")
                    ]
                ),
                w.QScrollArea(),
                w.QCalendarWidget(),
            ]
        )

        Builder(self, self.root)


if __name__ == "__main__":
    window = Home()
    window.show()

    app.start()
