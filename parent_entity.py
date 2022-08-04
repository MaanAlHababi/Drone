class ParentEntity:
    def __init__(self, game_width, game_height, widget):
        self.widget = widget
        self.width = game_width
        self.height = game_height

        self.w_width = self.widget.width
        self.w_height = self.widget.height

    def get_widget(self):
        return self.widget

    def get_coords(self):
        return [self.widget.pos, [self.widget.pos[0] + self.w_width, self.widget.pos[1] + self.w_height]]
