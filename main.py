import kivy
kivy.require('2.0.0')  # Kivy version control (02/02/2022 --latest)


from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder


from menu_button import Menu
from panel_add_ingredient import AddIngredient
from panel_application_info import AppInfo
from panel_front_page import FrontWidget
from panel_ingredients_data import IngredientsDataPanel
from results_tab_panel import ResultsTabPanel
from search_bar import SearchBar


class AlchemyBooklet(App):
    """Kivy App object."""

    def __init__(self, **kwargs):
        """Initializes Kivy app prerequisites."""
        super().__init__(**kwargs)

        """Loads and initializes the main widget tree and set its presets."""
        self.main = Builder.load_file('root_widget.kv')

        # Sets default values to tabs and panels.
        self.main.front_widget.results_panel.reset_panels()

        # Explicit update of ingredients panel 4th line parameters.
        self.main.front_widget.results_panel.ingredient_details_panel.line4.\
        name.halign = 'left'
        self.main.front_widget.results_panel.ingredient_details_panel.line4.\
        value.halign = 'left'

        # Run post kivy initialization code block.
        Clock.schedule_once(lambda dt: self._post_update(), 0.1)

        # Constant Updates
        Clock.schedule_interval(
            lambda dt: self._constant_updates(), 1/60  # 60 fps.
            )

    def _post_update(self):
        """Runs after kivy's widget tree initialization."""

        # Fixes custom tab width of "ResultsTabPanel" at "panel_front_page.kv".
        self.main.front_widget.results_panel.on_tab_width()

        # For initial setup of menu drop box width.
        self.main.menu.toggle_box_drop()

    def _constant_updates(self):
        """Code block that is constantly looped 60 times per second."""

        # Size & pos update of object id 'debug_button' of "RootWidget" at
        # "root_widget.kv".
        self.main.debug_button.size = self.main.debug_button.texture_size
        self.main.debug_button.x = self.main.x
        if self.main.debug_button.shown:
            self.main.debug_button.y = self.main.y
        else:
            self.main.debug_button.top = self.main.y - 10

        # Size & pos update of "FrontWidget" rule at "panel_front_page.kv".
        self.main.front_widget.pos = self.main.pos
        self.main.front_widget.size = self.main.size

        # Size & pos update of "AppInfo" at "panel_application_info.kv".
        self.main.app_info.size = self.main.size
        if self.main.app_info.shown:
            self.main.app_info.pos = self.main.pos
        else:
            self.main.app_info.top = self.main.y - 10

        # Size & pos update of "IngredientsDataPanel" at 
        # "panel_ingredients_data.kv".
        self.main.ingredients_data_panel.width = self.main.width
        self.main.ingredients_data_panel.height = self.main.height - \
        self.main.add_ingredient_button.height
        self.main.ingredients_data_panel.x = self.main.x
        if self.main.ingredients_data_panel.shown:
            self.main.ingredients_data_panel.top = self.main.top
        else:
            self.main.ingredients_data_panel.top = self.main.y - 10

        # Size & pos update of "ReturnButton" at 
        # "panel_ingredients_data.kv".
        self.main.return_button.width = \
        self.main.ingredients_data_panel.panel_grid.width*1/6
        self.main.return_button.height = \
        self.main.return_button.texture_size[1]
        self.main.return_button.right = self.main.right
        if self.main.return_button.shown:
            self.main.return_button.top = self.main.top
        else:
            self.main.return_button.top = self.main.y - 10

        # Size & pos update of "AddIngredient" at 
        # "panel_add_ingredient.kv".
        self.main.add_ingredient_panel.width = self.main.width
        self.main.add_ingredient_panel.height = self.main.height - \
        self.main.add_ingredient_button.height
        self.main.add_ingredient_panel.x = self.main.x
        if self.main.add_ingredient_panel.shown:
            self.main.add_ingredient_panel.top = self.main.top
        else:
            self.main.add_ingredient_panel.top = self.main.y - 10

        # Height update of 'note_text' of "panel_add_ingredient.kv".
        self.main.add_ingredient_panel.ids.note_text.height = \
        self.main.add_ingredient_panel.ids.note_text.texture_size[1]

        # Size & pos update of "AddIngredientButton" at 
        # "panel_ingredients_data.kv".
        self.main.add_ingredient_button.width = self.main.width
        self.main.add_ingredient_button.height = \
        self.main.add_ingredient_button.texture_size[1]
        self.main.add_ingredient_button.x = self.main.x
        if self.main.add_ingredient_button.shown:
            self.main.add_ingredient_button.y = self.main.y
        else:
            self.main.add_ingredient_button.top = self.main.y - 10

        # Scrollview suggestion box width update.
        self.main.scrollview_suggestions_box.width = \
        self.main.front_widget.search_bar.search_text_input.width

        # Scrollview suggestion box height update.
        set_height = self.main.height - abs(self.main.height - \
        self.main.front_widget.search_bar.search_text_input.y)
        min_height = \
        self.main.scrollview_suggestions_box.suggestions_box.minimum_height

        if  min_height < set_height:
            self.main.scrollview_suggestions_box.height = min_height
        else:
            self.main.scrollview_suggestions_box.height = set_height

        # Scrollview suggestion box position update.
        self.main.scrollview_suggestions_box.top = \
        self.main.front_widget.search_bar.search_text_input.y

        # Suggestions update.
        self.main.front_widget.search_bar.update_suggestions()

        # Menu button position update.
        self.main.menu.top = self.main.top
        self.main.menu.right =  self.main.right

        # Menu drop box position update.
        self.main.scrollview_menu_drop_box.top = self.main.menu.y
        self.main.scrollview_menu_drop_box.right = self.main.right

    def build(self):
        return self.main


if __name__ == '__main__':
    MyApplication = AlchemyBooklet()
    MyApplication.run()
