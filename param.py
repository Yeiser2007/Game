import pygame
import os
from ParametrosWindow import ParametersWindow  # Asegúrate de importar la clase ParametrosWindow


class Param:
    def __init__(self, start_window):
        self.start_window = start_window
        pygame.init()

        self.WIDTH, self.HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Ventana de Parámetros")

        self.background_img = pygame.image.load("Imagenes/fondo3.jpeg")
        self.background_img = pygame.transform.scale(self.background_img, (self.WIDTH, self.HEIGHT))

        self.font = pygame.font.Font(None, 36)

        self.life_percentage = 100
        self.damage_percentage = 15
        self.damage_percentage2 = 25
        self.damage_percentage3 = 25
        self.damage_percentage4 = 25
        self.next_button_rect = pygame.Rect(self.WIDTH - 350, self.HEIGHT - 100, 250, 80)
        self.back_button_rect = pygame.Rect(100, self.HEIGHT - 100, 250, 80)

        self.life_slider = pygame.Rect(300, 250, 250, 30)
        self.damage_slider = pygame.Rect(300, 300, 250, 30)
        self.damage_slider2 = pygame.Rect(300, 350, 250, 30)
        self.damage_slider3 = pygame.Rect(300, 400, 250, 30)
        self.damage_slider4 = pygame.Rect(300, 450, 250, 30)

        self.life_label = self.font.render("Vida:", True, (255, 255, 255))
        self.damage_label2 = self.font.render("Disparo Lineal:", True, (255, 255, 255))
        self.damage_label3 = self.font.render("Disparo Específico:", True, (255, 255, 255))
        self.damage_label4 = self.font.render("Choque:", True, (255, 255, 255))
        self.damage_label = self.font.render("Daño Mina:", True, (255, 255, 255))

        self.button_sound = pygame.mixer.Sound(os.path.join("audios", "click.mp3"))
        self.next_button_sound = pygame.mixer.Sound(os.path.join("audios", "next.mp3"))

        self.board_sizes = ["6x6", "8x8", "10x10"]
        self.board_size = 0
        self.current_board_size_index = 0

        self.board_size_rect = pygame.Rect(850, 300, 200, 50)
        self.board_size_label = self.font.render("Tamaño del tablero:", True, (255, 255, 255))
        self.prev_button_rect = pygame.Rect(1060, 300, 40, 50)
        self.next_button_board_size_rect = pygame.Rect(800, 300, 40, 50)

        self.top_image = pygame.image.load("Imagenes/title2.png")
        self.top_image = pygame.transform.scale(self.top_image, (500, 150))  # Redimensionar si es necesario
        self.top_image_rect = self.top_image.get_rect(
            midtop=(self.WIDTH / 2, 10))  # Centrar horizontalmente y posición superior

        # Definir colores
        self.WHITE = (255, 255, 255)
        self.HOVER_COLOR = (179, 243, 31)

    def draw_rounded_button(self, x, y, width, height, text, hover=False):
        color = self.HOVER_COLOR if hover else (0, 181, 25)
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.window, color, button_rect, border_radius=40)
        font = pygame.font.Font(None, 50)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.window.blit(text_surface, text_rect)

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
                        if (self.current_board_size_index == 0):
                            self.board_size = 6

                        elif (self.current_board_size_index == 1):
                            self.board_size = 8

                        elif (self.current_board_size_index == 2):
                            self.board_size = 10

                        # Crear una instancia de ParametrosWindow y pasar los parámetros
                        parametros_window = ParametersWindow(self.life_percentage, self.damage_percentage,
                                                             self.damage_percentage2, self.damage_percentage3,
                                                             self.damage_percentage4, self.board_size)
                        # Ejecutar la ventana ParametrosWindow
                        parametros_window.run()
                    elif self.life_slider.collidepoint(mouse_pos):
                        self.life_percentage = (mouse_pos[0] - self.life_slider.x) / self.life_slider.width * 100
                        self.button_sound.play()
                    elif self.damage_slider.collidepoint(mouse_pos):
                        self.damage_percentage = (mouse_pos[0] - self.damage_slider.x) / self.damage_slider.width * 100
                        self.button_sound.play()
                    elif self.damage_slider2.collidepoint(mouse_pos):
                        self.damage_percentage2 = (mouse_pos[
                                                       0] - self.damage_slider2.x) / self.damage_slider2.width * 100
                        self.button_sound.play()
                    elif self.damage_slider3.collidepoint(mouse_pos):
                        self.damage_percentage3 = (mouse_pos[
                                                       0] - self.damage_slider3.x) / self.damage_slider3.width * 100
                        self.button_sound.play()
                    elif self.damage_slider4.collidepoint(mouse_pos):
                        self.damage_percentage4 = (mouse_pos[
                                                       0] - self.damage_slider4.x) / self.damage_slider4.width * 100
                        self.button_sound.play()
                    elif self.prev_button_rect.collidepoint(mouse_pos):
                        self.current_board_size_index = (self.current_board_size_index - 1) % len(self.board_sizes)
                        self.button_sound.play()
                    elif self.next_button_board_size_rect.collidepoint(mouse_pos):
                        self.current_board_size_index = (self.current_board_size_index + 1) % len(self.board_sizes)
                        self.button_sound.play()
                    elif self.back_button_rect.collidepoint(mouse_pos):
                        print("Regresar a la ventana anterior")
                        self.button_sound.play()
                        running = False

            mouse_pos = pygame.mouse.get_pos()

            self.window.blit(self.background_img, (0, 0))
            self.window.blit(self.top_image, self.top_image_rect.topleft)

            pygame.draw.rect(self.window, (50, 50, 50), self.life_slider)
            life_fill_width = self.life_slider.width * (self.life_percentage / 100)
            pygame.draw.rect(self.window, (255, 255, 0),
                             (self.life_slider.x, self.life_slider.y, life_fill_width, self.life_slider.height))
            life_text = self.font.render(f"{int(self.life_percentage)}%", True, (255, 255, 255))
            self.window.blit(life_text, (self.life_slider.x + life_fill_width + 5, self.life_slider.y - 5))
            self.window.blit(self.life_label,
                             (self.life_slider.x - self.life_label.get_width() - 10, self.life_slider.y))

            pygame.draw.rect(self.window, (50, 50, 50), self.damage_slider)
            damage_fill_width = self.damage_slider.width * (self.damage_percentage / 100)
            pygame.draw.rect(self.window, (255, 255, 0),
                             (self.damage_slider.x, self.damage_slider.y, damage_fill_width, self.damage_slider.height))
            damage_text = self.font.render(f"{int(self.damage_percentage)}%", True, (255, 255, 255))
            self.window.blit(damage_text, (self.damage_slider.x + damage_fill_width + 5, self.damage_slider.y - 5))
            self.window.blit(self.damage_label,
                             (self.damage_slider.x - self.damage_label.get_width() - 10, self.damage_slider.y))

            pygame.draw.rect(self.window, (50, 50, 50), self.damage_slider2)
            damage_fill_width2 = self.damage_slider2.width * (self.damage_percentage2 / 100)
            pygame.draw.rect(self.window, (255, 255, 0), (
            self.damage_slider2.x, self.damage_slider2.y, damage_fill_width2, self.damage_slider2.height))
            damage_text2 = self.font.render(f"{int(self.damage_percentage2)}%", True, (255, 255, 255))
            self.window.blit(damage_text2, (self.damage_slider2.x + damage_fill_width2 + 5, self.damage_slider2.y - 5))
            self.window.blit(self.damage_label2,
                             (self.damage_slider2.x - self.damage_label2.get_width() - 10, self.damage_slider2.y))

            pygame.draw.rect(self.window, (50, 50, 50), self.damage_slider3)
            damage_fill_width3 = self.damage_slider3.width * (self.damage_percentage3 / 100)
            pygame.draw.rect(self.window, (255, 255, 0), (
            self.damage_slider3.x, self.damage_slider3.y, damage_fill_width3, self.damage_slider3.height))
            damage_text3 = self.font.render(f"{int(self.damage_percentage3)}%", True, (255, 255, 255))
            self.window.blit(damage_text3, (self.damage_slider3.x + damage_fill_width3 + 5, self.damage_slider3.y - 5))
            self.window.blit(self.damage_label3,
                             (self.damage_slider3.x - self.damage_label3.get_width() - 10, self.damage_slider3.y))

            pygame.draw.rect(self.window, (50, 50, 50), self.damage_slider4)
            damage_fill_width4 = self.damage_slider4.width * (self.damage_percentage4 / 100)
            pygame.draw.rect(self.window, (255, 255, 0), (
            self.damage_slider4.x, self.damage_slider4.y, damage_fill_width4, self.damage_slider4.height))
            damage_text4 = self.font.render(f"{int(self.damage_percentage4)}%", True, (255, 255, 255))
            self.window.blit(damage_text4, (self.damage_slider4.x + damage_fill_width4 + 5, self.damage_slider4.y - 5))
            self.window.blit(self.damage_label4,
                             (self.damage_slider4.x - self.damage_label4.get_width() - 10, self.damage_slider4.y))

            # Dibujar carrusel de tamaño del tablero
            self.window.blit(self.board_size_label, (
            self.board_size_rect.x - self.board_size_label.get_width() + 200, self.board_size_rect.y - 50))
            pygame.draw.rect(self.window, (50, 50, 50), self.board_size_rect)
            board_size_text = self.font.render(self.board_sizes[self.current_board_size_index], True, (255, 255, 255))
            board_size_text_rect = board_size_text.get_rect(center=self.board_size_rect.center)
            self.window.blit(board_size_text, board_size_text_rect)

            # Dibujar botones del carrusel
            pygame.draw.rect(self.window, (100, 100, 100), self.prev_button_rect)
            pygame.draw.polygon(self.window, (255, 255, 255),
                                [(self.prev_button_rect.x + 30, self.prev_button_rect.y + 25),
                                 (self.prev_button_rect.x + 10, self.prev_button_rect.y + 10),
                                 (self.prev_button_rect.x + 10, self.prev_button_rect.y + 40)])

            pygame.draw.rect(self.window, (100, 100, 100), self.next_button_board_size_rect)
            pygame.draw.polygon(self.window, (255, 255, 255),
                                [(self.next_button_board_size_rect.x + 10, self.next_button_board_size_rect.y + 25),
                                 (self.next_button_board_size_rect.x + 30, self.next_button_board_size_rect.y + 10),
                                 (self.next_button_board_size_rect.x + 30, self.next_button_board_size_rect.y + 40)])

            self.draw_rounded_button(self.next_button_rect.x, self.next_button_rect.y, self.next_button_rect.width,
                                     self.next_button_rect.height, "Siguiente",
                                     hover=self.next_button_rect.collidepoint(mouse_pos))
            self.draw_rounded_button(self.back_button_rect.x, self.back_button_rect.y, self.back_button_rect.width,
                                     self.back_button_rect.height, "Atrás",
                                     hover=self.back_button_rect.collidepoint(mouse_pos))

            pygame.display.flip()

        self.start_window.run()


if __name__ == "__main__":
    from Start import Start  # Mover la importación aquí para evitar el ciclo

    start_window = Start()
    param_window = Param(start_window)
    param_window.run()
