from __future__ import unicode_literals
from conexion import conectar
from conexion import conexionEjemplo
import psycopg2

def inputEmail():
    conn = conectar()
    cur = conn.cursor()
    repetido = True
    while repetido == True :
        repetido = False
        print("Ingrese email : ")
        mail = input()
        cur.execute("select correo from administrador ")
        # recorremos el cursor en la tabla de administrador
        for administrador in cur :
            if(administrador[0]==mail):
                print("Correo ingresado esta asociado a otra cuenta, intente con otro.")
                repetido = True
        #si no se encuentra ningun administrador con el nick correspondiente,
        #recorremos a los jugadores       
        if(repetido==False):
            cur.execute("select correo from jugador ")
            for jugador in cur:
                if(jugador[0]==mail):
                    print("Correo ingresado esta asociado a otra cuenta, intente con otro.")
                    repetido = True
        if repetido == False:
            cur.close()
            conn.close()
            return mail   
    

def IniciarSesion(nick,password) :
    inicio= False
    perfil = None
    conn = conectar()
    cur = conn.cursor()
    cur.execute("select nick,contraseña from administrador ")
    # recorremos el cursor en la tabla de administrador
    for administrador in cur :
        if(administrador[0]==nick):
            if(administrador[1]==password):
                print("\n Bienvenido "+nick+"\n")
                inicio=True
                perfil = "administrador"
    #si no se encuentra ningun administrador con el nick correspondiente,
    #recorremos a los jugadores       
    if(inicio==False):
        cur.execute("select nick,contraseña from jugador ")
        for jugador in cur:
            if(jugador[0]==nick):
                if(jugador[1]==password):
                    print("\n Bienvenido "+nick+"\n")
                    inicio=True
                    perfil = "jugador"
    conn.close()                    
    return perfil