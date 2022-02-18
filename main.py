import kivy
kivy.require('2.0.0')  # Kivy version control (02/02/2022 --latest)

import json
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import (
    ObjectProperty,
    )
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.widget import Widget


class AlchemyQuery:
    """For parsing and processing ingredient search query."""

    def __init__(self):
        # Load json database as 'adata'.
        with open('main_database.json', 'r') as f:
            self.adata = json.load(f)

        self._construct_data_pool()

        # Main key for pulling data.
        self.main_key = None

    def _construct_data_pool(self):
        """Constructs the data pool with as the following.
        [
        [name, weight, value, obtained, primary,  # List 1
        secondary, tertiary, quaternary],
        ...
        [name,weight, value, obtained, primary,  # List N
        secondary, tertiary, quaternary],
        ]
        """
        self.data_pool = []

        for x in range((len(self.adata['Ingredient'].keys()))):
            name = self.adata['Ingredient'][str(x)]
            weight = self.adata['Weight'][str(x)]
            value = self.adata['Value'][str(x)]
            obtained = self.adata['Obtained'][str(x)]
            primary = self.adata['Primary Effect'][str(x)]
            secondary = self.adata['Secondary Effect'][str(x)]
            tertiary = self.adata['Tertiary Effect'][str(x)]
            quaternary = self.adata['Quaternary Effect'][str(x)]

            self.data_pool.append(
                [name, str(weight), str(value), obtained, \
                primary, secondary, tertiary, quaternary]
                )


    def search(self, qeury_text):
        """Sets the key to be used to pull data."""
        word_pool = [i[0] for i in self.data_pool]

        for x, item in enumerate(word_pool):
            if qeury_text.lower().replace(' ', '') == \
            item.lower().replace(' ', ''):
                self.main_key = x

    def details(self):
        """Returns a list with the following structure.
        [Name, Weight, Value, Obtain, Primary Effect,
        Secondary Effect, Tertiary Effect, Quaternary Effect]
        """
        name = self.data_pool[self.main_key][0]
        weight = self.data_pool[self.main_key][1]
        value = self.data_pool[self.main_key][2]
        obtained = self.data_pool[self.main_key][3]
        primary = self.data_pool[self.main_key][4]
        secondary = self.data_pool[self.main_key][5]
        tertiary = self.data_pool[self.main_key][6]
        quaternary = self.data_pool[self.main_key][7]

        return [name, weight, value, obtained, \
        primary, secondary, tertiary, quaternary]

    def effects(self,):
        """Returns a nested list with the following structure.
        [
        [Ingredient 1, ..2, ..3, Ingredient N],  # Primary Effect
        [Ingredient 1, ..2, ..3, Ingredient N],  # Secondary Effect
        [Ingredient 1, ..2, ..3, Ingredient N],  # Tertiary Effect
        [Ingredient 1, ..2, ..3, Ingredient N]  # Quaternary Effect
        ]"""
        primary, secondary, tertiary, quaternary = [], [], [], []

        for x, y in enumerate(self.data_pool):
            for i in y:
                if i == self.data_pool[self.main_key][4]:
                    primary.append(self.data_pool[x][0])
                if i == self.data_pool[self.main_key][5]:
                    secondary.append(self.data_pool[x][0])
                if i == self.data_pool[self.main_key][6]:
                    tertiary.append(self.data_pool[x][0])
                if i == self.data_pool[self.main_key][7]:
                    quaternary.append(self.data_pool[x][0])

        return [primary, secondary, tertiary, quaternary]

    def tabs(self):
        """Returns a list with the following structure.
        [Primary Effect, Secondary Effect, Tertiary Effect, Quaternary Effect]
        """
        primary = self.data_pool[self.main_key][4]
        secondary = self.data_pool[self.main_key][5]
        tertiary = self.data_pool[self.main_key][6]
        quaternary = self.data_pool[self.main_key][7]

        return [primary, secondary, tertiary, quaternary]


class MyLabel(Label):
    """For adding a dynamic amount of labels."""
    pass


class ResultsTabPanel(TabbedPanel):
    """The page layout that contains the search results."""
    ingredient_details_panel = ObjectProperty(None)
    first_effect_panel = ObjectProperty(None)
    second_effect_panel = ObjectProperty(None)
    third_effect_panel = ObjectProperty(None)
    fourth_effect_panel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ResultsTabPanel, self).__init__(**kwargs)

    def add_to_details_panel(self, details):
        """Updates ingredient_details_panel
        with 'details' from :class: 'AlchemyQuery'"""
        # Add markup to text.
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

    def add_to_effects_panel(self, panel, ingredients):
        """Recursively adds items from 'ingredients' from
        :class: 'AlchemyQuery' to specified 'panel'."""
        panel.clear_widgets()
        for x, ingredient in enumerate(ingredients):
            if x%2 == 0:
                panel.add_widget(
                    MyLabel(
                        text = '[color=#AF9BDB][b]'+ingredient+'[/color][/b]'
                        )
                    )
            else:
                panel.add_widget(
                    MyLabel(
                        text = '[color=#FFEADD][b]'+ingredient+'[/color][/b]'
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


class PossibleResultsBox(GridLayout):
    """Outputs the possible results inside a scroll view box."""


class SearchBar(GridLayout):
    """A searchbar for the application."""
    search_text_input = ObjectProperty(None)

    # Main library to process search query.
    allib = AlchemyQuery()

    def search(self):
        self.allib.search(self.search_text_input.text)

        if not type(self.allib.main_key) == type(None):
            self.parent.results_panel.add_to_details_panel\
            (self.allib.details())
            self.parent.results_panel.update_tab_names(self.allib.tabs())
            self._add_effects(self.allib.effects())
            self.allib.main_key = None  # Resets main_key for resetting panels.

        else:
            self.parent.results_panel.reset_panels()

    def _add_effects(self, effects):
        """Adds ingredients to the four panels."""
        panels = [
        self.parent.results_panel.first_effect_panel,
        self.parent.results_panel.second_effect_panel,
        self.parent.results_panel.third_effect_panel,
        self.parent.results_panel.fourth_effect_panel
        ]

        for x, items in enumerate(effects):
            self.parent.results_panel.add_to_effects_panel(panels[x], items)


# class FrontWidget(GridLayout):
#     """The root widget of the application."""
#     pass


# class RootWidget(Widget):
#     """The root widget of the application."""
#     pass


class AlchemyIngredients(App):
    """Main application."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Window.size = (720, 1520)  # 16:9 screen ratio

        self._init_widget_tree()

    def _init_widget_tree(self):
        """Loads and initializes the main widget tree and its presets."""
        self.main = Builder.load_file('main_widget_tree.kv')
        print(self.main.front_widget.ids)

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

        # Updates and presets for suggestion box.
        Clock.schedule_interval(
            lambda dt: self._suggestion_box_update(), 1/60
            )

    def _suggestion_box_update(self):
        """Constantly updates the width and pos of the suggestion
        box to best match with the search text input box."""
        self.main.suggestions_box.width = \
        self.main.front_widget.search_bar.search_text_input.width
        self.main.suggestions_box.top = \
        self.main.front_widget.search_bar.search_text_input.y


    def build(self):
        return self.main


if __name__ == '__main__':
    MyApplication = AlchemyIngredients()
    MyApplication.run()
