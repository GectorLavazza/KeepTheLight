import random

import pygame
from pygame import Vector2
from pygame.sprite import Sprite

from settings import *


class Particle(Sprite):
    def __init__(self, screen, pos, dx, dy, color, time, *group):
        super().__init__(*group)
        self.color = color
        self.screen = screen

        self.image = self.get_image()
        self.image = pygame.transform.scale_by(self.image, random.choice([0.5, 0.75, 1]))
        self.rect = self.image.get_rect()

        self.velocity = Vector2(dx, dy)
        self.rect.center = pos

        self.elapsed_time = 0
        self.time = time

        self.base_pos = Vector2(pos)

    def get_image(self):
        w = h = PARTICLE_SIZE
        image = pygame.Surface((w, h), pygame.SRCALPHA)
        image.fill((0, 0, 0))

        for i in range(50):
            r = PARTICLE_SIZE / 2
            radius = (r - r / 80 * (50 - i))

            surface = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.circle(surface, self.color, (r, r), radius)

            image.blit(surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

        return image

    def update(self, dt):
        self.velocity.x += random.randint(-100, 100) / 1000
        self.velocity.y += random.randint(-100, 100) / 1000

        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt

        self.elapsed_time += dt

        if self.elapsed_time >= self.time:
            self.kill()

        if not (-20 <= self.rect.centerx <= WIDTH + 20 and
                -20 <= self.rect.centery <= HEIGHT + 20):
            self.kill()

        self.screen.blit(self.image, self.rect.topleft, special_flags=pygame.BLEND_RGB_MAX)


def create_particles(screen, color, position, amount, time, *group):
    for _ in range(random.randint(max(1, amount // 4 * 3), max(2, amount // 4 * 5))):
        dx = random.randint(-500, 500) / 500
        dy = random.randint(-500, 500) / 500
        t = random.randint(max(1, time // 4 * 3), max(2, time // 4 * 5))
        Particle(screen, position, dx, dy, color, t, *group)
