from obj import Obj, Star, Text, Bullet, Lunar, Asteroide, Cubo, Flower, EnemyBullet
from game_manager import GameController
import random
import pygame
import sys
import os

def resource_path(relative_path):
    """Obtém o caminho absoluto para o recurso."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Game:

    def __init__(self):
        # Inicializa o Game Controller
        self.game_manager = GameController(initial_lives=5)

        # Inicialização de objetos e Background
        self.bg = Obj(resource_path("assets/galax.jpg"), 0, 0)
        self.bg2 = Obj(resource_path("assets/galax.jpg"), 0, -4000)
        self.star = Star(resource_path("assets/star1.png"), 275, 450)

        self.change_scene = False
        self.score = Text(120, "0")
        self.lifes = Text(60, "5")

        # --- GRUPOS DE SPRITES ---
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.collectables = pygame.sprite.Group()

        self.all_sprites.add(self.star)
        self.flower = Flower()
        self.all_sprites.add(self.flower)
        self.collectables.add(self.flower)

        # Controle de Spawn
        self.spawn_time = pygame.time.get_ticks()
        self.initial_spawn_rate = 1500

        # --- Lógica de Carregamento de Sons (Existente e NOVO) ---
        self.sound_shot = None
        try:
            self.sound_shot = pygame.mixer.Sound(resource_path("assets/sounds/tiro.wav"))
            self.sound_shot.set_volume(0.5)

            # --- NOVOS SONS DE FALA (VOZ) ---
            self.sound_intro_speech = pygame.mixer.Sound(resource_path("assets/sounds/viceEnemy.mp3"))
            self.sound_damage_speech = pygame.mixer.Sound(resource_path("assets/sounds/voiceAlien.mp3"))
            self.sound_speed_up_speech = pygame.mixer.Sound(resource_path("assets/sounds/bateu.ogg"))

        except pygame.error as e:
            print(f"AVISO: Arquivo de som de jogo não encontrado ou erro de carregamento: {e}")

        # --- NOVO: Toca o áudio de INTRODUÇÃO ao iniciar a partida ---
        if self.sound_intro_speech:
            self.sound_intro_speech.play()

    def draw(self, window):
        self.bg.draw(window)
        self.bg2.draw(window)

        self.all_sprites.draw(window)

        self.score.draw(window, 160, 50)
        self.lifes.draw(window, 50, 50)

        speed_text = f"VEL: {self.game_manager.base_speed_multiplier:.2f}X"
        Text(30, speed_text, color=(0, 255, 0)).draw(window, 400, 10)

    def update(self):
        # CORREÇÃO: Removida a função 'shoot' aninhada
        if not self.game_manager.is_running:
            self.gameover()
            return

        self.move_bg()

        # 1. Lógica de Spawn Acelerada
        now = pygame.time.get_ticks()
        spawn_rate_effective = self.initial_spawn_rate / self.game_manager.base_speed_multiplier

        if now - self.spawn_time > spawn_rate_effective:
            self.spawn_enemy()
            self.spawn_time = now

        # 2. Atualização de Sprites
        self.all_sprites.update(game_manager=self.game_manager,
                                all_sprites=self.all_sprites,
                                enemy_bullets=self.enemy_bullets,
                                player_bullets=self.player_bullets)

        self.star.anim("star", 2, 3)

        # 3. Colisões
        self.check_collision_player()
        self.check_bullet_collisions()

        # 4. Movimento do Flower (Corrigido para usar respawn_flower)
        speed_flower = 5 * self.game_manager.base_speed_multiplier
        self.flower.rect[1] += speed_flower
        if self.flower.rect[1] > 640:
            self.flower.kill()
            self.respawn_flower()

        # 5. HUD e Game Over
        self.gameover()
        self.score.update_text(str(self.game_manager.score))
        self.lifes.update_text(str(self.game_manager.player_lives))

    def shoot(self):
        """Cria e dispara o projétil do jogador, e toca o som."""

        current_time = pygame.time.get_ticks()
        if current_time - self.star.last_shot_time > self.star.fire_rate:

            # 1. Toca o som do tiro (Lógica trazida da função aninhada)
            if self.sound_shot:
                self.sound_shot.play()

            # 2. Cria e adiciona a bala
            # Usei a posição central (centerx) da estrela para o tiro
            new_bullet = Bullet(self.star.rect.centerx, self.star.rect.top)
            self.all_sprites.add(new_bullet)
            self.player_bullets.add(new_bullet)
            self.star.last_shot_time = current_time

    # ... (Resto dos métodos sem alteração) ...

    def spawn_enemy(self):
        """Cria um inimigo aleatório (Lunar, Asteroide, Cubo)."""
        enemy_classes = [Lunar, Asteroide, Cubo]
        ChosenEnemy = random.choice(enemy_classes)

        new_enemy = ChosenEnemy()
        self.all_sprites.add(new_enemy)
        self.enemies.add(new_enemy)

    def respawn_flower(self):
        """Recria o coletável Flower."""
        self.flower = Flower()
        self.all_sprites.add(self.flower)
        self.collectables.add(self.flower)

    def check_bullet_collisions(self):
        """Colisão tiro do jogador (player_bullets) com inimigos."""
        hits = pygame.sprite.groupcollide(self.player_bullets, self.enemies, True, True)

        for bullet, hit_enemies in hits.items():
            for obj in hit_enemies:
                self.game_manager.update_score(10)
                self.spawn_enemy()

    def check_collision_player(self):
        """Colisão do jogador com inimigos, projéteis e coletáveis."""

        # 1. Colisão com INIMIGOS (Colisão direta)
        hit_enemies = pygame.sprite.spritecollide(self.star, self.enemies, True)
        for obj in hit_enemies:
            self.star.take_damage(1, self.game_manager)
            self.spawn_enemy()

            # 2. Colisão com PROJÉTEIS INIMIGOS
        hit_enemy_bullets = pygame.sprite.spritecollide(self.star, self.enemy_bullets, True)
        for bullet in hit_enemy_bullets:
            self.star.take_damage(bullet.damage, self.game_manager)

            # 3. Colisão com Coletáveis (Flower)
        hit_collectables = pygame.sprite.spritecollide(self.star, self.collectables, True)
        for obj in hit_collectables:
            self.game_manager.update_score(1)
            if self.star.sound_pts:
                self.star.sound_pts.play()
            self.respawn_flower()

    def move_bg(self):
        speed = 1 * self.game_manager.base_speed_multiplier
        self.bg.rect[1] += speed
        self.bg2.rect[1] += speed

        if self.bg.rect[1] > 640:
            self.bg.rect[1] = -4000

        if self.bg2.rect[1] > 640:
            self.bg2.rect[1] = -4000

    def gameover(self):
        if not self.game_manager.is_running:
            self.change_scene = True

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.game_manager.is_running:
                    self.shoot()