from parent_entity import ParentEntity

class Enemy(ParentEntity):
    speedy = 0

    def __init__(self, game_width, game_height, widget):
        super().__init__(
            game_width, game_height, widget
        )

        ParentEntity.all.append(widget)