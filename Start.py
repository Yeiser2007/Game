import pygame
import os
from param import Param

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definir dimensiones de la ventana principal
WIDTH, HEIGHT = 800, 600

# Crear la ventana principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ventana Principal")

# Cargar imagen de fondo de la ventana principal
background_img = pygame.image.load("Imagenes/fondo.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Cargar imágenes de los botones
play_img = pygame.image.load("Imagenes/play.png")
instructions_img = pygame.image.load("Imagenes/play.png")
credits_img = pygame.image.load("Imagenes/play.png")

# Escalar las imágenes de los botones
button_scale = 0.5
play_img = pygame.transform.scale(play_img,
                                  (int(play_img.get_width() * button_scale), int(play_img.get_height() * button_scale)))
instructions_img = pygame.transform.scale(instructions_img, (
int(instructions_img.get_width() * button_scale), int(instructions_img.get_height() * button_scale)))
credits_img = pygame.transform.scale(credits_img, (
int(credits_img.get_width() * button_scale), int(credits_img.get_height() * button_scale)))

# Cargar música de fondo
pygame.mixer.music.load(os.path.join("audios", "victoria2.mp3"))
pygame.mixer.music.play(-1)  # Repetir la música de fondo infinitamente

# Cargar efecto de sonido para el botón "Play"
button_sound = pygame.mixer.Sound(os.path.join("audios", "click.mp3"))

# Función para dibujar los botones
def draw_buttons():
    window.blit(play_img, (WIDTH / 2 - play_img.get_width() / 2, HEIGHT / 2 - 50))
    window.blit(instructions_img, (WIDTH / 2 - instructions_img.get_width() / 2, HEIGHT / 2 + 50))
    window.blit(credits_img, (WIDTH / 2 - credits_img.get_width() / 2, HEIGHT / 2 + 150))

# Loop del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Verificar si se hace clic en alguno de los botones
            mouse_pos = pygame.mouse.get_pos()
            play_rect = pygame.Rect(WIDTH / 2 - play_img.get_width() / 2, HEIGHT / 2 - 50, play_img.get_width(),
                                    play_img.get_height())
            instructions_rect = pygame.Rect(WIDTH / 2 - instructions_img.get_width() / 2, HEIGHT / 2 + 50,
                                            instructions_img.get_width(), instructions_img.get_height())
            credits_rect = pygame.Rect(WIDTH / 2 - credits_img.get_width() / 2, HEIGHT / 2 + 150,
                                       credits_img.get_width(), credits_img.get_height())
            if play_rect.collidepoint(mouse_pos):
                print("¡Clic en Play!")
                # Reproducir efecto de sonido
                button_sound.play()
                # Abrir la ventana de solicitud de parámetros
                parameter_window = Param()
                parameter_window.run()

    # Dibujar la imagen de fondo y los botones en la ventana principal
    window.blit(background_img, (0, 0))
    draw_buttons()

    pygame.display.flip()

# Salir de Pygame
pygame.quit()
