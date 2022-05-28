from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from front_panel import SearchBoxButton


from db_api import Database


class ManageIngredientsPanel(ScrollView):
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
        """Adds the default and preset custom ingredients to the page."""
        super().__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.update_contents(), 0.1)

    def update_contents(self):
        """Updates the content inside of the page."""
        api = Database()
        grid_layout = self.panel_grid
        color_a, color_b = '#93c47d', '#76a5af'
        for x, i in enumerate(api.ingredient_names):
            if x%2 == 0:
                self._add_ingredient(grid_layout, color_a, i)
            else:
                self._add_ingredient(grid_layout, color_b, i)

    def _add_ingredient(self, base_widget, color, button_text):
        """Adds a SearchBoxButton rule to a grid layout.

        Arguments
        ---------
        base_widget: kivy.uix.gridlayout object
            The grid layout that is used to add the button wigdet to.
        color: string
            The hex color to be used in the button's background.
        text: string
            The text that will be used for the button.
        """
        text = f'[color={color.upper()}][b][size=20dp]'+button_text[:]
        base_widget.add_widget(
            SearchBoxButton(
                size_hint = [1, None],
                text = text,
                padding = [5, 5],
                background_color = (64/255, 64/255, 64/255, 1),
                on_release = lambda ins: self._search_ingredient(text)
                )
            )

    def _search_ingredient(self, text):
        """Toggles the page and searches the ingredient.

        Arguments
        ---------
        text: string
            The string that will be passed to search the ingredient.
        """
        self.parent.front_panel.search_bar.suggestion_search(text)
        self.toggle_page()

    from py_templates import toggle_page as tp

    def toggle_page(self):
        """Extension of toggle_page method."""
        self.tp()

        # Hide/show "ReturnButton" of "manage_ingredients_panel.kv".
        if self.parent.return_button.shown:
            self.parent.return_button.shown = False
        else:
            self.parent.return_button.shown = True

        # Hide/show "AddIngredientButton" of "manage_ingredients_panel.kv".
        if self.parent.add_ingredient_button.shown:
            self.parent.add_ingredient_button.shown = False
        else:
            self.parent.add_ingredient_button.shown = True
