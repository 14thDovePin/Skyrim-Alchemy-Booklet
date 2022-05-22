def toggle_page(self):
    """Toggles the current page by changing it's size_x to 0 and back."""

    # Reference to height correction:
    # file "main.py", class "AlchemyBooklet", method "_constant_updates".
    if self.page_state == 'shown':
        self.page_state = 'hidden'

        # Hide other pages if shown.
        pages_state = [i for i in self.parent.children]
        pages_state.remove(self)
        for i in pages_state:
            if hasattr(i, "page_state"):
                i.page_state = "hidden"
                i.toggle_page()
                
    elif self.page_state == 'hidden':
        self.height = "0dp"
        self.page_state = 'shown'
