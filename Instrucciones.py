import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla en modo completo
pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
ANCHO, ALTO = pantalla.get_size()

# Constantes de color
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
AZUL = (0, 0, 255)

# Tamaño de los botones
BOTON_ANCHO = 80
BOTON_ALTO = 40

# Clase para los botones
class Boton:
    def __init__(self, text, pos, callback):
        self.text = text
        self.pos = pos
        self.callback = callback
        self.rect = pygame.Rect(pos, (BOTON_ANCHO, BOTON_ALTO))
        self.color = GRIS

    def draw(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)
        font = pygame.font.Font(None, 24)
        text = font.render(self.text, True, NEGRO)
        pantalla.blit(text, (self.pos[0] + 10, self.pos[1] + 10))

    def click(self):
        self.callback()

# Variables globales
text_area = ""
current_instruction = ""
awaiting_parameters = 0
temp_params = []

# Funciones de callback para los botones
def mostrar_botones_mov():
    ocultar_todos_botones()
    toggle_buttons(botones_mov)
    global current_instruction, awaiting_parameters
    current_instruction = "mov"
    awaiting_parameters = 1

def mostrar_botones_disp_l():
    ocultar_todos_botones()
    toggle_buttons(botones_disp_l)
    global current_instruction, awaiting_parameters
    current_instruction = "dis_l"
    awaiting_parameters = 1

def mostrar_botones_disp_e():
    ocultar_todos_botones()
    toggle_buttons(botones_disp_e[:4])
    global current_instruction, awaiting_parameters
    current_instruction = "dis_e"
    awaiting_parameters = 2

def mostrar_botones_rad():
    ocultar_todos_botones()
    toggle_buttons(botones_rad)
    global current_instruction, awaiting_parameters
    current_instruction = "rad"
    awaiting_parameters = 1

def mostrar_botones_if():
    ocultar_todos_botones()
    toggle_buttons(botones_if)
    global current_instruction, awaiting_parameters
    current_instruction = "if"
    awaiting_parameters = 3

def ocultar_todos_botones():
    for boton in todos_los_botones_secundarios:
        boton.color = GRIS

def toggle_buttons(buttons):
    for boton in buttons:
        boton.color = AZUL if boton.color == GRIS else GRIS

def anyadir_texto(texto):
    global text_area, current_instruction, awaiting_parameters, temp_params
    if awaiting_parameters > 0:
        if current_instruction in ["mov", "dis_l", "rad"]:
            text_area += f"{current_instruction}({texto})\n"
            awaiting_parameters = 0
        elif current_instruction == "dis_e" and awaiting_parameters == 2:
            temp_params.append(texto)
            awaiting_parameters -= 1
            toggle_buttons(botones_disp_e[4:])
        elif current_instruction == "dis_e" and awaiting_parameters == 1:
            temp_params.append(texto)
            text_area += f"{current_instruction}({temp_params[0]},{temp_params[1]})\n"
            awaiting_parameters = 0
            temp_params = []
            ocultar_todos_botones()
            current_instruction = ""
        elif current_instruction == "if" and awaiting_parameters == 3:
            text_area += f"{current_instruction}({texto} "
            awaiting_parameters -= 1
        elif current_instruction == "if" and awaiting_parameters == 2:
            text_area += f"{texto} "
            awaiting_parameters -= 1
        elif current_instruction == "if" and awaiting_parameters == 1:
            text_area += f"{texto}) then ("
            toggle_buttons(botones_principales)
            awaiting_parameters -= 1
        elif current_instruction == "if" and awaiting_parameters == 0:
            text_area += f"{texto})\n"
            awaiting_parameters = 0
            ocultar_todos_botones()
            current_instruction = ""
    else:
        text_area += texto + "\n"

def guardar_texto():
    global text_area
    with open("instrucciones.txt", "w") as f:
        f.write(text_area)

# Crear los botones principales
botones_principales = [
    Boton("mov", (50, 50), mostrar_botones_mov),
    Boton("dis_l", (50, 110), mostrar_botones_disp_l),
    Boton("dis_e", (50, 170), mostrar_botones_disp_e),
    Boton("rad", (50, 230), mostrar_botones_rad),
    Boton("if", (50, 290), mostrar_botones_if)
]

# Crear los botones secundarios
botones_mov = [
    Boton("n", (150, 50), lambda: anyadir_texto("n")),
    Boton("s", (150, 110), lambda: anyadir_texto("s")),
    Boton("e", (150, 170), lambda: anyadir_texto("e")),
    Boton("o", (150, 230), lambda: anyadir_texto("o"))
]

botones_disp_l = [
    Boton("n", (150, 50), lambda: anyadir_texto("n")),
    Boton("s", (150, 110), lambda: anyadir_texto("s")),
    Boton("e", (150, 170), lambda: anyadir_texto("e")),
    Boton("o", (150, 230), lambda: anyadir_texto("o"))
]

botones_disp_e = [
    Boton("n", (150, 50), lambda: anyadir_texto("n")),
    Boton("s", (150, 110), lambda: anyadir_texto("s")),
    Boton("e", (150, 170), lambda: anyadir_texto("e")),
    Boton("o", (150, 230), lambda: anyadir_texto("o")),
    Boton("1", (250, 50), lambda: anyadir_texto("1")),
    Boton("2", (250, 110), lambda: anyadir_texto("2")),
    Boton("3", (250, 170), lambda: anyadir_texto("3")),
    Boton("4", (250, 230), lambda: anyadir_texto("4")),
    Boton("5", (250, 290), lambda: anyadir_texto("5")),
    Boton("6", (250, 350), lambda: anyadir_texto("6")),
    Boton("7", (250, 410), lambda: anyadir_texto("7")),
    Boton("8", (250, 470), lambda: anyadir_texto("8")),
    Boton("9", (250, 530), lambda: anyadir_texto("9")),
    Boton("10", (250, 590), lambda: anyadir_texto("10"))
]

botones_rad = [
    Boton("n", (150, 50), lambda: anyadir_texto("n")),
    Boton("s", (150, 110), lambda: anyadir_texto("s")),
    Boton("e", (150, 170), lambda: anyadir_texto("e")),
    Boton("o", (150, 230), lambda: anyadir_texto("o"))
]

botones_if = [
    Boton("vida", (150, 50), lambda: anyadir_texto("vida")),
    Boton("rad", (150, 110), lambda: anyadir_texto("rad")),
    Boton("<", (150, 170), lambda: anyadir_texto("<")),
    Boton(">", (150, 230), lambda: anyadir_texto(">")),
    Boton("==", (150, 290), lambda: anyadir_texto("==")),
    Boton("then", (150, 350), lambda: anyadir_texto("recarga()"))
]

# Agrupar todos los botones secundarios
todos_los_botones_secundarios = botones_mov + botones_disp_l + botones_disp_e + botones_rad + botones_if

# Botón de guardar
boton_guardar = Boton("Guardar", (50, 350), guardar_texto)

# Bucle principal
while True:
    pantalla.fill(BLANCO)

    # Dibujar botones principales
    for boton in botones_principales:
        boton.draw(pantalla)

    # Dibujar botones secundarios visibles
    for boton in todos_los_botones_secundarios:
        if boton.color == AZUL:
            boton.draw(pantalla)

    # Dibujar el área de texto en el lado derecho
    pygame.draw.rect(pantalla, GRIS, (ANCHO - 350, 50, 300, ALTO - 100))
    font = pygame.font.Font(None, 24)
    lines = text_area.split("\n")
    y = 60
    for line in lines:
        text = font.render(line, True, NEGRO)
        pantalla.blit(text, (ANCHO - 340, y))
        y += 30

    # Dibujar el botón de guardar
    boton_guardar.draw(pantalla)

    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for boton in botones_principales + todos_los_botones_secundarios + [boton_guardar]:
                if boton.rect.collidepoint(event.pos):
                    boton.click()

    pygame.display.flip()
