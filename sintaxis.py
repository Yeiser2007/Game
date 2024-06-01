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

if __name__ == "__main__":
    nombres_archivos = ["Instrucciones/tanque1.txt", "Instrucciones/tanque2.txt", "Instrucciones/tanque3.txt",
                        "Instrucciones/tanque4.txt"]
    archivos = [open(nombre_archivo, 'r') for nombre_archivo in nombres_archivos]
    indices = [0] * len(nombres_archivos)

    while True:
        instrucciones = leer_proxima_instruccion(archivos, indices)
        if not instrucciones:
            break  # Se han leído todas las instrucciones de todos los archivos

        print("Instrucciones en esta ronda:")
        for instruccion, indice_archivo in instrucciones:
            print(f"Instrucción: {instruccion} (Archivo: {nombres_archivos[indice_archivo]})")
            comando, parametros = separar_parametros(instruccion)
            for parametro in parametros:
                print(f"Parámetro: {parametro.strip()}")
            validar_dos_parametros(instruccion)
            print()

    # Cerrar todos los archivos
    for archivo in archivos:
        archivo.close()