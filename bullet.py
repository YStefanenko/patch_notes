import pygame
import math


class Bullet:
    def __init__(self, position, direction):
        self.image = pygame.image.load('./assets/mouse.png')
        self.image = pygame.transform.scale(self.image, (63, 39))
        self.direction = direction
        angle = math.degrees(math.atan2(direction[1], direction[0]))
        self.image = pygame.transform.rotate(self.image, -angle)

        self.rect = self.image.get_rect()

        self.rect.center = position
        self.rect.size = (self.rect.size[0] * 0.8, self.rect.size[1] * 0.8)
        self.speed = 20

        self.static = False

    def update(self, viruses, tiles):
        if self.static:
            return
        self.rect.center = (self.rect.center[0] + self.direction[0] * self.speed, self.rect.center[1] + self.direction[1] * self.speed)
        self.speed = self.speed * 1.03


        for virus in viruses:
            if self.rect.colliderect(virus):
                virus.dead = True
                self.static = True
                return

        for tile in tiles:
            if self.rect.colliderect(tile):
                self.static = True
                return


    def render(self, canvas):
        canvas.blit(self.image, self.rect.topleft)