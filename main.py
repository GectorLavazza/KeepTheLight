import random
from sys import exit
from time import time

import pygame
from settings import *

from light import Light, Shooter
from enemy import Enemy

import numpy as np

from world import World


def main():
    pygame.init()
    pygame.mouse.set_visible(True)
    pygame.event.set_allowed(
        [pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN,
         pygame.MOUSEBUTTONUP])

    flags = pygame.DOUBLEBUF | pygame.SCALED
    screen = pygame.display.set_mode(screen_size, flags, depth=8, vsync=1)
    pygame.display.set_caption('Keep The Light')

    clock = pygame.time.Clock()
    last_time = time()

    running = 1

    light_surface = pygame.Surface(screen_size)

    array = np.random.randint(0,2,(WIDTH // 4, HEIGHT // 4))

    bg = pygame.surfarray.make_surface(array)
    bg = pygame.transform.scale_by(bg, 4)
    bg.set_alpha(64)

    world = World(screen)

    core_g = pygame.sprite.Group()
    towers_g = pygame.sprite.Group()
    bullets_g = pygame.sprite.Group()

    core = Light(light_surface, 100, CENTER, WHITE, 500, world, world.core_g)
    light = Shooter(light_surface, CENTER, world, world.towers_g)

    enemies_g = pygame.sprite.Group()
    enemy = Enemy((0, 0), core.rect.center, world, world.enemies_g)

    while running:
        dt = time() - last_time
        dt *= 60
        last_time = time()

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = 0

                if event.key == pygame.K_F10:
                    pygame.display.toggle_fullscreen()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    light.set = True
                    light = Shooter(light_surface, CENTER, world, world.towers_g)

        screen.fill((0, 0, 0))
        light_surface.fill((0, 0, 0))

        # screen.blit(bg, (0, 0))
        light.set_pos(mouse_pos)

        world.update(dt)
        screen.blit(light_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

        world.enemies_g.draw(screen)

        pygame.display.update(pygame.Rect(0, 0, WIDTH, HEIGHT))
        clock.tick()

    pygame.quit()
    exit()


if __name__ == '__main__':
    main()