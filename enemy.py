import pygame

from settings import BLACK


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
