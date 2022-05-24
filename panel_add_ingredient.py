from kivy.uix.scrollview import ScrollView
from app_api import ParseQuery


class AddIngredient(ScrollView):
    """A panel for adding an ingredient to the database."""

    def __init__(self, **kwargs):
        """Initiates object to communicate with the database."""
        super().__init__(**kwargs)
        self.api = ParseQuery()

    def return_effects(self):
        """Returns the all list of ingredient's effects from the database."""
        effects = []
        effects_raw = [i[4:8] for i in self.api.data_pool]
        for item in effects_raw:
            for effect in item:
                effects.append(effect)
        effects = set(sorted(effects))
        return sorted(list(effects))
