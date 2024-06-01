import pygame
import os
from param import Param

class Start:
    def __init__(self):
        pygame.init()

        # Definir colores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.HOVER_COLOR = (4, 111, 18)
        self.TEXT_COLOR = (255, 165, 0)

        # Obtener dimensiones de la pantalla
        screen_info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = screen_info.current_w, screen_info.current_h

        # Crear la ventana principal
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Ventana Principal")

        # Cargar imagen de fondo de la ventana principal
        self.background_img = pygame.image.load("Imagenes/fondo2.jpg")
        self.background_img = pygame.transform.scale(self.background_img, (self.WIDTH, self.HEIGHT))

        # Cargar música de fondo
        pygame.mixer.music.load(os.path.join("audios", "victoria2.mp3"))
        pygame.mixer.music.play(-1)  # Repetir la música de fondo infinitamente

        # Cargar efecto de sonido para el botón "Play"
        self.button_sound = pygame.mixer.Sound(os.path.join("audios", "click.mp3"))

        self.top_image = pygame.image.load("Imagenes/title.png")
        self.top_image = pygame.transform.scale(self.top_image, (900, 350))  # Redimensionar si es necesario
        self.top_image_rect = self.top_image.get_rect(midtop=(self.WIDTH / 2, 10))  # Centrar horizontalmente y posición superior

        # Definir los rectángulos de los botones fuera del bucle principal
        self.start_button_rect = pygame.Rect(self.WIDTH / 2 - 150, self.HEIGHT / 2 , 300, 80)
        self.instructions_button_rect = pygame.Rect(self.WIDTH / 2 - 150, self.HEIGHT / 2 + 150, 300, 80)

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
                    if self.start_button_rect.collidepoint(mouse_pos):
                        print("¡Clic en Start!")
                        self.button_sound.play()
                        param_window = Param(self)
                        param_window.run()
                    elif self.instructions_button_rect.collidepoint(mouse_pos):
                        print("¡Clic en Instrucciones!")
                        self.button_sound.play()
                        # Agregar la lógica para mostrar las instrucciones aquí

            mouse_pos = pygame.mouse.get_pos()

            self.window.blit(self.background_img, (0, 0))
            # Dibujar la imagen en la parte superior centrada
            self.window.blit(self.top_image, self.top_image_rect.topleft)
            self.draw_rounded_button(self.WIDTH / 2 - 150, self.HEIGHT / 2 , 300, 80, "Start", self.start_button_rect.collidepoint(mouse_pos))
            self.draw_rounded_button(self.WIDTH / 2 - 150, self.HEIGHT / 2 + 150, 300, 80, "Instrucciones", self.instructions_button_rect.collidepoint(mouse_pos))

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    start_window = Start()
    start_window.run()
