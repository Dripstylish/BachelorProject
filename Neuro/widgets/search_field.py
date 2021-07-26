from PySide6.QtWidgets import QLineEdit, QDialog

from PySide6Extended.core import app
from PySide6Extended.widget import Button, ScrollArea
from PySide6Extended.widget.layout import QBoxHorizontal, QBoxVertical
from PySide6Extended.widget.widget import Widget


class SearchField(Widget):
    def __init__(self):
        search_field = []

        self.search_field = QLineEdit("")
        search_field.append(self.search_field)
        self.search_button = Button("Search", click_event=self.search)
        search_field.append(self.search_button)

        super().__init__(layout=QBoxHorizontal(), children=search_field)

        self.search_list = None

    def set_search_list(self, search_list):
        self.search_list = search_list

    def search(self):
        print("Error: Overwrite search function!")

    def get_pop_up(self, search_result):
        return SideMenuButtonRenameDialog(search_result)


class SideMenuButtonRenameDialog(QDialog):
    def __init__(self, search_result, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search")

        layout = QBoxVertical()
        self.setLayout(layout)

        scroll_layout = QBoxVertical()
        scroll_area = ScrollArea(layout=scroll_layout, background=app.theme.window_secondary_color, children=search_result)
        layout.addWidget(scroll_area)

        self.exec()
