import pygame
import math
from sound import sound


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
