from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.popup import Popup


from db_api import Database
from templates import TogglePanel


class AddIngredientPanel(TogglePanel):
    """A panel for adding an ingredient to the database.

    Methods
    -------
    toggle_panel (inherited)
        Toggle visibility of panel on screen.
    reset_entries
        Reset all panel ingredient entries.
    update (override)
        Update panel assets and attributes.
    return_effects
        Return a set list of all the ingredient effects from the database.
    prep_entry
        Check ingredient entry, add it to the database.
    """

    def __init__(self, **kwargs):
        """Initialize connection with the database.

        Attributes
        ----------
        api: Database obj
            Contains data from database.
        ingredient_entry: list
            Contains 8 values to be appended to the database.
        UPDATE_ERROR_LABELS: bool
            If True updates the error labels of the panel.
        """
        super(AddIngredientPanel, self).__init__(**kwargs)
        # Pull data from the database.
        self.api = Database()  # TODO: pull database from root instead.
        self.ingredient_entry = None

        # Flag for updating the panel's error labels.
        self.UPDATE_ERROR_LABELS = False

    def reset_entries(self):
        """Reset all the panel entries manually."""
        self.ids.name.text = ''
        self.ids.value.text = ''
        self.ids.weight.text = ''
        self.ids.obtained_at.text = ''
        self.ids.primary_effect.text = 'Primary Effect'
        self.ids.secondary_effect.text = 'Secondary Effect'
        self.ids.tertiary_effect.text = 'Tertiary Effect'
        self.ids.quaternary_effect.text = 'Quaternary Effect'
        self.ids.custom_primary_effect.text = ''
        self.ids.custom_secondary_effect.text = ''
        self.ids.custom_tertiary_effect.text = ''
        self.ids.custom_quaternary_effect.text = ''

        # Reset error labels.
        if len(self.panel_grid.children) == 12:
            self.panel_grid.remove_widget(self.panel_grid.children[1])
            self.panel_grid.remove_widget(self.panel_grid.children[1])
        # Set error labels update flag to False.
        self.UPDATE_ERROR_LABELS = False

    def update(self, root):
        """Update panel assets and attributes.

        Arguments
        ---------
        root: kivy obj
            The root widget of the application.
        """
        # Update size & pos of the panel.
        self.size = root.size
        self.x = root.x

        # Show or hide the panel.
        if self.shown:
            self.top = root.top
        else:
            self.top = root.y - 10

        # Update height of "add_ingredient_panel.kv > ADD_Label.id: note_text".
        self.ids.note_text.height = self.ids.note_text.texture_size[1]

        # Check flag. Update attributes of error labels.
        if self.UPDATE_ERROR_LABELS:
            self.panel_grid.children[1].height = self.panel_grid.children[1].\
            texture_size[1]
            self.panel_grid.children[1].width = root.width
            self.panel_grid.children[1].text_size[0] = root.width

    def return_effects(self):
        """Return a set list of all ingredient effects from the database."""
        effects = []
        effects_raw = [i[4:8] for i in self.api.data_pool]
        for item in effects_raw:
            for effect in item:
                effects.append(effect)
        effects = set(sorted(effects))
        effects = sorted(list(effects))
        effects.insert(0, 'Custom')
        return effects

    def prep_entry(self):
        """Check ingredient entry and add prep it for database append.

        Note
        ----
        Button at "add_ingredient_panel.kv > ConfirmAdd > MyGrid > MyGrid >
        Button.text: Cancel" MUST set attribute "ingredient_entry" to None
        before dismissing the popup!

        Button at "add_ingredient_panel.kv > ConfirmAdd > MyGrid > MyGrid >
        Button.text: Confirm" calls the method "append_entry" before dismissing
        the popup. Method "append_entry" already clears the "ingredient_entry"
        attribute.
        """
        # Check. Return if there are any errors.
        if self._check_values():
            return

        # Pull ingredient entry and prep for database append.
        entry = self._pop_up_confirm()[::-1]

        # Process entry values data type.
        self.ingredient_entry = [
            entry[0],  # Name
            round(float(entry[1])),  # Value
            float(entry[2]),  # Weight
            entry[3],  # Obtained at
            entry[4],  # Primary Effect
            entry[5],  # Secondary Effect
            entry[6],  # Tertiary Effect
            entry[7],  # Quaternary Effect
            ]

    def append_entry(self):
        """Append ingredient entry to the database."""
        self.api.append_ingredient(self.ingredient_entry)

        # Clear and reset entry.
        self.ingredient_entry = None
        self.reset_entries()

        # Update the database connection & refresh "Manage Ingredients" panel.
        # TODO: Update database object in this line.
        self.parent.manage_ingredients_panel.update_ingredients()

    def _check_values(self):
        """Check all the input entry values of the panel.

        Note
        ----
        If there are any incorrect or empty inputs. The method will create and
        add a label where the errors will be printed out on the panel.
        Returns True if there are any errors, otherwise returns False.
        """
        # Pull raw ingredients name from the database for input evaluation.
        self.ingredients_name_pool = \
        [i[0].lower().replace(' ','') for i in self.api.data_pool]
        # Pull raw effects from the database for input evaluation.
        self.effects_pool = \
        [i.lower().replace(' ','') for i in self.return_effects()]

        # Create variable for error message & reference ingredient entries.
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

        # Set the default values for the panel's Spinner objects.
        default_values = [
            'Primary Effect',
            'Secondary Effect',
            'Tertiary Effect',
            'Quaternary Effect'
            ]

        # Check IF name input entry is empty.
        if not name:
            error_messages = error_messages + \
                '    Ingredient Name entry cannot be empty!\n'

        # Check IF name input entry is NOT in the database.
        elif name.lower().replace(' ','') in self.ingredients_name_pool:
            error_messages = error_messages + \
                '    Ingredient Name entry invalid! Database' + \
                ' contains an entry with the same name..\n'

        # Check IF value input entry is empty.
        if not value:
            error_messages = error_messages + \
            '    Value entry cannot be empty!\n'

        # Check IF value input entry is NOT a valid number.
        elif self._check_number(value):
            error_messages = error_messages + \
                '    Value entry invalid! Must be a valid number..\n'

        # Check IF weight input entry is empty.
        if not weight:
            error_messages = error_messages + \
            '    Weight entry cannot be empty!\n'

        # Check IF weight input entry is NOT a valid number.
        elif self._check_number(weight):
            error_messages = error_messages + \
                '    Weight entry invalid! Must be a valid number..\n'

        # Check IF weight input entry is empty.
        if not obtained_at:
            error_messages = error_messages + \
            '    Obtained at entry cannot be empty!\n'

        # Check block for ingredients effects input entry.
        for n, effect in enumerate(base_effects):

            # Check IF effect is unchanged.
            if effect == default_values[n]:
                error_messages = error_messages + \
                f'    Please choose a {default_values[n]}!\n'

            # Check IF effect is custom.
            elif effect == 'Custom':
                # Check if input entry is empty.
                if not custom_effects[n]:
                    error_messages = error_messages + \
                    f'    Custom {default_values[n]} entry cannot be empty!\n'

                # Check IF input entry is NOT in the database
                elif custom_effects[n].lower().replace(' ','') in \
                self.effects_pool:
                    error_messages = error_messages + \
                        f'    Custom {default_values[n]} entry invalid! ' + \
                        'Database contains an entry with the same name.. ' + \
                        'Please choose it from the selection box instead.\n'

        # Check IF there is an error.
        if error_messages:

            # Check IF error labels exist and update them.
            if len(self.panel_grid.children) == 12:
                self.panel_grid.children[1].text = '[b][size=18dp]' + \
                error_messages

            # Create and add the error labels to the panel.
            else:
                title = Label(
                    size_hint_y = None,
                    height = dp(40),
                    markup = True,
                    text = '[b][size=24dp]Adding Failed',
                    halign = 'left',
                    padding = [dp(20), dp(0)]
                    )

                error_message = Label(
                    size_hint_y = None,
                    markup = True,
                    text = '[b][size=18dp]' + error_messages,
                    halign = 'left',
                    padding = [dp(20), dp(0)]
                    )

                self.panel_grid.add_widget(title, 1)
                self.panel_grid.add_widget(error_message, 1)

                # Set error labels update flag to True.
                self.UPDATE_ERROR_LABELS = True

            return True

        # Check if error labels exist and remove them.
        else:
            if len(self.panel_grid.children) == 12:
                self.panel_grid.remove_widget(self.panel_grid.children[1])
                self.panel_grid.remove_widget(self.panel_grid.children[1])
            # Set error labels update flag to False.
            self.UPDATE_ERROR_LABELS = False
            return False

    def _pop_up_confirm(self):
        """Confirmation popup box when adding an ingredient to the database.

        Pull and return all entry data from the panel. Widget contains the
        summary of the ingredient entry in a simple format for user review.
        """
        # Create pop up widget.
        confirm_popup = ConfirmAdd()

        # Pull all panel entries.
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
            str(round(float(self.ids.value.text))),
            self.ids.name.text
            ]

        # Update pop up labels with ingredient entry.
        labels = confirm_popup.pop_up_labels.children[1:-1]
        for x, i in enumerate(labels):
            i.text = i.text + refs[x]

        # Open pop up widget.
        confirm_popup.open()

        # Return ingredient entry.
        return refs

    def _check_number(self, number):
        """Return True if string can be an integer or a float otherwise False.

        Arguments
        ---------
        number: string
            The string that is processed.

        Notes
        -----
        Returns True if check passes, otherwise returns False.
        """
        try:
            float(number)
            return False
        except ValueError:
            return True


class ConfirmAdd(Popup):
    """Add Ingredient pop up widget confirmation box."""
    pass
