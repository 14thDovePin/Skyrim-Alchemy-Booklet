import kivy
kivy.require('2.0.0')  # Kivy version control (02/02/2022 --latest)


from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder


from main_app_info import AppInfo
from main_aip import AIP
from main_front_widget import FrontWidget
from main_menu import Menu
from main_resultstabpanel import ResultsTabPanel
from main_searchbar import SearchBar


class AlchemyBooklet(App):
    """Main application."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._init_widget_tree()

    def _init_widget_tree(self):
        """Loads and initializes the main widget tree and its presets."""
        self.main = Builder.load_file('widget_root.kv')

        # Explicit update of tab_width. Required to fix tab buttons placement.
        Clock.schedule_once(
            self.main.front_widget.results_panel.on_tab_width, 0.1
            )

        # Sets default values to tabs and panels.
        self.main.front_widget.results_panel.reset_panels()

        # Explicit update of ingredients panel 4th line parameters.
        self.main.front_widget.results_panel.ingredient_details_panel.line4.\
        name.halign = 'left'
        self.main.front_widget.results_panel.ingredient_details_panel.line4.\
        value.halign = 'left'

        # For initial setup of menu drop box width.
        Clock.schedule_once(lambda dt: self.main.menu.toggle_box_drop(), 1/60)

        # Constant Updates.
        Clock.schedule_interval(
            lambda dt: self._constant_updates(), 1/60  # 60 fps.
            )

    def _constant_updates(self):
        """Code block that is constantly updated 60 frames per second."""

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

        # App info size & position update.
        self.main.app_info.top = self.main.top
        self.main.app_info.x = self.main.x
        self.main.app_info.width = self.main.width
        # referece "main_app_info.py" @ line 15-28.
        if self.main.app_info.page_state == 'hidden':
            self.main.app_info.height = self.main.height

        # AIP size & position update.
        self.main.aip.top = self.main.top
        self.main.aip.x = self.main.x
        self.main.aip.width = self.main.width
        # referece "main_aip.py" @ line 15-28.
        if self.main.aip.page_state == 'hidden':
            self.main.aip.height = self.main.height

        # Front_Widget size & position update.
        self.main.front_widget.top = self.main.top
        self.main.front_widget.x = self.main.x
        self.main.front_widget.width = self.main.width
        # referece "main_front_widget.py" @ line 15-28.
        if self.main.front_widget.page_state == 'hidden':
            self.main.front_widget.height = self.main.height

        # Show front_widget if every other page is hidden.
        pages = [i for i in self.main.children]
        pages.remove(self.main.front_widget)
        pages_state = []
        for i in pages:
            if hasattr(i, "page_state"):
                if i.page_state == "shown":
                    pages_state.append(True)
                else:
                    pages_state.append(False)
        if all(pages_state):
            self.main.front_widget.page_state = 'hidden'

    def build(self):
        return self.main


if __name__ == '__main__':
    MyApplication = AlchemyBooklet()
    MyApplication.run()
