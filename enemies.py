import random
import asyncio
from kivy.uix.image import Image

from parent_entity import ParentEntity
from bullets import Bullet

class Enemy(ParentEntity):
    enemies = []
    speedy = 0

    def __init__(self, game_width, game_height, widget, shoot_cooldown, health_value):
        super().__init__(
            game_width, game_height, widget
        )

        self.shoot_cooldown = shoot_cooldown
        self.original_cd = shoot_cooldown

        self.health_value = health_value

        Enemy.enemies.append(self)

    def move(self):
        new_pos = (self.widget.pos[0], self.widget.pos[1] + self.speedy)
        self.widget.pos = new_pos

    def shoot(self, widget):
        x, y = self.widget.pos
        bullets_dict = {"assets/evil_drone.png": "assets/evil_drone_bullet2.png",
                        "assets/angry_cloud.png": "assets/lightning_bullet2.png",
                        "assets/skullairballoon.png": "assets/bomb.png",
                        "assets/balloonjester.png": "assets/jesters_knife.png"}

        global entity_bullet, src
        for i in bullets_dict:
            if widget.source == i:
                src = bullets_dict.get(i)
        widget = Image(source=src,
                       pos=(x+20, y+20),
                       size=(50, 50))

        entity_bullet = Bullet(widget)


        Bullet.enemy_bullets.append(entity_bullet)
        return entity_bullet.widget