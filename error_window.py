import pygame
from level import Level
from levels import levels


class ErrorWindow:
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.rect = pygame.Rect(self.position, self.size)
        self.close_button = pygame.Rect((self.position[0] + size[0] - 50, self.position[1]), (50, 50))
        self.top_bar = pygame.Rect((self.position[0], self.position[1]), (self.size[0], 50))

        self.level = Level(levels[0])
        self.level_rect = pygame.Rect((self.position[0], self.position[1] + 50), (size[0], size[1] - 50))



    def render(self, canvas):
        pygame.draw.rect(canvas, (255, 255, 255), self.rect)
        pygame.draw.rect(canvas, (0, 0, 255), self.top_bar)
        pygame.draw.rect(canvas, (255, 0, 0), self.close_button)

        game_surface = pygame.transform.scale(self.level.render(), self.level_rect.size)
        canvas.blit(game_surface, self.level_rect.topleft)
