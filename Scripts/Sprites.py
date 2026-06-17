import glob
import os
import pygame
from pygame import *
from Scripts.init import *

class ArducibleLogo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./assets/Images/Arducible.png')
        self.img_width, self.img_height = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, (self.img_width*LARGEUR_ECRAN/1920, self.img_height*HAUTEUR_ECRAN/1080))


class Cible(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images.append(pygame.image.load('./assets/Images/Boule.png'))
        self.images.append(pygame.image.load('./assets/Images/BouleG.png'))
        self.images.append(pygame.image.load('./assets/Images/BouleGold.png'))
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i], (LARGEUR_ECRAN*0.25, HAUTEUR_ECRAN*0.44))
        self.image = self.images[0]
        self.rect = self.image.get_rect()


class ColoredRing(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images.append(pygame.image.load('./assets/Images/Background/redring.png'))
        self.images.append(pygame.image.load('./assets/Images/Background/greenring.png'))
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i], (258 * LARGEUR_ECRAN/1920, 395 * HAUTEUR_ECRAN/1080))
        self.image = self.images[0]
        self.rect = self.image.get_rect()


class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images.append(pygame.image.load('./assets/Images/Background/1.jpg'))
        self.images.append(pygame.image.load('./assets/Images/Background/1.png'))
        self.images.append(pygame.image.load('./assets/Images/Background/2.jpg'))
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i], (LARGEUR_ECRAN, HAUTEUR_ECRAN))
        self.image = self.images[0]
        self.rect = self.image.get_rect()


def _load_frames(folder):
    files = sorted(
        glob.glob(f'./assets/Images/{folder}/*.png'),
        key=lambda f: int(os.path.splitext(os.path.basename(f))[0])
    )
    return [pygame.image.load(f) for f in files]


class BackgroundFrame(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = _load_frames('frame')
        self.index = 0
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i], (LARGEUR_ECRAN, HAUTEUR_ECRAN))
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.increaseindex = True

    def update(self):
        if self.index >= len(self.images) - 1:
            self.increaseindex = False
        if self.index <= 0:
            self.increaseindex = True
        if self.increaseindex:
            self.index += 1
        else:
            self.index -= 1
        self.image = self.images[self.index]


class _AnimationLoop(pygame.sprite.Sprite):
    FPS = 10

    def __init__(self, folder):
        pygame.sprite.Sprite.__init__(self)
        self.images = _load_frames(folder)
        self.index = 0
        self.last_tick = pygame.time.get_ticks()
        self.img_width, self.img_height = self.images[0].get_rect().size
        self.res_img_width = self.img_width * LARGEUR_ECRAN / 1920 / 2
        self.res_img_height = self.img_height * HAUTEUR_ECRAN / 1080 / 2
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i], (self.res_img_width, self.res_img_height))
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_tick >= 1000 // self.FPS:
            self.last_tick = now
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]


class AnimationFrame1(_AnimationLoop):
    def __init__(self):
        super().__init__('vid1')

class AnimationFrame2(_AnimationLoop):
    def __init__(self):
        super().__init__('vid2')

class AnimationFrame3(_AnimationLoop):
    def __init__(self):
        super().__init__('vid3')

class AnimationFrame4(_AnimationLoop):
    def __init__(self):
        super().__init__('vid4')


class Anim1(pygame.sprite.Sprite):
    FRAME_DURATION = 1000 // 24  # ms par frame à 24 FPS

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        extensions = ('*.png', '*.jpg', '*.jpeg')
        files = sorted(f for ext in extensions for f in glob.glob(f'./assets/Images/anim1/{ext}'))
        self.images = [pygame.image.load(f) for f in files]
        self.index = 0
        self.last_tick = pygame.time.get_ticks()
        img_w, img_h = self.images[0].get_rect().size
        target_h = int(HAUTEUR_ECRAN * 0.4)
        target_w = int(img_w * target_h / img_h)
        self.anim_width = target_w
        self.anim_height = target_h
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i], (target_w, target_h))
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_tick >= self.FRAME_DURATION:
            self.last_tick = now
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]


class Anim1Flipped(Anim1):
    def __init__(self):
        super().__init__()
        self.images = [pygame.transform.flip(img, True, False) for img in self.images]
        self.image = self.images[self.index]
