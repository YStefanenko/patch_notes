import pygame
import time
import random
from levels import levels
from level import Level
from error import Error


class Scene:
    def __init__(self):
        self.stage = 'desktop2'
        self.stage_progression = ['intro', 'desktop1', 'desktop2', 'recycle_bin', 'desktop3', 'important_docs', 'desktop4', 'browser', 'desktop5', 'my_computer', 'system']
        self.frame = 0

        self.stage_text = {
            'desktop1': [
                'Oh no! A virus just attacked the PC...',
                'We need to fix this before it spreads!',
                'Use WAD and SPACE to move.',
                "Click to shoot. Don't touch the virus!",
            ]
        }
        self.stage_font = pygame.font.SysFont("Comic Sans MS", 48)

        self.errors = []
        self.main_level = Level(levels['main'])

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

        self.bubble = pygame.image.load('./assets/speech_bubble.png').convert_alpha()
        self.bubble = pygame.transform.scale(self.bubble, (900, 150))


        self.bin_background = pygame.image.load('./assets/recycle bin.png').convert()
        self.bin_background = pygame.transform.scale(self.bin_background, (1600, 900))

        self.docs_background = pygame.image.load('./assets/important documents.png').convert()
        self.docs_background = pygame.transform.scale(self.docs_background, (1600, 900))

        self.browser_background = pygame.image.load('./assets/web browser.png').convert()
        self.browser_background = pygame.transform.scale(self.browser_background, (1600, 900))

        self.computer_background = pygame.image.load('./assets/my computer.png').convert()
        self.computer_background = pygame.transform.scale(self.computer_background, (1600, 900))


    def update(self, mouse):
        self.frame += 1

        if self.stage == 'intro':
            if self.frame > 300:
                self.stage = self.stage_progression[self.stage_progression.index(self.stage) + 1]
                self.frame = 0

        elif self.stage == 'desktop1':
            if self.frame < 400:
                self.main_level.update(mouse)
            elif self.frame == 400:
                self.errors.append(Error((400, 100), (806, 498), 'File Not Found Error', levels['first']))
            elif self.frame > 430:
                self.errors[0].update(mouse)
                if self.errors[0].complete:
                    del self.errors[0]

            if self.frame > 400 and not self.errors:
                self.stage = self.stage_progression[self.stage_progression.index(self.stage) + 1]
                self.frame = 0

        elif self.stage == 'desktop2':
            if self.errors:
                for error in self.errors:
                    error.update(mouse)
                    if error.complete:
                        self.errors.remove(error)
            else:
                self.main_level.update(mouse)

            if self.frame == 1:
                self.errors.append(Error((400, 100), (806, 498), 'File Not Found Error', levels['first']))

            if self.frame > 1 and not self.errors:
                self.stage = self.stage_progression[self.stage_progression.index(self.stage) + 1]
                self.frame = 0

        elif self.stage == 'recycle_bin':
            for error in self.errors:
                error.update(mouse)

            if self.frame == 20:
                self.errors.append(Error((100, 100), (806, 498), "No Such File", levels['bin1']))
            elif self.frame == 100:
                self.errors.append(Error((700, 400), (806, 498), 'File Absent', levels['bin2']))

            if self.frame > 400:
                self.stage = self.stage_progression[self.stage_progression.index(self.stage) + 1]
                self.frame = 0


        elif self.stage == 'important_docs':
            for error in self.errors:
                error.update(mouse)

            if self.frame == 20:
                self.errors.append(Error((200, 200), (806, 498), "No Such File", levels['bin1']))
            elif self.frame == 100:
                self.errors.append(Error((400, 300), (806, 498), 'File Absent', levels['bin2']))

            if self.frame > 400:
                self.stage = self.stage_progression[self.stage_progression.index(self.stage) + 1]
                self.frame = 0


        elif self.stage == 'browser':
            for error in self.errors:
                error.update()

            if self.frame == 20:
                self.errors.append(Error((200, 200), (806, 498), "No Such File", levels['bin1']))
            elif self.frame == 100:
                self.errors.append(Error((400, 300), (806, 498), 'File Absent', levels['bin2']))

            if self.frame > 400:
                self.stage = self.stage_progression[self.stage_progression.index(self.stage) + 1]
                self.frame = 0


        elif self.stage == 'my_computer':
            for error in self.errors:
                error.update()

            if self.frame == 20:
                self.errors.append(Error((200, 200), (806, 498), "No Such File", levels['bin1']))
            elif self.frame == 100:
                self.errors.append(Error((400, 300), (806, 498), 'File Absent', levels['bin2']))

            if self.frame > 400:
                self.stage = self.stage_progression[self.stage_progression.index(self.stage) + 1]
                self.frame = 0



    def render(self, surface):
        if self.stage == 'intro':
            if self.frame < 150 or (int(self.frame / 7) % 2 and self.frame < 230):
                surface.blit(self.background, (0, 0))
                surface.blit(self.toolbar, (0, 832))
                surface.blit(self.computer, (25, 25))
                surface.blit(self.bin, (30, 178))
                surface.blit(self.browser, (40, 360))
                surface.blit(self.docs, (30, 490))
                surface.blit(self.time, self.time_rect)

                if int(self.frame / 30) % 2 and self.frame < 150:
                    surface.blit(self.virus, (500, 50))
                surface.blit(self.virus_text, self.virus_text_rect)

            else:
                surface.fill('black')

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
                self.main_level.player.render(surface)


        if self.stage == 'desktop1':
            if 30 < self.frame < 390:
                text = self.stage_font.render(self.stage_text['desktop1'][int((self.frame - 30) / 90)], True, (0, 0, 0))
                rect = self.time.get_rect(topleft=(self.main_level.player.rect.topleft[0] + 40, self.main_level.player.rect.topleft[1] - 110))

                surface.blit(self.bubble, (self.main_level.player.rect.topleft[0] + 20, self.main_level.player.rect.topleft[1] - 120))

                surface.blit(text, rect)

        elif self.stage == 'recycle_bin':
            surface.blit(self.bin_background, (0, 0))
            for error in self.errors:
                error.render(surface)
        elif self.stage == 'important_docs':
            surface.blit(self.docs_background, (0, 0))
            for error in self.errors:
                error.render(surface)
        elif self.stage == 'browser':
            surface.blit(self.browser_background, (0, 0))
            for error in self.errors:
                error.render(surface)
        elif self.stage == 'my_computer':
            surface.blit(self.computer_background, (0, 0))
            for error in self.errors:
                error.render(surface)





