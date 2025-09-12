import pygame
from error_window import ErrorWindow
from level import Level
from levels import levels
from player import Player


def print_virt_surf(screen, virt_surf):
    # Calculate best-fit scale factor
    scale = min(width / 1600, height / 900)
    new_w, new_h = int(1600 * scale), int(900 * scale)

    # Center in the screen (black bars if needed)
    x_offset = (width - new_w) // 2
    y_offset = (height - new_h) // 2

    screen.blit(pygame.transform.scale(virt_surf, (new_w, new_h)), (x_offset, y_offset))
    return new_w, new_h, x_offset, y_offset


pygame.init()

fps = 30

info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
virt_surf = pygame.Surface((1600, 900))

clock = pygame.time.Clock()

error = ErrorWindow((500, 200), (800, 500))
level = Level(levels[0])
background = pygame.image.load('./assets/background.jpg')
background = pygame.transform.scale(background, (1600, 900))

running = True
while running:
    virt_surf.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    error.render(virt_surf)
    print_virt_surf(screen, virt_surf)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
