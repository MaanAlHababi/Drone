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

from parent_entity import ParentEntity
from drone import PlayerDrone
from enemies import Enemy


class MainWidget(Widget):
    from controls import _keyboard_closed, _on_keyboard_down, _on_keyboard_up
    from update import update
    from clouds import init_clouds, move_clouds
    from balloons import init_balloons, move_balloons, check_drone_collect_balloon

    game_ongoing = False

    menu_widget = ObjectProperty()
    losingmenu_widget = ObjectProperty()
    score_widget1 = ObjectProperty()
    score_widget2 = ObjectProperty()

    drone = None
    healthbar = None

    drone_bullet = None

    bullets = []

    score = 0
    SCORE = StringProperty(str(score))

    round = 0

    clouds = []
    balloons = []
    balloon_list = []

    drone_coordinates = [[0, 0], [0, 0]]
    balloon_coordinates = [[0, 0], [0, 0]]

    entity_bullet = None
    entity_bullets = []
    ebullet_coordinates = [[0, 0], [0, 0]]



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file("menu.kv")
        Builder.load_file("losingmenu.kv")

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        Clock.schedule_interval(self.update, 1 / 6000)

        Clock.schedule_interval(self.init_balloons, 7)
        Clock.schedule_interval(self.init_clouds, 1 / 5)

    def reset(self):
        self.remove_widget(self.drone)
        for i in self.bullets:
            self.remove_widget(i)
        for i in self.clouds:
            self.remove_widget(i)
        for i in self.balloons:
            self.remove_widget(i)
        for i in self.entities:
            self.remove_widget(i)
        for i in self.entity_bullets:
            self.remove_widget(i)

        self.start()

    def start(self):
        self.game_ongoing = True
        self.menu_widget.opacity = 0
        self.losingmenu_widget.opacity = 0
        self.score_widget1.opacity = 1
        self.score_widget2.opacity = 1
        self.score = 0
        self.SCORE = str(0)

        self.init_drone()
        self.init_round()

    def init_drone(self):
        widget = Image(source="images/drone.png",
                       pos=(100, 300),
                       size=(75, 75))

        self.drone = PlayerDrone(self.width, self.height, widget)
        self.add_widget(self.drone.get_widget())

        self.healthbar = ProgressBar(max=150, value=self.drone.health)
        self.add_widget(self.healthbar)

    def init_round(self):
        self.round += 1
        enemies = ["images/evil_drone.png", "images/angry_cloud.png", "images/skullairballoon.png",
                   "images/balloonjester.png"]

        positions = [(700, 400), (700, 250), (700, 100)]

        enemy1 = Enemy(self.width, self.height,
                       Image(source=random.choice(enemies),
                             pos=positions[0],
                             size=(100, 100)))

        enemy2 = Enemy(self.width, self.height,
                       Image(source=random.choice(enemies),
                             pos=positions[1],
                             size=(100, 100)))

        enemy3 = Enemy(self.width, self.height,
                       Image(source=random.choice(enemies),
                             pos=positions[2],
                             size=(100, 100)))

        self.add_widget(enemy1.get_widget())
        self.add_widget(enemy2.get_widget())
        self.add_widget(enemy3.get_widget())

        self.add_widget(enemy1.shoot(enemy1.widget))

    def get_balloon_coordinates(self):
        for balloon in self.balloons:
            x1, y1 = balloon.pos[0], balloon.pos[1]
            self.balloon_coordinates[0] = [x1, y1]

            x2, y2 = balloon.pos[0] + balloon.width, balloon.pos[1] + balloon.height
            self.balloon_coordinates[1] = [x2, y2]

    def get_ebullet_coordinates(self):
        for child in self.entity_bullets:
            x1, y1 = child.pos
            self.ebullet_coordinates[0] = [x1, y1]

            x2, y2 = child.pos[0] + child.width, child.pos[1] + child.height
            self.ebullet_coordinates[1] = [x2, y2]

    def update_entity_bullets(self):
        for bullet in Enemy.enemy_bullets:
            bullet.pos[0] -= 10

    def check_ebullet_collision(self, dt):
        if self.game_ongoing:
            self.drone.get_coords()
            self.get_ebullet_coordinates()

            drone_xmin, drone_ymin = self.drone_coordinates[0][0], self.drone_coordinates[0][1]
            drone_xmax, drone_ymax = self.drone_coordinates[1][0], self.drone_coordinates[1][1]

            bullet_xmin, bullet_ymin = self.ebullet_coordinates[0][0], self.ebullet_coordinates[0][1]
            bullet_xmax, bullet_ymax = self.ebullet_coordinates[1][0], self.ebullet_coordinates[1][1]

            if ((drone_xmax - 40) >= bullet_xmin >= (drone_xmin - 50)) and (
                    (drone_ymax - 65) >= bullet_ymin >= (drone_ymin - 50)):
                for self.entity_bullet in self.entity_bullets:
                    self.remove_widget(self.entity_bullet)
                    for ebullet in self.entity_bullets:
                        self.entity_bullets.remove(ebullet)
                        self.remove_widget(ebullet)

                    # Player got hit
                    self.player_health -= 5
                    # print(self.player_health)
                    self.healthbar.value = self.player_health


class Drone(App):
    def build(self):
        Window.clearcolor = (.2, .6, .8, 1)
        xd = MainWidget()
        return xd

    async def kivyCoro(self):  # This is the method that's gonna launch your kivy app
        await self.async_run(async_lib='asyncio')
        # print('Kivy async app finished...')

    # This func will start all the "tasks", in this case the only task is the kivy app
    async def base(self):
        (done, pending) = await asyncio.wait({self.kivyCoro()},
                                             return_when='FIRST_COMPLETED')


if __name__ == '__main__':
    instanceApp = Drone()  # You have to instanciate your App class
    asyncio.run(instanceApp.base())  # Run in async mode

# Drone().run()
