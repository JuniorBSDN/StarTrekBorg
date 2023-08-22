import pygame
from menu import Menu, GameOver
from game import Game


class Main:

    def __init__(self):

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/deep.wav")
        pygame.mixer.music.play(-1)

        self.window = pygame.display.set_mode([600, 640])
        self.title = pygame.display.set_caption("Space is DEEP")
        self.loop = True
        self.fps = pygame.time.Clock()
        self.tema = pygame.mixer.Sound("assets/sounds/deep.wav")
        self.start_screen = Menu("assets/inicio1.png")
        self.game = Game()
        self.gameover = GameOver("assets/over.png")
        self.tiro = pygame.mixer.Sound("assets/sounds/tiro.wav")

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop = False

            if not self.start_screen.change_scene:
                self.start_screen.event(event)

            elif not self.game.change_scene:
                self.game.star.move_star(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.tiro.play()


            else:
                self.gameover.event(event)

    def draw(self):
        self.window.fill([0, 0, 0])
        if not self.start_screen.change_scene:
            self.start_screen.draw(self.window)

        elif not self.game.change_scene:
            self.game.draw(self.window)
            self.game.update()
        elif not self.gameover.change_scene:
            self.gameover.draw(self.window)
        else:
            self.start_screen.change_scene = False
            self.game.change_scene = False
            self.gameover.change_scene = False
            self.game.star.life = 3
            self.game.star.pts = 0

    def updates(self):

        while self.loop:
            self.fps.tick(30)
            self.draw()
            self.events()
            pygame.display.update()


Main().updates()
