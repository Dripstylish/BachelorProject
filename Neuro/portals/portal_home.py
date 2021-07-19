from PySide6.QtWidgets import QLabel

from Neuro.client import client
from Neuro.portals.portal_office import OfficePortal
from Neuro.widgets.page import SettingsPage
from Neuro.widgets.portal import Portal
from Neuro.widgets.side_menu import SideMenu, SideMenuButton
from PySide6Extended.widget import Scaffold, ProfileButton, Container, AppBar


class HomePortal(Portal):
    def __init__(self):
        super().__init__("Home")
        self.my_type = HomePortal

        self.main_page.addWidget(QLabel("Main Page"))

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
        side_menu_buttons = [SideMenuButton("Office", click_event=self.swap_portal_office)]

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
        page_settings.set_parent_portal(self)
        self.swap_page(page_settings)

    def swap_portal_office(self):
        self.swap_portal(OfficePortal())
