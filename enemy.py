import random

import pygame

from settings import BLACK, WIDTH, HEIGHT, CENTER


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, target_pos, world, *groups):
        super().__init__(*groups)

        self.world = world

        self.color = (0, 0, 0)

        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, self.color,
                           (self.image.width / 2, self.image.height / 2), self.image.width / 2)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.target_pos = target_pos

        self.speed = 2
        self.velocity = pygame.Vector2(0, 0)


    def update(self, dt):
        self.move(dt)
        if self.rect.center == CENTER:
            self.kill()
            core = self.world.core_g.sprites()[0]
            if self.color[0] >= 250:
                core.energy += 1
            else:
                core.energy -= 1 * (250 - self.color[0] // 50)

    def move(self, dt):
        d = pygame.Vector2(self.target_pos) - pygame.Vector2(self.rect.center)

        if d.length() > 0:
            d = d.normalize()

        self.velocity.x = d.x * self.speed * dt
        self.velocity.y = d.y * self.speed * dt

        self.rect.centerx += self.velocity.x
        self.rect.centery += self.velocity.y

    def update_image(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, self.color,
                           (self.image.width / 2, self.image.height / 2), self.image.width / 2)

class EnemySpawner:
    def __init__(self, world):
        self.max_tick = 30
        self.tick = self.max_tick

        self.world = world

        self.x = range(-50, WIDTH + 50, 50)
        self.y = range(-400, HEIGHT + 50, 50)

    def update(self, dt):
        self.tick -= dt
        if self.tick <= 0:
            self.tick = self.max_tick
            self.generate_enemy()

    def generate_enemy(self):
        pos = random.choice(self.x), random.choice(self.y)
        Enemy(pos, CENTER, self.world, self.world.enemies_g)
