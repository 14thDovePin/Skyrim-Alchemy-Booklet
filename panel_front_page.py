from kivy.uix.scrollview import ScrollView


class FrontWidget(ScrollView):
    """A page for adding new ingredients and related info into the database."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
