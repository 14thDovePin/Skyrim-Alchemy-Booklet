# Kivy version control (02/02/2022 --latest)
import kivy; kivy.require('2.0.0')
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder


from add_ingredient_panel import AddIngredientPanel
from application_info_panel import ApplicationInfoPanel
from db_api import Database
from manage_ingredients_panel import ManageIngredientsPanel
from front_panel import FrontPanel, MenuButton, Results, SearchBar


class AlchemyBooklet(App):
    """Kivy App object."""

    def __init__(self, **kwargs):
        """Set initial widget presets and constant updates for the application.

        Notes
        -----
        Most of the presets for the widgets are set after Kivy loads and
        initializes the widgets on its initialization. Therefore we should set
        most of our presets with a delay for it to work as we expected to.
        """
        super(AlchemyBooklet, self).__init__(**kwargs)

        # Load widget tree with custom kv file name.
        self.root = Builder.load_file('root.kv')

        # Create a database connection object for the root widget.
        self.root.database = Database()

        # Reset front panel widgets.
        self.root.front_panel.results_panel.reset_tabs()

        # Set some front panel parameters.
        self.root.front_panel.results_panel.ingredient_details_panel.line4.\
        name.halign = 'left'
        self.root.front_panel.results_panel.ingredient_details_panel.line4.\
        value.halign = 'left'

        # Run post kivy widget initialization code block.
        Clock.schedule_once(lambda dt: self._post_update(), 1/60)

        # Loop udpates 60 times per second.
        Clock.schedule_interval(
            lambda dt: self._constant_updates(), 1/60
            )

    def _post_update(self):
        """Extension of the constructor with a schedule delay."""

        # Explicit call of for correcting custom tab width.
        self.root.front_panel.results_panel.on_tab_width()

        # Set menu button's context menu width.
        self.root.menu_button.toggle_box_drop()

    def _constant_updates(self):
        """Code block that is constantly looped 60 times per second."""

        # Updates of "root.kv > RootWidget > Button.id: debug_button".
        # Update size & pos attribute. Check shown attribute.
        self.root.debug_button.size = self.root.debug_button.texture_size
        self.root.debug_button.x = self.root.x
        if self.root.debug_button.shown:
            self.root.debug_button.y = self.root.y
        else:
            self.root.debug_button.top = self.root.y - 10

        # Updates of "front_panel.py > FrontPanel".
        self.root.front_panel.update(self.root)

        # Updates of "application_info_panel.py > ApplicationInfoPanel".
        self.root.application_info_panel.update(self.root)

        # Updates of "manage_ingredients_panel.py > ManageIngredientsPanel".
        self.root.manage_ingredients_panel.update(self.root)

        # Updates of "add_ingredient_panel.py > AddIngredientPanel".
        self.root.add_ingredient_panel.update(self.root)

        # Update search suggestions.
        self.root.front_panel.search_bar.update_suggestions()

    def build(self):
        """Build the widget tree."""
        return self.root


if __name__ == '__main__':
    MyApplication = AlchemyBooklet()
    MyApplication.run()
