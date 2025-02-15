import random

import pygame
from settings import *

from particles import create_particles


class Light(pygame.sprite.Sprite):
    def __init__(self, screen, radius, pos, color, density, world, *groups):
        super().__init__(*groups)
        self.screen = screen
        self.world = world

        self.color = color
        self.density = density

        self.r = radius
        self.w = self.h = self.r * 2

        self.image = self.get_image()
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.zone = pygame.Rect(0, 0, self.w / 1.5, self.w / 1.5)
        self.zone.center = self.rect.center

        self.set = False

    def update(self, dt):
        self.screen.blit(self.image, self.rect.topleft, special_flags=pygame.BLEND_RGB_MAX)
        # pygame.draw.rect(self.screen, (255, 0, 0), self.zone)

    def get_image(self):
        image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        image.set_colorkey((0, 0, 0))

        for i in range(self.density):
            radius = (self.r - self.r / 80 * (self.density - i))

            surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            pygame.draw.circle(surface, self.color, (self.r, self.r), radius)

            image.blit(surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

        return image

    def set_pos(self, pos):
        self.rect.center = pos
        self.zone.center = pos


class Shooter(Light):
    def __init__(self, screen, pos, world, *groups):
        super().__init__(screen, 150, pos, YELLOW, 50, world, *groups)

        self.max_tick = 60
        self.tick = self.max_tick

    def update(self, dt):
        self.screen.blit(self.image, self.rect.topleft, special_flags=pygame.BLEND_RGB_MAX)
        # pygame.draw.rect(self.screen, (255, 0, 0), self.zone)
        if self.set:
            self.tick -= dt
            if self.tick <= 0:
                self.tick = self.max_tick
                v = [s for s in self.world.enemies_g.sprites()]
                if v:
                    s = random.choice(v)
                    Bullet(self.screen, self.rect.center, s.rect.center, self.world, self.world.bullets_g)


class Bullet(Light):
    def __init__(self, screen, pos, target_pos, world, *groups):
        super().__init__(screen, 30, pos, YELLOW, 50, world, *groups)
        self.speed = 15

        self.direction = pygame.Vector2(target_pos) - pygame.Vector2(pos)
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

    def update(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt
        self.rect.centery += self.direction.y * self.speed * dt

        self.screen.blit(self.image, self.rect.topleft, special_flags=pygame.BLEND_RGB_MAX)

        if not self.rect.colliderect(self.screen.get_rect()):
            self.kill()

        for enemy in self.world.enemies_g.sprites():
            if self.rect.colliderect(enemy.rect):
                r, g, b = enemy.color
                r, g, b = min(r + 10, 255), min(g + 10, 255), min(b + 10, 255)
                enemy.color = r, g, b
                enemy.update_image()
                create_particles(self.screen, YELLOW, enemy.rect.center, 10, 30, self.world.particles_g)
                self.kill()