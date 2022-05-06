from kivy.uix.scrollview import ScrollView


class AppInfo(ScrollView):
    """A page that displays information about the developer of the app."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    from main_toggle_page import toggle_page
        