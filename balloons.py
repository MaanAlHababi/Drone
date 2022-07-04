import random
from kivy.uix.image import Image
from drone import PlayerDrone

def init_balloons(self, dt):
    if self.game_ongoing:
        balloon_types = ["images/yellow_balloon.png", "images/green_balloon.png", "images/purple_balloon.png",
                         "images/red_balloon.png"]
        balloon_type = random.choice(balloon_types)

        x = random.randint(100, self.width)
        y = random.randint(50, 150)

        balloon = Image(source=balloon_type,
                        pos=(400, 300),
                        size=(75, 75))
        self.add_widget(balloon)
        self.balloons.append(balloon)
        self.balloon_list.append(balloon)

    else:
        pass

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
    for balloon in self.balloons:
        object_coords = [balloon.pos, [balloon.pos[0] + balloon.width, balloon.pos[1] + balloon.height]]
        # print(object_coords)
        # print(self.drone.get_coords())
        if self.drone.is_colliding_with(object_coords):
            self.remove_widget(balloon)
            self.balloons.remove(balloon)
            self.score += 1
            self.SCORE = (str(int(self.score)))
            #print("COLLIDING")

        #else:
            #print("NOT COLLIDING")

