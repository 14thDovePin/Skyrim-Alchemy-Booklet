import weakref


from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from app_api import ParseQuery


from kv_py_ref import ConfirmAdd


class AddIngredient(ScrollView):
    """A panel for adding an ingredient to the database."""

    def __init__(self, **kwargs):
        """Initiates object to communicate with the database."""
        super().__init__(**kwargs)
        self.api = ParseQuery()

        # For updating the "error_label" of "_check_values" when it is present.
        self.error_label = False

    from toggle_page import toggle_page

    def return_effects(self):
        """Returns the all list of ingredient's effects from the database."""
        effects = []
        effects_raw = [i[4:8] for i in self.api.data_pool]
        for item in effects_raw:
            for effect in item:
                effects.append(effect)
        effects = set(sorted(effects))
        effects = sorted(list(effects))
        effects.insert(0, 'Custom')
        return effects

    def cancel(self):
        """Toggles the page."""
        pass

    def _reset_entries(self):
        """Removes and resets all the panel's entries."""
        pass

    def add_ingredient(self):
        """Compiles and add the input values of the panel."""
        # Check and return if there are any errors.
        if self._check_values():
            return

        # Confirm ingredient append to database.
        ingredient_entry = self._pop_up_confirm().reverse()

    def _pop_up_confirm(self):
        """Creates a popup box for confirming to add to database.

        Popup box contains the summary of the ingredient entry for review.
        After confirming, the ingredient will then be added to the database.
        """
        # Popup instance.
        confirm_popup = ConfirmAdd()

        # References to the panel entries.
        refs = [
            self.ids.custom_quaternary_effect.text if \
            self.ids.quaternary_effect.text == 'Custom' else \
            self.ids.quaternary_effect.text,
            self.ids.custom_tertiary_effect.text if \
            self.ids.tertiary_effect.text == 'Custom' else \
            self.ids.tertiary_effect.text,
            self.ids.custom_secondary_effect.text if \
            self.ids.secondary_effect.text == 'Custom' else \
            self.ids.secondary_effect.text,
            self.ids.custom_primary_effect.text if \
            self.ids.primary_effect.text == 'Custom' else \
            self.ids.primary_effect.text,
            self.ids.obtained_at.text,
            self.ids.weight.text,
            self.ids.value.text,
            self.ids.name.text
            ]

        # Add pop up text values from entries in the follownig order:
        # quaternary, tertiary, secondary, primary, obtained, weight, value,
        # and name.
        labels = confirm_popup.contents.pop_up_labels.children[1:-1]
        for x, i in enumerate(labels):
            i.text = i.text + refs[x]

        # Open pop up.
        confirm_popup.open()

        # Return refs.
        return refs

    def _check_values(self):
        """Checks all of the input values of the panel.

        If there are any input errors or mishaps. The method will add a label
        containing all of the information regarding the input errors and
        mishaps at the panel.
        """
        # For comparing ingredients name with the database.
        self.ingredients_name_pool = \
        [i[0].lower().replace(' ','') for i in self.api.data_pool]
        # For comparing effects with the database.
        self.effects_pool = \
        [i.lower().replace(' ','') for i in self.return_effects()]

        # Message & references.
        error_messages = ''
        name = self.ids.name.text
        value = self.ids.value.text
        weight = self.ids.weight.text
        obtained_at = self.ids.obtained_at.text

        base_effects = [
            self.ids.primary_effect.text,
            self.ids.secondary_effect.text,
            self.ids.tertiary_effect.text,
            self.ids.quaternary_effect.text,
            ]

        custom_effects = [
            self.ids.custom_primary_effect.text,
            self.ids.custom_secondary_effect.text,
            self.ids.custom_tertiary_effect.text,
            self.ids.custom_quaternary_effect.text
            ]

        default_values = [
            'Primary Effect',
            'Secondary Effect',
            'Tertiary Effect',
            'Quaternary Effect'
            ]

        # Check IF name input is empty.
        if not name:
            error_messages = error_messages + \
                '    Ingredient Name entry cannot be empty!'

        # Check IF name input is NOT in the database.
        elif name.lower().replace(' ','') in self.ingredients_name_pool:
            error_messages = error_messages + \
                '    Ingredient Name entry invalid! Database' + \
                ' contains an entry with the same name..'

        # Check IF value input is empty.
        if not value:
            error_messages = error_messages + \
            '\n    Value entry cannot be empty!'

        # Check IF value input is NOT a valid number.
        elif self._check_number(value):
            error_messages = error_messages + \
                '\n    Value entry invalid! Must be a valid number..'

        # Check IF weight input is empty.
        if not weight:
            error_messages = error_messages + \
            '\n    Weight entry cannot be empty!'

        # Check IF weight input is NOT a valid number.
        elif self._check_number(weight):
            error_messages = error_messages + \
                '\n    Weight entry invalid! Must be a valid number..'

        # Check IF weight input is empty.
        if not obtained_at:
            error_messages = error_messages + \
            '\n    Obtained at entry cannot be empty!'

        # Check block for ingredients effects.
        for n, effect in enumerate(base_effects):

            # Check IF effect is unchanged.
            if effect == default_values[n]:
                error_messages = error_messages + \
                f'\n    Please choose a {default_values[n]}!'

            # Check IF effect is custom.
            elif effect == 'Custom':
                # Check if input is empty.
                if not custom_effects[n]:
                    error_messages = error_messages + \
                    f'\n    Custom {default_values[n]} entry cannot be empty!'

                # Check IF input is NOT in the database
                elif custom_effects[n].lower().replace(' ','') in \
                self.effects_pool:
                    error_messages = error_messages + \
                        f'\n    Custom {default_values[n]} entry invalid! ' + \
                        'Database contains an entry with the same name.. ' + \
                        'Please choose it from the selection box instead.'

        # Check IF there are any errors
        if error_messages:

            # Check IF error labels exists and updates them.
            if len(self.panel_grid.children) == 12:
                self.panel_grid.children[1].text = '[b][size=18dp]' + \
                error_messages

            # Output errors to panel by using labels.
            else:
                error_title = Label(
                    size_hint_y = None,
                    height = dp(40),
                    markup = True,
                    text = '[b][size=24dp]Adding Failed',
                    halign = 'left',
                    padding = [dp(20), dp(0)]
                    )

                error_label = Label(
                    size_hint_y = None,
                    markup = True,
                    text = '[b][size=18dp]' + error_messages,
                    halign = 'left',
                    padding = [dp(20), dp(0)]
                    )

                # Add the 2 labels to the panel.
                self.panel_grid.add_widget(error_title, 1)
                self.panel_grid.add_widget(error_label, 1)

                # Set the "error_label" atribute of "AddIngredient" class to
                # True to enable the label's height update at
                # "_constant_updates" of "AlchemyBooklet" of "main.py".
                self.error_label = True

            return True

        # Check if error labels still exists and remove them.
        else:
            if len(self.panel_grid.children) == 12:
                self.panel_grid.remove_widget(self.panel_grid.children[1])
                self.panel_grid.remove_widget(self.panel_grid.children[1])
            return False

    def _check_number(self, number):
        """Checks if the string can be considerd an integer or a float.

        Arguments
        ---------
        number: string
        The string that is to be tested if it is a valid number.
        """
        try:
            float(number)
            return False
        except ValueError:
            return True
