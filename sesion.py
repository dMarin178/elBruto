import tkinter as tk
from tkinter.messagebox import showinfo
from functools import partial
import tkinter.font as tkFont
from controller import getAvatar
from controller import report
from controller import getReportados
from controller import getOponente
from controller import banPlayer
from controller import subirExperiencia
from controller import subirStats
from funciones import pop_up_msg
from funciones import getNivel
from funciones import nextLvl
from controller import gastarPelea
from controller import getIntentos
from bloques_Procedimientos import actualizar_nivel
from bloques_Procedimientos import isBanned
from bloques_Procedimientos import porc_toxicos
from bloques_Procedimientos import top3
from bloques_Procedimientos import jugador_A_Admin
from bloques_Procedimientos import check_toxic


import random

def menuJugador(nick):
    sesionJugador = tk.Tk()
    sesionJugador.title("Perfil de "+nick)
    sesionJugador.geometry("400x400")
    #titulo del menu
    sesionJugador.configure(background = 'black')

    avatar= getAvatar(nick)
    check_toxic()

    titulo = tk.Label(sesionJugador, text = nick ,bg='black',fg='white', font= tkFont.Font(size=20))
    titulo.pack(pady=20)

    ptsAtck = tk.Label(sesionJugador ,text="Puntos de ataque : "+str(avatar[1]),bg='black',fg='white')
    ptsAtck.pack(pady=5)

    ptsDef = tk.Label(sesionJugador,text="Puntos de velocidad : "+str(avatar[2]),bg='black',fg='white')
    ptsDef.pack(pady=5)

    ptosVel = tk.Label(sesionJugador,text="Puntos de vida : "+str(avatar[3]),bg='black',fg='white')
    ptosVel.pack(pady=5)

    lvl = tk.Label(sesionJugador,text="nivel : "+ str(getNivel(avatar[4])),bg='black',fg='white')
    lvl.pack(pady=5)

    ptosExp=tk.Label(sesionJugador,text="experiencia : "+str(avatar[4])+"/"+str(nextLvl(getNivel(avatar[4]))) ,bg='black',fg='white')
    ptosExp.pack(pady=5)

    reportarJugador = tk.Button(sesionJugador ,text="Reportar jugador",command=reportPlayer)
    reportarJugador.pack(pady=10)

    luchar= tk.Button(sesionJugador,text="Luchar",command=lambda: puedeLuchar(nick))
    luchar.pack(pady=10)

    cerrarSesion= tk.Button(sesionJugador,text="Cerrar sesion",command=sesionJugador.destroy)
    cerrarSesion.pack(pady=10)

    sesionJugador.mainloop()

def puedeLuchar(nick):
    if(getIntentos(nick)>0):
        oponente = getOponente(nick)
        if(oponente!=None):
            gastarPelea(nick)
            windowLucha(nick,oponente)
        else: pop_up_msg("No hay oponente que cumpla los requisitos")   
    else:
        pop_up_msg("Gastaste todas las luchas del dia, vuelve mañana.")


def windowLucha(nick,oponente):
    ventanaLucha = tk.Tk()
    ventanaLucha.title("Batalla")
    ventanaLucha.geometry("220x150")
    ventanaLucha.configure(background = 'black')

    avatar=getAvatar(nick)
    nivel_actual = avatar[5]
    victoria=luchar(avatar,oponente)
    labelBatalla=tk.Label(ventanaLucha,text=" Se enfrento "+nick+" lvl "+str(nivel_actual)+" contra "+oponente[0]+" lvl "+str(getNivel(oponente[4])),bg="black",fg="white" )
    labelBatalla.pack(pady=5)
    if(victoria):
        labelResultado=tk.Label(ventanaLucha,text=" VICTORIA! , ganas: 100 exp",bg="black",fg="white")
        labelResultado.pack(pady=10)
        subirExperiencia(nick,100)
        actualizar_nivel(nick)
    else:
        labelResultado=tk.Label(ventanaLucha,text=" DERROTA , ganas: 20 exp",bg="black",fg="white")
        labelResultado.pack(pady=10)
        subirExperiencia(nick,20)
        #stats despues de la pelea
        actualizar_nivel(nick)
    if(nivel_actual < getNivel(avatar[4])):
        #si es 1: sube atck , si es 2: sube velocidad , si es 3: sube vida
        sube=random.randint(1,3)
        if(sube==1):
            subirStats(nick,"ataque")
        elif sube==2:
            subirStats(nick,"velocidad")
        else:
            subirStats(nick,"vida")
        labelSubirLvl=tk.Label(ventanaLucha,text=" Subiste de nivel ",bg="black",fg="white" )
        labelSubirLvl.pack()
    btnSalir = tk.Button(ventanaLucha,text = "Salir", command = ventanaLucha.destroy )
    btnSalir.pack(pady=10)


#Funcion de pelea, si el jugador gana, devuelve True , si no , devuelve False
def luchar(jugador,oponente):
    #jugador = nick,ataque,velocidad,vida,experiencia
    #oponente= nick,ataque,velocidad,vida
    vidaJugador=jugador[3]
    vidaOponente=oponente[3]
    while(vidaJugador>=0 and vidaOponente>=0):
        if(jugador[2]>=oponente[2]):
            if(falla(oponente[2])):
                vidaOponente=vidaOponente-jugador[1]
                print("vida oponente: "+str(vidaOponente))
                if(vidaOponente<=0):
                    return True
            else:
                print("Fallo ataque de "+ jugador[0])
            if(falla(jugador[2])):
                vidaJugador=vidaJugador-oponente[1]
                print("vida jugador: "+str(vidaJugador))
                if(vidaJugador<=0):
                    return  False
            else:
                print("Fallo ataque de "+ oponente[0])
        else:
            if(falla(jugador[2])):
                vidaJugador=vidaJugador-oponente[1]
                print("vida jugador :"+str(vidaJugador))
                if(vidaJugador<=0):
                    return False
            else:
                print("Fallo ataque de "+ oponente[0])
            if(falla(oponente[2])):
                vidaOponente=vidaOponente-jugador[1]
                print("vida oponente: "+str(vidaOponente))
                if(vidaOponente<=0):
                    return True
            else:
                print("Fallo ataque de "+ jugador[0])

#Funcion de fallo aleatorio dependiendo la velocidad
def falla(velocidad):
    if(velocidad>=80):
        probEsquivar=0.8
    else:
        probEsquivar=velocidad*0.01
    if(probEsquivar < random.random()):
        return True
    else:
        return False


def reportPlayer():
    reportWindow = tk.Tk()
    reportWindow.title("Reportar Jugador")
    reportWindow.geometry("280x200")
    reportWindow.configure(background = 'black')

    reportText = tk.Label(reportWindow,text = 'Ingrese el nick del jugador que desea reportar ',bg='black', fg='white')
    reportText.pack(pady=10)

    reportEntry = tk.Entry(reportWindow)
    reportEntry.pack(pady=5)

    def reportSinParametros():
        reportNick = reportEntry.get()
        if report(reportNick) == False:
            pop_up_msg("No se encontro al jugador. ")
        else: pop_up_msg("Jugador reportado ")

    reportButton = tk.Button(reportWindow, text='Reportar', command=reportSinParametros)
    reportButton.pack(pady=10)

    backButton = tk.Button(reportWindow,text="Volver", command=reportWindow.destroy)
    backButton.pack(pady=10)
    
    reportWindow.mainloop()

def menuAdmin(nick):
    sesionAdmin = tk.Tk()
    sesionAdmin.title("Administrador "+nick)
    sesionAdmin.geometry("400x600")
    #titulo del menu
    sesionAdmin.configure(background = 'black')

    titulo = tk.Label(sesionAdmin, text = "Bienvenido "+nick ,bg='black',fg='white', font= tkFont.Font(size=20))
    titulo.pack(pady=20)

    check_toxic()

    labelReportPlayers = tk.Label(sesionAdmin ,text="Lista de jugadores : ",bg='black',fg='white')
    labelReportPlayers.pack(pady=5)

    reportados = getReportados()
    for jugador in reportados:
        if(jugador[1] != 0):
            if(isBanned(jugador[0])==True):
                label_toxic = tk.Label(sesionAdmin, text = "JUGADOR TOXICO",bg='black' ,fg='white')
                label_toxic.pack()
            labelJugador = tk.Label(sesionAdmin,text= jugador[0]+" - Cantidad de reportes : "+str(jugador[1]), bg='black' ,fg='white')
            labelJugador.pack(pady=2)
            separador = tk.Label(sesionAdmin,text="-------------------------------",bg='black' ,fg='white')
            separador.pack()
    toxicos = tk.Label(sesionAdmin,text="Porcentaje de jugadores toxicos: "+str(round(porc_toxicos(),2))+"%",bg='black' ,fg='white')
    toxicos.pack()       

    topTitle= tk.Label(sesionAdmin,text="TOP 3 JUGADORES ",bg='black' ,fg='white')
    topTitle.pack(pady=10)
    top_lvl=top3()
    for i in range(3) :
        top= tk.Label(sesionAdmin,text= str(i+1)+"-"+str(top_lvl[i][0])+" , nivel :"+str(top_lvl[i][1]),bg='black' ,fg='white')
        top.pack()

    reportarJugador = tk.Button(sesionAdmin ,text="Bannear un jugador ",command=banWindow)
    reportarJugador.pack(pady=10)

    assenderJugador = tk.Button(sesionAdmin, text = "Cambiar jugador a administrador", command = asender_jugador_window )
    assenderJugador.pack(pady=10)

    cerrarSesion= tk.Button(sesionAdmin,text="Cerrar sesion",command=sesionAdmin.destroy)
    cerrarSesion.pack(pady=10)
    sesionAdmin.mainloop()

def banWindow():
    banWindow = tk.Tk()
    banWindow.title("Ban Window")
    banWindow.geometry("200x150")
    banWindow.configure(background = "black")

    titulo = tk.Label(banWindow,text="Nick del jugador que quiere banear",bg='black',fg='white')
    titulo.pack(pady=5)

    jugadorEntry = tk.Entry(banWindow)
    jugadorEntry.pack(pady=5)

    def executeBan():
        if(banPlayer(jugadorEntry.get())):
            pop_up_msg(jugadorEntry.get()+" a sido baneado")
        else:pop_up_msg("Nick ingresado no existe")

    banButton = tk.Button(banWindow,text="Banear jugador", command=executeBan)
    banButton.pack(pady=5)
    exitButton = tk.Button(banWindow,text="Salir", command=banWindow.destroy)
    exitButton.pack(pady=10)

def asender_jugador_window():
    asender_jugador_window = tk.Tk()
    asender_jugador_window.title("Jugador a Admin")
    asender_jugador_window.geometry("300x150")
    asender_jugador_window.configure(background = "black")

    titulo = tk.Label(asender_jugador_window,text="Nick del jugador que quiere cambiar a administrador",bg='black',fg='white')
    titulo.pack(pady=5)

    jugadorEntry = tk.Entry(asender_jugador_window)
    jugadorEntry.pack(pady=5)

    def jugadorAdmin():
        jugador_A_Admin(jugadorEntry.get())
        pop_up_msg("Jugador "+jugadorEntry.get()+ " ahora es administador")

    confirm_button = tk.Button(asender_jugador_window,text="Confirmar",command=jugadorAdmin )
    confirm_button.pack(pady=5)
    
    exit_button = tk.Button(asender_jugador_window,text="Salir",command=asender_jugador_window.destroy )
    exit_button.pack(pady=5)
        

