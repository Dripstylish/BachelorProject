from SecondBrain.Gui.Extended.ImageHandler import Icon
from SecondBrain.Gui.Extended.SaveFile import save_file
from SecondBrain.client.Subscription import PageSubscription

class Client:
    def __init__(self):
        self.username = "User"
        self.profile_picture = None
        self.current_page = None
        self.previous_page = None
        self.button_ids = []
        self.profile_picture = Icon("assets/icons/user.png", 50, 50).create_round_image("assets/profile_picture.png")
        self.threads = {
            "editor": None
        }

    def set_username(self, name):
        self.username = name
        self.save()

    def set_profile_picture(self, image):
        self.profile_picture = Icon(image, 50, 50).create_round_image("assets/profile_picture.png")
        self.save()

    def set_current_page(self, current_page):
        self.previous_page = current_page
        self.current_page = current_page
        page_subscription.push_notification()

    def get_button_id(self):
        i = 0
        while i in self.button_ids:
            i = i + 1
        self.button_ids.append(i)
        self.save()
        return i

    def load(self, load_file):
        self.username = load_file["username"]
        self.profile_picture = load_file["profile_picture"]
        self.button_ids = load_file["button_ids"]

    def save(self):
        client_dict = {
            "username": self.username,
            "profile_picture": self.profile_picture,
            "button_ids": self.button_ids
        }
        save_file.save_file["client"] = client_dict
        save_file.save_document()


client = Client()
page_subscription = PageSubscription()
