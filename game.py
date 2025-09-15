import pygame
import math
import random
import time
import asyncio



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

        self.fixed_text = pygame.transform.scale(pygame.image.load('./assets/fixed.png').convert_alpha(), (935, 265))
        self.dead_text = pygame.transform.scale(pygame.image.load('./assets/dead.png').convert_alpha(), (895, 265))


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

        self.surface = pygame.Surface((1600, 900), pygame.SRCALPHA)

        self.bullets = []

        self.complete = False
        self.complete_countdown = 0
        self.restart_countdown = 0

        self.static_target = False
        self.static_target_image = pygame.transform.scale(pygame.image.load('./assets/target.png').convert_alpha(), (150, 150))
        self.static_target_visual_rect = self.static_target_image.get_bounding_rect()
        self.static_target_rect = pygame.Rect((0, 0), (70, 70))




    def update(self, mouse):
        if self.complete_countdown:
            self.complete_countdown -= 1
            if self.complete_countdown == 0:
                self.complete = True

            self.player.update(self.tiles, mouse, self.viruses)

            return

        if self.restart_countdown:
            self.restart_countdown -= 1
            if self.restart_countdown == 0:
                self.__init__(self.data)

            return

        tiles = [virus.rect for virus in self.viruses] + self.tiles

        for i in range(len(self.viruses)):
            self.viruses[i].update(self.player.rect, tiles[:i] + tiles[i+1:])

        shoot = self.player.update(self.tiles, mouse, self.viruses)
        if self.player.dead:
            self.restart_countdown = 90

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

        for bullet in self.bullets:
            if self.static_target_rect.colliderect(bullet.rect):
                self.static_target = False

        complete = True

        for virus in self.viruses:
            if not virus.dead:
                complete = False
        if self.static_target:
            complete = False

        if complete:
            self.complete_countdown = 90


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

        if self.complete_countdown:
            self.surface.blit(self.fixed_text, (350, 318))
        elif self.restart_countdown:
            self.surface.blit(self.dead_text, (350, 318))

        if self.static_target:
            self.surface.blit(self.static_target_image, self.static_target_visual_rect)

        return self.surface


    def add_static_target(self, position):
        self.static_target_rect.center = position
        self.static_target_visual_rect.center = position
        self.static_target = True

levels = {
    'main': {
        'position': (400, 500),
        'level': [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
    },
    'first': {
        'position': (100, 800),
        'level': [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2],
        ]
    },
    'bin1': {
        'position': (100, 700),
        'level': [
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 0, 0],
        ]
    },
    'docs1': {
        'position': (100, 700),
        'level': [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 2, 0],
        ]
    },
    'docs2': {
        'position': (100, 700),
        'level': [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 1],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 2, 2, 2, 1],
        ]
    },
    'brow1': {
        'position': (100, 700),
        'level': [
            [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0],
            ]
    },
    'brow2': {
        'position': (100, 700),
        'level': [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
    },
    'comp1': {
        'position': (100, 700),
        'level': [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 2, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
        ]
    },
    'comp2': {
        'position': (100, 700),
        'level': [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 2, 2, 2, 0, 0, 0, 1, 2, 0, 1, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    },
    'comp3': {
        'position': (100, 700),
        'level': [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0],
        ]
    },
    'final': {
        'position': (100, 700),
        'level': [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2],
            [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 2, 2, 2, 2, 2],
            [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 2, 2, 2, 2, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2],
            [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2],
        ]
    },
}

class Player:
    def __init__(self, position):
        self.animation_frame = 0
        self.costumes = [
            pygame.transform.scale(pygame.image.load('./assets/idler.png').convert_alpha(), (112, 200)),
            pygame.transform.scale(pygame.image.load('./assets/idlel.png').convert_alpha(), (112, 200)),

            pygame.transform.scale(pygame.image.load('./assets/jumpr.png').convert_alpha(), (112, 200)),
            pygame.transform.scale(pygame.image.load('./assets/jumpl.png').convert_alpha(), (112, 200)),

            pygame.transform.scale(pygame.image.load('./assets/runr1.png').convert_alpha(), (112, 200)),
            pygame.transform.scale(pygame.image.load('./assets/runl1.png').convert_alpha(), (112, 200)),
            pygame.transform.scale(pygame.image.load('./assets/runr2.png').convert_alpha(), (112, 200)),
            pygame.transform.scale(pygame.image.load('./assets/runl2.png').convert_alpha(), (112, 200)),

        ]

        self.rect = self.costumes[0].get_bounding_rect()
        self.rect.topleft = position

        self.vx = 0
        self.vy = 0
        self.a = 10
        self.jump_power = -70
        self.on_ground = False

        self.reload = 0
        self.gun_direction = 0
        self.gun = pygame.transform.scale(pygame.image.load('./assets/gun.png').convert_alpha(), (80, 50))
        self.original_gun = self.gun
        self.gun_rect = self.gun.get_rect(center=self.rect.center)
        self.gun_offset = (40, 25)

        self.dead = False


    def update(self, tiles, mouse, viruses):
        if self.dead:
            return

        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_a]:
            self.vx -= self.a
            if self.vx < -30:
                self.vx = -30
            sound.play_sound('walk')

        if keys[pygame.K_d]:
            self.vx += self.a
            if self.vx > 30:
                self.vx = 30
            sound.play_sound('walk')

        self.vx = self.vx * 0.6

        # Apply gravity
        self.vy += 8
        if self.vy > 50:
            self.vy = 50

        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False
            sound.play_sound('jump')

        # Collision detection
        self.on_ground = False
        for tile in tiles:
            if tile.colliderect(self.rect.x + self.vx, self.rect.y, self.rect.width, self.rect.height):
                if self.vx > 0:
                    self.rect.x = tile.left - self.rect.width
                    self.vx = 0
                elif self.vx < 0:
                    self.rect.x = tile.right
                    self.vx = 0

        self.rect.x += self.vx

        for tile in tiles:
            if tile.colliderect(self.rect.x, self.rect.y + self.vy, self.rect.width, self.rect.height):
                if self.vy > 0:
                    self.rect.y = (tile.top - self.rect.height)
                    self.vy = 0
                    self.on_ground = True

                elif self.vy < 0:
                    self.rect.y = tile.bottom
                    self.vy = 0

        self.rect.y += self.vy

        if self.reload > 0:
            self.reload -= 1

        dx, dy = mouse[0] - self.rect.centerx, mouse[1] - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))

        if -90 < angle < 80:
            self.gun = pygame.transform.rotate(self.original_gun, angle)
        else:
            self.gun = pygame.transform.flip(self.original_gun, False, True)
            self.gun = pygame.transform.rotate(self.gun, angle)

        if self.vx < -2:
            self.gun_offset = (35, 25)
        else:
            self.gun_offset = (40, 25)

        self.gun_rect = self.gun.get_rect(center=(self.rect.center[0] + (self.gun_offset[0]), self.rect.center[1] + self.gun_offset[1]))

        # Shoot
        if keys[pygame.K_r] or pygame.mouse.get_pressed()[0]:
            if self.reload < 1:
                self.reload = 15
                return 1

        for virus in viruses:
            if self.rect.colliderect(virus.rect):
                self.dead = True
                sound.play_sound('deathp')


        if self.rect.x > 1600 or self.rect.x < 0 or self.rect.y > 900 or self.rect.y < 0:
            self.rect.x = 100
            self.rect.y = 700


        return 0


    def render(self, canvas):
        if self.vx < -2:
            if self.on_ground:
                costume = self.costumes[1 if self.animation_frame % 9 < 3 else 5 if self.animation_frame % 9 < 6 else 7]
            else:
                costume = self.costumes[3]

        elif self.vx > 2:
            if self.on_ground:
                costume = self.costumes[0 if self.animation_frame % 9 < 3 else 4 if self.animation_frame % 9 < 6 else 6]
            else:
                costume = self.costumes[2]

        else:
            if self.on_ground:
                if self.vx < 0:
                    costume = self.costumes[1]
                else:
                    costume = self.costumes[0]
            else:
                if self.vx < 0:
                    costume = self.costumes[3]
                else:
                    costume = self.costumes[2]


        canvas.blit(costume, self.rect.topleft)

        canvas.blit(self.gun, self.gun_rect)

        self.animation_frame += 1

class Scene:
    def __init__(self):
        self.stage = 'intro'
        self.stage_progression = ['intro', 'desktop1', 'desktop2', 'recycle_bin', 'desktop3', 'important_docs', 'desktop4', 'browser', 'desktop5', 'my_computer', 'system', 'win']
        self.frame = 0

        self.stage_text = {
            'desktop1': [
                'Oh no! A virus just attacked the PC...',
                'We need to fix this before it spreads!',
                'Use WAD and SPACE to move. Click...',
                "...or R to shoot. Don't touch the virus!",
            ],
            'desktop2': [
                "Let’s check the Recycle Bin. ",
                "Viruses love to hide there.",
                "Shoot the bin to continue",
            ],
            'desktop3': [
                "Huh, so the source wasn’t in the bin.",
                "Next stop… the Important Documents folder.",
                "If the virus got in there, we’re in real trouble.",
                "Shoot documents to continue",

            ],
            'desktop4': [
                "Documents folder secured.",
                "But I don’t think it ends there. ",
                "If I were a virus, I’d spread further...",
                "...let’s look into the Browser.",
                "Shoot the browser to continue",

            ],
            'desktop5': [
                "Browser’s cleaned up. Good. ",
                "That means the infection is deeper in the system. ",
                "Time to open up ‘My Computer’ and trace its roots.",
                "Shoot my computer to continue",

            ],
            'win': [
                "Nice, the computer is now clear!"
            ]

        }
        self.stage_font = pygame.font.SysFont("Comic Sans MS", 48)

        self.errors = []
        self.main_level = Level(levels['main'])
        self.main_level.add_static_target((-500, -500))

        self.background = pygame.image.load('./assets/desktop background.png').convert()
        self.background = pygame.transform.scale(self.background, (1600, 900))

        self.toolbar = pygame.image.load('./assets/toolbar.png').convert_alpha()
        self.toolbar = pygame.transform.scale(self.toolbar, (1600, 68))

        self.computer = pygame.image.load('./assets/my computer.png').convert_alpha()
        self.computer = pygame.transform.scale(self.computer, (106, 116))

        self.bin = pygame.image.load('./assets/recycle bin.png').convert_alpha()
        self.bin = pygame.transform.scale(self.bin, (80, 138))

        self.browser = pygame.image.load('./assets/web browser.png').convert_alpha()
        self.browser = pygame.transform.scale(self.browser, (73, 79))

        self.docs = pygame.image.load('./assets/important documents.png').convert_alpha()
        self.docs = pygame.transform.scale(self.docs, (89, 66))

        self.virus = pygame.image.load('./assets/virus.png').convert_alpha()
        self.virus = pygame.transform.scale(self.virus, (600, 600))
        font = pygame.font.SysFont(None, 150)
        self.virus_text = font.render('WARNING VIRUS FOUND!', True, (255, 40, 40))
        self.virus_text_rect = self.virus_text.get_rect(topleft=(120, 650))

        now = time.localtime()
        current_time = time.strftime("%H:%M", now)
        font = pygame.font.SysFont("Comic Sans MS", 48)
        self.time = font.render(current_time, True, (40, 40, 40))
        self.time_rect = self.time.get_rect(topleft=(1450, 832))

        self.original_bubble = pygame.image.load('./assets/speech_bubble.png').convert_alpha()
        self.original_bubble = pygame.transform.scale(self.original_bubble, (900, 150))


        self.bin_background = pygame.image.load('./assets/recycle_bin_background.png').convert()
        self.bin_background = pygame.transform.scale(self.bin_background, (1600, 900))

        self.docs_background = pygame.image.load('./assets/documents_background.png').convert()
        self.docs_background = pygame.transform.scale(self.docs_background, (1600, 900))

        self.browser_background = pygame.image.load('./assets/browser_background.png').convert()
        self.browser_background = pygame.transform.scale(self.browser_background, (1600, 900))

        self.computer_background = pygame.image.load('./assets/system32_background.png').convert()
        self.computer_background = pygame.transform.scale(self.computer_background, (1600, 900))

        self.intro = [pygame.transform.scale(pygame.image.load(f'./assets/vf{i+1}.png').convert(), (1600, 900)) for i in range(12)]


    def update(self, mouse):
        if self.errors:
            for error in self.errors:
                error.update(mouse)
                if error.level.complete:
                    self.errors.remove(error)

                if error.level.restart_countdown:
                    for error2 in self.errors:
                        if not error2.level.restart_countdown:
                            error2.level.restart_countdown = 90


        if self.stage == 'intro':
            if self.frame == 0:
                sound.set_music('menu')
            if self.frame > 238:
                self.stage = self.stage_progression[self.stage_progression.index(self.stage) + 1]
                self.frame = 0
                self.intro = None

        if self.stage == 'desktop1':
            if self.frame < 400:
                self.main_level.update(mouse)
            elif self.frame == 400:
                self.errors.append(Error((400, 100), (806, 498), 'ERROR', levels['first']))

            if self.frame > 400 and not self.errors:
                self.stage = self.stage_progression[self.stage_progression.index(self.stage) + 1]
                self.frame = 0

        if self.stage == 'desktop2':
            if self.frame == 0:
                sound.set_music('menu')
                self.main_level = Level(levels['main'])
                self.main_level.add_static_target((-100, -100))
            elif self.frame == len(self.stage_text[self.stage]) * 90 + 25:
                self.main_level.add_static_target((70, 330))

            self.main_level.update(mouse)

            if self.frame > 1 and self.main_level.complete_countdown:
                self.stage = self.stage_progression[self.stage_progression.index(self.stage) + 1]
                self.frame = 0

        if self.stage == 'recycle_bin':
            if self.frame == 0:
                sound.set_music('level')
            if self.frame == 30:
                self.errors.append(Error((100, 100), (806, 498), "FileNotFoundError", levels['bin1']))

            if self.frame > 30 and not self.errors:
                self.stage = self.stage_progression[self.stage_progression.index(self.stage) + 1]
                self.frame = 0

        if self.stage == 'desktop3':
            if self.frame == 0:
                sound.set_music('menu')
                self.main_level = Level(levels['main'])
                self.main_level.add_static_target((-100, -100))
            elif self.frame == len(self.stage_text[self.stage]) * 90 + 25:
                self.main_level.add_static_target((70, 592))

            self.main_level.update(mouse)

            if self.frame > 1 and self.main_level.complete_countdown:
                self.stage = self.stage_progression[self.stage_progression.index(self.stage) + 1]
                self.frame = 0

        if self.stage == 'important_docs':
            if self.frame == 0:
                sound.set_music('level')
            if self.frame == 30:
                self.errors.append(Error((200, 200), (806, 498), "AccessDeniedError", levels['docs1']))
            elif 30 < self.frame < 1000000:
                if not self.errors:
                    self.errors.append(Error((400, 300), (806, 498), 'CorruptFileError', levels['docs2']))
                    self.frame = 1000000

            if self.frame > 1000000 and not self.errors:
                self.stage = self.stage_progression[self.stage_progression.index(self.stage) + 1]
                self.frame = 0

        if self.stage == 'desktop4':
            if self.frame == 0:
                sound.set_music('menu')
                self.main_level = Level(levels['main'])
                self.main_level.add_static_target((-100, -100))
            elif self.frame == len(self.stage_text[self.stage]) * 90 + 25:
                self.main_level.add_static_target((70, 462))

            self.main_level.update(mouse)

            if self.frame > 1 and self.main_level.complete_countdown:
                self.stage = self.stage_progression[self.stage_progression.index(self.stage) + 1]
                self.frame = 0

        if self.stage == 'browser':
            if self.frame == 0:
                sound.set_music('level')
            if self.frame == 30:
                self.errors.append(Error((100, 100), (806, 498), "ProxyHijackError", levels['brow1']))
            elif self.frame == 90:
                self.errors.append(Error((600, 300), (806, 498), 'CookieOverflowError', levels['brow2']))

            if self.frame > 100 and not self.errors:
                self.stage = self.stage_progression[self.stage_progression.index(self.stage) + 1]
                self.frame = 0

        if self.stage == 'desktop5':
            if self.frame == 0:
                sound.set_music('menu')
                self.main_level = Level(levels['main'])
                self.main_level.add_static_target((-100, -100))
            elif self.frame == len(self.stage_text[self.stage]) * 90 + 25:
                self.main_level.add_static_target((70, 140))

            self.main_level.update(mouse)

            if self.frame > 1 and self.main_level.complete_countdown:
                self.stage = self.stage_progression[self.stage_progression.index(self.stage) + 1]
                self.frame = 0

        if self.stage == 'my_computer':
            if self.frame == 0:
                sound.set_music('boss')
            if self.frame == 30:
                self.errors.append(Error((200, 200), (806, 498), "KernelFaultException", levels['comp1']))
            elif self.frame == 100:
                self.errors.append(Error((600, 100), (806, 498), 'DriverCrashError', levels['comp2']))
            elif 100 < self.frame < 1000000:
                if len(self.errors) == 0:
                    self.errors.append(Error((300, 350), (806, 498), 'RegistryCorruptionError', levels['comp3']))
                    self.frame = 1000000

            if self.frame > 1000000 and not self.errors:
                self.stage = self.stage_progression[self.stage_progression.index(self.stage) + 1]
                self.frame = 0

        if self.stage == 'system':
            if self.frame == 0:
                self.main_level = Level(levels['final'])

            self.main_level.update(mouse)

            if self.frame > 1 and self.main_level.complete_countdown:
                self.stage = self.stage_progression[self.stage_progression.index(self.stage) + 1]
                self.frame = 0

        if self.stage == 'win':
            if self.frame == 0:
                self.main_level = Level(levels['main'])

            self.main_level.update(mouse)

        self.frame += 1




    def render(self, surface):
        if self.stage == 'intro':
            surface.blit(self.intro[int(self.frame/20)], (0, 0))

        if self.stage[:-1] == 'desktop':
            surface.blit(self.background, (0, 0))
            surface.blit(self.toolbar, (0, 832))
            surface.blit(self.computer, (25, 25))
            surface.blit(self.bin, (30, 178))
            surface.blit(self.browser, (40, 360))
            surface.blit(self.docs, (30, 490))
            surface.blit(self.time, self.time_rect)
            if self.errors:
                for error in self.errors:
                    error.render(surface)
            else:
                surface.blit(self.main_level.render(), (0, -66))

            if 30 < self.frame < len(self.stage_text[self.stage]) * 90 + 30:
                text = self.stage_font.render(self.stage_text[self.stage][int((self.frame - 30) / 90)][:min(self.frame - 30 - int((self.frame - 30) / 90) * 90, len(self.stage_text[self.stage][int((self.frame - 30) / 90)]))], True, (0, 0, 0))
                rect = text.get_rect(topleft=(self.main_level.player.rect.topleft[0] + 40, self.main_level.player.rect.topleft[1] - 110))

                bubble_size = max(rect.width, 600) + 30
                bubble = pygame.transform.scale(self.original_bubble, (bubble_size, 150))

                surface.blit(bubble, (self.main_level.player.rect.topleft[0] + 20, self.main_level.player.rect.topleft[1] - 120))

                surface.blit(text, rect)


        elif self.stage == 'recycle_bin':
            surface.blit(self.bin_background, (0, 0))
        elif self.stage == 'important_docs':
            surface.blit(self.docs_background, (0, 0))
        elif self.stage == 'browser':
            surface.blit(self.browser_background, (0, 0))
        elif self.stage == 'my_computer':
            surface.blit(self.computer_background, (0, 0))

        elif self.stage == 'system':
            surface.blit(self.background, (0, 0))
            surface.blit(self.toolbar, (0, 832))
            surface.blit(self.computer, (25, 25))
            surface.blit(self.bin, (30, 178))
            surface.blit(self.browser, (40, 360))
            surface.blit(self.docs, (30, 490))
            surface.blit(self.time, self.time_rect)
            if self.errors:
                for error in self.errors:
                    error.render(surface)
            else:
                surface.blit(self.main_level.render(), (0, -66))

        elif self.stage == 'win':
            surface.blit(self.background, (0, 0))
            surface.blit(self.toolbar, (0, 832))
            surface.blit(self.computer, (25, 25))
            surface.blit(self.bin, (30, 178))
            surface.blit(self.browser, (40, 360))
            surface.blit(self.docs, (30, 490))
            surface.blit(self.time, self.time_rect)
            if self.errors:
                for error in self.errors:
                    error.render(surface)
            else:
                surface.blit(self.main_level.render(), (0, -66))

            if 30 < self.frame < len(self.stage_text[self.stage]) * 90 + 30:
                text = self.stage_font.render(self.stage_text[self.stage][int((self.frame - 30) / 90)][:min(self.frame - 30 - int((self.frame - 30) / 90) * 90, len(self.stage_text[self.stage][int((self.frame - 30) / 90)]))], True, (0, 0, 0))
                rect = text.get_rect(topleft=(self.main_level.player.rect.topleft[0] + 40, self.main_level.player.rect.topleft[1] - 110))

                bubble_size = max(rect.width, 600) + 30
                bubble = pygame.transform.scale(self.original_bubble, (bubble_size, 150))

                surface.blit(bubble, (self.main_level.player.rect.topleft[0] + 20, self.main_level.player.rect.topleft[1] - 120))

                surface.blit(text, rect)

        for error in self.errors:
            error.render(surface)

pygame.mixer.init()


class SoundManager:
    def __init__(self):
        self.music_intro = None
        self.music_loop = None
        self.music_playing = False
        self.sounds = {'walk1': pygame.mixer.Sound('./assets/walk-1.ogg'),
                       'walk2': pygame.mixer.Sound('./assets/walk-2.ogg'),
                       'walk3': pygame.mixer.Sound('./assets/walk-3.ogg'),
                       'walk4': pygame.mixer.Sound('./assets/walk-4.ogg'),
                       'walk5': pygame.mixer.Sound('./assets/walk-5.ogg'),
                       'walk6': pygame.mixer.Sound('./assets/walk-6.ogg'),
                       'walk7': pygame.mixer.Sound('./assets/walk-7.ogg'),
                       'walk8': pygame.mixer.Sound('./assets/walk-8.ogg'),
                       'walk9': pygame.mixer.Sound('./assets/walk-9.ogg'),
                       'walk10': pygame.mixer.Sound('./assets/walk-10.ogg'),
                       'deathp': pygame.mixer.Sound('./assets/player-death.ogg'),
                       'deathv': pygame.mixer.Sound('./assets/enemy-death.ogg'),
                       'error1': pygame.mixer.Sound('./assets/error-1.ogg'),
                       'error2': pygame.mixer.Sound('./assets/error-2.ogg'),
                       'error3': pygame.mixer.Sound('./assets/error-3.ogg'),
                       'error4': pygame.mixer.Sound('./assets/error-4.ogg'),
                       'gun1': pygame.mixer.Sound('./assets/gunV2-1.ogg'),
                       'gun2': pygame.mixer.Sound('./assets/gunV2-2.ogg'),
                       'gun3': pygame.mixer.Sound('./assets/gunV2-3.ogg'),
                       'jump': pygame.mixer.Sound('./assets/jump-1.ogg'),

                       }
        self.MUSIC_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.MUSIC_END)



    def play_sound(self, name):
        if name == 'walk':
            self.sounds[name + str(random.randint(1, 10))].play()
        elif name == 'error':
            self.sounds[name + str(random.randint(1, 4))].play()
        elif name == 'gun':
            self.sounds[name + str(random.randint(1, 3))].play()
        else:
            self.sounds[name].play()


    def handle_event(self, event):
        if event.type == self.MUSIC_END and self.music_loop:
            # Switch to loop forever
            pygame.mixer.music.load(self.music_loop)
            pygame.mixer.music.play(-1)  # loop infinitely

    def set_music(self, type):
        if type == 'menu':
            intro_path = './assets/menu-music-INTRO.ogg'
            loop_path = './assets/menu-music-LOOP.ogg'
        elif type == 'level':
            intro_path = './assets/level-1-INTRO.ogg'
            loop_path = './assets/level-1-LOOP.ogg'
        else:
            intro_path = './assets/boss-music-INTRO.ogg'
            loop_path = './assets/boss-music-LOOP.ogg'

        self.music_intro = intro_path
        self.music_loop = loop_path
        self.music_playing = True

        pygame.mixer.music.load(self.music_intro)
        pygame.mixer.music.play()

        pygame.mixer.music.queue(self.music_loop)

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False

    def is_music_playing(self):
        return pygame.mixer.music.get_busy()


sound = SoundManager()


class Virus:
    def __init__(self, position):
        self.animation_frame = 0
        self.costumes = [
            pygame.transform.scale(pygame.image.load('./assets/virus1.png').convert_alpha(), (100, 99)),
            pygame.transform.scale(pygame.image.load('./assets/virus2.png').convert_alpha(), (100, 119)),
            pygame.transform.scale(pygame.image.load('./assets/virus3.png').convert_alpha(), (100, 134)),
        ]

        self.rect = self.costumes[0].get_bounding_rect()
        self.rect.topleft = position
        self.rect.size = (self.rect.size[0] * 0.5, self.rect.size[1])

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
            surface.blit(self.costumes[0], (self.rect.topleft[0], self.rect.topleft[1] + 105 - self.costumes[0].get_height()))

        else:
            costume = self.costumes[int(self.animation_frame / 3) % 3]
            surface.blit(costume, (self.rect.topleft[0], self.rect.topleft[1] + 105 - costume.get_height()))
            self.animation_frame += 1



def print_virt_surf(screen, virt_surf):
    screen.blit(pygame.transform.scale(virt_surf, (new_w, new_h)), (x_offset, y_offset))
    return new_w, new_h, x_offset, y_offset


def convert_mouse(mouse):
    mx, my = mouse
    mx -= x_offset
    my -= y_offset
    virt_x = int(mx / new_w * 1600)
    virt_y = int(my / new_h * 900)
    return virt_x, virt_y


pygame.init()

fps = 30

info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
virt_surf = pygame.Surface((1600, 900))

scale = min(width / 1600, height / 900)
new_w, new_h = int(1600 * scale), int(900 * scale)
x_offset = (width - new_w) // 2
y_offset = (height - new_h) // 2

clock = pygame.time.Clock()

async def main():
    scene = Scene()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            sound.handle_event(event)

        scene.update(convert_mouse(pygame.mouse.get_pos()))
        scene.render(virt_surf)

        print_virt_surf(screen, virt_surf)

        pygame.display.flip()
        clock.tick(fps)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
