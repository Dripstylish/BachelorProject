import pyautogui
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QLabel

from SecondBrain.Gui.Application import app, icon
from SecondBrain.Gui.Extended import Builder, Scaffold, AppBar, Container
from SecondBrain.Gui.Extended.SaveFile import save_file
from SecondBrain.Gui.Extended.SideMenu import SideMenu, SideMenuButton, DraggableSideMenuButton, ProfileButton
from SecondBrain.Gui.Extended.PageWidgets import Page, Breadcrumb
from SecondBrain.client import client, page_subscription

resolution = pyautogui.size()

class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setWindowIcon(QIcon('web.png'))

        # Load save file, or create a new one if none exists
        save_file.load_document()

        # load client
        if save_file.save_file["client"] is not None:
            client.load(save_file.loaded_file["client"])

        # create settings menu
        profile_button = ProfileButton(client.username, client.profile_picture)
        profile_container = Container(children=[profile_button])
        profile_container.setMinimumHeight(50)

        # create new page button
        add_page_button = SideMenuButton("New Page", QIcon(icon.fi_rr_plus_small))
        buttom_container = Container(children=[add_page_button])

        if save_file.save_file["side_menu"] is not None:
            side_menu_buttons = []
            for button_dict in save_file.loaded_file["side_menu"].keys():
                new_button = DraggableSideMenuButton("", 0)
                new_button.load(save_file.loaded_file["side_menu"][button_dict])
                if button_dict == next(iter(save_file.loaded_file["side_menu"])):
                    client.set_current_page(new_button.page)
                side_menu_buttons.append(new_button)
        else:
            save_file.save_file["side_menu"] = {}
            current_page = Page("Untitled")
            client.set_current_page(current_page)
            button = DraggableSideMenuButton(current_page.page_title, page=current_page)
            button.save()
            side_menu_buttons = [button]


        # create breadcrumbs
        self.breadcrumb = Breadcrumb()
        page_subscription.subscribe(self.breadcrumb, self.breadcrumb.update_breadcrumbs)

        # create app bar
        self.appbar = AppBar(
            left=[
                self.breadcrumb
            ],
            right=[Container()]
        )

        # create side menu and install buttons
        self.side_menu = SideMenu(
            top=profile_container,
            children=side_menu_buttons,
            buttom=buttom_container)

        # add new page button functionality
        add_page_button.clicked.connect(self.add_button_to_list)

        # create scaffold and install widgets
        self.root = Scaffold(
            appbar=self.appbar,
            sidemenu=self.side_menu,
            page=[
                client.current_page
            ]
        )
        Builder(self, self.root)

        # subscribe to page updates
        page_subscription.subscribe(self, self.update_page)

    def add_button_to_list(self):
        button = DraggableSideMenuButton("New Page", client.get_button_id())
        button.save()
        self.side_menu.list_widget.append(button, "New Page")

    def update_page(self):
        self.root.main.deleteAll()
        self.root.main.addWidget(self.appbar)
        self.root.main.addWidget(client.current_page)

if __name__ == "__main__":
    window = Home()
    window.resize(resolution[0]/1.5, resolution[1]/1.5)
    window.show()

    app.start()
