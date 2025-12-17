# obj.py (VERSÃO FINAL com correção de movimento)
import pygame
import random
import math
import os
import sys

def resource_path(relative_path):
    """Obtém o caminho absoluto para o recurso."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# --- Configurações Básicas ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.mixer.init()


# ==============================================================================
# CLASSES BASE DO SEU PROJETO
# ==============================================================================

class Obj(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, window):
        window.blit(self.image, self.rect)

    # Adicionado para compatibilidade com o .update() do all_sprites.group
    def update(self, **kwargs):
        pass

    def anim(self, name, max_frames, speed):
        pass


class Text:
    def __init__(self, size, text, color=(255, 255, 255)):
        pygame.font.init()
        self.font = pygame.font.Font(None, size)
        self.color = color
        self.text = text
        self.surface = self.font.render(self.text, True, self.color)

    def draw(self, window, x, y):
        window.blit(self.surface, (x, y))

    def update_text(self, new_text):
        self.text = new_text
        self.surface = self.font.render(self.text, True, self.color)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([5, 15])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -15

    def update(self, **kwargs):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


class Star(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10
        self.pts = 0
        self.life = 5
        self.fire_rate = 200
        self.last_shot_time = pygame.time.get_ticks()

        # CORREÇÃO CRÍTICA: Manter o try/except para evitar crash de som
        try:
            self.sound_block = pygame.mixer.Sound(resource_path("assets/sounds/explosion.mp3"))
            self.sound_pts = pygame.mixer.Sound(resource_path("assets/sounds/collect.wav"))
        except pygame.error:
            print("AVISO: Arquivos de som 'block.ogg' ou 'point.ogg' não encontrados.")
            self.sound_block = None
            self.sound_pts = None

    def draw(self, window):
        window.blit(self.image, self.rect)

    def anim(self, name, max_frames, speed):
        pass

    def update(self, game_manager, **kwargs):
        keys = pygame.key.get_pressed()

        # CORREÇÃO: Adicionando controle vertical
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Sincronização de Vidas
        self.life = game_manager.player_lives

        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def take_damage(self, damage, game_manager):
        """Lida com o dano e notifica o Game Manager."""
        game_manager.player_hit(damage)
        if self.sound_block:
            self.sound_block.play()


# --- INIMIGOS E PROJÉTEIS (Sem Alteração) ---

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=7, damage=1):
        super().__init__()
        self.image = pygame.Surface([5, 15])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.damage = damage

    def update(self, game_manager, **kwargs):
        self.rect.y += game_manager.get_effective_speed(self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path, speed, shoot_rate=2500):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(random.randint(50, SCREEN_WIDTH - 50), -50))
        self.speed = speed
        self.shoot_rate = shoot_rate
        self.last_shot_time = pygame.time.get_ticks()

    def update(self, game_manager, all_sprites, enemy_bullets, **kwargs):
        self.rect.y += game_manager.get_effective_speed(self.speed)

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_rate:
            if random.random() < 0.7:
                self.fire_bullet(all_sprites, enemy_bullets)
            self.last_shot_time = current_time

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def fire_bullet(self, all_sprites, enemy_bullets):
        new_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(new_bullet)
        enemy_bullets.add(new_bullet)


class Lunar(Enemy):
    def __init__(self):
        super().__init__(resource_path("assets/lu1.PNG"), speed=8)


class Asteroide(Enemy):
    def __init__(self):
        super().__init__(resource_path("assets/ast1.PNG"), speed=13)


class Cubo(Enemy):
    def __init__(self):
        super().__init__(resource_path("assets/cubo1.PNG"), speed=1)


class Flower(Obj):
    def __init__(self):
        super().__init__(resource_path("assets/florwer1.PNG"), random.randrange(0, 550), -200)