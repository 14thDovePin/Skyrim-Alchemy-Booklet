from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kv_py_ref import SearchBoxButton


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
                    SearchBoxButton(
                        text = '[color=#AF9BDB][b]'+ingredient+'[/color][/b]',
                        background_color = (64/255, 64/255, 64/255, 1),
                        on_release = lambda ins: \
                        self.parent.search_bar.suggestion_search(ins.text)
                        )
                    )
            else:
                panel.add_widget(
                    SearchBoxButton(
                        text = '[color=#FFEADD][b]'+ingredient+'[/color][/b]',
                        background_color = (64/255, 64/255, 64/255, 1),
                        on_release = lambda ins: \
                        self.parent.search_bar.suggestion_search(ins.text)
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
