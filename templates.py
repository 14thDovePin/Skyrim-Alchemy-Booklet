from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView


class MyGrid(GridLayout):
    """A GridLayout with tailored presets."""
    pass


class TogglePanel(ScrollView):
    """A base template of a panel that can be shown or hidden on screen.

    Attributes
    ----------
    shown: boolean
        Determines whether the panel is shown or hidden on the screen. Defaults
    to False.

    Methods
    -------
    toggle_panel (inherited)
        Toggles page visibility on screen.
    update (override)
        Update panel assets and attributes.

    Note
    ----
    Attribute 'shown' is found at 'templates.kv > TogglePanel'.
    """
    def __init__(self, **kwargs):
        """Set class attributes."""
        super(TogglePanel, self).__init__(**kwargs)

    def toggle_panel(self):
        """Set panel attribute 'shown' to True if False and False if True."""
        if self.shown:
            self.shown = False
        else:
            self.shown = True

    def update(self):
        """Update panel assets and attributes.

        Override this method for updating your panel.
        """
        pass
