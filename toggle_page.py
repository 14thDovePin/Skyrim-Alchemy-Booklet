def toggle_page(self):
    """Sets page/panel attribute 'shown' to True if False or otherwise so."""
    if self.shown:
        self.shown = False
    else:
        self.shown = True
