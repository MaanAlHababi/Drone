import asyncio
import random

from kivy.uix.image import Image

from parent_entity import ParentEntity
from drone import PlayerDrone

# Here you create a coroutine (global scope)
async def delayWithoutFreeze():
    await asyncio.sleep(.35)

async def enemyShootDelay():
    await asyncio.sleep(random.random())


# MAIN GAME LOOP

def update(self, dt):
    if self.game_ongoing:

        self.move_clouds()
        self.move_balloons()
        self.check_drone_collect_balloon()
        self.update_entity_bullets()

        #self.check_ebullet_collision()


        # UPDATES PLAYER MOVEMENT AND FIXES POSITION IF OUT OF WINDOW BOUNDS
        self.drone.move()
        self.drone.check_outOf_window()

        # CHECK THE PLAYER'S HEALTH
        if self.healthbar.value == 0:
            # print("GAME OVER")
            self.game_ongoing = False
            self.losingmenu_widget.opacity = 1


        # UPDATE PLAYER'S BULLETS
        for self.drone_bullet in self.bullets:
            self.drone_bullet.pos[0] += 10

        pass

    else:
        pass

def shoot(self):
    x = self.drone.get_coords()[0][0]
    y = self.drone.get_coords()[0][1] - 20

    self.drone_bullet = Image(source="images/drone_bullet.png",
                              pos=(x, y))

    self.add_widget(self.drone_bullet)
    self.bullets.append(self.drone_bullet)

    asyncio.create_task(delayWithoutFreeze(), name='shootTask')