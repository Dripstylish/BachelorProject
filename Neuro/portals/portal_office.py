from PySide6.QtWidgets import QLabel

from Neuro.client import client
from Neuro.portals.portal_notebooks import NotebooksPortal
from Neuro.widgets.page import SettingsPage
from Neuro.widgets.portal import Portal
from Neuro.widgets.side_menu import SideMenuButton, SideMenu
from PySide6Extended.widget import ProfileButton, Container, AppBar, Scaffold


class OfficePortal(Portal):
    def __init__(self):
        super().__init__("Office")
        self.my_type = OfficePortal

        self.main_page.addWidget(QLabel("Office Page"))

        # create settings menu
        self.profile_button = ProfileButton(client.username, client.profile_picture)
        self.profile_button.clicked.connect(self.swap_page_settings)
        profile_container = Container(children=[self.profile_button])
        profile_container.setMinimumHeight(50)

        # create app bar
        self.appbar = AppBar(
            left=[self.breadcrumb]
        )

        # create side menu buttons
        side_menu_buttons = [SideMenuButton("Notebooks", click_event=self.swap_page_notebooks)]

        # create side menu and install buttons
        self.side_menu = SideMenu(
            top=profile_container,
            middle=side_menu_buttons)

        self.root = Scaffold(
            appbar=self.appbar,
            sidemenu=self.side_menu,
            page=self.main_page
        )

    def swap_page_settings(self):
        page_settings = SettingsPage(self.profile_button, self.swap_page_settings)
        print(self.family_tree[0])
        page_settings.set_parent_portal(self.family_tree[0])
        self.swap_page(page_settings)

    def swap_page_notebooks(self):
        self.swap_portal(NotebooksPortal())
