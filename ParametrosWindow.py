import pygame

class ParametersWindow:
    def __init__(self, life_percentage, damage_percentage):
        pygame.init()

        self.WIDTH, self.HEIGHT = 800, 600
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Ventana de Parámetros")

        self.font = pygame.font.Font(None, 36)

        self.life_percentage = life_percentage
        self.damage_percentage = damage_percentage

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.window.fill((255, 255, 255))

            # Mostrar los parámetros seleccionados
            life_text = self.font.render(f"Vida: {self.life_percentage}", True, (0, 0, 0))
            damage_text = self.font.render(f"Daño: {self.damage_percentage}", True, (0, 0, 0))

            self.window.blit(life_text, (100, 100))
            self.window.blit(damage_text, (100, 200))

            pygame.display.flip()

        pygame.quit()
