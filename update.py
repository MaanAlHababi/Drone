import asyncio
import random

from kivy.uix.image import Image

from parent_entity import ParentEntity
from drone import PlayerDrone
from enemies import Enemy
from bullets import Bullet, DroneBullet, check_collision


# Here you create a coroutine (global scope)
async def delayWithoutFreeze():
    await asyncio.sleep(.45)


# MAIN GAME LOOP

def update(self, dt):
    if self.game_ongoing:

        self.move_clouds()
        self.move_balloons()
        self.check_drone_collect_balloon()
        self.check_collision()

        # UPDATES PLAYER MOVEMENT AND FIXES POSITION IF OUT OF WINDOW BOUNDS
        self.drone.move()
        self.drone.check_outOf_window()

        for bullet in Bullet.enemy_bullets:
            if Bullet.check_outOf_window(bullet):
                self.remove_widget(bullet.widget)
                Bullet.enemy_bullets.remove(bullet)

        for bullet in DroneBullet.bullets:
            if DroneBullet.check_outOf_window(bullet):
                self.remove_widget(bullet.widget)
                DroneBullet.bullets.remove(bullet)

        # CHECK THE PLAYER'S HEALTH
        if self.drone.health <= 0:
            self.game_ongoing = False
            self.losingmenu_widget.opacity = 1

        # UPDATE PLAYER'S BULLETS
        for bullet in DroneBullet.bullets:
            bullet.widget.pos[0] += 10

        pass

        # MOB SHOOTING & UPDATING BULLETS
        self.mobShoot()

        for bullet in Bullet.enemy_bullets:
            bullet.widget.pos[0] -= 10

    else:
        pass


def shoot(self):
    x = self.drone.get_coords()[0][0]
    y = self.drone.get_coords()[0][1] - 20

    widget = Image(source="assets/drone_bullet.png",
                   pos=(x, y))

    drone_bullet = DroneBullet(widget, self.width, self.height)

    self.add_widget(drone_bullet.widget)
    DroneBullet.bullets.append(drone_bullet)

    asyncio.create_task(delayWithoutFreeze(), name='shootTask')
