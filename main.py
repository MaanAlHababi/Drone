from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget

import assets.HealthBar.info

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
from bullets import Bullet, DroneBullet

class MainWidget(Widget):
    from controls import _keyboard_closed, _on_keyboard_down, _on_keyboard_up
    from update import update
    from clouds import init_clouds, move_clouds
    from balloons import init_balloons, move_balloons, check_drone_collect_balloon
    from bullets import check_collision

    game_ongoing = False

    menu_widget = ObjectProperty()
    losingmenu_widget = ObjectProperty()
    score_widget1 = ObjectProperty()
    score_widget2 = ObjectProperty()

    drone = None
    healthbar = None
    drone_coordinates = [[0, 0], [0, 0]]

    round = 0
    score = 0
    SCORE = StringProperty(str(score))

    clouds = []
    balloons = []

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
        self.remove_widget(self.drone.widget)
        for i in DroneBullet.bullets:
            self.remove_widget(i)
        for i in self.clouds:
            self.remove_widget(i)
        for i in self.balloons:
            self.remove_widget(i)
        for i in Enemy.enemies:
            self.remove_widget(i.widget)
        for i in Bullet.enemy_bullets:
            self.remove_widget(i.widget)

        DroneBullet.bullets.clear()
        self.clouds.clear()
        self.balloons.clear()
        Enemy.enemies.clear()
        Bullet.enemy_bullets.clear()
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
        widget = Image(source="assets/drone.png",
                       pos=(100, 300),
                       size=(75, 75))

        self.drone = PlayerDrone(self.width, self.height, widget)
        self.add_widget(self.drone.get_widget())

        self.healthbar = ProgressBar(max=assets.HealthBar.info.start_v, value=self.drone.health)
        self.add_widget(self.healthbar)

    def init_round(self):
        self.round += 1

        enemies = ["assets/evil_drone.png", "assets/angry_cloud.png", "assets/skullairballoon.png",
                   "assets/balloonjester.png"]

        positions = [(700, 400), (700, 250), (700, 100)]
        img_size = (100, 100)

        enemy1 = Enemy(self.width, self.height,
                       Image(source=random.choice(enemies),
                             pos=positions[0],
                             size=img_size))

        enemy2 = Enemy(self.width, self.height,
                       Image(source=random.choice(enemies),
                             pos=positions[1],
                             size=img_size))

        enemy3 = Enemy(self.width, self.height,
                       Image(source=random.choice(enemies),
                             pos=positions[2],
                             size=img_size))

        self.add_widget(enemy1.get_widget())
        self.add_widget(enemy2.get_widget())
        self.add_widget(enemy3.get_widget())

    def mobShoot(self):
        async def mobShootDelay():
            await asyncio.sleep(5 * 60000)

        mobs = Enemy.enemies
        m = random.choice(mobs)
        self.add_widget(m.shoot(m.widget))
        j = 0
        for task in asyncio.all_tasks():
            if task.get_name() == 'mobShootTask':
                j += 1
            if j == 0:
                asyncio.create_task(mobShootDelay(), name='mobShootTask')


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
