import pygame

class ParametersWindow:
    def __init__(self, life_percentage, damage_percentage,damage_percentage2,damage_percentage3,damage_percentage4,board_size):
        pygame.init()

        self.WIDTH, self.HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Ventana de Parámetros")

        self.font = pygame.font.Font(None, 36)

        self.life_percentage = life_percentage
        self.damage_percentage = damage_percentage
        self.damage_percentage2 = damage_percentage2
        self.damage_percentage3 = damage_percentage3
        self.damage_percentage4 = damage_percentage4
        self.board_size = board_size

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.window.fill((255, 255, 255))

            # Mostrar los parámetros seleccionados
            life_text = self.font.render(f"Vida: {self.life_percentage}", True, (0, 0, 0))
            damage_text = self.font.render(f"Daño mina: {self.damage_percentage}", True, (0, 0, 0))
            damage_text2 = self.font.render(f"Daño disp e: {self.damage_percentage2}", True, (0, 0, 0))
            damage_text3 = self.font.render(f"Daño disp l : {self.damage_percentage3}", True, (0, 0, 0))
            damage_text4 = self.font.render(f"Daño choque: {self.damage_percentage4}", True, (0, 0, 0))
            damage_text5 = self.font.render(f"tablero: {self.board_size}", True, (0, 0, 0))

            self.window.blit(life_text, (100, 100))
            self.window.blit(damage_text, (100, 200))
            self.window.blit(damage_text2, (100, 300))
            self.window.blit(damage_text3, (100, 400))
            self.window.blit(damage_text4, (100, 500))
            self.window.blit(damage_text5, (100, 600))

            pygame.display.flip()

        pygame.quit()
