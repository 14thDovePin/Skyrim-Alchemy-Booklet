from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kv_py_ref import SearchBoxButton
from query_parser import ParseQuery


class SearchBar(GridLayout):
    """Searchbar for the main page of the application."""
    search_text_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Main library to process search query.
        self.api = ParseQuery()
        # Prevents suggestion box from updating when not needed.
        self.retain_query = ''

    def search(self):
        """Initiates search and displays updates GUI data."""
        self.api.update_idx_key(self.search_text_input.text)
        self.parent.parent.parent.scrollview_suggestions_box.\
        suggestions_box.clear_widgets()

        if not type(self.api.index_key) == type(None):
            self.parent.parent.results_panel.update_details_panel\
            (self.api.details())
            self.parent.parent.results_panel.update_tab_names(self.api.tabs())
            self._update_effects(self.api.effects())
            self.api.index_key = None  # Resets index_key for resetting panels.

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
            self.parent.parent.parent.scrollview_suggestions_box.\
            suggestions_box.clear_widgets()
            items = self.api.search_suggestions(self.search_text_input.text)
            for x, i in enumerate(items):
                if x%2 == 0:
                    self.parent.parent.parent.scrollview_suggestions_box.\
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
                    self.parent.parent.parent.scrollview_suggestions_box.\
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
