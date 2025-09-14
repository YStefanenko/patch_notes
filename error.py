import pygame
from level import Level
from levels import levels
from sound import sound


class Error:
    def __init__(self, position, size, title, data):
        self.background = pygame.image.load('./assets/popup_window_02.png').convert_alpha()
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

        self.frame = 0

        sound.play_sound('error')


    def update(self, mouse):
        if self.frame > 60:
            size = self.level_rect.size
            mouse = ((mouse[0] - self.position[0] - 10) / size[0] * 1600, (mouse[1] - self.position[1] - 65) / size[1] * 900)

            self.level.update(mouse)



    def render(self, surface):
        surface.blit(self.background, self.position)
        surface.blit(self.title, (self.position[0] + 15, self.position[1] + 15))

        if self.frame > 60:
            game_surface = pygame.transform.scale(self.level.render(), self.level_rect.size)
            surface.blit(game_surface, self.level_rect.topleft)

        self.frame += 1
