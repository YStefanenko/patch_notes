import pygame
import time
import random
from levels import levels
from level import Level
from error import Error
from sound import sound


class Scene:
    def __init__(self):
        self.stage = 'browser'
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
                print(rect.width)
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
                print(rect.width)
                bubble = pygame.transform.scale(self.original_bubble, (bubble_size, 150))

                surface.blit(bubble, (self.main_level.player.rect.topleft[0] + 20, self.main_level.player.rect.topleft[1] - 120))

                surface.blit(text, rect)

        for error in self.errors:
            error.render(surface)
