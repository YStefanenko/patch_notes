import pygame
from player import Player
from virus import Virus
import random
from bullet import Bullet
import math


class Level:
    def __init__(self, data):
        self.data = data

        self.player = Player(self.data['position'])

        self.viruses = []

        self.available_textures = [
            pygame.transform.scale(pygame.image.load('./assets/arrow up.png').convert_alpha(), (100, 100)),
            pygame.transform.scale(pygame.image.load('./assets/arrow down.png').convert_alpha(), (100, 100)),
            pygame.transform.scale(pygame.image.load('./assets/arrow right.png').convert_alpha(), (100, 100)),
            pygame.transform.scale(pygame.image.load('./assets/arrow left.png').convert_alpha(), (100, 100)),
            pygame.transform.scale(pygame.image.load('./assets/minus.png').convert_alpha(), (100, 100)),
            pygame.transform.scale(pygame.image.load('./assets/square.png').convert_alpha(), (100, 100)),
            pygame.transform.scale(pygame.image.load('./assets/X.png').convert_alpha(), (100, 100))
        ]

        tile_size = 100
        self.tiles = []
        self.tile_textures = []
        row_index = 0
        for row in self.data['level']:
            col_index = 0
            for tile in row:
                if tile == 1:
                    rect = pygame.Rect(col_index * tile_size, row_index * tile_size, tile_size, tile_size)
                    self.tiles.append(rect)
                    self.tile_textures.append(random.randint(0, len(self.available_textures) - 1))
                elif tile == 2:
                    self.viruses.append(Virus((col_index * tile_size, row_index * tile_size)))
                col_index += 1
            row_index += 1

        self.tiles.append(pygame.Rect((0, 900), (1600, 100)))
        self.tiles.append(pygame.Rect((0, -100), (1600, 100)))
        self.tiles.append(pygame.Rect((-100, 0), (100, 900)))
        self.tiles.append(pygame.Rect((1600, 0), (100, 900)))

        self.tile_textures.append(None)
        self.tile_textures.append(None)
        self.tile_textures.append(None)
        self.tile_textures.append(None)

        if 'platform' in self.data:
            self.tiles.append(pygame.Rect(self.data['platform']))
            self.tile_textures.append(None)

        self.surface = pygame.Surface((1600, 900), pygame.SRCALPHA)

        self.bullets = []

        self.complete = False

    def update(self, mouse):
        tiles = [virus.rect for virus in self.viruses] + self.tiles

        for i in range(len(self.viruses)):
            self.viruses[i].update(self.player.rect, tiles[:i] + tiles[i+1:])

        shoot = self.player.update(self.tiles, mouse)
        if shoot:
            mouse = (mouse[0] - self.player.rect.center[0] - self.player.gun_offset[0], mouse[1] - self.player.rect.center[1] - self.player.gun_offset[1])
            x, y = mouse
            length = math.sqrt(x ** 2 + y ** 2)
            if length == 0:
                direction = (0, 0)
            else:
                direction = (x / length, y / length)

            self.bullets.append(Bullet((self.player.rect.center[0] + self.player.gun_offset[0], self.player.rect.center[1] + self.player.gun_offset[1]), direction))

        for bullet in self.bullets:
            bullet.update(self.viruses, self.tiles)

        self.complete = True

        for virus in self.viruses:
            if not virus.dead:
                self.complete = False



    def render(self):
        self.surface.fill((0, 0, 0, 0))

        for tile, texture in zip(self.tiles, self.tile_textures):
            if texture is not None:
                self.surface.blit(self.available_textures[texture], tile)

        for virus in self.viruses:
            virus.render(self.surface)

        for bullet in self.bullets:
            bullet.render(self.surface)

        self.player.render(self.surface)


        return self.surface
