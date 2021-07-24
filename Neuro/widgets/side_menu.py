from PySide6 import QtCore, QtGui
from PySide6.QtCore import QMimeData, QSize, QTimer
from PySide6.QtGui import QDrag, QAction
from PySide6.QtWidgets import QLineEdit, QDialog

from Neuro.client import client
import Neuro.client.database as db
from PySide6Extended.core import app
from PySide6Extended.widget import Button, LayoutBoxHorizontal
from PySide6Extended.widget.layout import QBoxVertical
from PySide6Extended.widget.pop_up_menu import PopUpMenu
from PySide6Extended.widget.scroll import ScrollArea
from PySide6Extended.widget.widget import Widget


class SideMenu(Widget):
    def __init__(self, top=None, middle=None, bottom=None, portal=None):
        super().__init__(QBoxVertical())
        if portal is not None:
            self.portal = portal
            self.portal.subscribe_to_save(self, self.save)

        self.list_widget = None

        if top is not None:
            self.addWidget(top)

        if middle is not None:
            self.list_widget = SideMenuListWidget(middle)

            layout = QBoxVertical()
            layout.addWidget(self.list_widget)
            layout.addStretch()

            scroll_area = ScrollArea(layout=layout, background=app.theme.window_secondary_color)
            self.addWidget(scroll_area)

        if bottom is not None:
            self.addWidget(bottom)

        self.setAutoFillBackground(True)
        self.setFixedWidth(200)
        app.theme.change_window_color(self, app.theme.window_secondary_color)

    def save(self):
        if self.portal is None:
            return
        self.list_widget.save()


class SideMenuListWidget(Widget):
    def __init__(self, children):
        if children:
            self.button_type = type(children[0])
        else:
            self.button_type = DraggableSideMenuButton

        new_children = [SideMenuDropArea(self)]
        for child in children:
            child.addParentListWidget(self)
            new_children.append(child)
            new_children.append(SideMenuDropArea(self))
        super().__init__(children=new_children)
        self.setAutoFillBackground(True)
        self.setAcceptDrops(True)
        app.theme.change_window_color(self, app.theme.window_secondary_color)

    def append(self, widget, text):
        if self.exists(widget):
            previous_index = self.indexOf(widget)
            self.removeWidget(self.getWidgetAt(previous_index))
            self.removeWidget(self.getWidgetAt(previous_index - 1))
        new_button = self.button_type(text, widget.portal, widget.parent)
        new_button.addParentListWidget(self)
        self.addWidget(new_button)
        self.addWidget(SideMenuDropArea(self))

    def appendAtTop(self, widget, text):
        if self.exists(widget):
            previous_index = self.indexOf(widget)
            self.removeWidget(self.getWidgetAt(previous_index))
            self.removeWidget(self.getWidgetAt(previous_index - 1))
        new_button = self.button_type(text, widget.portal, widget.parent)
        new_button.addParentListWidget(self)
        self.insertWidget(0, new_button)
        self.insertWidget(0, SideMenuDropArea(self))

    def insert(self, index, widget, text):
        if index == 0:
            self.appendAtTop(widget, text)
            self.clean_list()
            return
        if index == len(self.children) - 1:
            self.append(widget, text)
            self.clean_list()
            return
        if self.exists(widget):
            previous_index = self.indexOf(widget)
            self.removeWidget(self.getWidgetAt(previous_index))
            self.removeWidget(self.getWidgetAt(previous_index - 1))
            if previous_index <= index:
                index = index - 2
        new_button = self.button_type(text, widget.portal, widget.parent)
        new_button.addParentListWidget(self)
        self.insertWidget(index, new_button)
        self.insertWidget(index, SideMenuDropArea(self))
        self.clean_list()

    def remove(self, widget):
        index = self.indexOf(widget)
        self.removeWidget(widget)
        self.removeWidget(self.getWidgetAt(index - 1))

    def clean_list(self):
        clean_list = [SideMenuDropArea(self)]
        while self.children:
            if issubclass(type(self.children[0]), DraggableSideMenuButton):
                clean_list.append(self.children[0])
                clean_list.append(SideMenuDropArea(self))
                self.children[0].delete()
                #save_file.save_file["side_menu"].pop("{}".format(self.children[0].id))
            self.removeWidget(self.children[0])

        for child in clean_list:
            self.addWidget(child)
            if issubclass(type(child), DraggableSideMenuButton):
                child.save()

    def save(self):
        for child in self.children:
            if issubclass(type(child), DraggableSideMenuButton):
                child.save()


class SideMenuDropArea(Widget):
    def __init__(self, parent_list):
        super().__init__()
        self.parent_list = parent_list
        self.setAutoFillBackground(True)
        self.setAcceptDrops(True)
        app.theme.change_window_color(self, app.theme.window_secondary_color)
        self.setFixedHeight(5)

    def dragEnterEvent(self, e):
        mime_data = e.mimeData()
        if issubclass(type(mime_data.button_object), DraggableSideMenuButton) and self.parent_list == mime_data.parent_list_widget:
            if self.parent_list.indexOf(mime_data.button_object) == self.parent_list.indexOf(
                    self) + 1 or self.parent_list.indexOf(mime_data.button_object) == self.parent_list.indexOf(
                self) - 1 or self.parent_list.indexOf(mime_data.button_object) == -1:
                pass
            else:
                app.theme.change_window_color(self, app.theme.highlight_color)
                e.accept()
        super().dragEnterEvent(e)

    def dragLeaveEvent(self, e):
        app.theme.change_window_color(self, app.theme.window_secondary_color)
        super().dragLeaveEvent(e)

    def dropEvent(self, e):
        app.theme.change_window_color(self, app.theme.window_secondary_color)
        e.accept()
        mime_data = e.mimeData()
        if issubclass(type(mime_data.button_object), DraggableSideMenuButton) and self.parent_list == mime_data.parent_list_widget:
            index = self.parent_list.indexOf(self)
            text = mime_data.button_text
            self.parent_list.insert(index, mime_data.button_object, text)
            mime_data.button_object.deleteLater()
        super().dropEvent(e)


class SideMenuButton(Button):
    def __init__(self, text, icon=None, click_event=None, list_widget=None):
        self.parent_list = None

        super().__init__(text, icon, click_event)
        if list_widget is not None:
            self.list_widget = list_widget

        if icon is not None:
            self.setIconSize(QSize(20, 20))

    def addParentListWidget(self, parent_list):
        self.parent_list = parent_list


class DraggableSideMenuButton(SideMenuButton):
    def __init__(self, text, button_id=None, image=None, click_event=None):
        super().__init__(text, image)
        self.setAutoFillBackground(True)
        self.drag = QDrag(self)
        self.click_hold = False
        self.setAcceptDrops(True)
        self.drop_zone = None

        if button_id is None:
            self.id = client.get_button_id()
        else:
            self.id = button_id

        self.click_event = click_event

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.button_held_check())
        self.held_time = 0

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        self.fold_out_menu = PopUpMenu(self)
        rename_button = QAction('Rename', self)
        rename_button.triggered.connect(self.rename)
        self.fold_out_menu.addAction(rename_button)
        delete_button = QAction('Delete', self)
        delete_button.triggered.connect(self.delete)
        self.fold_out_menu.addAction(delete_button)

    def context_menu(self, point):
        self.fold_out_menu.exec(self.mapToGlobal(point))

    def button_held_check(self):
        self.held_time += 0.05

    def mouseMoveEvent(self, e):
        if e.buttons() != QtCore.Qt.LeftButton or self.held_time < 0.2:
            return
        mime_data = SideMenuButtonMimeData(self, self.parent_list, self.text())
        mime_data.setText(self.text())

        self.drag = QDrag(self)
        self.drag.setMimeData(mime_data)
        self.drag.setHotSpot(e.pos())

        pixmap = QtGui.QPixmap(self.size())
        self.render(pixmap)
        self.drag.setPixmap(pixmap)
        self.drag.exec(QtCore.Qt.MoveAction)

    def mousePressEvent(self, e):
        self.setStyleSheet("background-color:{};".format(app.theme.button_pressed_color))
        self.timer.start(50)

        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.setStyleSheet("background-color:{};".format(app.theme.highlight_color))
        self.timer.stop()

        if self.held_time < 0.2:
            if self.click_event:
                self.click_event()

        self.held_time = 0

        super().mouseReleaseEvent(e)

    def enterEvent(self, e):
        self.setStyleSheet("background-color:{};".format(app.theme.highlight_color))
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.setStyleSheet("background-color:{};".format(app.theme.window_secondary_color))
        super().leaveEvent(e)

    def dragEnterEvent(self, e):
        mime_data = e.mimeData()
        if mime_data.button_object != self:
            if self.parent_list.indexOf(self) < len(self.parent_list.children) - 2:
                if mime_data.button_object == self.parent_list.getWidgetAt(self.parent_list.indexOf(self) + 2):
                    return
            if issubclass(type(mime_data.button_object), DraggableSideMenuButton) and self.parent_list == mime_data.parent_list_widget:
                e.accept()
                self.drop_zone = self.parent_list.getWidgetAt(self.parent_list.indexOf(self) + 1)
                app.theme.change_window_color(self.drop_zone, app.theme.highlight_color)
        else:
            e.ignore()
        super().dragEnterEvent(e)

    def dragLeaveEvent(self, e):
        app.theme.change_window_color(self.drop_zone, app.theme.window_secondary_color)
        super().dragLeaveEvent(e)

    def dropEvent(self, e):
        mime_data = e.mimeData()
        app.theme.change_window_color(self.drop_zone, app.theme.window_secondary_color)
        if mime_data.button_object != self:
            e.accept()
            if issubclass(type(mime_data.button_object), DraggableSideMenuButton) and self.parent_list == mime_data.parent_list_widget:
                index = self.parent_list.indexOf(self.drop_zone)
                text = mime_data.button_text
                self.parent_list.insert(index, mime_data.button_object, text)
                mime_data.button_object.deleteLater()
        else:
            e.ignore()
        super().dropEvent(e)

    def rename(self):
        SideMenuButtonRenameDialog(self)
        self.save()

    def delete(self):
        self.parent_list.remove(self)
        self.save()

    def save(self):
        print("not implemented save button")
        button_dict = {
            "id": self.id,
            "text": self.text(),
        }
        # todo

    def load(self, load_file):
        self.id = load_file["id"]
        self.setText(load_file["text"])


class SideMenuButtonMimeData(QMimeData):
    def __init__(self, button_object, parent_list, text, click_event=None):
        super().__init__()
        self.button_object = button_object
        self.parent_list_widget = parent_list
        self.button_text = text
        self.click_event = click_event


class SideMenuButtonRenameDialog(QDialog):
    def __init__(self, button, parent=None):
        super().__init__(parent)
        self.button = button
        self.setWindowTitle("Rename")

        layout = QBoxVertical()
        self.setLayout(layout)

        self.name_box = QLineEdit(self.button.text())

        layout.addWidget(LayoutBoxHorizontal(
            children=[self.name_box]
        ))

        layout.addWidget(LayoutBoxHorizontal(
            children=[
                Button("Accept", click_event=self.rename),
                Button("Cancel", click_event=self.cancel)
            ]
        ))

        self.exec()

    def rename(self):
        self.button.setText(self.name_box.text())
        self.button.parent.name = self.name_box.text()
        self.button.portal.page_subscription.push_notification()
        self.close()

    def cancel(self):
        self.close()