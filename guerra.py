import pygame
import random
import time

# Inicializar pygame y obtener información de la pantalla
pygame.init()
info = pygame.display.Info()
ANCHO_VENTANA, ALTO_VENTANA = info.current_w, info.current_h  # Dimensiones de la pantalla

# Definir constantes
# Definir constantes
FILAS, COLUMNAS = 7, 7
TAMANO_CELDA = min((ANCHO_VENTANA ) // COLUMNAS, (ALTO_VENTANA ) // FILAS)  # Tamaño de celda ajustado

# Posicionar el tablero centrado
MARGEN_X = (ANCHO_VENTANA - (COLUMNAS * TAMANO_CELDA)) // 2
MARGEN_Y = (ALTO_VENTANA - (FILAS * TAMANO_CELDA)) // 2
# Colores
COLOR_FONDO = (255, 255, 255)
COLOR_TEXTO = (0, 0, 0)
COLOR_DISPARO = (255, 0, 0)
COLOR_RADAR = (0, 255, 0)

# Cargar imágenes de tanques, minas y fondo del tablero
imagen_fondo_interfaz = pygame.image.load("Imagenes/fondo.jpg")
imagen_fondo_interfaz = pygame.transform.scale(imagen_fondo_interfaz, (ANCHO_VENTANA, ALTO_VENTANA))
imagen_fondo_tablero = pygame.image.load("Imagenes/tablero.jpeg")
imagen_fondo_tablero = pygame.transform.scale(imagen_fondo_tablero, (COLUMNAS * TAMANO_CELDA, FILAS * TAMANO_CELDA))
imagen_tanque_rojo = pygame.image.load("Imagenes/tanque1.png")
imagen_tanque_verde = pygame.image.load("Imagenes/tanque2.png")
imagen_tanque_azul = pygame.image.load("Imagenes/tanque3.png")
imagen_tanque_amarillo = pygame.image.load("Imagenes/tanque4.png")
imagen_mina = pygame.image.load("Imagenes/mina.png")

imagenes_tanques = [imagen_tanque_rojo, imagen_tanque_verde, imagen_tanque_azul, imagen_tanque_amarillo]
imagen_mina = pygame.transform.scale(imagen_mina, (TAMANO_CELDA, TAMANO_CELDA))

# Cargar sonido de ganador
pygame.mixer.init()
sonido_ganador = pygame.mixer.Sound("audios/felicidades.mp3")
disparo_s = pygame.mixer.Sound("audios/disp.mp3")
radar_s = pygame.mixer.Sound("audios/radar.mp3")
recarga_s = pygame.mixer.Sound("audios/recarga.mp3")
mov_s = pygame.mixer.Sound("audios/giro.mp3")
mina_s = pygame.mixer.Sound("audios/explosion.mp3")
disp_E = pygame.mixer.Sound("audios/disp_e.mp3")
#Leer archivos
nombres_archivos = ["Instrucciones/tanque1.txt", "Instrucciones/tanque2.txt", "Instrucciones/tanque3.txt",
                    "Instrucciones/tanque4.txt"]


# Clase Tanque
class Tanque:
    def __init__(self, numero, x, y, imagen):
        self.numero = numero
        self.x = x
        self.y = y
        self.imagen_original = imagen
        self.imagen = pygame.transform.scale(imagen, (TAMANO_CELDA, TAMANO_CELDA))
        self.danio_recibido = 0
        self.vida = 50
        self.recargas = 0  # Contador de recargas
        self.ultimo_danio = 0  # Daño recibido en el último disparo

    def mover(self, direccion, minas):
        nueva_x, nueva_y = self.x, self.y
        if direccion == "n":
            nueva_y -= 1
            print("se movio al n")
        elif direccion == "s":
            nueva_y += 1
            print("se movio al n")
        elif direccion == "e":
            nueva_x += 1
            print("se movio al n")
        elif direccion == "o":
            nueva_x -= 1

        # Verificar que la nueva posición esté dentro del tablero
        if 0 <= nueva_x < COLUMNAS and 0 <= nueva_y < FILAS:
            # Verificar si la nueva posición está ocupada por otro tanque
            if any(tanque.x == nueva_x and tanque.y == nueva_y for tanque in tanques):
                print(f"Tanque {self.numero} no puede moverse a ({nueva_x}, {nueva_y}). Posición ocupada.")
                self.vida -= 10  # Reducir la vida
            else:
                self.x, self.y = nueva_x, nueva_y
                self.verificar_mina(minas)
        else:
            self.vida -= 10

    def disparar(self, direccion, tanques, trayectorias):
        self.girar(direccion)
        if direccion == "n":
            trayectoria = [(self.x, y) for y in range(self.y - 1, -1, -1)]
        elif direccion == "s":
            trayectoria = [(self.x, y) for y in range(self.y + 1, FILAS)]
        elif direccion == "e":
            trayectoria = [(x, self.y) for x in range(self.x + 1, COLUMNAS)]
        elif direccion == "o":
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

        if direccion == "n":
            x, y = self.x, self.y - valor
        elif direccion == "s":
            x, y = self.x, self.y + valor
        elif direccion == "e":
            x, y = self.x + valor, self.y
        elif direccion == "o":
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
        if direccion == "n":
            posiciones = [(self.x, y) for y in range(self.y - 1, -1, -1)]
        elif direccion == "s":
            posiciones = [(self.x, y) for y in range(self.y + 1, FILAS)]
        elif direccion == "e":
            posiciones = [(x, self.y) for x in range(self.x + 1, COLUMNAS)]
        elif direccion == "o":
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
        if direccion == "n":
            self.imagen = pygame.transform.rotate(self.imagen_original, 0)
        elif direccion == "s":
            self.imagen = pygame.transform.rotate(self.imagen_original, 180)
        elif direccion == "e":
            self.imagen = pygame.transform.rotate(self.imagen_original, 270)
        elif direccion == "o":
            self.imagen = pygame.transform.rotate(self.imagen_original, 90)
        self.imagen = pygame.transform.scale(self.imagen, (TAMANO_CELDA, TAMANO_CELDA))

    def verificar_mina(self, minas):
        for mina in minas:
            if self.x == mina[0] and self.y == mina[1]:
                pygame.mixer.Sound.play(mina_s)
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

def leer_proxima_instruccion(archivos, indices):
    instrucciones = []
    for i, archivo in enumerate(archivos):
        try:
            instruccion = next(archivo).strip()
            instrucciones.append((instruccion, i))  # Guardamos el índice del archivo junto con la instrucción
            indices[i] += 1
        except StopIteration:
            archivo.seek(0)  # Volver al principio del archivo si ya no hay más instrucciones
            indices[i] = 0  # Reiniciar el índice para la próxima ronda
            instruccion = next(archivo).strip()
            instrucciones.append((instruccion, i))  # Guardamos la primera instrucción del archivo
    return instrucciones

def separar_parametros(instruccion):
    if '(' in instruccion:
        comando, parametros = instruccion.split('(')
        parametros = parametros.strip(')').split(',')
    else:
        comando = instruccion
        parametros = []
    return comando, parametros

def validar_dos_parametros(instruccion):
    comando, parametros = separar_parametros(instruccion)
    if len(parametros) == 2:
        print(f"La instrucción '{comando}' tiene dos parámetros: {parametros[0]} y {parametros[1]}")
    else:
        print(f"La instrucción '{comando}' no tiene dos parámetros")

# Crear tanques y minas
tanques = [Tanque(i, random.randint(0, COLUMNAS-1), random.randint(0, FILAS-1), imagen) for i, imagen in enumerate(imagenes_tanques)]
minas = generar_minas(5)
def mostrar_mensaje(ventana, mensaje):
    fuente = pygame.font.SysFont(None, 48)
    texto = fuente.render(mensaje, True, (255, 0, 0))
    ventana.blit(texto, (100, 100))
    pygame.display.flip()
    time.sleep(2)  # Mostrar el mensaje por 2 segundos

def dibujar_cuadricula(ventana, filas, columnas, tamano_celda, color=(0, 0, 0)):
    for x in range(0, columnas * tamano_celda, tamano_celda):
        pygame.draw.line(ventana, color, (x, 0), (x, filas * tamano_celda))
    for y in range(0, filas * tamano_celda, tamano_celda):
        pygame.draw.line(ventana, color, (0, y), (columnas * tamano_celda, y))

def mostrar_tablero():
    ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Simulador de Combate de Tanques")
    nombres_archivos = ["Instrucciones/tanque1.txt", "Instrucciones/tanque2.txt", "Instrucciones/tanque3.txt",
                        "Instrucciones/tanque4.txt"]
    archivos = [open(nombre_archivo, 'r') for nombre_archivo in nombres_archivos]
    indices = [0] * len(nombres_archivos)
    trayectorias = []
    disparos_especificos = []
    radar_areas = []
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

        instrucciones = leer_proxima_instruccion(archivos, indices)
        if not instrucciones:
            break

        for instruccion, indice_archivo in instrucciones:
            if instruccion is None:
                mostrar_mensaje(ventana, f"Tanque {indice_archivo + 1} se quedó sin instrucciones")
                continue

            inst, parametros = separar_parametros(instruccion)
            tanque = tanques[indice_archivo]
            if tanque.esta_vivo():
                if inst == "mov":
                    pygame.mixer.Sound.play(mov_s)
                    for parametro in parametros:
                        tanque.mover(parametro.strip(), minas)
                elif inst == "recarga":
                    pygame.mixer.Sound.play(recarga_s)
                    tanque.recargar()
                elif inst == "rad":
                    print(instruccion)
                    pygame.mixer.Sound.play(radar_s)
                    for parametro in parametros:
                        print(f"Parámetro: {parametro.strip()}")
                        tanque.radar(parametro.strip(), tanques, radar_areas)
                elif inst == "dis_e":
                    pygame.mixer.Sound.play(disp_E)
                    par=[]
                    for parametro in parametros:
                        print(f"Parámetro: {parametro.strip()}")
                        par.append(parametro.strip())
                    print(par)
                    tanque.disparo_especifico(par[0],int(par[1]),tanques,disparos_especificos)
                elif inst == "dis_l":
                    pygame.mixer.Sound.play(disparo_s)
                    for parametro in parametros:
                        tanque.girar(parametro.strip())
                        tanque.disparar(parametro.strip(), tanques, trayectorias)

            # Redibujar el estado de todos los tanques y otros elementos del tablero
            ventana.blit(imagen_fondo_tablero, (0, 0))
            dibujar_cuadricula(ventana, FILAS, COLUMNAS, TAMANO_CELDA)
            for mina in minas:
                ventana.blit(imagen_mina, (mina[0] * TAMANO_CELDA, mina[1] * TAMANO_CELDA))
            for t in tanques:
                ventana.blit(t.imagen, (t.x * TAMANO_CELDA, t.y * TAMANO_CELDA))
                fuente = pygame.font.SysFont(None, 20)
                texto_identificador = fuente.render(f"Tanque {t.numero + 1}", True, COLOR_TEXTO)
                ventana.blit(texto_identificador, (
                (t.x + 0.5) * TAMANO_CELDA - texto_identificador.get_width() // 2, (t.y + 0.25) * TAMANO_CELDA))

            for trayectoria in trayectorias:
                for (x, y) in trayectoria:
                    pygame.draw.circle(ventana, COLOR_DISPARO, ((x + 0.5) * TAMANO_CELDA, (y + 0.5) * TAMANO_CELDA), 5)
            trayectorias.clear()

            for (x, y) in disparos_especificos:
                pygame.draw.circle(ventana, COLOR_DISPARO, ((x + 0.5) * TAMANO_CELDA, (y + 0.5) * TAMANO_CELDA), 18)
            disparos_especificos.clear()

            for area in radar_areas:
                for (x, y) in area:
                    pygame.draw.circle(ventana, COLOR_RADAR, ((x + 0.5) * TAMANO_CELDA, (y + 0.5) * TAMANO_CELDA), 10)
            radar_areas.clear()

            fuente = pygame.font.SysFont(None, 24)
            for t in tanques:
                y_texto = t.numero * 100 + 50
                texto_estado = fuente.render(f"Tanque {t.numero + 1}", True, COLOR_TEXTO)
                ventana.blit(texto_estado, (ANCHO_VENTANA - 200, y_texto))
                y_texto += 20
                texto_vida = fuente.render(f"Vida: {t.vida}", True, COLOR_TEXTO)
                ventana.blit(texto_vida, (ANCHO_VENTANA - 200, y_texto))
                y_texto += 20
                texto_recargas = fuente.render(f"Recargas: {t.recargas}", True, COLOR_TEXTO)
                ventana.blit(texto_recargas, (ANCHO_VENTANA - 200, y_texto))
                y_texto += 20
                texto_ultimo_danio = fuente.render(f"Daño Recibido: {t.ultimo_danio}", True, COLOR_TEXTO)
                ventana.blit(texto_ultimo_danio, (ANCHO_VENTANA - 200, y_texto))

            pygame.display.flip()
            time.sleep(2)  # Pausa después de cada instrucción

        tanques_vivos = [tanque for tanque in tanques if tanque.esta_vivo()]
        if len(tanques_vivos) == 1:
            ganador = tanques_vivos[0]
            ventana_ganador(ganador)
            fin_simulacion = True

        reloj.tick(10)  # Reducido a 10 FPS para hacerlo más lento

    for archivo in archivos:
        archivo.close()

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