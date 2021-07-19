from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QFileDialog

from Gui_unrefactored.Extended import Container

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class FileDialogExample(Container):
    def __init__(self):
        super().__init__()
        filter = "Wav File (*.wav)"
        self._audio_file = QFileDialog.getOpenFileName(self, "Audio File",
                                                   "/myfolder/folder", filter)
        self._audio_file = str(self._audio_file)