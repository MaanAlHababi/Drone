class ParentEntity:
    all = []
    def __init__(self, game_width, game_height, widget):
        self.widget = widget
        self.width = game_width
        self.height = game_height

    def check_outOf_window(self, widget):
        if widget.pos[1] <= -10:
            widget.pos[1] = -10

        elif widget.pos[1] >= self.height - 70:
            widget.pos[1] = self.height - 70

        if widget.pos[0] <= 0:
            widget.pos[0] = 0

        elif widget.pos[0] >= self.width - 80:
            widget.pos[0] = self.width - 80

    def get_widget(self):
        return self.widget