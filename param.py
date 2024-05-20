import pygame
from ParametrosWindow import ParametersWindow
import os

class Param:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 800, 600
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Ventana de Parámetros")

        self.background_img = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.background_img.fill((255, 255, 255))

        self.font = pygame.font.Font(None, 36)

        self.life_percentage = 50
        self.damage_percentage = 50
        self.next_button_rect = pygame.Rect(self.WIDTH - 230, self.HEIGHT - 80, 200, 50)

        self.life_slider = pygame.Rect(300, 300, 200, 20)
        self.damage_slider = pygame.Rect(300, 350, 200, 20)

        self.life_label = self.font.render("Vida:", True, (0, 0, 0))
        self.damage_label = self.font.render("Daño:", True, (0, 0, 0))

        self.button_sound = pygame.mixer.Sound(os.path.join("audios", "click.mp3"))
        self.next_button_sound = pygame.mixer.Sound(os.path.join("audios", "next.mp3"))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.next_button_rect.collidepoint(mouse_pos):
                        print("Parámetro de vida:", self.life_percentage)
                        print("Parámetro de daño:", self.damage_percentage)

                        self.next_button_sound.play()

                        # Cierra la ventana actual
                        running = False

                        # Abre la nueva ventana de parámetros
                        parameters_window = ParametersWindow(self.life_percentage, self.damage_percentage)
                        parameters_window.run()

                    elif self.life_slider.collidepoint(mouse_pos):
                        self.life_percentage = (mouse_pos[0] - self.life_slider.x) / self.life_slider.width * 100
                        self.button_sound.play()
                    elif self.damage_slider.collidepoint(mouse_pos):
                        self.damage_percentage = (mouse_pos[0] - self.damage_slider.x) / self.damage_slider.width * 100
                        self.button_sound.play()

            self.window.blit(self.background_img, (0, 0))

            # Dentro del bucle principal
            pygame.draw.rect(self.window, (50, 50, 50), self.life_slider)
            life_fill_width = self.life_slider.width * (self.life_percentage / 100)
            pygame.draw.rect(self.window, (255, 255, 0),
                             (self.life_slider.x, self.life_slider.y, life_fill_width, self.life_slider.height))
            life_text = self.font.render(f"{int(self.life_percentage)}%", True,
                                         (0, 0, 0))  # Renderizar el texto del porcentaje
            self.window.blit(life_text, (
            self.life_slider.x + life_fill_width + 5, self.life_slider.y - 5))  # Mostrar el texto del porcentaje

            self.window.blit(self.life_label,
                             (self.life_slider.x - self.life_label.get_width() - 10, self.life_slider.y))

            pygame.draw.rect(self.window, (50, 50, 50), self.damage_slider)
            damage_fill_width = self.damage_slider.width * (self.damage_percentage / 100)
            pygame.draw.rect(self.window, (255, 255, 0),
                             (self.damage_slider.x, self.damage_slider.y, damage_fill_width, self.damage_slider.height))
            damage_text = self.font.render(f"{int(self.damage_percentage)}%", True,
                                           (0, 0, 0))  # Renderizar el texto del porcentaje
            self.window.blit(damage_text, (
            self.damage_slider.x + damage_fill_width + 5, self.damage_slider.y - 5))  # Mostrar el texto del porcentaje

            self.window.blit(self.damage_label,
                             (self.damage_slider.x - self.damage_label.get_width() - 10, self.damage_slider.y))

            pygame.draw.rect(self.window, (0, 128, 0), self.next_button_rect)
            next_text = self.font.render("Siguiente", True, (255, 255, 255))
            next_text_rect = next_text.get_rect(center=self.next_button_rect.center)
            self.window.blit(next_text, next_text_rect)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    param_window = Param()
    param_window.run()
