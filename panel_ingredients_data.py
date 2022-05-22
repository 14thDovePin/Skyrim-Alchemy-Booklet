from kivy.uix.scrollview import ScrollView


class IngredientsDataPanel(ScrollView):
    """A page interface for managing the app's database.

    Page contains the list of all ingredients stored inside the database.
    Has a button for adding custom ingredients.
    Custom ingredients have a [-] button besides them. Interacting with the
    button prompts the user if they wish to remove the selected ingredient.

    Note.
    Users cannot change any of Skyrim's basegame ingredients. They can only
    create and modify their own custom ingredients.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    from toggle_page import toggle_page as tp

    def toggle_page(self):
        """Extension of the class method "toggle_page".

        Hides/shows the "Add Custom Ingredient" button.
        """
        self.tp()
        button = self.parent.add_ingredient_button

        if button.shown:
            button.top = self.parent.y - 10  # For extra clearance.
            button.shown = False
        else:
            button.y = self.parent.y
            button.shown = True
