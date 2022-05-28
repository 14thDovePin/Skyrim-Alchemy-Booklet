from db_api import Database
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel


class FrontPanel(ScrollView):
    """A page for adding new ingredients and related info into the database."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SearchBar(GridLayout):
    """Searchbar for the main page of the application."""
    search_text_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Main library to process search query.
        self.api = Database()
        # Prevents suggestion box from updating when not needed.
        self.retain_query = ''

    def search(self):
        """Initiates search and displays updates GUI data."""
        self.api.update_idx_key(self.search_text_input.text)
        self.parent.parent.parent.search_suggestions_box.\
        suggestions_box.clear_widgets()

        if not type(self.api.search_key) == type(None):
            self.parent.parent.results_panel.update_details_panel\
            (self.api.details())
            self.parent.parent.results_panel.update_tab_names(self.api.tabs())
            self._update_effects(self.api.effects())
            self.api.search_key = None  # Resets index_key for resetting panels.

        else:
            self.parent.parent.results_panel.reset_panels()

        # Set current tab to ingredients_details tab. FR: 0003
        Clock.schedule_once(lambda dt:
            self.parent.parent.results_panel.switch_to(
            self.parent.parent.results_panel.tab_list[-1]
            ), 1/60
            )

    def _update_effects(self, effects):
        """Adds ingredients to the four panels."""
        panels = [
        self.parent.parent.results_panel.first_effect_panel,
        self.parent.parent.results_panel.second_effect_panel,
        self.parent.parent.results_panel.third_effect_panel,
        self.parent.parent.results_panel.fourth_effect_panel
        ]

        for x, items in enumerate(effects):
            self.parent.parent.results_panel.update_effects_panel(panels[x], \
                items)

    def update_suggestions(self):
        """Updates items in suggestion box."""
        if self.search_text_input.text != self.retain_query:
            self.retain_query = self.search_text_input.text
            self.parent.parent.parent.search_suggestions_box.\
            suggestions_box.clear_widgets()
            items = self.api.search_suggestions(self.search_text_input.text)
            for x, i in enumerate(items):
                if x%2 == 0:
                    self.parent.parent.parent.search_suggestions_box.\
                    suggestions_box.add_widget(
                    SearchBoxButton(
                        text = '[color=#AF9BDB][b]'+i+'[/color][/b]',
                        background_color = (62/255, 62/255, 40/255, 1),
                        on_release = lambda ins: self.suggestion_search(
                            ins.text
                            )  # FR: 0001
                        )
                    )
                else:
                    self.parent.parent.parent.search_suggestions_box.\
                    suggestions_box.add_widget(
                    SearchBoxButton(
                        text = '[color=#FFEADD][b]'+i+'[/color][/b]',
                        background_color = (62/255, 62/255, 40/255, 1),
                        on_release = lambda ins: self.suggestion_search(
                            ins.text
                            )
                        )
                    )

    def suggestion_search(self, input_text):
        """Callback function to autosearch clicked suggested results."""
        # Filter input_text from markup.
        input_text = [i for i in input_text]
        for x, i in enumerate(input_text[:]):
            if i == '[':
                remove = True
            if remove:
                input_text.pop(x)
                input_text.insert(x, '')
            if i == ']':
                remove = False
        input_text = ''.join(input_text)

        self.retain_query = input_text
        self.search_text_input.text = input_text
        self.search()


class Results(TabbedPanel):
    """The page layout that contains the search results."""
    ingredient_details_panel = ObjectProperty(None)
    first_effect_panel = ObjectProperty(None)
    second_effect_panel = ObjectProperty(None)
    third_effect_panel = ObjectProperty(None)
    fourth_effect_panel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Results, self).__init__(**kwargs)

    def update_details_panel(self, details):
        """Updates ingredient_details_panel
        with 'details' from :class: 'AlchemyQuery'"""
        # Add markup to text.
        details = details[:]
        for x, detail in enumerate(details[:]):
            detail = '[b]'+detail+'[/b]'
            details[x] = detail
        self.ingredient_details_panel.line1.value.text = details[0]
        self.ingredient_details_panel.line2.value.text = details[1]
        self.ingredient_details_panel.line3.value.text = details[2]
        self.ingredient_details_panel.line4.value.text = details[3]
        self.ingredient_details_panel.effects.first.value.text = details[4]
        self.ingredient_details_panel.effects.second.value.text = details[5]
        self.ingredient_details_panel.effects.third.value.text = details[6]
        self.ingredient_details_panel.effects.fourth.value.text = details[7]

    def update_effects_panel(self, panel, ingredients):
        """Recursively adds items from 'ingredients' from
        :class: 'AlchemyQuery' to specified 'panel'."""
        panel.clear_widgets()
        for x, ingredient in enumerate(ingredients):
            if x%2 == 0:
                panel.add_widget(
                    SearchBoxButton(
                        text = '[color=#AF9BDB][b]'+ingredient+'[/color][/b]',
                        background_color = (64/255, 64/255, 64/255, 1),
                        on_release = lambda ins: \
                        self.parent.parent.search_bar.suggestion_search(
                            ins.text
                            )
                        )
                    )
            else:
                panel.add_widget(
                    SearchBoxButton(
                        text = '[color=#FFEADD][b]'+ingredient+'[/color][/b]',
                        background_color = (64/255, 64/255, 64/255, 1),
                        on_release = lambda ins: \
                        self.parent.parent.search_bar.suggestion_search(
                            ins.text
                            )
                        )
                    )

    def update_tab_names(self, tabs):
        """Updates all effect_tab with 'tabs' from :class: 'AlchemyQuery'"""
        effects_panel_tabs = [
        self.ids.first_effect_tab,
        self.ids.second_effect_tab,
        self.ids.third_effect_tab,
        self.ids.fourth_effect_tab,
        ]

        # Add markup to text.
        for x, i in enumerate(tabs[:]):
            i = '[b]'+i+'[/b]'
            tabs[x] = i
        for x, tab in enumerate(effects_panel_tabs):
            tab.text = tabs[x]
        # Explicite udpate of tab width.
        Clock.schedule_once(self.on_tab_width, 0.1)

    def reset_panels(self):
        """Resets all panel widgets to default output."""
        self._reset_tab_names()
        self._reset_details_panel()

        # Clear all effects panel.
        panels = [
            self.first_effect_panel,
            self.second_effect_panel,
            self.third_effect_panel,
            self.fourth_effect_panel,
            ]

        for panel in panels:
            panel.clear_widgets()
            panel.add_widget(
                Label(text='[b]No results..[/b]', markup=True)
                )


    def _reset_details_panel(self):
        """Sets default output to ingredients_details_panel."""
        self.ingredient_details_panel.line1.name.text = \
        "[color=#29a329][b]Ingredient Name:[/b][/color]"
        self.ingredient_details_panel.line1.value.text = \
        "[b]N.A.[/b]"
        self.ingredient_details_panel.line2.name.text = \
        "[color=#29a329][b]Weight:[/b][/color]"
        self.ingredient_details_panel.line2.value.text = \
        "[b]N.A.[/b]"
        self.ingredient_details_panel.line3.name.text = \
        "[color=#29a329][b]Value:[/b][/color]"
        self.ingredient_details_panel.line3.value.text = \
        "[b]N.A.[/b]"
        self.ingredient_details_panel.line4.name.text = \
        "[color=#29a329][b]Obtained from/at:[/b][/color]"
        self.ingredient_details_panel.line4.value.text = \
        "    [b]N.A.[/b]"

        self.ingredient_details_panel.effects.first.name.text = \
        "[color=#29a329][b]Primary Effect[/b][/color]"
        self.ingredient_details_panel.effects.first.value.text = \
        "[b]N.A.[/b]"
        self.ingredient_details_panel.effects.second.name.text = \
        "[color=#29a329][b]Secondary Effect[/b][/color]"
        self.ingredient_details_panel.effects.second.value.text = \
        "[b]N.A.[/b]"
        self.ingredient_details_panel.effects.third.name.text = \
        "[color=#29a329][b]Tertiary Effect[/b][/color]"
        self.ingredient_details_panel.effects.third.value.text = \
        "[b]N.A.[/b]"
        self.ingredient_details_panel.effects.fourth.name.text = \
        "[color=#29a329][b]Quaternary Effect[/b][/color]"
        self.ingredient_details_panel.effects.fourth.value.text = \
        "[b]N.A.[/b]"

    def _reset_tab_names(self):
        """Sets default output to panel tab names."""
        tabs = [
        self.ids.first_effect_tab,
        self.ids.second_effect_tab,
        self.ids.third_effect_tab,
        self.ids.fourth_effect_tab,
        ]

        names = [  # Defined default names.
            "[b]Primary\nEffect[/b]",
            "[b]Secondary\nEffect[/b]",
            "[b]Tertiary\nEffect[/b]",
            "[b]Quaternary\nEffect[/b]"
            ]

        for x, tab in enumerate(tabs):
            tab.text = names[x]


class SearchBoxButton(Button):
    """Use for adding a dynamic number of buttons."""
    pass


# TODO: Move this class to its proper file.
class MenuBoxButton(SearchBoxButton):
    """The option button inside the menu drop box."""

    def on_release(self):
        """Toggle its parent drop box once selected."""
        # MyGrid > MenuDropBox > RootWidget
        self.parent.parent.parent.menu_button.toggle_box_drop()
