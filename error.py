import pygame
from level import Level
from levels import levels


class Error:
    def __init__(self, position, size, title, data):
        self.background = pygame.image.load('./assets/popup window 02.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (806, 498))

        font = pygame.font.SysFont(None, 64)
        self.title = font.render(title, True, (0, 0, 0))

        self.position = position
        self.size = size
        self.rect = pygame.Rect(self.position, self.size)
        self.close_button = pygame.Rect((self.position[0] + size[0] - 50, self.position[1]), (50, 50))
        self.top_bar = pygame.Rect((self.position[0], self.position[1]), (self.size[0], 50))

        self.level = Level(data)
        self.level_rect = pygame.Rect((self.position[0] + 10, self.position[1] + 65), (size[0] - 13, size[1] - 75))


    def update(self):
        self.level.update()


    def render(self, surface):
        surface.blit(self.background, self.position)
        surface.blit(self.title, (self.position[0] + 15, self.position[1] + 15))

        game_surface = pygame.transform.scale(self.level.render(), self.level_rect.size)
        surface.blit(game_surface, self.level_rect.topleft)
