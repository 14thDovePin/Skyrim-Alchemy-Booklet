from templates import TogglePanel


class ApplicationInfoPanel(TogglePanel):
    """A page that displays information about the developer of the app.

    Methods
    -------
    toggle_panel (inherited)
        Toggle visibility of panel on screen.
    update (override)
        Update panel assets and attributes.
    """

    def __init__(self, **kwargs):
        """Pass keyword arguments to super class."""
        super(ApplicationInfoPanel, self).__init__(**kwargs)

    def update(self, root):
        """Update panel assets and attributes.

        Arguments
        ---------
        root: kivy obj
            The root widget of the application.
        """
        # Panel size & pos attribute update.
        self.size = root.size
        self.x = root.x

        # Show or hide the panel depending on 'shown' attribute state.
        if self.shown:
            self.top = root.top
        else:
            self.top = root.y - 10
