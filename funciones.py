import tkinter as tk
from tkinter.messagebox import showinfo


def pop_up_msg(mensaje):
    win = tk.Toplevel()
    win.wm_title("Window")

    l = tk.Label(win, text=mensaje)
    l.pack(pady=5)

    b = tk.Button(win, text="Ok", command=win.destroy)
    b.pack(pady=5)

#devuelve el nivel que se encuentra el jugador
def getNivel(ptosExperiencia):
    if(ptosExperiencia < 150):
        return 1
    else:
        nivel = abs((ptosExperiencia-100)//50)+1
        return nivel

#devuelve los puntos de experiencia necesarios para subir de nivel
def nextLvl(nivel):
    ptos=nivel*50+100
    return ptos
