class ParentEntity:
    def __init__(self, game_width, game_height, widget):
        self.widget = widget
        self.width = game_width
        self.height = game_height

    def get_widget(self):
        return self.widget
