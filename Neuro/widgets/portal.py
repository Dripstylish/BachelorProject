import copy

from Neuro.widgets.breadcrumb import Breadcrumb
from Neuro.widgets.page import Page
from PySide6Extended.core import app
from PySide6Extended.core.subscription import Subscription
from PySide6Extended.widget.widget import Widget
import Neuro.client.database as db


class Portal(Widget):
    def __init__(self, portal_name: str = None, icon: str = None, click_event=None):
        super().__init__()

        self.name = portal_name
        self.icon = icon
        self.my_type = Portal

        if click_event is not None:
            self.click_event = click_event
        else:
            self.click_event = self.swap_portal_home

        self.parent = None
        self.family_tree = [self]

        self.save_subscription = Subscription()
        self.page_subscription = Subscription()

        self.main_page = Page(None, None)
        self.main_page.set_parent_portal(self)

        self.current_page = self.main_page
        self.root = None

        # create breadcrumbs
        self.breadcrumb = Breadcrumb(self.family_tree)
        self.subscribe_to_page(self.breadcrumb, self.update_breadcrumbs)

    def swap_page(self, page):
        self.current_page = page

        self.root.main.deleteAll()
        self.root.main.addWidget(self.appbar)
        self.root.main.addWidget(self.current_page)

        self.page_subscription.push_notification()

    def swap_portal(self, portal):
        new_portal = portal
        new_portal.set_parent(self)
        app.home.swap_portal(new_portal)
        new_portal.page_subscription.push_notification()

    def swap_portal_home(self):
        new_self = self.my_type()
        if self.parent is not None:
            new_self.set_parent(self.parent)
        app.home.swap_portal(new_self)
        new_self.page_subscription.push_notification()


    def set_parent(self, portal_parent):
        self.parent = portal_parent
        self.family_tree = copy.copy(self.parent.family_tree)
        self.family_tree.append(self)

    def subscribe_to_save(self, subscriber, event):
        self.save_subscription.subscribe(subscriber, event)

    def subscribe_to_page(self, subscriber, event):
        self.page_subscription.subscribe(subscriber, event)

    def save_portal(self):
        portal_dict = {
            "portal_name": self.name
        }

        if not db.get_portal(self.name):
            db.add_portal(portal_dict)
        else:
            db.update_portal(self.name, portal_dict)

    def update_breadcrumbs(self):
        breadcrumb_path = list(self.family_tree)
        if self.current_page != self.main_page:
            breadcrumb_path.append(self.current_page)
        self.breadcrumb.set_breadcrumb_path(breadcrumb_path)
