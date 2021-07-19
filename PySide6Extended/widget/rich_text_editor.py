from PySide6 import QtCore
from PySide6.QtGui import QFont, QTextListFormat
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtWidgets import QTextEdit, QDialog, QComboBox

from PySide6Extended.widget import Button
from PySide6Extended.widget.layout import QBoxHorizontal
from PySide6Extended.widget.widget import Widget
from PySide6Extended.core import app

icon = app.theme.icon

class TextEditor(Widget):
    def __init__(self, parent_page):

        self.parent_page = parent_page
        self.main_window = TextEditorMainWindow(self)
        self.stylizer = TextEditorStylizer(self.main_window)
        self.main_window.setStylizer(self.stylizer)

        super(TextEditor, self).__init__(children=[self.stylizer, self.main_window])

    def save(self):
        self.parent_page.parent_button.save()


class TextEditorMainWindow(QTextEdit):
    def __init__(self, parent_editor):
        super(TextEditorMainWindow, self).__init__()

        self.parent_editor = parent_editor
        self.setViewportMargins(10, 10, 10, 10)
        app.theme.change_placeholder_text_color(self, app.theme.highlight_text_color)
        self.setPlaceholderText("Type here ...")

        self.stylizer = None

    def setStylizer(self, stylizer):
        self.stylizer = stylizer

    def keyPressEvent(self, e):
        super().keyPressEvent(e)
        self.save()

    def mousePressEvent(self, e):
        super(TextEditorMainWindow, self).mousePressEvent(e)
        self.check_styles()

    def keyReleaseEvent(self, e):
        super(TextEditorMainWindow, self).keyReleaseEvent(e)
        if QtCore.Qt.Key.Key_Up or QtCore.Qt.Key.Key_Down or QtCore.Qt.Key.Key_Left or QtCore.Qt.Key.Key_Right:
            self.check_styles()

    def check_styles(self):
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

        # check alignment
        if self.alignment() == QtCore.Qt.AlignLeft:
            self.stylizer.alignment_left.toggle_on()
            self.stylizer.alignment_center.toggle_off()
            self.stylizer.alignment_right.toggle_off()

        if self.alignment() == QtCore.Qt.AlignHCenter:
            self.stylizer.alignment_left.toggle_off()
            self.stylizer.alignment_center.toggle_on()
            self.stylizer.alignment_right.toggle_off()

        if self.alignment() == QtCore.Qt.AlignRight:
            self.stylizer.alignment_left.toggle_off()
            self.stylizer.alignment_center.toggle_off()
            self.stylizer.alignment_right.toggle_on()

        # check font size
        if self.fontPointSize() == 13.0:
            self.stylizer.header_dropdown.setCurrentText("Text")
        if self.fontPointSize() == 40.0:
            self.stylizer.header_dropdown.setCurrentText("Header 1")
        if self.fontPointSize() == 30.0:
            self.stylizer.header_dropdown.setCurrentText("Header 2")
        if self.fontPointSize() == 20.0:
            self.stylizer.header_dropdown.setCurrentText("Header 3")

        # check list
        if self.textCursor().currentList() is not None:
            self.stylizer.bullet_button.toggle_on()
        if self.textCursor().currentList() is None:
            self.stylizer.bullet_button.toggle_off()

    def save(self):
        self.parent_editor.save()


class TextEditorStylizer(Widget):
    def __init__(self, editor):
        layout = QBoxHorizontal()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        super(TextEditorStylizer, self).__init__(layout=layout)

        self.editor = editor

        self.header_dropdown = StyleDropDownHeaders(self)
        self.bold_button = StyleToggleButton(self, icon=icon.fi_rr_bold, click_event=self.style_bold)
        self.italics_button = StyleToggleButton(self, icon=icon.fi_rr_italic, click_event=self.style_italics)
        self.bullet_button = StyleToggleButton(self, icon=icon.fi_rr_list, click_event=self.style_bullet_points)
        self.alignment_left = StyleToggleButton(self, icon=icon.fi_rr_align_left, click_event=self.style_align_left)
        self.alignment_center = StyleToggleButton(self, icon=icon.fi_rr_align_center, click_event=self.style_align_center)
        self.alignment_right = StyleToggleButton(self, icon=icon.fi_rr_align_right, click_event=self.style_align_right)
        self.print_button = StyleButton(self, icon=icon.fi_rr_print, click_event=self.print_page)

        self.addWidget(self.header_dropdown)
        self.addWidget(self.bold_button)
        self.addWidget(self.italics_button)
        self.addWidget(self.bullet_button)
        self.addWidget(self.alignment_left)
        self.addWidget(self.alignment_center)
        self.addWidget(self.alignment_right)
        self.addWidget(self.print_button)

        # underline does not seem to work proper in PySide6 currently
        # self.underline_button = StyleButton(icon=icon.fi_rr_underline, click_event=self.style_underline)
        # self.addWidget(self.underline_button)

        self.addStretch()

    def print_page(self):
        document = self.editor.document()
        printer = QPrinter()
        dlg = QPrintDialog(printer, self)
        if dlg.exec() != QDialog.Accepted:
            return
        document.print_(printer)

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

    def style_align_left(self):
        self.alignment_center.toggle_off()
        self.alignment_right.toggle_off()
        self.editor.setAlignment(QtCore.Qt.AlignLeft)

    def style_align_center(self):
        self.alignment_left.toggle_off()
        self.alignment_right.toggle_off()
        self.editor.setAlignment(QtCore.Qt.AlignHCenter)

    def style_align_right(self):
        self.alignment_left.toggle_off()
        self.alignment_center.toggle_off()
        self.editor.setAlignment(QtCore.Qt.AlignRight)

    def style_bullet_points(self):
        if self.bullet_button.button_toggled:
            self.editor.textCursor().currentList().remove(self.editor.textCursor().block())
            format = self.editor.textCursor().block().blockFormat()
            format.setIndent(0)
            self.editor.textCursor().setBlockFormat(format)
        else:
            listFormat = QTextListFormat()
            listFormat.setStyle(QTextListFormat.ListDisc)
            self.editor.textCursor().createList(listFormat)

    def save(self):
        self.editor.save()


class StyleButton(Button):
    def __init__(self, parent_menu, text=None, icon=None, click_event=None):
        super().__init__(text, icon, click_event)

        self.parent_menu = parent_menu
        self.setFixedWidth(40)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.parent_menu.save()


class StyleToggleButton(Button):
    def __init__(self, parent_menu, text=None, icon=None, click_event=None):
        super().__init__(text, icon, click_event)

        self.parent_menu = parent_menu
        self.button_toggled = False
        self.setFixedWidth(40)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.toggle_button()
        self.parent_menu.save()

    def toggle_button(self):
        if self.button_toggled:
            self.toggle_off()
        else:
            self.toggle_on()

    def toggle_on(self):
        self.setStyleSheet("background-color:{};".format(app.theme.button_pressed_color))
        self.button_toggled = True

    def toggle_off(self):
        self.setStyleSheet("")
        self.button_toggled = False


class StyleDropDown(QComboBox):
    def __init__(self, parent_menu, lists=None):
        super().__init__()
        self.parent_menu = parent_menu

        if lists is None:
            lists = []

        for item in lists:
            self.addItem(item)


class StyleDropDownHeaders(StyleDropDown):
    def __init__(self, parent_menu):
        super().__init__(parent_menu)

        self.addItem("Text")
        self.addItem("Header 1")
        self.addItem("Header 2")
        self.addItem("Header 3")

        self.currentIndexChanged.connect(self.check_selected)

    def check_selected(self):
        if self.currentText() == "Text":
            self.style_text()
        if self.currentText() == "Header 1":
            self.style_header1()
        if self.currentText() == "Header 2":
            self.style_header2()
        if self.currentText() == "Header 3":
            self.style_header3()
        self.parent_menu.save()

    def style_text(self):
        self.parent_menu.editor.setFontPointSize(13)

    def style_header1(self):
        self.parent_menu.editor.setFontPointSize(40)

    def style_header2(self):
        self.parent_menu.editor.setFontPointSize(30)

    def style_header3(self):
        self.parent_menu.editor.setFontPointSize(20)
