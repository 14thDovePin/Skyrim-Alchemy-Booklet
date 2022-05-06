from kivy.uix.gridlayout import GridLayout


class FrontWidget(GridLayout):
    """A page for adding new ingredients and related info into the database."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    from main_toggle_page import toggle_page
