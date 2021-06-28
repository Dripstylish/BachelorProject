import copy

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QPushButton, QTextEdit

from SecondBrain.Gui.Application import app, icon
from SecondBrain.Gui.Extended import Widget, QBoxHorizontal, Button
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


class TextEditor(Widget):
    def __init__(self):

        self.editor = TextEditorMainWindow()
        self.stylizer = TextEditorStylizer(self.editor)
        self.editor.setStylizer(self.stylizer)
        
        super(TextEditor, self).__init__(children=[self.stylizer, self.editor])


class TextEditorMainWindow(QTextEdit):
    def __init__(self):
        super(TextEditorMainWindow, self).__init__()

        self.setViewportMargins(10, 10, 10, 10)
        app.theme.change_placeholder_text_color(self, app.theme.highlight_text_color)
        self.setPlaceholderText("Type here ...")

        self.stylizer = None

    def setStylizer(self, stylizer):
        self.stylizer = stylizer

    def mousePressEvent(self, e):
        super(TextEditorMainWindow, self).mousePressEvent(e)

        # check bold
        if self.fontWeight() == QFont.Bold:
            self.stylizer.bold_button.toggle_on()
        else:
            self.stylizer.bold_button.toggle_off()

        # check italics
        if self.fontItalic():
            self.stylizer.italics_button.toggle_on()
        else:
            self.stylizer.italics_button.toggle_off()

        # check underline
        # if self.fontUnderline():
        #     self.stylizer.underline_button.toggle_on()
        # else:
        #     self.stylizer.underline_button.toggle_off()


class TextEditorStylizer(Widget):
    def __init__(self, editor):
        self.editor = editor
        super(TextEditorStylizer, self).__init__(layout=QBoxHorizontal())

        self.bold_button = StyleButton(icon=icon.fi_rr_bold, click_event=self.style_bold)
        self.italics_button = StyleButton(icon=icon.fi_rr_italic, click_event=self.style_italics)
        #self.underline_button = StyleButton(icon=icon.fi_rr_underline, click_event=self.style_underline) # underline does not seem to work proper in pyside6 currently

        self.addWidget(self.bold_button)
        self.addWidget(self.italics_button)
        #self.addWidget(self.underline_button)

        self.addStretch()

    def style_bold(self):
        if self.bold_button.button_toggled:
            self.editor.setFontWeight(QFont.Normal)
        else:
            self.editor.setFontWeight(QFont.Bold)

    def style_italics(self):
        if self.italics_button.button_toggled:
            self.editor.setFontItalic(False)
        else:
            self.editor.setFontItalic(True)

    def style_underline(self):
        if self.italics_button.button_toggled:
            font = QFont()
            current_font = self.editor.currentFont()
            if current_font.bold():
                font.setBold(True)
            if current_font.italic():
                font.setItalic(True)
            self.editor.setCurrentFont(font)
        else:
            self.editor.setFontUnderline(True)


class StyleButton(Button):
    def __init__(self, text=None, icon=None, click_event=None):
        super(StyleButton, self).__init__(text, icon, click_event)
        self.button_toggled = False
        self.setFixedWidth(40)

    def mouseReleaseEvent(self, e):
        super(StyleButton, self).mouseReleaseEvent(e)
        self.toggle_button()

    def toggle_button(self):
        if self.button_toggled:
            self.toggle_off()
        else:
            self.toggle_on()

    def toggle_on(self):
        self.setStyleSheet("background-color:{};".format(app.theme.pressed_color))
        self.button_toggled = True

    def toggle_off(self):
        self.setStyleSheet("")
        self.button_toggled = False


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
