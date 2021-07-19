from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QWidget

from PySide6Extended.core.style import color
from PySide6Extended.core.style.icon import Icon


class Theme:
    """
    A class used to manage the application theme
    """
    def __init__(self, app, theme=None):
        self.primary_color = None
        self.secondary_color = None
        self.window_color = None
        self.window_secondary_color = None
        self.text_color = None
        self.highlight_color = None
        self.highlight_text_color = None
        self.button_pressed_color = None

        self.app = app
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
            "@pressed": self.button_pressed_color,
            "@dropdown_icon": self.icon.fi_rr_angle_small_down
        }

        with open("PySide6Extended/core/style/stylesheet.qss", "r") as f:
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
        self.button_pressed_color = pressed
        self.build()

    def black(self):
        self.custom_theme(primary=color.Dark().primary,
                          secondary=color.Dark().secondary,
                          window=color.Dark().primary,
                          window_secondary=color.Dark().secondary,
                          text="white",
                          highlight=color.Dark().highlight,
                          highlight_text=color.Grey(500).color,
                          pressed=color.Dark().pressed)

    def white(self):
        self.custom_theme(primary=color.Light().primary,
                          secondary=color.Light().secondary,
                          window=color.Light().primary,
                          window_secondary=color.Light().secondary,
                          text=color.Grey(900).color,
                          highlight=color.Light().highlight,
                          highlight_text=color.Grey(700).color,
                          pressed=color.Light().pressed)

    def blue(self):
        self.custom_theme(primary=color.Blue().color,
                          secondary=color.Light().secondary,
                          window=color.Light().primary,
                          window_secondary=color.Light().secondary,
                          text="black",
                          highlight=color.Light().highlight,
                          highlight_text="black",
                          pressed=color.Light().pressed)

    @staticmethod
    def change_window_color(widget: QWidget, color):
        palette = widget.palette()
        palette.setColor(QPalette.Window, color)
        widget.setPalette(palette)

    @staticmethod
    def change_text_color(widget: QWidget, color):
        palette = widget.palette()
        palette.setColor(QPalette.Text, color)
        widget.setPalette(palette)

    @staticmethod
    def change_placeholder_text_color(widget: QWidget, color):
        palette = widget.palette()
        palette.setColor(QPalette.PlaceholderText, color)
        widget.setPalette(palette)
