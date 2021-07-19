from PySide6.QtGui import QPalette

from Gui_unrefactored.Theme import Color
from Gui_unrefactored.Theme.Icon import Icon


class Theme:
    def __init__(self, app, theme=None):
        self.app = app
        self.primary_color = None
        self.secondary_color = None
        self.window_color = None
        self.window_secondary_color = None
        self.text_color = None
        self.highlight_color = None
        self.highlight_text_color = None
        self.pressed_color = None

        if app.palette().window().color().name() == "#323232":
            self.dark_mode = True
        else:
            self.dark_mode = False

        self.icon = Icon(self)

        self.stylesheet = None
        if theme is None:
            if self.dark_mode:
                self.black()
            else:
                self.white()

    def build(self):
        palette = self.app.palette()
        palette.setColor(QPalette.Window, self.window_color)
        self.app.setPalette(palette)

        definitions = {
            "@primary": self.primary_color,
            "@secondary": self.secondary_color,
            "@window_secondary": self.window_secondary_color,
            "@window": self.window_color,
            "@text": self.text_color,
            "@highlight_text": self.highlight_text_color,
            "@highlight": self.highlight_color,
            "@pressed": self.pressed_color,
            "@dropdown_icon": self.icon.fi_rr_angle_small_down
        }

        with open("Gui_unrefactored/Theme/stylesheet.qss", "r") as f:
            self.stylesheet = f.read()
            for key in definitions.keys():
                self.stylesheet = self.stylesheet.replace(key, definitions[key])

        self.app.setStyleSheet(self.stylesheet)

    def custom_theme(self, primary, secondary, window, window_secondary, text, highlight, highlight_text, pressed):
        self.primary_color = primary
        self.secondary_color = secondary
        self.window_color = window
        self.window_secondary_color = window_secondary
        self.text_color = text
        self.highlight_color = highlight
        self.highlight_text_color = highlight_text
        self.pressed_color = pressed
        self.build()

    def black(self):
        self.custom_theme(primary=Color.Dark().primary,
                          secondary=Color.Dark().secondary,
                          window=Color.Dark().primary,
                          window_secondary=Color.Dark().secondary,
                          text="white",
                          highlight=Color.Dark().highlight,
                          highlight_text=Color.Grey(500).color,
                          pressed=Color.Dark().pressed)

    def white(self):
        self.custom_theme(primary=Color.Light().primary,
                          secondary=Color.Light().secondary,
                          window=Color.Light().primary,
                          window_secondary=Color.Light().secondary,
                          text=Color.Grey(900).color,
                          highlight=Color.Light().highlight,
                          highlight_text=Color.Grey(700).color,
                          pressed=Color.Light().pressed)

    def blue(self):
        self.custom_theme(primary=Color.Blue().color,
                          secondary=Color.Light().secondary,
                          window=Color.Light().primary,
                          window_secondary=Color.Light().secondary,
                          text="black",
                          highlight=Color.Light().highlight,
                          highlight_text="black",
                          pressed=Color.Light().pressed)

    def change_window_color(self, widget, color):
        palette = widget.palette()
        palette.setColor(QPalette.Window, color)
        widget.setPalette(palette)

    def change_text_color(self, widget, color):
        palette = widget.palette()
        palette.setColor(QPalette.Text, color)
        widget.setPalette(palette)

    def change_placeholder_text_color(self, widget, color):
        palette = widget.palette()
        palette.setColor(QPalette.PlaceholderText, color)
        widget.setPalette(palette)