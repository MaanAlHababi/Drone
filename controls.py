import asyncio
from drone import PlayerDrone

async def delayWithoutFreeze():
    # print('Wait 3 segs...')
    await asyncio.sleep(.55)
    # print('3 segs elapsed...')

def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard = None


def _on_keyboard_down(self, keyboard, keycode, text, modifiers, cooldown=3):
    j = 0  # This is a counter to know if a delay task is running
    if keycode[1] == 'w':
        PlayerDrone.speedy = +5

    elif keycode[1] == 'a':
        PlayerDrone.speedx = -5

    elif keycode[1] == 's':
        PlayerDrone.speedy = -5

    elif keycode[1] == 'd':
        PlayerDrone.speedx = +5

    elif keycode[1] == 'spacebar':
        for task in asyncio.all_tasks():  # This loop checks if there's a delay already running
            if task.get_name() == 'shootTask':
                j += 1
                # print('Theres already {} shootTask'.format(j))
            if j == 0:  # If j == 0 means that no delay is running so you can press and action again
                # This is how you call the async func
                asyncio.create_task(delayWithoutFreeze(), name='shootTask')
                self.shoot()

def _on_keyboard_up(self, keyboard, keycode):
    if keycode[1] == 'w':
        PlayerDrone.speedy = 0

    elif keycode[1] == 'a':
        PlayerDrone.speedx = 0

    elif keycode[1] == 's':
        PlayerDrone.speedy = 0

    elif keycode[1] == 'd':
        PlayerDrone.speedx = 0
