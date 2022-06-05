from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel


from db_api import Database
from templates import TogglePanel


class MenuButton(Button):
    """Menu button of the front panel.

    Methods
    -------
    toggle_box_drop
        Toggle context menu visibility on screen.
    """

    def __init__(self, **kwargs):
        """Pass keyword arguments to super class."""
        super(MenuButton, self).__init__(**kwargs)

    def toggle_box_drop(self):
        """Toggle context menu visibility on screen.

        Note
        ----
        context menu -> "front_panel.py > ContextMenu"
        """

        # Check flag. Set default width of context menu buttons.
        if self.parent.context_menu.SETUP_WIDTH:
            children = [i for i in \
            self.parent.context_menu.context_menu.children]
            def_width = max([i.width for i in children]) + 20
            self.parent.context_menu.width = f"{def_width}dp"
            for i in children:
                i.size_hint = 1, None
                i.size = i.texture_size
                i.text_size = i.size
            self.parent.context_menu.SETUP_WIDTH = None  # Disable flag.
            self.toggle_box_drop()

        # Set context menu height.
        if self.drop_box == 'shown':
            self.parent.context_menu.height = \
            self.parent.context_menu.context_menu.minimum_height
            self.parent.context_menu.top = \
            self.parent.menu_button.y
            self.drop_box = 'hidden'
        elif self.drop_box == 'hidden':
            self.parent.context_menu.height = "0dp"
            self.drop_box = 'shown'


class ContextMenu(ScrollView):
    """Context menu.
    
    Methods
    -------
    on_touch_down (override)
        Toggle context menu visibility on screen when mouse input is out of
        bounds.
    """
    SETUP_WIDTH = True  # Flag for initial context menu box width update.

    def on_touch_down(self, touch):  # Footnote [1]
        """Extension of on_touch_down method."""
        if not self.collide_point(*touch.pos) and \
        not self.parent.menu_button.collide_point(*touch.pos) and \
        self.parent.menu_button.drop_box == 'hidden':
            self.parent.menu_button.toggle_box_drop()

        return super(ContextMenu, self).on_touch_down(touch)


class ButtonLabel(Button):
    """A Button disguised as a Label."""
    pass


class ContextMenuButton(ButtonLabel):
    """Context menu button.

    Methods
    -------
    on_release (override)
        Toggle context menu visibility on screen.
    """

    def on_release(self):
        """Toggle context menu visibility on screen."""
        # MyGrid > ContextMenu > RootWidget
        self.parent.parent.parent.menu_button.toggle_box_drop()


class FrontPanel(TogglePanel):
    """The front page of the application."""

    def __init__(self, **kwargs):
        """Pass keyword arguments to super class.

        Methods
        -------
        update (override)
            Update panel assets and attributes.
        """
        super(FrontPanel, self).__init__(**kwargs)

    def update(self, root):
        """Update panel assets and attributes.

        Arguments
        ---------
        root: kivy obj
            The root widget of the application.
        """
        # Update size and pos attributes.
        self.pos = root.pos
        self.size = root.size

        # Prep & update size & "front_panel.kv > SearchSuggestionsBox".
        root.search_suggestions_box.width = \
        self.search_bar.search_text_input.width
        # Height from the bottom of the window to the bottom of the text input.
        set_height = root.height - abs(root.height - \
        self.search_bar.search_text_input.y)
        # Height from minimum_height attribute of search suggestions box.
        min_height = root.search_suggestions_box.suggestions_box.minimum_height

        # Set height of search suggestions box.
        if  min_height < set_height:
            root.search_suggestions_box.height = min_height
        else:
            root.search_suggestions_box.height = set_height

        # Set pos of search suggestions box.
        root.search_suggestions_box.top = self.search_bar.search_text_input.y

        # Update pos of "root.kv > MenuButton".
        root.menu_button.top = root.top
        root.menu_button.right =  root.right

        # Update pos of "root.vk > ContextMenu".
        root.context_menu.top = root.menu_button.y
        root.context_menu.right = root.right


class SearchBar(GridLayout):
    """Searchbar of the front panel.

    Methods
    -------
    search
        Initiate ingredient search using the text input.
    update_suggestions
        Update search suggestion box.
    suggestion_search
        Initiate ingredient search using passed argument.
    """
    search_text_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        """Create class attributes and connection to database.

        Attributes
        ----------
        api: Database obj
            Contains data from database.
        retain_query: string
            Last text input from search bar. Prevents suggestion box from
            updating when not needed.
        """
        super(SearchBar, self).__init__(**kwargs)
        # Run post kivy widget initialization code block.
        Clock.schedule_once(lambda dt: self._post_update(), 1/60)
        self.retain_query = ''

    def _post_update(self):
        """Extension of the constructor with a schedule delay."""
        # Create a reference to the root widget's database attribute.
        self.api = self.parent.parent.parent.database

    def search(self):
        """Initiate search and update widgets displaying results."""
        self.api.update_pull_key(self.search_text_input.text)
        self.parent.parent.parent.search_suggestions_box.\
        suggestions_box.clear_widgets()

        # If search returns an ingredient. Update widgets displaying results.
        if not type(self.api.search_key) == type(None):
            self.parent.parent.results_panel.update_details_panel\
            (self.api.details())
            self.parent.parent.results_panel.update_tab_names(self.api.tabs())
            self._update_effects(self.api.effects())
            self.api.search_key = None  # Reset search_key

        # Reset widgets displaying results.
        else:
            self.parent.parent.results_panel.reset_tabs()

        # Set current tab to "Ingredient Description" tab. Footnote [3]
        Clock.schedule_once(lambda dt:
            self.parent.parent.results_panel.switch_to(
            self.parent.parent.results_panel.tab_list[-1]
            ), 1/60
            )

    def _update_effects(self, effects):
        """Add ingredients to results tabbed panel."""
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
        """Update search suggestion box."""
        # Check if search bar input text is same from last search.
        if self.search_text_input.text != self.retain_query:

            # Retain search bar input text and clear suggestions box.
            self.retain_query = self.search_text_input.text
            self.parent.parent.parent.search_suggestions_box.\
            suggestions_box.clear_widgets()

            # Update suggestions box.
            items = self.api.search_suggestions(self.search_text_input.text)
            for x, i in enumerate(items):
                if x%2 == 0:
                    self.parent.parent.parent.search_suggestions_box.\
                    suggestions_box.add_widget(
                    ButtonLabel(
                        text = '[color=#AF9BDB][b]'+i+'[/color][/b]',
                        background_color = (62/255, 62/255, 40/255, 1),
                        on_release = lambda ins: self.suggestion_search(
                            ins.text
                            )  # Footnote [2]
                        )
                    )
                else:
                    self.parent.parent.parent.search_suggestions_box.\
                    suggestions_box.add_widget(
                    ButtonLabel(
                        text = '[color=#FFEADD][b]'+i+'[/color][/b]',
                        background_color = (62/255, 62/255, 40/255, 1),
                        on_release = lambda ins: self.suggestion_search(
                            ins.text
                            )
                        )
                    )

    def suggestion_search(self, input_text):
        """Initiate ingredient search using passed argument."""
        # Filter input_text from markup.
        # "[b]Example Ingredient[\b]" -> "Example Ingredient"
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

        # Initiate search for input_text.
        self.retain_query = input_text
        self.search_text_input.text = input_text
        self.search()


class Results(TabbedPanel):
    """The tabbed panel containing the search results.

    Methods
    -------
    update_details_panel
        Update "Ingredient Details" tab.
    update_effects_panel
        Update the last 4 panels. Primary Effect -> Quaternary Effect
    update_tab_names
        Update the names of the last 4 tabs accordingly.
    reset_tabs
        Reset all tabs' widgets text values to default.
    """
    ingredient_details_panel = ObjectProperty(None)
    first_effect_panel = ObjectProperty(None)
    second_effect_panel = ObjectProperty(None)
    third_effect_panel = ObjectProperty(None)
    fourth_effect_panel = ObjectProperty(None)

    def __init__(self, **kwargs):
        """Pass keyword arguments to super class."""
        super(Results, self).__init__(**kwargs)

    def update_details_panel(self, details):
        """Update "Ingredient Details" tab."""
        # Add markup to text.
        details = details[:]
        for x, detail in enumerate(details[:]):
            detail = '[b]'+detail+'[/b]'
            details[x] = detail

        # Update widgets.
        self.ingredient_details_panel.line1.value.text = details[0]
        self.ingredient_details_panel.line2.value.text = details[1]
        self.ingredient_details_panel.line3.value.text = details[2]
        self.ingredient_details_panel.line4.value.text = details[3]
        self.ingredient_details_panel.effects.first.value.text = details[4]
        self.ingredient_details_panel.effects.second.value.text = details[5]
        self.ingredient_details_panel.effects.third.value.text = details[6]
        self.ingredient_details_panel.effects.fourth.value.text = details[7]

    def update_effects_panel(self, panel, ingredients):
        """Update the last 4 panels. Primary Effect -> Quaternary Effect"""
        # Clear widgets from the 4 tabs.
        panel.clear_widgets()
        # Recursively add ingredients to their respective panels.
        for x, ingredient in enumerate(ingredients):
            if x%2 == 0:
                panel.add_widget(
                    ButtonLabel(
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
                    ButtonLabel(
                        text = '[color=#FFEADD][b]'+ingredient+'[/color][/b]',
                        background_color = (64/255, 64/255, 64/255, 1),
                        on_release = lambda ins: \
                        self.parent.parent.search_bar.suggestion_search(
                            ins.text
                            )
                        )
                    )

    def update_tab_names(self, tabs):
        """Update the names of the last 4 tabs accordingly.

        Note
        ----
        The last 4 tabs' names are updated with the searched ingredient's four
        effects accordingly.
        """
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
        Clock.schedule_once(self.on_tab_width, 1/60)

    def reset_tabs(self):
        """Reset all tabs' widgets text values to default."""
        self._reset_tab_names()
        self._reset_ingredient_details_tab()

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

    def _reset_tab_names(self):
        """Reset the tab names of the last 4 tabs back to default."""
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

    def _reset_ingredient_details_tab(self):
        """Reset "Ingredient Details" tab's widgets text values to default."""
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


# [1]: https://stackoverflow.com/questions/48487175/kivy-scrollview-doesnt-work-with-on-touch-down-method
# [2]: https://stackoverflow.com/questions/64634875/how-can-you-pass-parameters-to-kivy-buttons-bind-functions
# [3]: https://stackoverflow.com/questions/49050300/kivy-how-to-define-which-tab-is-to-be-active-on-opening-a-tabbedpanel
