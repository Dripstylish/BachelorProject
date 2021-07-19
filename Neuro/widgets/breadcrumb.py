from PySide6.QtWidgets import QLabel

from PySide6Extended.widget import Button
from PySide6Extended.widget.layout import QBoxHorizontal
from PySide6Extended.widget.widget import Widget


class Breadcrumb(Widget):
    def __init__(self, path: list = None):
        super().__init__(layout=QBoxHorizontal())
        self.breadcrumb_path = None
        if path is not None:
            self.set_breadcrumb_path(path)
        else:
            self.set_breadcrumb_path([])

    def set_breadcrumb_path(self, path: list):
        self.breadcrumb_path = path
        self.update_breadcrumbs()

    def create_breadcrumbs(self):
        if len(self.breadcrumb_path) > 3:
            self.addWidget(BreadcrumbButton(self.breadcrumb_path[0].name, self.breadcrumb_path[0].icon, self.breadcrumb_path[0].click_event))
            self.addWidget(QLabel(" > ... > "))
            self.addWidget(BreadcrumbButton(self.breadcrumb_path[len(self.breadcrumb_path) - 2].name, self.breadcrumb_path[len(self.breadcrumb_path) - 2].icon, self.breadcrumb_path[len(self.breadcrumb_path) - 2].click_event))
            self.addWidget(QLabel(" > "))
            self.addWidget(BreadcrumbButton(self.breadcrumb_path[len(self.breadcrumb_path) - 1].name, self.breadcrumb_path[len(self.breadcrumb_path) - 1].icon, self.breadcrumb_path[len(self.breadcrumb_path) - 1].click_event))
            return
        i = 1
        for node in self.breadcrumb_path:
            button = BreadcrumbButton(node.name, node.icon, node.click_event)
            button.setFixedWidth(self.fontMetrics().boundingRect(button.text()).width()+8)
            self.addWidget(button)
            if i == len(self.breadcrumb_path):
                return
            else:
                label = QLabel(" > ")
                label.setFixedWidth(15)
                self.addWidget(label)
                i += 1

    def update_breadcrumbs(self):
        self.deleteAll()
        self.create_breadcrumbs()


class BreadcrumbButton(Button):
    def __init__(self, text, icon=None, click_event=None):
        super().__init__(text, icon, click_event)
