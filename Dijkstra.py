
#---------------------------------------LIBRERÍAS---------------------------------------#
import pygame
import sys
import math
import tkinter.messagebox as tkMessageBox
import tkinter as tk
from tkinter import ttk

#------------------------------------INTERFAZ GRÁFICA------------------------------------#
#------------------------------------Ventana Principal-----------------------------------#
pygame.init()
ancho_ventana = 500
alto_ventana = 500

ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
fuente = pygame.font.SysFont(None, 30)
Color = (255, 255, 255)

#_______________________Color de los nodos________________________________#     
colores = {
    "fondo": (255, 255, 255),
    "obstaculo": (24, 23, 28),
    "visitado": (180, 180, 180),
    "camino": (50, 90, 140),
    "inicio": (0, 128, 0),
    "objetivo": (199, 29, 41)
}

def rgb_a_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

#_______________________Texto en pantalla________________________________#     
def dibujar_texto(texto, pos_x, pos_y):
    texto_renderizado = fuente.render(texto, True, (0, 0, 0))
    ventana.blit(texto_renderizado, (pos_x, pos_y))

columnas = 10
filas = 10

ancho_nodo = ancho_ventana // columnas
alto_nodo = alto_ventana// filas

# Matrices
cuadricula = []
cola = []
camino = []


#_______________________Booleanos de control de nodos_______________________________#     
class Lienzo:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.inicio = False
        self.obstaculo = False
        self.objetivo = False
        self.vecinos = []
        self.distancia_desde_inicio = float('inf')
        self.visitado = False
        self.prioridad = None

    def dibujar(self, ventana, color):
        pygame.draw.rect(ventana, color, (self.x * ancho_nodo,
                                           self.y * alto_nodo, ancho_nodo - 2, alto_nodo - 2))        
#---------------------MÉTODO PARA GUARDAR VECINOS EN TODOS LOS EJES--------------------------#

    def establecer_vecinos(self):
        if self.x > 0:
            self.vecinos.append(cuadricula[self.x - 1][self.y])
        if self.x < columnas - 1:
            self.vecinos.append(cuadricula[self.x + 1][self.y])
        if self.y > 0:
            self.vecinos.append(cuadricula[self.x][self.y - 1])
        if self.y < filas - 1:
            self.vecinos.append(cuadricula[self.x][self.y + 1])

        if self.x > 0 and self.y > 0:
            self.vecinos.append(cuadricula[self.x - 1][self.y - 1])
        if self.x > 0 and self.y < filas - 1:
            self.vecinos.append(cuadricula[self.x - 1][self.y + 1])
        if self.x < columnas - 1 and self.y > 0:
            self.vecinos.append(cuadricula[self.x + 1][self.y - 1])
        if self.x < columnas - 1 and self.y < filas - 1:
            self.vecinos.append(cuadricula[self.x + 1][self.y + 1])


for i in range(columnas):
    fila = []
    for j in range(filas):
        fila.append(Lienzo(i, j))
    cuadricula.append(fila)

for i in range(columnas):
    for j in range(filas):
        cuadricula[i][j].establecer_vecinos()

#----------------------------------VENTANA SECUNDARIA INFORMATIVA------------------------------------#

# Función para abrir la ventana secundaria
def abrir_ventana_secundaria(colores):
    # Crear una ventana secundaria.
    ventana_secundaria = tk.Toplevel()
    # Obtener las dimensiones de la ventana principal
    ventana_principal_dimensiones = ventana.get_rect()

    # Calcular la posición de la ventana secundaria
    pos_x_ventana_secundaria = ventana_principal_dimensiones.left  # A 80 pixeles a la izquierda de la ventana principal
    pos_y_ventana_secundaria = ventana_principal_dimensiones.centery  # Centrada en el eje Y de la ventana principal

    # Crear la ventana secundaria con la posición calculada
    ventana_secundaria.geometry(f"+{pos_x_ventana_secundaria + 80}+{pos_y_ventana_secundaria}")
    # Eliminar menú
    ventana_secundaria.overrideredirect(True)

    lienzo = tk.Canvas(ventana_secundaria, width= ancho_ventana //2 , height=alto_ventana //2)
    lienzo.pack()

    # Coordenadas y dimensiones de los rectángulos
    x = 20  # Coordenada x inicial
    y = 60  # Coordenada y inicial 
    ancho = ancho_nodo /2 # Ancho de los rectángulos, ajustado para dejar espacio en los márgenes
    alto = alto_nodo /2 # Alto de los rectángulos, dividido por el número de colores + título

    # Dibujar píxeles de colores verticalmente en el lienzo
    espacio = lienzo.create_rectangle(x, y, x + ancho, y + alto, fill=rgb_a_hex(colores["fondo"]))  # Espacio
    lienzo.create_rectangle(x, y + alto, x + ancho, y + 2 * alto, fill=rgb_a_hex(colores["inicio"]))  # Nodo inicial
    lienzo.create_rectangle(x, y + 2 * alto, x + ancho, y + 3 * alto, fill=rgb_a_hex(colores["objetivo"]))  # Nodo objetivo
    lienzo.create_rectangle(x, y + 3 * alto, x + ancho, y + 4 * alto, fill=rgb_a_hex(colores["obstaculo"]))  # Nodo obstaculo
    lienzo.create_rectangle(x, y + 4 * alto, x + ancho, y + 5 * alto, fill=rgb_a_hex(colores["visitado"]))  # Nodos visitados
    lienzo.create_rectangle(x, y + 5 * alto, x + ancho, y + 6 * alto, fill=rgb_a_hex(colores["camino"]))  # Nodos visitados    

    # Texto sobre los cuadrados 
    lienzo.create_text(120, 20, anchor=tk.CENTER, text="Nodos por color", font=("Arial", 16, "bold"))  # Título
    lienzo.create_text(80, y + 1.5 * alto, anchor=tk.W, text="inicio", font=("Arial", 12, "bold"))  # Nodo inicial
    lienzo.create_text(80, y + 2.5 * alto, anchor=tk.W, text="objetivo", font=("Arial", 12, "bold"))  # Nodo objetivo
    lienzo.create_text(80, y + 3.5 * alto, anchor=tk.W, text="obstaculo", font=("Arial", 12, "bold"))  # Nodo obstaculo
    lienzo.create_text(80, y + 4.5 * alto, anchor=tk.W, text="visitado", font=("Arial", 12, "bold")) # Nodos visitados
    lienzo.create_text(80, y + 5.5 * alto, anchor=tk.W, text="camino", font=("Arial", 12, "bold")) # Nodos visitados

    # Crear espacio
    lienzo.itemconfig(espacio, state="hidden")

#-------------------------------------------IMPRESIÓN DE MENSAJES-------------------------------------------#

def calcular_distancia(nodo1, nodo2):
    distancia = math.sqrt((nodo1.x - nodo2.x) ** 2 + (nodo1.y - nodo2.y) ** 2)
    return distancia

def mostrar_mensaje(titulo, mensaje):
    ventana = tk.Tk()
    ventana.withdraw()
    tkMessageBox.showinfo(titulo, mensaje)


#----------------------------------------------MÉTODO DIJKSTRA -----------------------------------------------#
 
def dijkstra(nodo_inicio, nodo_objetivo):    
    # Paso 1:  Establecer la distancia desde el nodo de inicio a 0 y agregarlo a la cola de prioridad
    nodo_inicio.distancia_desde_inicio = 0
    cola.append(nodo_inicio)

    # Paso 1.1: Mientras haya nodos en la cola de prioridad
    while cola:
        # Ordenar la cola de prioridad según la distancia desde el inicio
        cola.sort(key=lambda nodo: nodo.distancia_desde_inicio)
        # Tomar el nodo con la distancia mínima desde el inicio
        nodo_actual = cola.pop(0)
                  

        # Si el nodo actual es el nodo objetivo, terminar el algoritmo
        if nodo_actual == nodo_objetivo:
            abrir_ventana_secundaria(colores)  # Pasar el diccionario colores como argumento
            # Paso 2: Calcular la distancia recorrida y muestra un mensaje con el resultado
            distancia_recorrida = nodo_actual.distancia_desde_inicio
            mostrar_mensaje("Distancia Recorrida", f"La distancia recorrida es de {distancia_recorrida:.2f} unidades")            
            # Paso 3: Reconstruir el camino desde el nodo objetivo al nodo inicial
            while nodo_actual.prioridad:
                camino.append(nodo_actual)
                nodo_actual = nodo_actual.prioridad
            camino.append(nodo_inicio)
            break

        # Paso 4: Para cada vecino del nodo actual
        for vecino in nodo_actual.vecinos:
            # Si el vecino no es un obstáculo y no ha sido visitado
            if not vecino.obstaculo and not vecino.visitado:                
                # Calcular la distancia desde el inicio hasta el vecino pasando por el nodo actual
                distancia_desde_inicio_hacia_vecino = nodo_actual.distancia_desde_inicio + calcular_distancia(nodo_actual, vecino)
                # Si esta distancia es menor que la distancia almacenada en el vecino
                if distancia_desde_inicio_hacia_vecino < vecino.distancia_desde_inicio:
                    # Actualizar la distancia almacenada en el vecino y establecer al nodo actual como su prioridad
                    vecino.distancia_desde_inicio = distancia_desde_inicio_hacia_vecino
                    vecino.prioridad = nodo_actual
                    # Si el vecino no está en la cola de prioridad agregarlo
                    if vecino not in cola:
                        cola.append(vecino)                        
        # Marcar el nodo actual como visitado para evitar ciclos infinitos
        nodo_actual.visitado = True

#--------------------------------------------BUCLE PRINCIPAL---------------------------------------------#

def main():
    pygame.display.set_caption("Algoritmo de búsqueda de caminos con Dijkstra")
    # Mostrar mensaje con las instrucciones
    mostrar_mensaje("Instrucciones", "Haz clic izquierdo para establecer el nodo de inicio.\nHaz clic derecho para establecer el nodo objetivo.\nHaz clic izquierdo y arrastra para colocar obstáculos.\nPresiona cualquier tecla para iniciar la búsqueda.")


#_________________________Booleanos de control_________________________________#
    objetivo_establecido = False
    inicio_establecido = False
    buscando_camino = False
    nodo_inicio = None
    nodo_objetivo = None
#_______________________Controles del programa_________________________________#
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    x, y = pygame.mouse.get_pos()
                    i = x // ancho_nodo
                    j = y // alto_nodo
                    if not inicio_establecido and not cuadricula[i][j].obstaculo:
                        cuadricula[i][j].inicio = True
                        inicio_establecido = True
                        nodo_inicio = cuadricula[i][j]
                        cola.append(nodo_inicio)
                elif event.button == 3:  
                    x, y = pygame.mouse.get_pos()
                    i = x // ancho_nodo
                    j = y // alto_nodo
                    if not objetivo_establecido and not cuadricula[i][j].obstaculo and not cuadricula[i][j].inicio:  
                        cuadricula[i][j].objetivo = True
                        objetivo_establecido = True
                        nodo_objetivo = cuadricula[i][j]           

            elif event.type == pygame.MOUSEMOTION: 
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                if event.buttons[0]:
                    i = x // ancho_nodo
                    j = y // alto_nodo
                    if not cuadricula[i][j].inicio:  
                        cuadricula[i][j].obstaculo = True
                if event.buttons[2] and not objetivo_establecido:
                    i = x // ancho_nodo
                    j = y // alto_nodo
                    cuadricula[i][j].objetivo = True
                    objetivo_establecido = True
                    nodo_objetivo = cuadricula[i][j]
        
#_______________________Catch errors________________________________#
            elif event.type == pygame.KEYDOWN:
                if inicio_establecido and objetivo_establecido:
                    dijkstra(nodo_inicio, nodo_objetivo)
                    if not camino:
                        mostrar_mensaje("Error", "No hay caminos posibles debido a los obstáculos en el camino.")
                    else:
                        buscando_camino = True
                elif not (inicio_establecido and objetivo_establecido):
          
                    mostrar_mensaje("Error", "Debes establecer un nodo de inicio y un nodo objetivo antes de iniciar la búsqueda.")
        
        
#_______________________Impresora de nodos________________________________#        
        ventana.fill((234, 235, 237)) 
        
        for i in range(columnas):
            for j in range(filas):
                lienzo = cuadricula[i][j]
                color = colores["fondo"]  # Color de fondo predeterminado
                if lienzo.obstaculo:
                    color = colores["obstaculo"]  # Color del obstáculo
                if lienzo.visitado:  
                    color = colores["visitado"]  # Color del nodo visitado
                if lienzo in camino:
                    color = colores["camino"]  # Color del camino
                if lienzo.inicio:
                    color = colores["inicio"]  # Color del nodo inicial
                if lienzo.objetivo:
                    color = colores["objetivo"]  # Color del nodo final

                lienzo.dibujar(ventana, color)

        pygame.display.flip()

if __name__ == "__main__":
    main()
