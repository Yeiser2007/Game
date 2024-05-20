import pygame
import random
import time

# Definir constantes
ANCHO_VENTANA, ALTO_VENTANA = 800, 600
FILAS, COLUMNAS = 8, 8
TAMANO_CELDA = min(ANCHO_VENTANA // COLUMNAS, ALTO_VENTANA // FILAS)

# Colores
COLOR_FONDO = (255, 255, 255)
COLOR_TEXTO = (0, 0, 0)
COLOR_DISPARO = (255, 0, 0)
COLOR_RADAR = (0, 255, 0)

# Cargar imágenes de tanques y minas
imagen_tanque_rojo = pygame.image.load("Imagenes/tanque1.jpg")
imagen_tanque_verde = pygame.image.load("Imagenes/tanque2.jpg")
imagen_tanque_azul = pygame.image.load("Imagenes/tanque3.jpg")
imagen_tanque_amarillo = pygame.image.load("Imagenes/tanque4.jpg")
imagen_mina = pygame.image.load("Imagenes/mina.jpeg")

imagenes_tanques = [imagen_tanque_rojo, imagen_tanque_verde, imagen_tanque_azul, imagen_tanque_amarillo]
imagen_mina = pygame.transform.scale(imagen_mina, (TAMANO_CELDA, TAMANO_CELDA))

# Clase Tanque
class Tanque:
    def __init__(self, numero, x, y, imagen):
        self.numero = numero
        self.x = x
        self.y = y
        self.imagen_original = imagen
        self.imagen = pygame.transform.scale(imagen, (TAMANO_CELDA, TAMANO_CELDA))
        self.direccion = random.choice(["norte", "sur", "este", "oeste"])
        self.danio_recibido = 0
        self.vida = 100
        self.recargas = 0  # Contador de recargas
        self.ultimo_danio = 0  # Daño recibido en el último disparo

    def mover(self, direccion, minas):
        nueva_x, nueva_y = self.x, self.y
        if direccion == "norte":
            nueva_y -= 1
        elif direccion == "sur":
            nueva_y += 1
        elif direccion == "este":
            nueva_x += 1
        elif direccion == "oeste":
            nueva_x -= 1

        # Verificar que la nueva posición esté dentro del tablero
        if 0 <= nueva_x < COLUMNAS and 0 <= nueva_y < FILAS:
            self.x, self.y = nueva_x, nueva_y
            self.verificar_mina(minas)
        else:
            self.vida -= 10

    def disparar(self, direccion, tanques, trayectorias):
        self.girar(direccion)
        if direccion == "norte":
            trayectoria = [(self.x, y) for y in range(self.y - 1, -1, -1)]
        elif direccion == "sur":
            trayectoria = [(self.x, y) for y in range(self.y + 1, FILAS)]
        elif direccion == "este":
            trayectoria = [(x, self.y) for x in range(self.x + 1, COLUMNAS)]
        elif direccion == "oeste":
            trayectoria = [(x, self.y) for x in range(self.x - 1, -1, -1)]

        trayectorias.append(trayectoria)
        for (x, y) in trayectoria:
            for tanque in tanques:
                if tanque.x == x and tanque.y == y:
                    tanque.recibir_danio(20)
                    self.ultimo_danio = 20
                    print(f"Tanque {self.numero} disparó al {direccion}. Impacto!")
                    return
        self.ultimo_danio = 0
        print(f"Tanque {self.numero} disparó al {direccion}. No impacto.")

    def disparo_especifico(self, direccion, valor, tanques, disparos_especificos):
        self.girar(direccion)
        if valor < 0 or valor > 7:
            print(f"Tanque {self.numero} disparo específico inválido: valor {valor} fuera de rango")
            return

        if direccion == "norte":
            x, y = self.x, self.y - valor
        elif direccion == "sur":
            x, y = self.x, self.y + valor
        elif direccion == "este":
            x, y = self.x + valor, self.y
        elif direccion == "oeste":
            x, y = self.x - valor, self.y

        if 0 <= x < COLUMNAS and 0 <= y < FILAS:
            disparos_especificos.append((x, y))
            for tanque in tanques:
                if tanque.x == x and tanque.y == y:
                    tanque.recibir_danio(20)
                    self.ultimo_danio = 20
                    print(f"Tanque {self.numero} disparó {valor} casillas al {direccion}. Impacto en ({x}, {y})!")
                    return
            self.ultimo_danio = 0
            print(f"Tanque {self.numero} disparó {valor} casillas al {direccion}. No impacto.")
        else:
            print(f"Tanque {self.numero} disparó {valor} casillas al {direccion}, pero está fuera del tablero.")

    def recibir_danio(self, danio):
        self.danio_recibido += danio
        self.vida -= danio

    def esta_vivo(self):
        return self.vida > 0

    def radar(self, direccion, tanques, radar_areas):
        if direccion == "norte":
            posiciones = [(self.x, y) for y in range(self.y - 1, -1, -1)]
        elif direccion == "sur":
            posiciones = [(self.x, y) for y in range(self.y + 1, FILAS)]
        elif direccion == "este":
            posiciones = [(x, self.y) for x in range(self.x + 1, COLUMNAS)]
        elif direccion == "oeste":
            posiciones = [(x, self.y) for x in range(self.x - 1, -1, -1)]

        radar_areas.append(posiciones)
        tanque_encontrado = False

        for dist, (x, y) in enumerate(posiciones, 1):
            if any(tanque.x == x and tanque.y == y for tanque in tanques):
                print(f"Tanque {self.numero} radar {direccion}: Tanque a {dist} casillas")
                tanque_encontrado = True
                return dist

        # Si no se encontró un tanque, marcar la última casilla alcanzada como muro
        if not tanque_encontrado:
            if posiciones:
                # Última posición en la lista de posiciones
                x, y = posiciones[-1]
                dist = len(posiciones)
                print(f"Tanque {self.numero} radar {direccion}: Muro a {dist} casillas en ({x}, {y})")
                return -dist

        print(f"Tanque {self.numero} radar {direccion}: No hay tanques ni muros")
        return None

    def recargar(self):
        if self.recargas < 3:
            self.vida = min(self.vida + 10, 100)
            self.recargas += 1
            print(f"Tanque {self.numero} recargó. Vida actual: {self.vida}. Recargas usadas: {self.recargas}")
        else:
            print(f"Tanque {self.numero} ya ha usado sus 3 recargas.")

    def girar(self, direccion):
        if direccion == "norte":
            self.imagen = pygame.transform.rotate(self.imagen_original, 0)
        elif direccion == "sur":
            self.imagen = pygame.transform.rotate(self.imagen_original, 180)
        elif direccion == "este":
            self.imagen = pygame.transform.rotate(self.imagen_original, 270)
        elif direccion == "oeste":
            self.imagen = pygame.transform.rotate(self.imagen_original, 90)
        self.imagen = pygame.transform.scale(self.imagen, (TAMANO_CELDA, TAMANO_CELDA))

    def verificar_mina(self, minas):
        for mina in minas:
            if self.x == mina[0] and self.y == mina[1]:
                minas.remove(mina)
                self.recibir_danio(20)
                print(f"Tanque {self.numero} ha pasado por una mina y ha recibido 20 de daño.")

# Función para evaluar condiciones y ejecutar acciones
def evaluar_condicion(tanque, condicion, accion, tanques, minas, trayectorias, disparos_especificos, radar_areas):
    if eval(condicion):
        if accion == "mover":
            direccion = random.choice(["norte", "sur", "este", "oeste"])
            tanque.mover(direccion, minas)
        elif accion == "disparar":
            direccion = random.choice(["norte", "sur", "este", "oeste"])
            tanque.disparar(direccion, tanques, trayectorias)
        elif accion == "disparo_especifico":
            direccion = random.choice(["norte", "sur", "este", "oeste"])
            valor = random.randint(0, 7)
            tanque.disparo_especifico(direccion, valor, tanques, disparos_especificos)
        elif accion == "radar":
            direccion = random.choice(["norte", "sur", "este", "oeste"])
            tanque.radar(direccion, tanques, radar_areas)
        elif accion == "recargar":
            tanque.recargar()

# Función para dibujar la interfaz
def dibujar_interfaz(screen, tanques, minas, trayectorias, disparos_especificos, radar_areas, tamano_celda, margen_x, margen_y):
    screen.fill(COLOR_FONDO)

    # Dibujar la cuadrícula del tablero
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            rect = pygame.Rect(margen_x + columna * tamano_celda, margen_y + fila * tamano_celda, tamano_celda, tamano_celda)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

    # Dibujar las minas
    for mina in minas:
        rect = pygame.Rect(margen_x + mina[0] * tamano_celda, margen_y + mina[1] * tamano_celda, tamano_celda, tamano_celda)
        screen.blit(imagen_mina, rect)

    # Dibujar los tanques y su información
    fuente = pygame.font.Font(None, 36)
    for tanque in tanques:
        if tanque.esta_vivo():
            screen.blit(tanque.imagen, (margen_x + tanque.x * tamano_celda, margen_y + tanque.y * tamano_celda))
            texto_vida = fuente.render(f"Tanque {tanque.numero} Vida: {tanque.vida} Daño: {tanque.ultimo_danio}", True, COLOR_TEXTO)
            screen.blit(texto_vida, (10, 10 + (tanque.numero - 1) * 30))

    # Dibujar trayectorias de disparos
    for trayectoria in trayectorias:
        for (x, y) in trayectoria:
            pygame.draw.circle(screen, COLOR_DISPARO, (margen_x + x * tamano_celda + tamano_celda // 2, margen_y + y * tamano_celda + tamano_celda // 2), 3)
    trayectorias.clear()  # Borrar trayectorias después de dibujarlas

    # Dibujar disparos específicos
    for (x, y) in disparos_especificos:
        pygame.draw.circle(screen, COLOR_DISPARO, (margen_x + x * tamano_celda + tamano_celda // 2, margen_y + y * tamano_celda + tamano_celda // 2), 3)
    disparos_especificos.clear()  # Borrar disparos específicos después de dibujarlos

    # Dibujar áreas de radar
    for area in radar_areas:
        for (x, y) in area:
            pygame.draw.rect(screen, COLOR_RADAR, (margen_x + x * tamano_celda, margen_y + y * tamano_celda, tamano_celda, tamano_celda))
    radar_areas.clear()  # Borrar áreas de radar después de dibujarlas

    # Verificar colisiones entre tanques
    posiciones_ocupadas = {}
    for tanque in tanques:
        if tanque.esta_vivo():
            pos = (tanque.x, tanque.y)
            if pos in posiciones_ocupadas:
                tanque.recibir_danio(10)
                posiciones_ocupadas[pos].recibir_danio(10)
                print(f"Tanques {tanque.numero} y {posiciones_ocupadas[pos].numero} colisionaron y recibieron 10 de daño.")
            else:
                posiciones_ocupadas[pos] = tanque

    # Actualizar la pantalla
    pygame.display.flip()

# Función para mostrar el mensaje de victoria
def mostrar_victoria(screen, tanque_ganador, tamano_celda, margen_x, margen_y):
    screen.fill(COLOR_FONDO)
    fuente = pygame.font.Font(None, 74)
    mensaje = fuente.render(f"¡Felicidades! Ha ganado el tanque {tanque_ganador.numero}", True, COLOR_TEXTO)
    screen.blit(mensaje, (ANCHO_VENTANA // 2 - mensaje.get_width() // 2, ALTO_VENTANA // 2 - mensaje.get_height() // 2))
    screen.blit(tanque_ganador.imagen, (ANCHO_VENTANA // 2 - tamano_celda // 2, ALTO_VENTANA // 2 - tamano_celda // 2 - 100))
    pygame.display.flip()
    time.sleep(5)

# Configuración inicial de pygame
pygame.init()
screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Batalla de Tanques")

# Crear lista de minas
minas = [(random.randint(0, COLUMNAS-1), random.randint(0, FILAS-1)) for _ in range(5)]

# Crear lista de tanques
tanques = [Tanque(i+1, random.randint(0, COLUMNAS-1), random.randint(0, FILAS-1), imagenes_tanques[i]) for i in range(4)]

# Margen para centrar el tablero
margen_x = (ANCHO_VENTANA - COLUMNAS * TAMANO_CELDA) // 2
margen_y = (ALTO_VENTANA - FILAS * TAMANO_CELDA) // 2

# Listas para almacenar trayectorias y disparos específicos
trayectorias = []
disparos_especificos = []
radar_areas = []

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Evaluar condiciones y ejecutar acciones para cada tanque
    for tanque in tanques:
        if tanque.esta_vivo():
            evaluar_condicion(tanque, "tanque.vida > 0", random.choice(["mover", "disparar", "disparo_especifico", "radar", "recargar"]), tanques, minas, trayectorias, disparos_especificos, radar_areas)

    # Dibujar la interfaz
    dibujar_interfaz(screen, tanques, minas, trayectorias, disparos_especificos, radar_areas, TAMANO_CELDA, margen_x, margen_y)

    # Verificar si solo queda un tanque vivo
    tanques_vivos = [tanque for tanque in tanques if tanque.esta_vivo()]
    if len(tanques_vivos) == 1:
        mostrar_victoria(screen, tanques_vivos[0], TAMANO_CELDA, margen_x, margen_y)
        running = False

    # Pausar un poco para controlar la velocidad del juego
    time.sleep(1)

pygame.quit()
