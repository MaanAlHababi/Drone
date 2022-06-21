import random
from kivy.uix.image import Image

def init_clouds(self, dt):
    if self.game_ongoing:
        cloud_types = ["images/cloudbig.png", "images/cloudbig1.png", "images/cloudbig2.png"]
        cloud_type = random.choice(cloud_types)

        a = self.width
        b = self.width - 10

        x = random.randint(b, a)
        y = random.randint(-100, self.height)

        cloud = Image(source=cloud_type,
                      pos=(x, y))
        self.add_widget(cloud)
        self.clouds.append(cloud)


def move_clouds(self, *args):
    out_cloud_list = []  # If cloud not in screen remove:
    for child in self.children and self.clouds:
        if child.pos[0] < -50:
            out_cloud_list.append(child)

        else:
            child.pos[0] -= 5

    for self.cloud in out_cloud_list:
        self.remove_widget(self.cloud)