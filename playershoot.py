import asyncio
from kivy.uix.image import Image


# Here you create a coroutine (global scope)
async def delayWithoutFreeze():
    # print('Wait 3 segs...')
    await asyncio.sleep(.55)
    # print('3 segs elapsed...')


def shoot(self):
    self.get_drone_coordinates()
    # print(self.drone_coordinates[0][0])
    # print(self.drone_coordinates[0][1])

    x = self.drone_coordinates[0][0]
    y = self.drone_coordinates[0][1] - 20

    self.drone_bullet = Image(source="images/drone_bullet.png",
                              pos=(x, y))

    self.add_widget(self.drone_bullet)
    self.bullets.append(self.drone_bullet)

    asyncio.create_task(delayWithoutFreeze(), name='shootTask')


def update_player_bullet(self):
    for self.drone_bullet in self.bullets:
        self.drone_bullet.pos[0] += 10

    pass