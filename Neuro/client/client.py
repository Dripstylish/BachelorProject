import Neuro.client.database as db
from PySide6Extended.core.image_handler import Icon


class Client:
    def __init__(self):
        self.username = "User"
        self.profile_picture = None

        self.previous_location = None
        self.button_ids = []

        # set default profile picture
        self.profile_picture = Icon("assets/icons/user.png").create_round_image("assets/profile_picture.png")

        self.threads = {
            "editor": None
        }

    def set_username(self, name):
        self.username = name
        self.save()

    def set_profile_picture(self, image):
        self.profile_picture = Icon(image).create_round_image("assets/profile_picture.png")
        self.save()

    def get_button_id(self):
        i = 0
        while i in self.button_ids:
            i = i + 1
        self.button_ids.append(i)
        self.save()
        return i

    def load(self):
        if not db.db.Users().records:
            self.save()
        else:
            client = db.db.Users().records["0"]
            self.username = client["username"]
            self.profile_picture = client["profile_picture"]
            self.button_ids = ["button_ids"]

    def save(self):
        client_dict = {
            "username": self.username,
            "profile_picture": self.profile_picture,
            "button_ids": self.button_ids
        }

        if not db.get_client(self.username):
            db.add_client(client_dict)
        else:
            db.update_client(self.username, client_dict)

client = Client()
