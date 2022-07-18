from kivy.uix.image import Image
from parent_entity import ParentEntity


class PlayerDrone(ParentEntity):
    health = 150

    speedx = 0
    speedy = 0

    def __init__(self, game_width, game_height, widget):
        super().__init__(game_width, game_height, widget)
        self.widget = widget
        self.game_width = game_width
        self.game_height = game_height

        self.width = self.widget.width
        self.height = self.widget.height

        self.health = 150

    def get_health(self):
        return self.health

    def damage(self, dmg_amt):
        self.health -= dmg_amt

    def move(self):
        new_pos = (self.widget.pos[0] + self.speedx, self.widget.pos[1] + self.speedy)
        self.widget.pos = new_pos

    def is_colliding_with(self, collidable_object):
        drone_coords = self.get_coords()

        drone_xmin, drone_xmax = drone_coords[0][0], drone_coords[1][0]
        drone_ymin, drone_ymax = drone_coords[0][1], drone_coords[1][1]

        object_xmin, object_xmax = collidable_object[0][0], collidable_object[1][0]
        object_ymin, object_ymax = collidable_object[0][1], collidable_object[1][1]

        if (object_xmax >= drone_xmax >= object_xmin and object_ymax >= drone_ymin >= object_ymin
        ) or \
                (object_xmax >= drone_xmax >= object_xmin and object_ymax >= drone_ymax >= object_ymin
                ) or \
                (object_xmax >= drone_xmin >= object_xmin and object_ymax >= drone_ymin >= object_ymin

                ) or \
                (object_xmax >= drone_xmin >= object_xmin and object_ymax >= drone_ymax >= object_ymin

                ):
            return True

    def check_outOf_window(self):
        if self.widget.pos[1] <= -10:
            self.widget.pos[1] = -10

        elif self.widget.pos[1] >= self.game_height - 70:
            self.widget.pos[1] = self.game_height - 70

        if self.widget.pos[0] <= 0:
            self.widget.pos[0] = 0

        elif self.widget.pos[0] >= self.game_width - 80:
            self.widget.pos[0] = self.game_width - 80