from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel

import Neuro.client.database as db
from Neuro.client import client
from Neuro.widgets.page import SettingsPage, Page
from Neuro.widgets.portal import Portal
from Neuro.widgets.side_menu import SideMenuButton, SideMenu, DraggableSideMenuButton
from PySide6Extended.core import app
from PySide6Extended.widget import ProfileButton, Container, AppBar, Scaffold
from PySide6Extended.widget.rich_text_editor import TextEditor

icon = app.theme.icon


class NotebookPortal(Portal):
    def __init__(self, title, parent_notebook):
        self.title = title
        self.parent_notebook = parent_notebook
        super().__init__(title)
        self.my_type = NotebookPortal

        # create settings menu
        self.profile_button = ProfileButton(client.username, client.profile_picture)
        self.profile_button.clicked.connect(self.swap_page_settings)
        profile_container = Container(children=[self.profile_button])
        profile_container.setMinimumHeight(50)

        # create new notebook button
        add_page_button = SideMenuButton("New Page", QIcon(icon.fi_rr_plus_small), click_event=self.create_new_page)
        bottom_container = Container(children=[add_page_button])

        # create app bar
        self.appbar = AppBar(
            left=[self.breadcrumb]
        )

        # load notebook pages
        if db.get_all_notebook_pages(self.parent_notebook.id):
            side_menu_buttons = []
            for notebook_page in dict(db.get_all_notebook_pages(self.parent_notebook.id)).values():
                loaded_notebook_page = NotebookPage(notebook_page["page_title"], self, parent_notebook, notebook_page["page_id"])
                loaded_notebook_page.load_contents(notebook_page["page_contents"])
                loaded_notebook_page.save()
                side_menu_buttons.append(loaded_notebook_page.button)
        else:
            notebook_page = NotebookPage("New Page", self, self.parent_notebook)
            notebook_page.save()
            side_menu_buttons = [notebook_page.button]

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

        self.main_page.addWidget(QLabel("Notebook Page"))

    def swap_page_settings(self):
        page_settings = SettingsPage(self.profile_button, self.swap_page_settings)
        print(self.family_tree[0])
        page_settings.set_parent_portal(self.family_tree[0])
        self.swap_page(page_settings)

    def swap_portal_home(self):
        new_self = self.my_type(self.title, self.parent_notebook)
        if self.parent is not None:
            new_self.set_parent(self.parent)
        app.home.swap_portal(new_self)
        new_self.page_subscription.push_notification()

    def create_new_page(self):
        page = NotebookPage("New Page", self, self.parent_notebook)
        page.save()
        self.side_menu.list_widget.append(page.button, page.button.text())

class NotebookPage(Page):
    def __init__(self, title, portal, parent, id=None):
        self.portal = portal
        self.button = NotebookPageButton(title, self.portal, self)

        self.editor = TextEditor(self)
        super().__init__(title, self.button, children=[self.editor])

        self.parent = parent

        if id:
            self.id = id
        else:
            print(db.get_last_notebook_page_id(self.parent.id))
            self.id = str(int(db.get_last_notebook_page_id(self.parent.id)) + 1)

        self.save()

    def save(self):
        page_dict = {
            "page_title": self.name,
            "page_id": self.id,
            "page_contents": self.editor.main_window.toHtml()
        }

        if db.get_notebook_page(self.parent.id, self.id):
            result = db.get_notebook_page(self.parent.id, self.id)
            key = result[0]
            self.parent.pages[key] = page_dict
            self.parent.save()
        else:
            self.parent.pages[str(len(self.parent.pages))] = page_dict
            print(self.parent.pages)
            self.parent.save()

    def delete(self):
        db.delete_notebook_page(self.parent.id, self.id)

    def get_save_dict(self):
        page_dict = {
            "page_title": self.name,
            "page_id": self.id,
            "page_contents": self.editor.main_window.toHtml()
        }
        return page_dict

    def load_contents(self, page_contents):
        self.editor.main_window.setHtml(page_contents)


class NotebookPageButton(DraggableSideMenuButton):
    def __init__(self, text: str, portal, parent):
        self.parent = parent
        self.portal = portal
        super().__init__(text, click_event=self.swap_page)

    def save(self):
        self.parent.save()

    def delete(self):
        self.parent.delete()
        self.parentWidget().removeWidget(self)

    def swap_page(self):
        self.portal.swap_page(self.parent)
