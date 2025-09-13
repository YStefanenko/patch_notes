import pygame
from player import Player


class Level:
    def __init__(self, data):
        self.player = Player(data['position'])

        tile_size = 100
        self.platforms = []
        for platform in data['platforms']:
            rect = pygame.Rect(platform[0][0], platform[0][1], platform[1][0], platform[1][1])
            self.platforms.append(rect)

        self.surface = pygame.Surface((1600, 900))
        self.surface.convert_alpha(self.surface)

    def update(self):
        self.player.update(self.platforms)


    def render(self):
        self.surface.fill((215, 231, 211))

        for tile in self.platforms:
            pygame.draw.rect(self.surface, (147, 117, 136), tile)

        self.player.render(self.surface)

        return self.surface
