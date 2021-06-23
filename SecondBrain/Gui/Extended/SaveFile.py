import copy
import os.path
import json

class SaveFile:
    def __init__(self):
        self.path = os.path.expanduser("~") + "/SecondBrain/save/"
        self.file_name = "save_file.json"
        self.full_path = os.path.join(self.path, self.file_name)
        self.save_file = {
            "settings": None,
            "client": None,
            "side_menu": None
        }
        self.loaded_file = None

    def save_document(self):
        with open(self.full_path, "w") as f:
            f.write(json.dumps(self.save_file, indent=4))

    def load_document(self):
        if self.save_file_exists():
            with open(self.full_path, "r") as f:
                self.loaded_file = copy.deepcopy(json.loads(f.read()))
                self.save_file = copy.deepcopy(self.loaded_file)
        else:
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            self.save_document()

    def save_file_exists(self):
        return os.path.exists(self.full_path)

save_file = SaveFile()
