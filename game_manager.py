# game_manager.py
class GameController:
    """
    Gerencia a pontuação, o estado do jogo (vidas, rodando/game over)
    e o fator de dificuldade (aceleração global).
    """

    def __init__(self, initial_lives=5):
        # --- Variáveis de Estado do Jogo ---
        self.score = 0
        self.is_running = True
        self.player_lives = initial_lives

        # --- Variáveis de Controle de Velocidade (Dificuldade) ---
        self.base_speed_multiplier = 1.0  # O multiplicador atual
        self.acceleration_interval = 50  # Aumenta a cada 100 pontos
        self.next_speed_threshold = 100  # Próximo marco para aceleração
        self.speed_increase_factor = 0.05  # Aumento de 5% por intervalo (5%)
        self.max_speed_multiplier = 3.0  # Velocidade máxima do jogo

    def update_score(self, points):
        """
        Adiciona pontos e verifica se o limite de aceleração foi atingido.
        """
        if not self.is_running:
            return

        self.score += points

        if self.score >= self.next_speed_threshold:
            # Aumenta o multiplicador de velocidade, respeitando o limite
            new_multiplier = self.base_speed_multiplier + self.speed_increase_factor
            self.base_speed_multiplier = min(new_multiplier, self.max_speed_multiplier)

            # Define o próximo marco
            self.next_speed_threshold += self.acceleration_interval

            print(f"DIFICULDADE AUMENTADA! Novo Multiplicador: {self.base_speed_multiplier:.2f}x")

    def get_effective_speed(self, standard_velocity):
        """
        Retorna a velocidade real de um objeto, aplicando o multiplicador de dificuldade.
        """
        return standard_velocity * self.base_speed_multiplier

    def player_hit(self, damage=1):
        """
        Lógica para quando o jogador é atingido.
        """
        if self.is_running:
            self.player_lives -= damage

            if self.player_lives <= 0:
                self.game_over()

    def game_over(self):
        """
        Define o estado do jogo para Game Over.
        """
        self.is_running = False
        print(f"*** GAME OVER! Pontuação final: {self.score} ***")