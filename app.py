import pygame
from scene import Scene
import random
import time


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

scene = Scene()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    scene.update()
    scene.render(virt_surf)

    print_virt_surf(screen, virt_surf)

    pygame.display.flip()
    clock.tick(fps)
    print("FPS:", int(clock.get_fps()))

pygame.quit()
