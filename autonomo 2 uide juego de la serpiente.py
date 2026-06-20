import tkinter as tk
import random

# Configuración panel
ANCHO = 450
ALTO  = 450
CELDA = 15
VELOCIDAD = 190   # conf milisegundos

# Estado del juego
serpiente    = []
direccion    = [0, 1]
comida       = []
puntaje      = 0
juego_activo = False

# Inicializar / Reiniciar
def inicializar_juego():
    global serpiente, direccion, comida, puntaje, juego_activo

    serpiente    = [[10, 10], [10, 9], [10, 8]]
    direccion    = [0, 1]
    puntaje      = 0
    juego_activo = True

    generar_comida()
    label_puntaje.config(text="Puntaje: 0")

def generar_comida():
    global comida
    filas = ALTO // CELDA
    cols  = ANCHO // CELDA
    while True:
        f = random.randint(0, filas - 1)
        c = random.randint(0, cols  - 1)
        if [f, c] not in serpiente:
            comida = [f, c]
            break

# Controles de teclado
def cambiar_direccion(event):
    global direccion
    if not juego_activo:
        return
    teclas = {
        "Up":    [-1,  0],
        "Down":  [ 1,  0],
        "Left":  [ 0, -1],
        "Right": [ 0,  1],
    }
    nueva = teclas.get(event.keysym)
    # Evitar dirección opuesta
    if nueva and (direccion[0] + nueva[0] != 0 or direccion[1] + nueva[1] != 0):
        direccion = nueva

# Lógica principal (gameloop)
def gameloop():
    global puntaje, juego_activo

    if not juego_activo:
        return

    # Mover serpiente
    cabeza_nueva = [
        serpiente[0][0] + direccion[0],
        serpiente[0][1] + direccion[1],
    ]
    serpiente.insert(0, cabeza_nueva)

    # ¿Comió comida?
    if cabeza_nueva == comida:
        puntaje += 1
        label_puntaje.config(text=f"Puntaje: {puntaje}")
        generar_comida()
        # No se elimina el último segmento → serpiente crece
    else:
        serpiente.pop()   # Eliminar último segmento (movimiento normal)

    # Detectar colisión con paredes o consigo misma
    fila, col = cabeza_nueva
    filas = ALTO // CELDA
    cols  = ANCHO // CELDA
    if (fila < 0 or fila >= filas or col < 0 or col >= cols
            or cabeza_nueva in serpiente[1:]):
        juego_activo = False
        mostrar_game_over()
        return

    # Renderizar
    renderizar()

    # Controlar velocidad (delay)
    ventana.after(VELOCIDAD, gameloop)

# Renderizado en pantalla
def renderizar():
    canvas.delete("all")

    # Comida
    c0 = comida[1] * CELDA
    f0 = comida[0] * CELDA
    canvas.create_oval(c0+2, f0+2, c0+CELDA-2, f0+CELDA-2, fill="red", outline="")

    # Serpiente
    for i, seg in enumerate(serpiente):
        x = seg[1] * CELDA
        y = seg[0] * CELDA
        color = "#0025cc" if i == 0 else "#1a00aa"
        canvas.create_rectangle(x+1, y+1, x+CELDA-1, y+CELDA-1, fill=color, outline="")

def mostrar_game_over():
    renderizar()
    cx, cy = ANCHO // 2, ALTO // 2
    canvas.create_text(cx, cy - 15, text="GAME OVER",
                       fill="white", font=("Arial", 20, "bold"))
    canvas.create_text(cx, cy + 15,
                       text=f"Puntaje: {puntaje}  |  Enter para reiniciar",
                       fill="white", font=("Arial", 11))

def iniciar_o_reiniciar(event=None):
    inicializar_juego()
    gameloop()

# Configurar ventana Tkinter
ventana = tk.Tk()
ventana.title("Juego de la Serpiente Autonomo 2")
ventana.resizable(False, False)

label_puntaje = tk.Label(ventana, text="Puntaje: 0", font=("Arial", 13))
label_puntaje.pack()

canvas = tk.Canvas(ventana, width=ANCHO, height=ALTO, bg="#1a1a2e")
canvas.pack()

tk.Label(ventana, text="Flechas: mover  |  Enter: iniciar/reiniciar",
font=("Arial", 9), fg="gray").pack()

ventana.bind("<Up>",    cambiar_direccion)
ventana.bind("<Down>",  cambiar_direccion)
ventana.bind("<Left>",  cambiar_direccion)
ventana.bind("<Right>", cambiar_direccion)
ventana.bind("<Return>", iniciar_o_reiniciar)

# Mensaje inicial
canvas.create_text(ANCHO // 2, ALTO // 2, text="Presione ENTER para iniciar",
fill="white", font=("Arial", 14))

ventana.mainloop()