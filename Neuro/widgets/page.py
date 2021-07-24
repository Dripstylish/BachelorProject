import copy

from PySide6.QtWidgets import QLabel

from PySide6Extended.widget.layout import QBoxHorizontal
from PySide6Extended.widget.widget import Widget


class Page(Widget):
    def __init__(self, title, parent_button=None, icon=None, click_event=None, children=None):
        super().__init__(layout=QBoxHorizontal(), children=children)
        self.parent_button = parent_button
        self.parent = None
        self.name = title
        self.icon = icon
        self.click_event = click_event
        self.family_tree = [self]

    def set_parent_portal(self, parent):
        self.parent = parent
        self.family_tree = copy.copy(parent.family_tree)

        if self.name is not None:
            self.family_tree.append(self)

    def rename_page(self, new_title):
        self.name = new_title

    def save(self):
        pass

    def load(self, load_file):
        pass

class SettingsPage(Page):
    def __init__(self, parent_button, click_event):

        children = [QLabel("Settings Page")]

        super().__init__("Settings", parent_button, children=children, click_event=click_event)