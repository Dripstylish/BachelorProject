from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel

from Neuro.client import client
import Neuro.client.database as db
from Neuro.widgets.page import SettingsPage
from Neuro.widgets.portal import Portal
from Neuro.widgets.side_menu import SideMenuButton, SideMenu
from PySide6Extended.core import app
from PySide6Extended.widget import ProfileButton, Container, AppBar, Scaffold

icon = app.theme.icon


class NotebookPortal(Portal):
    def __init__(self, title):
        self.title = title
        super().__init__(title)
        self.my_type = NotebookPortal

        # create settings menu
        self.profile_button = ProfileButton(client.username, client.profile_picture)
        self.profile_button.clicked.connect(self.swap_page_settings)
        profile_container = Container(children=[self.profile_button])
        profile_container.setMinimumHeight(50)

        # create new notebook button
        add_page_button = SideMenuButton("New Page", QIcon(icon.fi_rr_plus_small))
        bottom_container = Container(children=[add_page_button])

        # create app bar
        self.appbar = AppBar(
            left=[self.breadcrumb]
        )

        # create side menu buttons
        side_menu_buttons = []

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
        new_self = self.my_type(self.title)
        if self.parent is not None:
            new_self.set_parent(self.parent)
        app.home.swap_portal(new_self)
        new_self.page_subscription.push_notification()