"""Python references to the Kivy's rule definition."""


from kivy.uix.button import Button


class SearchBoxButton(Button):
    """For adding a dynamic number of buttons."""
    pass


class MenuBoxButton(SearchBoxButton):
    """For toggling menu_drop_box once an item has been selected."""

    def on_press(self):
        # MyGrid > MenuDropBox > RootWidget
        self.parent.parent.parent.menu.toggle_box_drop()
