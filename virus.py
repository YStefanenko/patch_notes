import pygame
import random


class Virus:
    def __init__(self, position):
        self.animation_frame = 0
        self.costumes = [
            pygame.transform.scale(pygame.image.load('./assets/virus1.png').convert_alpha(), (100, 99)),
            pygame.transform.scale(pygame.image.load('./assets/virus2.png').convert_alpha(), (100, 119)),
            pygame.transform.scale(pygame.image.load('./assets/virus3.png').convert_alpha(), (100, 134)),
        ]

        self.rect = self.costumes[1].get_bounding_rect()
        self.rect.topleft = position

        self.vx = 0
        self.vy = 0
        self.a = 1
        self.jump_power = -32
        self.on_ground = False

        self.dead = False

    def update(self, player_rect, tiles):
        if self.dead:
            return

        self.vy += 8
        if self.vy > 50:
            self.vy = 50

        self.on_ground = False
        for tile in tiles:
            if tile.colliderect(self.rect.x + self.vx, self.rect.y, self.rect.width, self.rect.height):
                if self.vx > 0:
                    self.vx = (tile.left - self.rect.width) - self.rect.x
                elif self.vx < 0:
                    self.vx = tile.right - self.rect.x

        self.rect.x += self.vx

        for tile in tiles:
            if tile.colliderect(self.rect.x, self.rect.y + self.vy, self.rect.width, self.rect.height):
                if self.vy > 0:
                    self.vy = (tile.top - self.rect.height) - self.rect.y
                    self.on_ground = True
                elif self.vy < 0:
                    self.vy = tile.bottom - self.rect.y

        self.rect.y += self.vy

        if player_rect.x < self.rect.x:
            self.vx -= self.a
            if self.vx < -10:
                self.vx = -10
        else:
            self.vx += self.a
            if self.vx > 10:
                self.vx = 10



    def render(self, surface):
        if self.dead:
            surface.blit(self.costumes[0], (self.rect.topleft[0], self.rect.topleft[1] + 134 - self.costumes[0].get_height()))

        else:
            costume = self.costumes[int(self.animation_frame / 3) % 3]
            surface.blit(costume, (self.rect.topleft[0], self.rect.topleft[1] + 134 - costume.get_height()))
            self.animation_frame += 1
