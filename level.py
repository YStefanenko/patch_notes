import pygame
from player import Player


class Level:
    def __init__(self, data):
        self.player = Player(100, 100)

        tile_size = 100
        self.tiles = []
        row_index = 0
        for row in data:
            col_index = 0
            for tile in row:
                if tile == 1:
                    rect = pygame.Rect(col_index * tile_size, row_index * tile_size, tile_size, tile_size)
                    self.tiles.append(rect)
                col_index += 1
            row_index += 1

    def render(self):
        self.player.update(self.tiles)
        surface = pygame.Surface((1600, 900))

        for tile in self.tiles:
            pygame.draw.rect(surface, (0, 255, 0), tile)
        self.player.render(surface)

        return surface
