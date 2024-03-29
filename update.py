import asyncio
import random

from kivy.uix.image import Image

from parent_entity import ParentEntity
from drone import PlayerDrone
from enemies import Enemy
from bullets import Bullet, DroneBullet, check_collision


# Here you create a coroutine (global scope)
async def delayWithoutFreeze():
    await asyncio.sleep(.35)


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

        # CHECK THE PLAYER'S HEALTH | Health bar follows player
        self.healthbar.pos = (self.drone.widget.pos[0] - 13, self.drone.widget.pos[1] + 25)
        if self.drone.health <= 0:
            self.lose()

        # CHECK EACH MOB'S HEALTH | Health bar follows mobs
        if len(Enemy.enemies) > 0:
            for mob in Enemy.enemies:
                if mob.health_value <= 0:
                    self.remove_widget(mob.widget)
                    Enemy.enemies.remove(mob)
                    self.score += 5
                    self.SCORE = (str(int(self.score)))


        # UPDATE PLAYER'S BULLETS
        for bullet in DroneBullet.bullets:
            bullet.widget.pos[0] += 10

        pass

        # CHECK PLAYER BULLET COLLISION WITH MOBS
        if len(Enemy.enemies) > 0:
            for mob in Enemy.enemies:
                for bullet in DroneBullet.bullets:
                    if bullet.is_colliding_with(mob):
                        self.remove_widget(bullet.widget)
                        DroneBullet.bullets.remove(bullet)
                        # Mob got hit
                        mob.health_value -= 5


        else:
            self.init_round()

        # MOB SHOOTING
        m = self.mobShoot()
        try:
            if m.shoot_cooldown == 0:
                self.add_widget(m.shoot(m.widget))
                m.shoot_cooldown = m.original_cd

            elif m.shoot_cooldown > 0:
                m.shoot_cooldown -= 1

            else:
                pass
        except AttributeError:
            pass

        finally:
            pass


        # UPDATING BULLETS
        for bullet in Bullet.enemy_bullets:
            bullet.widget.pos[0] -= 10

    else:
        pass


def shoot(self):
    x = self.drone.get_coords()[0][0]
    y = self.drone.get_coords()[0][1]

    widget = Image(source="assets/drone_bullet.png",
                   pos=(x, y),
                   size=(50, 50))

    drone_bullet = DroneBullet(widget, self.width, self.height)

    self.add_widget(drone_bullet.widget)
    DroneBullet.bullets.append(drone_bullet)

    asyncio.create_task(delayWithoutFreeze(), name='shootTask')
