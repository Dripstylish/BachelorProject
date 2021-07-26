from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel

import Neuro.client.database as db
from Neuro.client import client
from Neuro.portals.portal_notebook import NotebookPortal
from Neuro.widgets.page import SettingsPage
from Neuro.widgets.portal import Portal
from Neuro.widgets.search_field import SearchField
from Neuro.widgets.side_menu import SideMenu, SideMenuButton, DraggableSideMenuButton
from PySide6Extended.core import app
from PySide6Extended.widget import ProfileButton, Container, AppBar, Scaffold

icon = app.theme.icon


class NotebooksPortal(Portal):
    def __init__(self):
        super().__init__("Notebooks")
        self.my_type = NotebooksPortal

        # create settings menu
        self.profile_button = ProfileButton(client.username, client.profile_picture)
        self.profile_button.clicked.connect(self.swap_page_settings)
        profile_container = Container(children=[self.profile_button])
        profile_container.setMinimumHeight(50)

        # create new notebook button
        add_page_button = SideMenuButton("New Notebook", QIcon(icon.fi_rr_plus_small), click_event=self.new_notebook)
        bottom_container = Container(children=[add_page_button])

        # create app bar
        self.appbar = AppBar(
            left=[self.breadcrumb]
        )

        # load notebooks
        if db.get_all_notebooks():
            side_menu_buttons = []
            for notebook in dict(db.get_all_notebooks()).values():
                loaded_notebook = Notebook(notebook["title"], notebook["id"], self, notebook["pages"])
                loaded_notebook.save()
                side_menu_buttons.append(loaded_notebook.button)
        else:
            notebook = Notebook("New Notebook", portal=self)
            notebook.save()
            side_menu_buttons = [notebook.button]

        # create side menu and install buttons
        self.side_menu = SideMenu(
            top=profile_container,
            middle=side_menu_buttons,
            bottom=bottom_container,
            portal=self)

        self.root = Scaffold(
            appbar=self.appbar,
            sidemenu=self.side_menu,
            page=self.main_page
        )

        self.main_page.addWidget(QLabel("Notebooks Main Page"))

    def swap_page_settings(self):
        page_settings = SettingsPage(self.profile_button, self.swap_page_settings)
        print(self.family_tree[0])
        page_settings.set_parent_portal(self.family_tree[0])
        self.swap_page(page_settings)

    def new_notebook(self):
        notebook = Notebook("New Notebook", portal=self)
        self.side_menu.list_widget.append(notebook.button, notebook.button.text())
        notebook.save()


class Notebook:
    def __init__(self, text: str, id: str = None, portal: NotebooksPortal = None, pages: dict = None):
        self.name = text

        self.portal = portal

        if pages:
            self.pages = pages
        else:
            self.pages = {}

        if id is not None:
            self.id = id
        else:
            self.id = str(int(db.get_last_notebook_id()) + 1)

        self.button = NotebookButton(text, portal, self)

    def check_if_page_exists(self, page):
        for notebook_page in self.pages.values():
            if notebook_page["page_id"] == page.id:
                return True
        return False

    def save(self):
        notebook_dict = {
            "title": self.name,
            "id": self.id,
            "pages": self.pages
        }
        if db.get_notebook(self.id):
            db.update_notebook(self.id, notebook_dict)
        else:
            db.add_notebook(notebook_dict)

    def delete(self):
        db.delete_notebook(self.id)


class NotebookButton(DraggableSideMenuButton):
    def __init__(self, text: str, portal, parent: Notebook):
        self.parent = parent
        self.portal = portal
        super().__init__(text, click_event=self.enter_notebook)

    def enter_notebook(self):
        self.portal.swap_portal(NotebookPortal(self.text(), self.parent))

    def save(self):
        self.parent.save()

    def delete(self):
        self.parent.delete()
        self.parentWidget().removeWidget(self)
