import pygame
import random
import time

# Inicializar pygame y obtener información de la pantalla
pygame.init()
info = pygame.display.Info()
ANCHO_VENTANA, ALTO_VENTANA = info.current_w, info.current_h  # Dimensiones de la pantalla

# Definir constantes
FILAS, COLUMNAS = 7, 7  # 4 filas y 3 columnas para la tabla
TAMANO_CELDA = min(ANCHO_VENTANA // COLUMNAS, ALTO_VENTANA // FILAS)  # Ajustar tamaño de celda

# Colores
COLOR_FONDO = (255, 255, 255)
COLOR_TEXTO = (0, 0, 0)
COLOR_DISPARO = (255, 0, 0)
COLOR_RADAR = (0, 255, 0)

# Cargar imágenes de tanques, minas y fondo del tablero
imagen_fondo_interfaz = pygame.image.load("Imagenes/fondo.jpg")
imagen_fondo_interfaz = pygame.transform.scale(imagen_fondo_interfaz, (ANCHO_VENTANA, ALTO_VENTANA))
imagen_fondo_tablero = pygame.image.load("Imagenes/tablero.jpg")
imagen_fondo_tablero = pygame.transform.scale(imagen_fondo_tablero, (COLUMNAS * TAMANO_CELDA, FILAS * TAMANO_CELDA))
imagen_tanque_rojo = pygame.image.load("Imagenes/tanque1.jpg")
imagen_tanque_verde = pygame.image.load("Imagenes/tanque2.jpg")
imagen_tanque_azul = pygame.image.load("Imagenes/tanque3.jpg")
imagen_tanque_amarillo = pygame.image.load("Imagenes/tanque4.jpg")
imagen_mina = pygame.image.load("Imagenes/mina.jpeg")

imagenes_tanques = [imagen_tanque_rojo, imagen_tanque_verde, imagen_tanque_azul, imagen_tanque_amarillo]
imagen_mina = pygame.transform.scale(imagen_mina, (TAMANO_CELDA, TAMANO_CELDA))

# Cargar sonido de ganador
pygame.mixer.init()
sonido_ganador = pygame.mixer.Sound("audios/felicidades.mp3")

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
                print(f"Tanque {self.numero} pisó una mina en ({self.x}, {self.y}). Vida restante: {self.vida}")

def generar_minas(num_minas):
    minas = []
    while len(minas) < num_minas:
        x = random.randint(0, COLUMNAS - 1)
        y = random.randint(0, FILAS - 1)
        if (x, y) not in minas:
            minas.append((x, y))
    return minas

# Crear tanques y minas
tanques = [Tanque(i, random.randint(0, COLUMNAS-1), random.randint(0, FILAS-1), imagen) for i, imagen in enumerate(imagenes_tanques)]
minas = generar_minas(5)

def mostrar_tablero():
    ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Simulador de Combate de Tanques")

    instrucciones = ["avanzar", "girar", "disparar", "radar", "recargar"]
    trayectorias = []  # Lista para almacenar trayectorias de disparos normales
    disparos_especificos = []  # Lista para almacenar posiciones de disparos específicos
    radar_areas = []  # Lista para almacenar áreas de radar

    reloj = pygame.time.Clock()
    fin_simulacion = False

    while not fin_simulacion:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fin_simulacion = True

        ventana.blit(imagen_fondo_interfaz, (0, 0))
        ventana.blit(imagen_fondo_tablero, (0, 0))

        for mina in minas:
            ventana.blit(imagen_mina, (mina[0] * TAMANO_CELDA, mina[1] * TAMANO_CELDA))

        for i, tanque in enumerate(tanques):
            if tanque.esta_vivo():
                instruccion = random.choice(instrucciones)
                if instruccion == "avanzar":
                    direccion = random.choice(["norte", "sur", "este", "oeste"])
                    tanque.mover(direccion, minas)
                elif instruccion == "girar":
                    direccion = random.choice(["norte", "sur", "este", "oeste"])
                    tanque.girar(direccion)
                elif instruccion == "disparar":
                    direccion = random.choice(["norte", "sur", "este", "oeste"])
                    tanque.disparar(direccion, tanques, trayectorias)
                    # Eliminar la trayectoria del disparo si no hay más tanques en esa línea
                    trayectorias = [trayectoria for trayectoria in trayectorias if any((tanque.x, tanque.y) in trayectoria for tanque in tanques)]
                elif instruccion == "radar":
                    direccion = random.choice(["norte", "sur", "este", "oeste"])
                    tanque.radar(direccion, tanques, radar_areas)
                elif instruccion == "recargar":
                    tanque.recargar()

                ventana.blit(tanque.imagen, (tanque.x * TAMANO_CELDA, tanque.y * TAMANO_CELDA))
                # Mostrar la etiqueta del tanque con su identificador
                fuente = pygame.font.SysFont(None, 20)
                texto_identificador = fuente.render(f"Tanque {tanque.numero + 1}", True, COLOR_TEXTO)
                ventana.blit(texto_identificador, ((tanque.x + 0.5) * TAMANO_CELDA - texto_identificador.get_width() // 2, (tanque.y + 0.25) * TAMANO_CELDA))

                # Dibujar las trayectorias de los disparos
                for trayectoria in trayectorias:
                    for (x, y) in trayectoria:
                        pygame.draw.circle(ventana, COLOR_DISPARO, ((x + 0.5) * TAMANO_CELDA, (y + 0.5) * TAMANO_CELDA), 5)

                # Dibujar las posiciones de los disparos específicos
                for (x, y) in disparos_especificos:
                    pygame.draw.circle(ventana, COLOR_DISPARO, ((x + 0.5) * TAMANO_CELDA, (y + 0.5) * TAMANO_CELDA), 5)

                # Dibujar las áreas de radar
                for area in radar_areas:
                    for (x, y) in area:
                        pygame.draw.circle(ventana, COLOR_RADAR, ((x + 0.5) * TAMANO_CELDA, (y + 0.5) * TAMANO_CELDA), 5)
                radar_areas.clear()  # Borrar las áreas de radar después de mostrarlas

                # Mostrar la tabla de estado del tanque en el lado derecho de la pantalla
                fuente = pygame.font.SysFont(None, 24)
                y_texto = tanque.numero * 100 + 50
                texto_estado = fuente.render(f"Tanque {tanque.numero + 1}", True, COLOR_TEXTO)
                ventana.blit(texto_estado, (COLUMNAS * TAMANO_CELDA + 20, y_texto))
                y_texto += 20
                texto_instruccion = fuente.render(f"Instrucción: {instruccion}", True, COLOR_TEXTO)
                ventana.blit(texto_instruccion, (COLUMNAS * TAMANO_CELDA + 20, y_texto))
                y_texto += 20
                texto_vida = fuente.render(f"Vida: {tanque.vida}", True, COLOR_TEXTO)
                ventana.blit(texto_vida, (COLUMNAS * TAMANO_CELDA + 20, y_texto))
                y_texto += 20
                texto_recargas = fuente.render(f"Recargas: {tanque.recargas}", True, COLOR_TEXTO)
                ventana.blit(texto_recargas, (COLUMNAS * TAMANO_CELDA + 20, y_texto))

                # Mostrar el daño recibido en el último disparo
                y_texto += 20
                texto_ultimo_danio = fuente.render(f"Daño Recibido: {tanque.ultimo_danio}", True, COLOR_TEXTO)
                ventana.blit(texto_ultimo_danio, (COLUMNAS * TAMANO_CELDA + 20, y_texto))

        # Verificar si solo queda un tanque vivo
        tanques_vivos = [tanque for tanque in tanques if tanque.esta_vivo()]
        if len(tanques_vivos) == 1:
            ganador = tanques_vivos[0]
            ventana_ganador(ganador)
            fin_simulacion = True

        pygame.display.flip()
        reloj.tick(1)

    pygame.quit()

def ventana_ganador(tanque_ganador):
    # Mostrar ventana de ganador
    ventana_ganador = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("¡Tenemos un ganador!")
    fuente = pygame.font.SysFont(None, 48)
    texto_ganador = fuente.render(f"¡El Tanque {tanque_ganador.numero + 1} es el ganador!", True, (0, 255, 0))
    ventana_ganador.blit(imagen_fondo_interfaz, (0, 0))
    ventana_ganador.blit(texto_ganador, (ANCHO_VENTANA // 2 - texto_ganador.get_width() // 2, ALTO_VENTANA // 2 - texto_ganador.get_height() // 2))
    pygame.display.flip()
    pygame.mixer.Sound.play(sonido_ganador)
    time.sleep(5)
    pygame.quit()

# Mostrar el tablero
mostrar_tablero()

