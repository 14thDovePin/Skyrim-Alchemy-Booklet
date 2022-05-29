"""File contains some of templates.kv file's Python class references and
also contains other helper/template: functions; methods; classes"""


from kivy.uix.scrollview import ScrollView


def toggle_page(self):  # TODO: Omit block.
    """Sets page/panel attribute 'shown' to True if False or otherwise so."""
    if self.shown:
        self.shown = False
    else:
        self.shown = True


class TogglePanel(ScrollView):
    """A base template of a panel that can be shown or hidden on screen.

    Attributes
    ----------
    shown: boolean
        Determines whether the panel is shown or hidden on the screen. Defaults
    to False.

    Methods
    -------
    toggle_page
        Toggles page visibility on screen.

    Note
    ----
    Attribute 'shown' is found at 'templates.kv > TogglePanel'.
    """
    def __init__(self, **kwargs):
        """Set class attributes."""
        super(ScrollView, self).__init__(**kwargs)

    def toggle_page(self):  # TODO: Rename method to "toggle_panel".
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
