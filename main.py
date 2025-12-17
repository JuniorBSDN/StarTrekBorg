import pygame
import sys
import os
from game import Game  # Importa a classe Game
from menu import Menu, GameOver


def resource_path(relative_path):
    """Obtém o caminho absoluto para o recurso."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



# --- CONFIGURAÇÕES DO PYGAME ---
pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter Acelerado")
CLOCK = pygame.time.Clock()
FPS = 60

# Garante que os recursos de áudio sejam inicializados
pygame.mixer.init()
pygame.mixer.music.load(resource_path("assets/sounds/deep.wav"))
pygame.mixer.music.play(-1)


def game_loop():
    # Inicializa as Cenas
    menu_scene = Menu(resource_path("assets/menu.jpg"))
    game_scene = Game()
    game_over_scene = GameOver(resource_path("assets/over.png"))
    current_scene = menu_scene
    running = True

    while running:
        CLOCK.tick(FPS)

        # 1. Tratamento de Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            current_scene.event(event)

        # 2. Lógica de Mudança de Cena
        if current_scene.change_scene:
            if current_scene == menu_scene:
                game_scene = Game()
                current_scene = game_scene

            elif current_scene == game_scene:
                current_scene = game_over_scene

            elif current_scene == game_over_scene:
                current_scene = menu_scene
            current_scene.change_scene = False

        # 3. Atualização e Desenho

        if current_scene == game_scene:
            current_scene.update()

        current_scene.draw(SCREEN)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game_loop()