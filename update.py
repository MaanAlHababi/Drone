def update(self, dt):
    if self.game_ongoing:
        self.move_clouds()
        self.move_balloons()
        self.check_drone_collect_balloon()
        self.update_player_bullet()
        self.update_entity_bullets()
        self.update_entities()
        self.check_ebullet_collision()
        self.checkHealth()

        self.drone.pos[1] += self.current_speed_y
        self.drone.pos[0] += self.current_speed_x
        if self.drone.pos[1] <= -10:
            self.drone.pos[1] = -10

        elif self.drone.pos[1] >= self.height - 70:
            self.drone.pos[1] = self.height - 70

        if self.drone.pos[0] <= 0:
            self.drone.pos[0] = 0

        elif self.drone.pos[0] >= self.width - 80:
            self.drone.pos[0] = self.width - 80

    if not self.game_ongoing:
        pass