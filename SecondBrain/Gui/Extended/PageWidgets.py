import copy

from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QLabel, QPushButton, QTextEdit

from SecondBrain.Gui.Extended import Widget, QBoxHorizontal
from SecondBrain.client import client


class Page(Widget):
    def __init__(self, title, children=None):

        editor = TextEditor()

        super(Page, self).__init__(layout=QBoxHorizontal(), children=[editor])
        self.page_title = title
        self.parent = None
        self.family_tree = [self]

    def set_parent_page(self, parent):
        self.parent = parent
        self.family_tree = copy.copy(parent.family_tree)
        self.family_tree.append(self)

    def rename_page(self, new_title):
        self.page_title = new_title

    def save(self):
        page_dict = {
            "page_title": self.page_title
        }
        return page_dict

    def load(self, load_file):
        self.page_title = load_file["page_title"]

class TextEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.select_triggered = False
        self.setViewportMargins(10, 10, 10, 10)
        self.editor_cursor = QTextCursor(self.textCursor())

    def mouseMoveEvent(self, e):
        if self.textCursor().hasSelection():
            self.select_triggered = True
            print()
            #layout = self.document().findBlock(self.textCursor().selectionStart()).layout()
            #position = layout.boundingRect()
            #print(position)
        super().mouseMoveEvent(e)


class Breadcrumb(Widget):
    def __init__(self):
        super().__init__(layout=QBoxHorizontal())
        self.create_breadcrumbs()

    def create_breadcrumbs(self):
        family_tree = client.current_page.family_tree
        if len(family_tree) > 2:
            self.addWidget(BreadcrumbButton(family_tree[0].page_title))
            self.addWidget(QLabel(" > ... > "))
            self.addWidget(BreadcrumbButton(family_tree[len(family_tree - 1)].page_title))
        i = 1
        for node in client.current_page.family_tree:
            button = BreadcrumbButton(node.page_title)
            button.setFixedWidth(self.fontMetrics().boundingRect(button.text()).width()+8)
            self.addWidget(button)
            if i == len(family_tree):
                return
            else:
                label = QLabel(" > ")
                label.setFixedWidth(15)
                self.addWidget(label)
                i += 1

    def update_breadcrumbs(self):
        self.deleteAll()
        self.create_breadcrumbs()

class BreadcrumbButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
