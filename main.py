import kivy
kivy.require('2.0.0')  # Kivy version control (02/02/2022 --latest)


from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder


from overlays import MenuButton
from add_ingredient_panel import AddIngredientPanel
from application_info_panel import ApplicationInfoPanel
from manage_ingredients_panel import ManageIngredientsPanel


# NOTE: Temporary Indent
from front_panel import FrontPanel, SearchBar, Results


class AlchemyBooklet(App):
    """Kivy App object."""

    def __init__(self, **kwargs):
        """Set widget presets before and after 1 kivy life cycle.

        Notes
        -----
        Many of the presets for the widgets are set after Kivy loads and
        initializes the widgets on its first cycle. Therefore we run it with
        after some cycles.
        """
        super().__init__(**kwargs)

        # Load widget tree with custom kv file name.
        self.main = Builder.load_file('root.kv')

        # Reset front_panel widgets.
        self.main.front_panel.results_panel.reset_panels()

        # Explicit update of ingredients panel 4th line parameters.
        self.main.front_panel.results_panel.ingredient_details_panel.line4.\
        name.halign = 'left'
        self.main.front_panel.results_panel.ingredient_details_panel.line4.\
        value.halign = 'left'

        # Run post kivy initialization code block.
        Clock.schedule_once(lambda dt: self._post_update(), 0.1)

        # Constant Updates
        Clock.schedule_interval(
            lambda dt: self._constant_updates(), 1/60  # 60 fps.
            )

    def _post_update(self):
        """Extension of the constructor with delayed schedule."""

        # Explicit call of function for custom tab.
        self.main.front_panel.results_panel.on_tab_width()

        # Set menu drop box width.
        self.main.menu_button.toggle_box_drop()

    def _constant_updates(self):
        """Code block that is constantly looped 60 times per second."""

        # Size & pos update of object id 'debug_button' of "RootWidget" at
        # "root.kv".
        self.main.debug_button.size = self.main.debug_button.texture_size
        self.main.debug_button.x = self.main.x
        if self.main.debug_button.shown:
            self.main.debug_button.y = self.main.y
        else:
            self.main.debug_button.top = self.main.y - 10

        # Size & pos update of "FrontPanel" rule at "front_panel.kv".
        self.main.front_panel.pos = self.main.pos
        self.main.front_panel.size = self.main.size

        # Size & pos update of "ApplicationInfoPanel" at "application_info_panel.kv".
        self.main.app_info_panel.size = self.main.size
        if self.main.app_info_panel.shown:
            self.main.app_info_panel.pos = self.main.pos
        else:
            self.main.app_info_panel.top = self.main.y - 10

        # Size & pos update of "ManageIngredientsPanel" at 
        # "manage_ingredients_panel.kv".
        self.main.manage_ingredients_panel.width = self.main.width
        self.main.manage_ingredients_panel.height = self.main.height - \
        self.main.add_ingredient_button.height
        self.main.manage_ingredients_panel.x = self.main.x
        if self.main.manage_ingredients_panel.shown:
            self.main.manage_ingredients_panel.top = self.main.top
        else:
            self.main.manage_ingredients_panel.top = self.main.y - 10

        # Size & pos update of "ReturnButton" at 
        # "manage_ingredients_panel.kv".
        self.main.return_button.width = \
        self.main.manage_ingredients_panel.panel_grid.width*1/6
        self.main.return_button.height = \
        self.main.return_button.texture_size[1]
        self.main.return_button.right = self.main.right
        if self.main.return_button.shown:
            self.main.return_button.top = self.main.top
        else:
            self.main.return_button.top = self.main.y - 10

        # Size & pos update of "AddIngredientPanel" at 
        # "add_ingredient_panel.kv".
        self.main.add_ingredient_panel.size = self.main.size
        self.main.add_ingredient_panel.x = self.main.x
        if self.main.add_ingredient_panel.shown:
            self.main.add_ingredient_panel.top = self.main.top
        else:
            self.main.add_ingredient_panel.top = self.main.y - 10

        # Height update of 'note_text' of "add_ingredient_panel.kv".
        self.main.add_ingredient_panel.ids.note_text.height = \
        self.main.add_ingredient_panel.ids.note_text.texture_size[1]

        # Height, width, and text_size update of the error labels of
        # "_check_values" of "AddIngredint" of "add_ingredient_panel.py".
        if self.main.add_ingredient_panel.error_label:
            self.main.add_ingredient_panel.panel_grid.children[1].height = \
            self.main.add_ingredient_panel.panel_grid.children[1].\
            texture_size[1]
            self.main.add_ingredient_panel.panel_grid.children[1].width \
            = self.main.width
            self.main.add_ingredient_panel.panel_grid.children[1].text_size[0]\
            = self.main.width

        # Size & pos update of "AddIngredientButton" at 
        # "manage_ingredients_panel.kv".
        self.main.add_ingredient_button.width = self.main.width
        self.main.add_ingredient_button.height = \
        self.main.add_ingredient_button.texture_size[1]
        self.main.add_ingredient_button.x = self.main.x
        if self.main.add_ingredient_button.shown:
            self.main.add_ingredient_button.y = self.main.y
        else:
            self.main.add_ingredient_button.top = self.main.y - 10

        # Scrollview suggestion box width update.
        self.main.search_suggestions_box.width = \
        self.main.front_panel.search_bar.search_text_input.width

        # Scrollview suggestion box height update.
        set_height = self.main.height - abs(self.main.height - \
        self.main.front_panel.search_bar.search_text_input.y)
        min_height = \
        self.main.search_suggestions_box.suggestions_box.minimum_height

        if  min_height < set_height:
            self.main.search_suggestions_box.height = min_height
        else:
            self.main.search_suggestions_box.height = set_height

        # Scrollview suggestion box position update.
        self.main.search_suggestions_box.top = \
        self.main.front_panel.search_bar.search_text_input.y

        # Suggestions update.
        self.main.front_panel.search_bar.update_suggestions()

        # Menu button position update.
        self.main.menu_button.top = self.main.top
        self.main.menu_button.right =  self.main.right

        # Menu drop box position update.
        self.main.menu_drop_box.top = self.main.menu_button.y
        self.main.menu_drop_box.right = self.main.right

    def build(self):
        return self.main


if __name__ == '__main__':
    MyApplication = AlchemyBooklet()
    MyApplication.run()
