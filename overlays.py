from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


class MenuButton(Button):
    """The menu button for the applicatoin."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def toggle_box_drop(self):
        """Toggles the menu drop box by changing it's size_x to 0 and back."""

        # Sets the default width if not setup.
        # Note code block is a crude solution!
        if self.parent.menu_drop_box.default_width == 0:
            children = [i for i in \
            self.parent.menu_drop_box.menu_drop_box.children]
            def_width = max([i.width for i in children]) + 20
            self.parent.menu_drop_box.width = f"{def_width}dp"
            for i in children:
                i.size_hint = 1, None
                i.size = i.texture_size
                i.text_size = i.size
            self.parent.menu_drop_box.default_width = 1  # Lock.
            self.toggle_box_drop()

        # Sets the correct height.
        if self.drop_box == 'shown':
            self.parent.menu_drop_box.height = \
            self.parent.menu_drop_box.menu_drop_box.minimum_height
            self.parent.menu_drop_box.top = \
            self.parent.menu_button.y
            self.drop_box = 'hidden'
        elif self.drop_box == 'hidden':
            self.parent.menu_drop_box.height = "0dp"
            self.drop_box = 'shown'


class MenuDropBox(ScrollView):
    """The menu drop box that contains options and items."""

    def on_touch_down(self, touch):  # FR: 0004
        if not self.collide_point(*touch.pos) and \
        not self.parent.menu_button.collide_point(*touch.pos) and \
        self.parent.menu_button.drop_box == 'hidden':
            self.parent.menu_button.toggle_box_drop()

        return super(MenuDropBox, self).on_touch_down(touch)
