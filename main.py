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
from entities import Entity


class MainWidget(Widget):
    from controls import _keyboard_closed, _on_keyboard_down, _on_keyboard_up
    from update import update, check_outOf
    from clouds import init_clouds, move_clouds
    from balloons import init_balloons, move_balloons, check_drone_collect_balloon
    from playershoot import update_player_bullet, shoot
    from dronehealthcheck import checkHealth

    game_ongoing = False

    menu_widget = ObjectProperty()
    losingmenu_widget = ObjectProperty()
    score_widget1 = ObjectProperty()
    score_widget2 = ObjectProperty()

    drone = None
    drone_bullet = None
    bullets = []

    score = 0
    SCORE = StringProperty(str(score))

    clouds = []
    balloons = []
    balloon_list = []

    drone_coordinates = [[0, 0], [0, 0]]
    balloon_coordinates = [[0, 0], [0, 0]]

    entity1_coordinates = [[0, 0], [0, 0]]
    entity2_coordinates = [[0, 0], [0, 0]]
    entity3_coordinates = [[0, 0], [0, 0]]

    round = 0
    entities = []

    entity_bullet = None
    entity_bullets = []
    ebullet_coordinates = [[0, 0], [0, 0]]

    healthbar = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file("menu.kv")
        Builder.load_file("losingmenu.kv")

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        Clock.schedule_interval(self.check_ebullet_collision, 1 / 60)
        Clock.schedule_interval(self.update, 1 / 600)
        Clock.schedule_interval(self.check_outOf, 1 / 600)
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
        # self.init_round()

    def init_drone(self):
        self.drone = PlayerDrone(self.width, self.height,
                                 Image(source="images/drone.png",
                                       pos=(100, 300),
                                       size=(75, 75)))
        self.add_widget(self.drone.get_widget())

        self.healthbar = ProgressBar(max=150, value=self.drone.health)
        self.add_widget(self.healthbar)

    def init_round(self):
        self.round += 1
        enemies = ["images/evil_drone.png", "images/angry_cloud.png", "images/skullairballoon.png",
                   "images/balloonjester.png"]

        positions = [(700, 400), (700, 250), (700, 100)]

        entity1 = Entity(self.width, self.height,
                         Image(source=random.choice(enemies),
                               pos=positions[0],
                               size=(75, 75)))

        entity2 = Entity(self.width, self.height,
                         Image(source=random.choice(enemies),
                               pos=positions[1],
                               size=(75, 75)))

        entity3 = Entity(self.width, self.height,
                         Image(source=random.choice(enemies),
                               pos=positions[2],
                               size=(75, 75)))

        self.add_widget(entity1.get_widget())
        self.add_widget(entity2.get_widget())
        self.add_widget(entity3.get_widget())

        '''
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
        self.entities.append(entity3)'''

    def get_balloon_coordinates(self):
        for balloon in self.balloons:
            x1, y1 = balloon.pos[0], balloon.pos[1]
            self.balloon_coordinates[0] = [x1, y1]

            x2, y2 = balloon.pos[0] + balloon.width, balloon.pos[1] + balloon.height
            self.balloon_coordinates[1] = [x2, y2]

    def get_entity_coordinates(self):
        # First Entity
        self.entity1_coordinates[0] = self.entities[0].pos

        self.entity1_coordinates[1][0] = self.entities[0].pos[0] + self.entities[0].width
        self.entity1_coordinates[1][1] = self.entities[0].pos[1] + self.entities[0].height

        # Second Entity
        self.entity2_coordinates[0] = self.entities[1].pos

        self.entity2_coordinates[1][0] = self.entities[1].pos[0] + self.entities[1].width
        self.entity2_coordinates[1][1] = self.entities[1].pos[1] + self.entities[1].height

        # Third Entity
        self.entity3_coordinates[0] = self.entities[2].pos

        self.entity3_coordinates[1][0] = self.entities[2].pos[0] + self.entities[2].width
        self.entity3_coordinates[1][1] = self.entities[2].pos[1] + self.entities[2].height

    def get_ebullet_coordinates(self):
        for child in self.entity_bullets:
            x1, y1 = child.pos
            self.ebullet_coordinates[0] = [x1, y1]

            x2, y2 = child.pos[0] + child.width, child.pos[1] + child.height
            self.ebullet_coordinates[1] = [x2, y2]

    def entity_shoot(self):
        global x, y
        self.get_entity_coordinates()
        mob = random.choice(self.entities)
        if self.entities.index(mob) == 0:
            x, y = self.entity1_coordinates[0]

        elif self.entities.index(mob) == 1:
            x, y = self.entity2_coordinates[0]

        elif self.entities.index(mob) == 2:
            x, y = self.entity3_coordinates[0]

        if mob.source == "images/evil_drone.png":
            self.entity_bullet = Image(source="images/evil_drone_bullet2.png",
                                       pos=(x, y))

        elif mob.source == "images/angry_cloud.png":
            self.entity_bullet = Image(source="images/lightning_bullet2.png",
                                       pos=(x, y))

        elif mob.source == "images/skullairballoon.png":
            self.entity_bullet = Image(source="images/bomb.png",
                                       pos=(x, y))

        elif mob.source == "images/balloonjester.png":
            self.entity_bullet = Image(source="images/jesters_knife.png",
                                       pos=(x, y))

        self.add_widget(self.entity_bullet)
        self.entity_bullets.append(self.entity_bullet)
        # Add to list for them to move
        # print(self.entity_bullets)

    def update_entity_bullets(self):
        drone_xmin, drone_ymin = self.drone.get_coords()[0][0], self.drone.get_coords()[0][1]
        drone_xmax, drone_ymax = self.drone.get_coords()[1][0], self.drone.get_coords()[1][1]

        self.get_ebullet_coordinates()
        bullet_xmin, bullet_ymin = self.ebullet_coordinates[0][0], self.ebullet_coordinates[0][1] - 20
        bullet_xmax, bullet_ymax = self.ebullet_coordinates[1][0], self.ebullet_coordinates[1][1]

        xdistance = bullet_xmax - drone_xmin
        ydistance = bullet_ymin - drone_ymax

        final_xdistance = (xdistance / 60) + 1
        final_ydistance = (ydistance / 60) + 1

        for self.entity_bullet in self.entity_bullets:
            for child in self.entity_bullets:
                if child.pos[1] <= 0:
                    self.remove_widget(child)
                    self.entity_bullets.remove(child)

                elif child.pos[1] >= self.height - 10:
                    self.remove_widget(child)
                    self.entity_bullets.remove(child)

                if child.pos[0] <= -10:
                    self.remove_widget(child)
                    self.entity_bullets.remove(child)

                elif child.pos[0] >= self.width - 10:
                    self.remove_widget(child)
                    self.entity_bullets.remove(child)

            self.entity_bullet.pos[0] -= final_xdistance
            self.entity_bullet.pos[1] -= final_ydistance

    def check_ebullet_collision(self, dt):
        if self.game_ongoing:
            self.drone.get_coords()
            self.get_ebullet_coordinates()

            drone_xmin, drone_ymin = self.drone_coordinates[0][0], self.drone_coordinates[0][1]
            drone_xmax, drone_ymax = self.drone_coordinates[1][0], self.drone_coordinates[1][1]

            bullet_xmin, bullet_ymin = self.ebullet_coordinates[0][0], self.ebullet_coordinates[0][1]
            bullet_xmax, bullet_ymax = self.ebullet_coordinates[1][0], self.ebullet_coordinates[1][1]

            # print(bullet_xmin, bullet_xmax, bullet_ymin, bullet_ymax)
            # print(drone_xmin, drone_xmax, drone_ymin, drone_ymax)
            if ((drone_xmax - 40) >= bullet_xmin >= (drone_xmin - 50)) and (
                    (drone_ymax - 65) >= bullet_ymin >= (drone_ymin - 50)):
                # print("hit")
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
            z = random.randint(1, 3000)

            def upward():
                child.pos[1] += .1

            def downward():
                child.pos[1] -= .1

            if z >= 2800 or z % 2 == 0:
                for i in range(random.randint(1, 20)):
                    upward()

            else:
                for i in range(random.randint(1, 22)):
                    downward()

            # BORDER LIMITS --- BORDER LIMITS --- BORDER LIMITS
            if child.pos[1] <= -10:
                child.pos[1] = -10

            elif child.pos[1] >= self.height - 70:
                child.pos[1] = self.height - 70

            if child.pos[0] <= 0:
                child.pos[0] = 0

            elif child.pos[0] >= self.width - 80:
                child.pos[0] = self.width - 80

        # SHOOT
        a = random.randint(1, 50)
        if a == 25:
            self.entity_shoot()


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
