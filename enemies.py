from kivy.uix.image import Image

from parent_entity import ParentEntity


class Enemy(ParentEntity):
    enemies = []
    enemy_bullets = []
    speedy = 0

    def __init__(self, game_width, game_height, widget):
        super().__init__(
            game_width, game_height, widget
        )

        Enemy.enemies.append(widget)

    def move(self):
        new_pos = (self.widget.pos[0], self.widget.pos[1] + self.speedy)
        self.widget.pos = new_pos

    def get_pos(self, widget):
        return self.widget.pos

    def shoot(self, widget):
        x, y = self.get_pos(widget)

        global entity_bullet
        if widget.source == "images/evil_drone.png":
            entity_bullet = Image(source="images/evil_drone_bullet2.png",
                                  pos=(x, y))

        elif widget.source == "images/angry_cloud.png":
            entity_bullet = Image(source="images/lightning_bullet2.png",
                                  pos=(x, y))

        elif widget.source == "images/skullairballoon.png":
            entity_bullet = Image(source="images/bomb.png",
                                  pos=(x, y))

        elif widget.source == "images/balloonjester.png":
            entity_bullet = Image(source="images/jesters_knife.png",
                                  pos=(x, y))


        Enemy.enemy_bullets.append(entity_bullet)
        return entity_bullet
