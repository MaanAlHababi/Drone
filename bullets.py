import drone
from drone import PlayerDrone


class ParentBullet:
    def __init__(self, widget):
        self.widget = widget

        self.width = self.widget.width
        self.height = self.widget.height

    def get_coords(self):
        return [self.widget.pos, [self.widget.pos[0] + self.width, self.widget.pos[1] + self.height]]


class DroneBullet(ParentBullet):
    bullets = []

    def __init__(self, widget, game_width, game_height):
        super().__init__(widget)
        self.widget = widget

        self.width = self.widget.width
        self.height = self.widget.height

        self.game_width = game_width
        self.game_height = game_height

    def check_outOf_window(self):
        if self.widget.pos[0] >= self.game_width - 20:
            return True
        return False

    def is_colliding_with(self, mob):
        mob_xmin, mob_xmax = mob.get_coords()[0][0], mob.get_coords()[1][0]
        mob_ymin, mob_ymax = mob.get_coords()[0][1], mob.get_coords()[1][1]

        bullet_xmin, bullet_xmax = self.get_coords()[0][0], self.get_coords()[1][0]
        bullet_ymin, bullet_ymax = self.get_coords()[0][1], self.get_coords()[1][1]

        if (mob_xmax >= bullet_xmax >= mob_xmin + 50) and (mob_ymax >= bullet_ymin and mob_ymin <= bullet_ymax
        ):
            return True


class Bullet(ParentBullet):
    enemy_bullets = []

    def __init__(self, widget):
        super().__init__(widget)
        self.widget = widget

        self.width = self.widget.width
        self.height = self.widget.height

    def check_outOf_window(self):
        if self.widget.pos[0] <= -20:
            return True
        return False

    def is_colliding_with(self, drone_coords):
        drone_xmin, drone_xmax = drone_coords[0][0], drone_coords[1][0]
        drone_ymin, drone_ymax = drone_coords[0][1], drone_coords[1][1]

        bullet_xmin, bullet_xmax = self.get_coords()[0][0], self.get_coords()[1][0]
        bullet_ymin, bullet_ymax = self.get_coords()[0][1], self.get_coords()[1][1]

        if (bullet_xmax >= drone_xmax >= bullet_xmin and (bullet_ymin <= drone_ymax and bullet_ymax >= drone_ymin)
        ):
            return True


def check_collision(self):
    for bullet in Bullet.enemy_bullets:
        if Bullet.is_colliding_with(bullet, drone.PlayerDrone.get_coords(self.drone)):
            self.remove_widget(bullet.widget)
            Bullet.enemy_bullets.remove(bullet)

            # Player got hit
            self.drone.health -= 5
            # print(self.drone.health)
            self.healthbar.value = self.drone.health
