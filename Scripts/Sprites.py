import glob
import os
import random
import pygame
from pygame import *
from Scripts.init import *
from Scripts.dialogues import FANNY_DIALOGUES, get_pose_tier, get_dialogue_tier

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
    """9 paires de fond de partie (1.jpg..9.jpg / 1.png..9.png), un fond
    différent tous les BACKGROUND_SCORE_SEUIL points (score // seuil,
    plafonné à la dernière paire). Chaque `N.jpg` est la variante opaque
    (pas de webcam), chaque `N.png` a le trou ovale découpé exactement à
    l'emplacement où s'affiche le flux caméra (voir showcam()/draw_camring()
    dans main.py) -- les deux variantes d'un même numéro doivent rester
    visuellement identiques à part ce trou."""

    NUM_BACKGROUNDS = 9
    SCORE_SEUIL = 20

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.no_webcam_images = []
        self.webcam_images = []
        for i in range(1, self.NUM_BACKGROUNDS + 1):
            jpg = pygame.image.load(f'./assets/Images/Background/{i}.jpg')
            png = pygame.image.load(f'./assets/Images/Background/{i}.png')
            jpg = pygame.transform.scale(jpg, (LARGEUR_ECRAN, HAUTEUR_ECRAN))
            png = pygame.transform.scale(png, (LARGEUR_ECRAN, HAUTEUR_ECRAN))
            self.no_webcam_images.append(jpg)
            self.webcam_images.append(png)
        self.index = 0
        self.image = self.no_webcam_images[0]
        self.rect = self.image.get_rect()

    def index_for_score(self, score):
        return min(score // self.SCORE_SEUIL, self.NUM_BACKGROUNDS - 1)

    def update_for_score(self, score, webcam_compatibility):
        """À appeler chaque frame en jeu (gamestate==1) : choisit le fond
        correspondant au score, dans la variante webcam ou non."""
        self.index = self.index_for_score(score)
        self.image = self.webcam_images[self.index] if webcam_compatibility else self.no_webcam_images[self.index]

    def freeze_for_ending(self):
        """Écran de fin : toujours la variante SANS webcam (aucun flux
        caméra n'est dessiné dans le trou hors de gamestate==1), du fond
        qui était affiché au dernier coup de la manche."""
        self.image = self.no_webcam_images[self.index]

    def reset(self, webcam_compatibility):
        self.index = 0
        self.image = self.webcam_images[0] if webcam_compatibility else self.no_webcam_images[0]


def _load_frames(folder):
    all_files = glob.glob(f'./assets/Images/{folder}/*.png')
    files = sorted(
        (f for f in all_files if os.path.splitext(os.path.basename(f))[0].isdigit()),
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


class AnimationLoop(pygame.sprite.Sprite):
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


class FannySpinner(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        original = pygame.image.load('./assets/Images/fanny_10x10cm.png').convert_alpha()
        target_size = int(HAUTEUR_ECRAN * 0.22)
        self._original = pygame.transform.smoothscale(original, (target_size, target_size))
        self._angle = 0
        self.image = self._original
        self.rect = self.image.get_rect()

    def update(self, speed=2):
        self._angle = (self._angle - speed) % 360
        cx, cy = self.rect.center
        self.image = pygame.transform.rotate(self._original, self._angle)
        self.rect = self.image.get_rect(center=(cx, cy))

    def draw(self, surface, cx, cy):
        self.rect.center = (cx, cy)
        surface.blit(self.image, self.rect)


_dialogue_font = pygame.font.SysFont("Arial", max(14, round(HAUTEUR_ECRAN / 42)))
_BUBBLE_BG = (255, 255, 255, 235)
_BUBBLE_BORDER = (40, 40, 40)
_BUBBLE_TEXT = (20, 20, 20)
_BUBBLE_PADDING = 12


def _wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if font.size(candidate)[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def build_bubble_surface(text, width):
    """Construit la surface de la bulle de dialogue à une LARGEUR FIXE
    (indépendante du texte, pour que la position de Fanny ne bouge pas
    quand la réplique change) ; seule la hauteur varie selon le nombre de
    lignes. À appeler uniquement quand le texte change, pas à chaque frame."""
    available_width = width - 2 * _BUBBLE_PADDING
    lines = _wrap_text(text, _dialogue_font, available_width)
    line_surfaces = [_dialogue_font.render(line, True, _BUBBLE_TEXT) for line in lines]
    # Un mot isolé trop long pour available_width (résolutions très basses,
    # mots français longs) ne peut pas être coupé par _wrap_text : on le
    # réduit pour qu'il ne déborde jamais du cadre fixe de la bulle.
    for i, line_surf in enumerate(line_surfaces):
        if line_surf.get_width() > available_width:
            line_surfaces[i] = pygame.transform.smoothscale(
                line_surf, (available_width, line_surf.get_height())
            )
    line_height = _dialogue_font.get_linesize()
    height = line_height * len(line_surfaces) + 2 * _BUBBLE_PADDING

    bubble = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(bubble, _BUBBLE_BG, bubble.get_rect(), border_radius=14)
    pygame.draw.rect(bubble, _BUBBLE_BORDER, bubble.get_rect(), width=2, border_radius=14)
    for i, line_surf in enumerate(line_surfaces):
        bubble.blit(line_surf, (_BUBBLE_PADDING, _BUBBLE_PADDING + i * line_height))
    return bubble


class FannySpecialZero(pygame.sprite.Sprite):
    """Image spéciale "13-0" (tradition pétanque : l'équipe perdante embrasse
    la Fanny) : affichée à l'écran de fin de manche uniquement si le joueur
    termine à 0 point, avec sa réplique dédiée jouée une seule fois. La
    bulle de texte réutilise build_bubble_surface (retour à la ligne, cadre
    net) plutôt que la police néon du jeu, qui est trop large pour une
    phrase complète sans chevaucher HIGH SCORE/YOUR SCORE au centre."""

    TEXT = "Viens faire bisous et recommence."
    VOICE_PATH = './assets/Sounds/VoicesFanny/special_13_0.wav'

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        original = pygame.image.load('./assets/Images/FannySpecial13_0.png').convert_alpha()
        target_height = int(HAUTEUR_ECRAN * 0.55)
        w, h = original.get_rect().size
        ratio = target_height / h
        self.image = pygame.transform.smoothscale(original, (int(w * ratio), target_height))
        self.rect = self.image.get_rect()
        self.bubble_surface = build_bubble_surface(self.TEXT, self.rect.width)
        self.gap = int(HAUTEUR_ECRAN * 0.015)
        self._played = False

    def reset(self):
        self._played = False

    def draw(self, surface, cx, top_y):
        bubble_rect = self.bubble_surface.get_rect(midtop=(cx, top_y))
        surface.blit(self.bubble_surface, bubble_rect)
        self.rect.midtop = (cx, bubble_rect.bottom + self.gap)
        surface.blit(self.image, self.rect)
        if not self._played:
            self._played = True
            if os.path.isfile(self.VOICE_PATH):
                try:
                    channel4.play(pygame.mixer.Sound(self.VOICE_PATH))
                except pygame.error:
                    pass


class ShuffleBag:
    """Pioche des indices 0..n-1 sans répétition jusqu'à épuisement du sac,
    puis remélange et recommence. Garantit qu'une pose ou une réplique
    n'est jamais réutilisée avant que toutes les autres du même palier
    soient passées."""

    def __init__(self, size):
        self._size = size
        self._bag = []

    def draw(self):
        if not self._bag:
            self._bag = list(range(self._size))
            random.shuffle(self._bag)
        return self._bag.pop()

    def reset(self):
        self._bag = []


class FannyCompanion(pygame.sprite.Sprite):
    """Compagnon in-game de Fanny, ancré dans le coin supérieur gauche de
    l'écran : bulle de dialogue à gauche, personnage à droite de la bulle.
    La POSE change tous les 5 points (60 paliers, sur une grande partie de
    la banque d'images) tandis que le DIALOGUE change tous les 30 points
    (10 paliers de répliques) — les deux progressions sont volontairement
    découplées pour exploiter beaucoup plus d'images sans avoir à écrire
    des dizaines de répliques redondantes. La surface de la bulle et
    l'image du personnage ne sont recalculées que lorsque le texte/la pose
    changent réellement (pas à chaque frame) ; le dimensionnement (taille
    du sprite, largeur de bulle, marges) est proportionnel à
    LARGEUR_ECRAN/HAUTEUR_ECRAN, donc cohérent quelle que soit la
    résolution choisie dans config.ini (1920x1080, 1280x720, 640x360,
    426x240, ou 1024x768 par défaut)."""

    ENDING_INVITE_TEXT = "Retente ta chance, je ne demande que ça."
    ENDING_VOICE_PATH = './assets/Sounds/VoicesFanny/ending_invite.wav'

    def __init__(self, pose_max_tier=59, dialogue_max_tier=9):
        pygame.sprite.Sprite.__init__(self)
        self.pose_max_tier = pose_max_tier
        self.dialogue_max_tier = dialogue_max_tier
        self.gap = int(LARGEUR_ECRAN * 0.015)
        self.bubble_width = int(LARGEUR_ECRAN * 0.22)

        self.tier_images = {}
        self.pose_bags = {}
        target_height = int(HAUTEUR_ECRAN * 0.45)
        for tier in range(pose_max_tier + 1):
            folder = f'./assets/Images/FannyPoses/tier{tier}'
            files = sorted(glob.glob(f'{folder}/*.png'))
            images = []
            for f in files:
                img = pygame.image.load(f).convert_alpha()
                w, h = img.get_rect().size
                ratio = target_height / h
                images.append(pygame.transform.smoothscale(img, (int(w * ratio), target_height)))
            self.tier_images[tier] = images
            self.pose_bags[tier] = ShuffleBag(len(images))

        self.dialogue_bags = {}
        for tier, contexts in FANNY_DIALOGUES.items():
            for context, lines in contexts.items():
                self.dialogue_bags[(tier, context)] = ShuffleBag(len(lines))

        self.ending_bubble = build_bubble_surface(self.ENDING_INVITE_TEXT, self.bubble_width)
        self._ending_played = False

        self.reset()

    def _set_dialogue(self, tier, context, index):
        text = FANNY_DIALOGUES[tier][context][index]
        self.dialogue = text
        self.bubble_surface = build_bubble_surface(text, self.bubble_width)

        voice_path = f'./assets/Sounds/VoicesFanny/tier{tier}_{context}_{index}.wav'
        if os.path.isfile(voice_path):
            try:
                channel4.play(pygame.mixer.Sound(voice_path))
            except pygame.error:
                pass  # pas de voix générée pour cette réplique, on garde juste le texte

    def reset(self):
        self.pose_tier = 0
        self.dialogue_tier = 0
        self._ending_played = False
        for bag in self.pose_bags.values():
            bag.reset()
        for bag in self.dialogue_bags.values():
            bag.reset()

        pose_idx = self.pose_bags[0].draw()
        self.image = self.tier_images[0][pose_idx]
        self.rect = self.image.get_rect()

        intro_idx = self.dialogue_bags[(0, "intro")].draw()
        self._set_dialogue(0, "intro", intro_idx)

    def on_score_update(self, score):
        new_pose_tier = min(get_pose_tier(score), self.pose_max_tier)
        if new_pose_tier != self.pose_tier:
            self.pose_tier = new_pose_tier
            pose_idx = self.pose_bags[self.pose_tier].draw()
            self.image = self.tier_images[self.pose_tier][pose_idx]
            self.rect = self.image.get_rect()

        self.dialogue_tier = min(get_dialogue_tier(score), self.dialogue_max_tier)
        hit_idx = self.dialogue_bags[(self.dialogue_tier, "hit")].draw()
        self._set_dialogue(self.dialogue_tier, "hit", hit_idx)

    def draw(self, surface, right_x, y):
        """(right_x, y) est le coin supérieur DROIT du personnage, destiné
        à rester dans le coin supérieur droit de l'écran. La bulle de
        dialogue est placée à gauche du personnage (largeur fixe, donc le
        personnage ne bouge pas horizontalement quand le texte change)."""
        self.rect.topright = (right_x, y)
        bubble_x = self.rect.left - self.gap - self.bubble_width
        surface.blit(self.bubble_surface, (bubble_x, y))
        surface.blit(self.image, self.rect)

    def draw_ending(self, surface, cx, top_y):
        """Écran de fin de manche (score > 0) : affiche la dernière pose
        débloquée (self.image, déjà à jour depuis la partie) avec une
        invitation à retenter sa chance, dans une bulle au-dessus."""
        bubble_rect = self.ending_bubble.get_rect(midtop=(cx, top_y))
        surface.blit(self.ending_bubble, bubble_rect)
        self.rect.midtop = (cx, bubble_rect.bottom + self.gap)
        surface.blit(self.image, self.rect)
        if not self._ending_played:
            self._ending_played = True
            if os.path.isfile(self.ENDING_VOICE_PATH):
                try:
                    channel4.play(pygame.mixer.Sound(self.ENDING_VOICE_PATH))
                except pygame.error:
                    pass
