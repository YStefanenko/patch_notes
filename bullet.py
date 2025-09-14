import pygame
import math
from sound import sound


class Bullet:
    def __init__(self, position, direction):
        self.image = pygame.image.load('./assets/mouse.png')
        self.image = pygame.transform.scale(self.image, (63, 39))
        self.direction = direction
        angle = math.degrees(math.atan2(direction[1], direction[0]))
        self.image = pygame.transform.rotate(self.image, -angle)

        self.rect = self.image.get_rect()
        self.visual_rect = self.image.get_rect()

        self.rect.center = position
        self.rect.size = (self.rect.size[0] * 0.5, self.rect.size[1] * 0.5)

        self.visual_rect.center = position

        self.speed = 30

        self.static = False
        sound.play_sound('gun')

    def update(self, viruses, tiles):
        if self.static:
            return
        self.rect.center = (self.rect.center[0] + self.direction[0] * self.speed, self.rect.center[1] + self.direction[1] * self.speed)
        self.visual_rect.center = self.rect.center
        self.speed = self.speed


        for virus in viruses:
            if not virus.dead:
                if self.rect.colliderect(virus):
                    virus.dead = True
                    sound.play_sound('deathv')

                    self.static = True
                    return

        for tile in tiles:
            if self.rect.colliderect(tile):
                self.static = True
                return


    def render(self, canvas):
        canvas.blit(self.image, self.visual_rect.topleft)