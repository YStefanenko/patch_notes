import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill('blue')
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vx = 0
        self.vy = 0
        self.a = 3
        self.jump_power = -64
        self.on_ground = False

    def update(self, tiles):
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_a]:
            self.vx -= self.a
            if self.vx < -20:
                self.vx = -20
        if keys[pygame.K_d]:
            self.vx += self.a
            if self.vx > 20:
                self.vx = 20
        self.vx = self.vx * 0.8

        # Apply gravity
        self.vy += 8
        if self.vy > 50:
            self.vy = 50

        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False

        # Collision detection
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


    def render(self, canvas):
        canvas.blit(self.image, self.rect.topleft)
