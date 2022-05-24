from kivy.uix.scrollview import ScrollView
from app_api import ParseQuery


class AddIngredient(ScrollView):
    """A panel for adding an ingredient to the database."""

    def __init__(self, **kwargs):
        """Initiates object to communicate with the database."""
        super().__init__(**kwargs)
        self.api = ParseQuery()
