import pygame
from settings import *

class World:
    def __init__(self, screen):
        self.screen = screen

        self.enemies_g = pygame.sprite.Group()
        self.core_g = pygame.sprite.Group()
        self.towers_g = pygame.sprite.Group()
        self.bullets_g = pygame.sprite.Group()
        self.particles_g = pygame.sprite.Group()

    def update(self, dt):
        self.enemies_g.update(dt)
        self.core_g.update(dt)
        self.towers_g.update(dt)
        self.bullets_g.update(dt)
        self.particles_g.update(dt)
