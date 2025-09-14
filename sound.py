import pygame
import random

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