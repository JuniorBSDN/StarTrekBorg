import pygame


class Obj:

    def __init__(self, image, x, y):

        self.group = pygame.sprite.Group()
        self.sprite = pygame.sprite.Sprite(self.group)

        self.sprite.image = pygame.image.load(image)
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect[0] = x
        self.sprite.rect[1] = y

        self.frame = 1
        self.tick = 0

    def draw(self, window):
        self.group.draw(window)

    def anim(self, image, tick, frames):
        self.tick += 1

        if self.tick == tick:
            self.tick = 0
            self.frame += 1

        if self.frame == frames:
            self.frame = 1

        self.sprite.image = pygame.image.load("assets/" + image + str(self.frame) + ".png")


class Star(Obj):

    def __init__(self, image, x, y):
        super().__init__(image, x, y)

        pygame.mixer.init() # iniciando o mixer
        self.sound_pts = pygame.mixer.Sound("assets/sounds/collect.wav")
        self.sound_block = pygame.mixer.Sound("assets/sounds/bateu.ogg")

        self.speed = 0
        self.acceleration = 0.4
        self.life = 3
        self.pts = 0


    def move_star(self, event):

        if event.type == pygame.MOUSEMOTION:
            self.sprite.rect[0] = pygame.mouse.get_pos()[0] - 35
            self.sprite.rect[1] = pygame.mouse.get_pos()[1] - 35




    def colision(self, group, name):

        name = name
        colison = pygame.sprite.spritecollide(self.sprite, group, True)

        if name == "Flower" and colison:
            self.pts += 1
            self.sound_pts.play()
        elif name == "ast" and colison:
            self.life -= 1
            self.sound_block.play()




    def colision(self, group, name):

        name = name
        colison = pygame.sprite.spritecollide(self.sprite, group, True)

        if name == "Flower" and colison:
            self.pts += 1
            self.sound_pts.play()
        elif name == "ast" and colison:
            self.life -= 1
            self.sound_block.play()


class Text:

    def __init__(self, size, text):

        self.font = pygame.font.SysFont("Arial bold", size)
        self.render = self.font.render(text, False, (255, 255, 255))

    def draw(self, window, x, y):
        window.blit(self.render, (x, y))

    def update_text(self, update):
        self.render = self.font.render(update, False, (255, 255, 255))
