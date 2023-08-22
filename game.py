from obj import Obj, Star, Text
import random


class Game:

    def __init__(self):

        self.bg = Obj("assets/galax.jpg", 0, 0)
        self.bg2 = Obj("assets/galax.jpg", 0, -4000)


        self.lunar= Obj("assets/lu1.PNG", random.randrange(0,550),-200)
        self.asteroide = Obj("assets/ast1.PNG", random.randrange(0, 550), -50)
        self.flower = Obj("assets/florwer1.PNG", random.randrange(0, 550), -200)
        self.star = Star("assets/star1.png", 275, 450)
        self.star2 = Star("assets/star1.png", 275, 400)
        self.cubo = Obj("assets/cubo1.PNG", random.randrange(0, 550), -200)
        self.change_scene = False
        self.score = Text(120, "0")
        self.lifes = Text(60, "3")


    def draw(self, window):

        self.bg.draw(window)
        self.bg2.draw(window)
        self.cubo.draw(window)
        self.star.draw(window)
        self.asteroide.draw(window)
        self.flower.draw(window)
        self.lunar.draw(window)

        self.score.draw(window, 160, 50)
        self.lifes.draw(window, 50, 50)

    def update(self):

        self.move_bg()
        self.cubo.anim("cubo", 8, 5)
        self.asteroide.anim("ast", 8, 5)
        self.lunar.anim("lu",8,4)
        self.flower.anim("florwer", 5, 3)#("image", veloc img, quantidade de img)
        self.star.anim("star", 2, 3)
        self.move_cubo()
        self.move_lu()
        self.move_ast()
        self.move_flower()
        self.star.colision(self.asteroide.group, "ast")
        self.star.colision(self.flower.group, "Flower")
        self.gameover()
        self.score.update_text(str(self.star.pts))
        self.lifes.update_text(str(self.star.life))

    def move_bg(self):
        self.bg.sprite.rect[1] += 1 #(velocidade do objeto)
        self.bg2.sprite.rect[1] += 1

        if self.bg.sprite.rect[1] > 4000:
            self.bg.sprite.rect[1] = 0

        if self.bg2.sprite.rect[1] > 0:
            self.bg2.sprite.rect[1] = -4000

    def move_cubo(self):
        self.cubo.sprite.rect[1] += 1
        if self.cubo.sprite.rect[1] > 640:
            self.cubo = Obj("assets/cubo1.PNG", random.randrange(0,550), -200)

    def move_lu(self):
        self.lunar.sprite.rect[1] += 8
        if self.lunar.sprite.rect[1] > 640:
            self.lunar = Obj("assets/lu1.PNG", random.randrange(0, 550), -200)


    def move_ast(self):
        self.asteroide.sprite.rect[1] += 13

        if self.asteroide.sprite.rect[1] > 640:
            self.asteroide.sprite.kill()
            self.asteroide = Obj("assets/ast1.PNG", random.randrange(0, 550), -50)

    def move_flower(self):
        self.flower.sprite.rect[1] += 5
        if self.flower.sprite.rect[1] > 640:
            self.flower.sprite.kill()
            self.flower = Obj("assets/florwer1.png", random.randrange(0, 550), -200)

    def gameover(self):
        if self.star.life <= 0:
            self.change_scene = True
