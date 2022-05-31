from kivy.clock import Clock
from front_panel import ButtonLabel


from db_api import Database
from templates import TogglePanel


class ManageIngredientsPanel(TogglePanel):
    """A panel for managing the ingredients database.

    Methods
    -------
    toggle_panel (override)
        Toggle visibility of panel and its overlays on screen.
    udpate (override)
        Update panel assets and attributes.
    update_ingredients
        Update ingredient name list of the panel.

    Note
    ----
    Panel contains all of the ingredients name stored inside the database.
    Items are displayed in a single column. Each item is a ButtonLabel (See
    "front_panel.py > ButtonLabel") that can be pressed to auto search the
    ingredient displaying its results. Of course this also means toggling the
    current panel for that. Custom added ingredients has a remove button on its
    right for removing the ingredient entry from the database permanently.

    Cannot remove any items belonging to the INGREDIENTS table of the database.
    Refer to "db_app.py > Database > pull_data" for more information.
    """

    def __init__(self, **kwargs):
        """Add the base and custom ingredients to the panel."""
        super(ManageIngredientsPanel, self).__init__(**kwargs)

        # Schedule update_ingredients method.
        Clock.schedule_once(lambda dt: self.update_ingredients(), 1/60)

    def toggle_panel(self):
        """Toggle visibility of panel and its overlays on screen."""
        # Toggle panel.
        if self.shown:
            self.shown = False
        else:
            self.shown = True

        # Toggle "manage_ingredients_panel.kv > ReturnButton".
        if self.parent.return_button.shown:
            self.parent.return_button.shown = False
        else:
            self.parent.return_button.shown = True

        # Toggle "manage_ingredients_panel.kv > AddCustomIngredientButton".
        if self.parent.add_custom_ingredient_button.shown:
            self.parent.add_custom_ingredient_button.shown = False
        else:
            self.parent.add_custom_ingredient_button.shown = True

    def update(self, root):
        """Update panel assets and attributes.

        Arguments
        ---------
        root: kivy obj
            The root widget of the application.
        """
        # Update size and pos attribute.
        self.width = root.width
        self.height = root.height - \
        root.add_custom_ingredient_button.height
        self.x = root.x

        # Show or hide the panel.
        if self.shown:
            self.top = root.top
        else:
            self.top = root.y - 10

        # Update size & pos of "manage_ingredients_panel.kv > ReturnButton".
        root.return_button.width = \
        self.panel_grid.width*1/6
        root.return_button.height = \
        root.return_button.texture_size[1]
        root.return_button.right = root.right
        # Show or hide ReturnButton.
        if root.return_button.shown:
            root.return_button.top = root.top
        else:
            root.return_button.top = root.y - 10

        # Update size & pos of "manage_ingredients_panel.kv >
        # AddCustomIngredientButton".
        root.add_custom_ingredient_button.width = root.width
        root.add_custom_ingredient_button.height = \
        root.add_custom_ingredient_button.texture_size[1]
        root.add_custom_ingredient_button.x = root.x
        # Show or hide ReturnButton.
        if root.add_custom_ingredient_button.shown:
            root.add_custom_ingredient_button.y = root.y
        else:
            root.add_custom_ingredient_button.top = root.y - 10

    def update_ingredients(self):
        """Update ingredient name list of the panel."""
        api = self.parent.database
        grid_layout = self.panel_grid
        grid_layout.clear_widgets()
        color_a, color_b = '#93c47d', '#76a5af'
        for x, i in enumerate(api.ingredient_names):
            if x%2 == 0:
                self._add_ingredient(grid_layout, color_a, i)
            else:
                self._add_ingredient(grid_layout, color_b, i)

    def _add_ingredient(self, base_widget, color, button_text):
        """Add a ButtonLabel rule with a remove Button to a widget.

        Arguments
        ---------
        base_widget: kivy object
            The widget that is used to add the button wigdet to.
        color: string
            The hex color to be used in the button's background.
        text: string
            The text that will replace the button's text attribute.

        Note
        ----
        ButtonLabel is a Button diguised as a Label. In this case here there is
        also another button 1/5th of its width to the right, it is for removing
        the custom added ingredient from the database permanently.
        """
        # TODO: Add button option to remove CUSTOM ingredient!
        text = f'[color={color.upper()}][b][size=20dp]'+button_text[:]
        base_widget.add_widget(
            ButtonLabel(
                size_hint = [1, None],
                text = text,
                padding = [5, 5],
                background_color = (64/255, 64/255, 64/255, 1),
                on_release = lambda ins: self._search(text)
                )
            )

    def _search(self, text):
        """Toggle panel and search the ingredient.

        Arguments
        ---------
        text: string
            The string that will be used to search.
        """
        self.parent.front_panel.search_bar.suggestion_search(text)
        self.toggle_panel()
