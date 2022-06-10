import random
from kivy.uix.image import Image

def init_balloons(self, dt):
    balloon_types = ["images/yellow_balloon.png", "images/green_balloon.png", "images/purple_balloon.png",
                     "images/red_balloon.png"]
    balloon_type = random.choice(balloon_types)

    x = random.randint(100, self.width)
    y = random.randint(50, 150)

    balloon = Image(source=balloon_type,
                    pos=(x, y))
    self.add_widget(balloon)
    self.balloons.append(balloon)
    self.balloon_list.append(balloon)

def move_balloons(self):
    for child in self.balloons:
        if child.pos[0] < -50 or child.pos[1] > self.height - 50:
            self.remove_widget(child)
            self.balloon_list.clear()
            self.balloons.clear()

        else:
            child.pos[0] -= 2
            child.pos[1] += 3

def check_drone_collect_balloon(self):
    self.get_drone_coordinates()
    self.get_balloon_coordinates()

    drone_xmax, drone_ymax = self.drone_coordinates[1][0], self.drone_coordinates[1][1]

    balloon_xmin, balloon_ymin = self.balloon_coordinates[0][0], self.balloon_coordinates[0][1]
    balloon_xmax, balloon_ymax = self.balloon_coordinates[1][0], self.balloon_coordinates[1][1]

    drone_center_x = drone_xmax - self.drone.width / 2
    drone_center_y = drone_ymax - self.drone.height / 2

    if balloon_xmax >= drone_center_x >= balloon_xmin and balloon_ymax >= drone_center_y >= balloon_ymin:
        for balloon in self.balloons:
            self.remove_widget(balloon)
            for balloon_ in self.balloons:
                self.balloons.remove(balloon_)
                self.remove_widget(balloon_)
            self.score += 1
            self.SCORE = (str(int(self.score)))