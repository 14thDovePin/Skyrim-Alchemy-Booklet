from kivy.uix.scrollview import ScrollView


class ApplicationInfoPanel(ScrollView):
    """A page that displays information about the developer of the app."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    from templates import toggle_page
        