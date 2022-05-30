# Kivy version control (02/02/2022 --latest)
import kivy; kivy.require('2.0.0')
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder


from add_ingredient_panel import AddIngredientPanel
from application_info_panel import ApplicationInfoPanel
from manage_ingredients_panel import ManageIngredientsPanel
from front_panel import FrontPanel, MenuButton, Results, SearchBar


class AlchemyBooklet(App):
    """Kivy App object."""

    def __init__(self, **kwargs):
        """Set initial widget presets and constant updates for the applicatoin.

        Notes
        -----
        Most of the presets for the widgets are set after Kivy loads and
        initializes the widgets on its initialization. Therefore we should set
        most of our presets with a delay for it to work as we expected to.
        """
        super(AlchemyBooklet, self).__init__(**kwargs)

        # Load widget tree with custom kv file name.
        self.main = Builder.load_file('root.kv')

        # Reset front panel widgets.
        self.main.front_panel.results_panel.reset_tabs()

        # Set some front panel parameters.
        self.main.front_panel.results_panel.ingredient_details_panel.line4.\
        name.halign = 'left'
        self.main.front_panel.results_panel.ingredient_details_panel.line4.\
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
        self.main.front_panel.results_panel.on_tab_width()

        # Set menu button's context menu width.
        self.main.menu_button.toggle_box_drop()

    def _constant_updates(self):
        """Code block that is constantly looped 60 times per second."""

        # Updates of "root.kv > RootWidget > Button.id: debug_button".
        # Update size & pos attribute. Check shown attribute.
        self.main.debug_button.size = self.main.debug_button.texture_size
        self.main.debug_button.x = self.main.x
        if self.main.debug_button.shown:
            self.main.debug_button.y = self.main.y
        else:
            self.main.debug_button.top = self.main.y - 10

        # Updates of "front_panel.py > FrontPanel".
        self.main.front_panel.update(self.main)

        # Updates of "application_info_panel.py > ApplicationInfoPanel".
        self.main.application_info_panel.update(self.main)

        # Updates of "manage_ingredients_panel.py > ManageIngredientsPanel".
        self.main.manage_ingredients_panel.update(self.main)

        # Updates of "add_ingredient_panel.py > AddIngredientPanel".
        self.main.add_ingredient_panel.update(self.main)

        # Update search suggestions.
        self.main.front_panel.search_bar.update_suggestions()

    def build(self):
        """Build the widget tree."""
        return self.main


if __name__ == '__main__':
    MyApplication = AlchemyBooklet()
    MyApplication.run()
