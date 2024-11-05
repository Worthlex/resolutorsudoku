import pygame
import sys
import time

pygame.font.init()

# Verificamos si el número es válido en la celda
def esValido(bo, num, pos):
    # Verificamos la fila
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Verificamos la columna
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Verificamos el cuadrante 3x3
    cuad_x = pos[1] // 3
    cuad_y = pos[0] // 3

    for i in range(cuad_y * 3, cuad_y * 3 + 3):
        for j in range(cuad_x * 3, cuad_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True

# Encontramos una celda vacía
def encontrarCeldaVacia(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # fila, columna
    return None

# Resolver Sudoku gráficamente paso a paso
def resolverSudokuGrafico(ventana, tablero):
    find = encontrarCeldaVacia(tablero)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if esValido(tablero, i, (row, col)):
            tablero[row][col] = i
            dibujarTablero(ventana, tablero, time.time() - inicio_tiempo)  # Actualizamos tablero
            pygame.display.update()
            pygame.time.delay(50)  # Pausa para ver el proceso

            # Se devuelve el control al bucle principal para actualizar el cronómetro
            if resolverSudokuGrafico(ventana, tablero):
                return True

            tablero[row][col] = 0  # Retroceso
            dibujarTablero(ventana, tablero, time.time() - inicio_tiempo)  # Actualizamos tablero
            pygame.display.update()
            pygame.time.delay(50)

    return False

# Dibujamos el tablero
def dibujarTablero(ventana, tablero, tiempo):
    ventana.fill((255, 255, 255))
    pygame.draw.rect(ventana, (0, 0, 0), (50, 50, 450, 450), 2)
    # (0,0,0) es el color
    # Dibujamos los números del tablero
    for i in range(9):
        for j in range(9):
            if tablero[i][j] != 0:
                pygame.draw.rect(ventana, (0, 0, 0), (50 + j * 50, 50 + i * 50, 50, 50), 2)
                text = fuente.render(str(tablero[i][j]), 1, (0, 0, 0))
                text_rect = text.get_rect(center=(50 + j * 50 + 25, 50 + i * 50 + 25))
                ventana.blit(text, text_rect)

    # Dibujamos las líneas de la cuadrícula
    for i in range(10):
        grosor = 4 if i % 3 == 0 else 2
        pygame.draw.line(ventana, (0, 0, 0), (50, 50 + i * 50), (500, 50 + i * 50), grosor)
        pygame.draw.line(ventana, (0, 0, 0), (50 + i * 50, 50), (50 + i * 50, 500), grosor)

    # Dibujamos el tiempo en pantalla
    tiempo_texto = fuente.render("Tiempo: " + str(int(tiempo)) + " s", 1, (0, 0, 0))
    ventana.blit(tiempo_texto, (50, 520))

# Inicializamos el tablero
tablero = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Inicializamos la ventana
ventana = pygame.display.set_mode((550, 650))
pygame.display.set_caption("Resolutor de Sudoku con Backtracking")
fuente = pygame.font.SysFont("comicsans", 40)

# Reloj para medir el tiempo de resolución
inicio_tiempo = time.time()

# Variable para rastrear si el Sudoku ha sido resuelto
sudoku_resuelto = False
tiempo_final = 0  # Variable para almacenar el tiempo final

# Mantenemos la ventana abierta y actualizamos el tiempo
while True:
    # Actualiza el tiempo solo si el Sudoku no ha sido resuelto
    if not sudoku_resuelto:
        tiempo_actual = time.time() - inicio_tiempo
    else:
        tiempo_actual = tiempo_final

    dibujarTablero(ventana, tablero, tiempo_actual)

    # Solo intentar resolver el Sudoku si no ha sido resuelto
    if not sudoku_resuelto:
        sudoku_resuelto = resolverSudokuGrafico(ventana, tablero)
        if sudoku_resuelto:  # Si se resuelve, guardamos el tiempo
            tiempo_final = time.time() - inicio_tiempo  # Guardamos el tiempo en el momento de resolución

    # Si el Sudoku está resuelto, mantenemos la ventana abierta
    if sudoku_resuelto:
        pygame.display.update()
        # Mantener la ventana abierta hasta que el usuario cierre
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    pygame.display.update()