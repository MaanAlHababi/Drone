from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget

Config.set('graphics', 'width', '1050')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.properties import Clock, StringProperty, ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
import random
import asyncio


class MainWidget(Widget):
    from controls import _keyboard_closed, _on_keyboard_down, _on_keyboard_up
    from update import update
    from clouds import init_clouds, move_clouds
    from balloons import init_balloons, move_balloons, check_drone_collect_balloon
    from playershoot import shoot, update_player_bullet
    from dronehealthcheck import checkHealth

    game_ongoing = False

    menu_widget = ObjectProperty()
    score_widget1 = ObjectProperty()
    score_widget2 = ObjectProperty()

    drone = None
    drone_bullet = None

    entity_bullet = None

    SCORE = StringProperty("0")
    score = 0

    clouds = []
    balloons = []
    balloon_list = []
    bullets = []

    current_speed_y = 0
    current_speed_x = 0

    drone_coordinates = [(0, 0), (0, 0)]
    balloon_coordinates = [(0, 0), (0, 0)]
    entity_coordinates = [(0, 0), (0, 0)]
    ebullet_coordinates = [(0, 0), (0, 0)]

    round = 0
    entities = []
    entity_bullets = []


    healthbar = None
    player_health = 150

    enemy_health = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file("menu.kv")

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def start(self):
        self.game_ongoing = True
        self.menu_widget.opacity = 0
        self.score_widget1.opacity = 1
        self.score_widget2.opacity = 1

        self.init_drone()

        self.init_round()

        Clock.schedule_interval(self.update, 1 / 600)
        Clock.schedule_interval(self.init_balloons, 7)
        Clock.schedule_interval(self.init_clouds, 1 / 5)

    def init_drone(self):
        self.drone = Image(source="images/drone.png",
                           pos=(100, 300))

        self.add_widget(self.drone)
        self.drone_coordinates[0] = self.drone.pos

        self.healthbar = ProgressBar(max=150, value=self.player_health)

        self.add_widget(self.healthbar)

    def init_round(self):
        self.round += 1

        enemies = ["images/evil_drone.png", "images/angry_cloud.png", "images/skullairballoon.png"]

        positions = [(700, 400), (700, 250), (700, 100)]

        entity1 = Image(source=random.choice(enemies),
                        pos=positions[0])

        entity2 = Image(source=random.choice(enemies),
                        pos=positions[1])

        entity3 = Image(source=random.choice(enemies),
                        pos=positions[2])

        self.add_widget(entity1)
        self.add_widget(entity2)
        self.add_widget(entity3)

        self.entities.append(entity1)
        self.entities.append(entity2)
        self.entities.append(entity3)

    def get_drone_coordinates(self):
        x1, y1 = self.drone.pos
        self.drone_coordinates[0] = (x1, y1)

        x2, y2 = self.drone.pos[0] + self.drone.width, self.drone.pos[1] + self.drone.height
        self.drone_coordinates[1] = (x2, y2)

    def get_balloon_coordinates(self):
        for balloon in self.balloons:
            x1, y1 = balloon.pos[0], balloon.pos[1]
            self.balloon_coordinates[0] = (x1, y1)

            x2, y2 = balloon.pos[0] + balloon.width, balloon.pos[1] + balloon.height
            self.balloon_coordinates[1] = (x2, y2)

    def get_entity_coordinates(self):
        for child in self.entities:
            x1, y1 = child.pos
            self.entity_coordinates[0] = (x1, y1)

            x2, y2 = child.pos[0] + child.width, child.pos[1] + child.height
            self.entity_coordinates[1] = (x2, y2)

    def get_ebullet_coordinates(self):
        for child in self.entity_bullets:
            x1, y1 = child.pos
            self.ebullet_coordinates[0] = (x1, y1)

            x2, y2 = child.pos[0] + child.width, child.pos[1] + child.height
            self.ebullet_coordinates[1] = (x2, y2)

    def entity_shoot(self):
        print(self.entities)
        for child in self.entities:
            self.get_entity_coordinates()


            x = self.entity_coordinates[0][0]
            y = self.entity_coordinates[0][1] - 20

            if child.source == "images/evil_drone.png":
                self.entity_bullet = Image(source="images/evil_drone_bullet2.png",
                                           pos=(x, y))

            elif child.source == "images/angry_cloud.png":
                self.entity_bullet = Image(source="images/lightning_bullet2.png",
                                           pos=(x, y))

            elif child.source == "images/skullairballoon.png":
                self.entity_bullet = Image(source="images/bomb.png",
                                           pos=(x, y))

        self.add_widget(self.entity_bullet)
        self.entity_bullets.append(self.entity_bullet)  # Add to list for them to move

    def update_entity_bullets(self):
        self.get_drone_coordinates()
        self.get_entity_coordinates()

        drone_xmin, drone_ymin = self.drone_coordinates[0][0], self.drone_coordinates[0][1]
        drone_xmax, drone_ymax = self.drone_coordinates[1][0], self.drone_coordinates[1][1]

        bullet_xmin, bullet_ymin = self.entity_coordinates[0][0], self.entity_coordinates[0][1] - 20
        bullet_xmax, bullet_ymax = self.entity_coordinates[1][0], self.entity_coordinates[1][1]

        xdistance = bullet_xmax - drone_xmin
        ydistance = bullet_ymin - drone_ymax

        final_xdistance = (xdistance / 60) + 1
        final_ydistance = (ydistance / 60) + 1

        for self.entity_bullet in self.entity_bullets:
            for child in self.entity_bullets:
                if child.pos[1] <= 0:
                    self.remove_widget(child)

                elif child.pos[1] >= self.height - 10:
                    self.remove_widget(child)

                if child.pos[0] <= -10:
                    self.remove_widget(child)

                elif child.pos[0] >= self.width - 10:
                    self.remove_widget(child)

            self.entity_bullet.pos[0] -= final_xdistance
            self.entity_bullet.pos[1] -= final_ydistance

        pass

    def check_ebullet_collision(self):
        self.get_drone_coordinates()
        self.get_ebullet_coordinates()

        drone_xmax, drone_ymax = self.drone_coordinates[1][0], self.drone_coordinates[1][1]

        bullet_xmin, bullet_ymin = self.ebullet_coordinates[0][0], self.ebullet_coordinates[0][1]
        bullet_xmax, bullet_ymax = self.ebullet_coordinates[1][0], self.ebullet_coordinates[1][1]

        drone_center_x = drone_xmax - self.drone.width / 2
        drone_center_y = drone_ymax - self.drone.height / 2

        if bullet_xmax >= drone_center_x >= bullet_xmin and bullet_ymax >= drone_center_y >= bullet_ymin:

            for self.entity_bullet in self.entity_bullets:
                self.remove_widget(self.entity_bullet)
                for ebullet in self.entity_bullets:
                    self.entity_bullets.remove(ebullet)
                    self.remove_widget(ebullet)

                # print("Player got hit")
                self.player_health -= 5
                # print(self.player_health)
                self.healthbar.value = self.player_health

    def update_entities(self):
        for child in self.entities:
            self.entity_shoot()
            break


            # BORDER LIMITS --- BORDER LIMITS --- BORDER LIMITS
            #if child.pos[1] <= -10:
            #    child.pos[1] = -10

            #elif child.pos[1] >= self.height - 70:
            #    child.pos[1] = self.height - 70

            #if child.pos[0] <= 0:
            #    child.pos[0] = 0

            #elif child.pos[0] >= self.width - 80:
            #    child.pos[0] = self.width - 80

class Drone(App):
    def build(self):
        Window.clearcolor = (.2, .6, .8, 1)
        xd = MainWidget()
        return xd

    async def kivyCoro(self):  # This is the method that's gonna launch your kivy app
        await self.async_run(async_lib='asyncio')
        print('Kivy async app finished...')

    # This func will start all the "tasks", in this case the only task is the kivy app
    async def base(self):
        (done, pending) = await asyncio.wait({self.kivyCoro()},
                                             return_when='FIRST_COMPLETED')


if __name__ == '__main__':
    instanceApp = Drone()  # You have to instanciate your App class
    asyncio.run(instanceApp.base())  # Run in async mode

# Drone().run()
