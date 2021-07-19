class Palette:
    def __init__(self, color_palette=None, value=None):
        if color_palette is None:
            self.color_palette = {
                50: "#E3F2FD",
                100: "#BBDEFB",
                200: "#90CAF9",
                300: "#64B5F6",
                400: "#42A5F5",
                500: "#2196F3",
                600: "#1E88E5",
                700: "#1976D2",
                800: "#1565C0",
                900: "#0D47A1"
            }
        else:
            self.color_palette = color_palette

        if value is None:
            self.color = self.color_palette[500]
        else:
            self.color = self.color_palette[value]


class Blue(Palette):
    def __init__(self, value=None):
        super().__init__(value=value)


class BlueGrey(Palette):
    def __init__(self, value=None):
        self.color_palette = {
            50: "#ECEFF1",
            100: "#CFD8DC",
            200: "#B0BEC5",
            300: "#90A4AE",
            400: "#78909C",
            500: "#607D8B",
            600: "#546E7A",
            700: "#455A64",
            800: "#37474F",
            900: "#263238"
        }
        super().__init__(self.color_palette, value)


class Grey(Palette):
    def __init__(self, value=None):
        self.color_palette = {
            50: "#FAFAFA",
            100: "#F5F5F5",
            200: "#EEEEEE",
            300: "#E0E0E0",
            400: "#BDBDBD",
            500: "#9E9E9E",
            600: "#757575",
            700: "#616161",
            800: "#424242",
            900: "#212121"
        }
        super().__init__(self.color_palette, value)

class Dark:
    def __init__(self):
        self.primary = "#2f3437"
        self.secondary = "#373c3f"
        self.highlight = "#454b4f"
        self.pressed = "#40464a"

class Light:
    def __init__(self):
        self.primary = "#FFFFFF"
        self.secondary = "#F5F5F5"
        self.highlight = Grey(300).color
        self.pressed = Grey(400).color