from parent_entity import ParentEntity
from drone import PlayerDrone


def update(self, dt):
    if self.game_ongoing:
        drone_pos = self.drone.get_coords()

        self.move_clouds()
        self.move_balloons()
        self.check_drone_collect_balloon()
        self.update_player_bullet()
        self.checkHealth()
        #self.update_entity_bullets()
        #self.update_entities()
        #self.check_ebullet_collision()

        drone_pos[0][0] += PlayerDrone.speedx
        drone_pos[0][1] += PlayerDrone.speedy

    if not self.game_ongoing:
        pass

def check_outOf(self, dt):
    if self.game_ongoing:
        for entity in ParentEntity.all:
            ParentEntity.check_outOf_window(self, entity)

    if not self.game_ongoing:
        pass