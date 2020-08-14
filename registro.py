import tkinter as tk
from tkinter.messagebox import showinfo
from controller import RegistrarUsuario
from controller import generarAvatar

def registro():

    ventanaRegistro = tk.Tk()
    ventanaRegistro.title("Registro de cuenta nueva ")
    ventanaRegistro.geometry("400x500")
    ventanaRegistro.configure(background = 'black')

    nickLabel = tk.Label(ventanaRegistro, text="Ingrese su Nick",bg='black',fg='white')
    nickLabel.pack()
    nickEntry = tk.Entry(ventanaRegistro)
    nickEntry.pack()

    emailLabel = tk.Label(ventanaRegistro, text="Ingrese su correo electronico",bg='black',fg='white')
    emailLabel.pack()
    emailEntry = tk.Entry(ventanaRegistro)
    emailEntry.pack()

    passLabel = tk.Label(ventanaRegistro, text="Ingrese su Contraseña",bg='black',fg='white')
    passLabel.pack()
    passEntry = tk.Entry(ventanaRegistro,show ="*")
    passEntry.pack()

    pass2Label = tk.Label(ventanaRegistro, text="Ingrese su Contraseña otra vez",bg='black',fg='white')
    pass2Label.pack()
    pass2Entry = tk.Entry(ventanaRegistro,show ="*")
    pass2Entry.pack()

    nombreLabel = tk.Label(ventanaRegistro, text="Ingrese su nombre",bg='black',fg='white')
    nombreLabel.pack()
    nombreEntry = tk.Entry(ventanaRegistro)
    nombreEntry.pack()

    aPaternoLabel = tk.Label(ventanaRegistro, text="Ingrese su apellido paterno",bg='black',fg='white')
    aPaternoLabel.pack()
    aPaternoEntry = tk.Entry(ventanaRegistro)
    aPaternoEntry.pack()

    aMaternoLabel = tk.Label(ventanaRegistro, text="Ingrese su apellido materno",bg='black',fg='white')
    aMaternoLabel.pack()
    aMaternoEntry = tk.Entry(ventanaRegistro)
    aMaternoEntry.pack()

    paisLabel = tk.Label(ventanaRegistro, text="Pais",bg='black',fg='white')
    paisLabel.pack()
    paisEntry = tk.Entry(ventanaRegistro)
    paisEntry.pack()

    def passwordIguales(pass1,pass2):
        if(pass1 == pass2):
            return True
        else:
            return False

    def pop_up_msg(mensaje):
        win = tk.Toplevel()
        win.wm_title("Mensaje")

        l = tk.Label(win, text=mensaje)
        l.grid(row=0, column=0)

        b = tk.Button(win, text="Okay", command=win.destroy)
        b.grid(row=1, column=0)

    def confirmar():
        if(passwordIguales(passEntry.get(),pass2Entry.get())):
            listaDatos = []
            listaDatos.append(nickEntry.get())
            listaDatos.append(nombreEntry.get())
            listaDatos.append(aPaternoEntry.get())
            listaDatos.append(aMaternoEntry.get())
            listaDatos.append(emailEntry.get())
            listaDatos.append(passEntry.get())
            listaDatos.append(paisEntry.get())
            
            RegistrarUsuario(listaDatos)
            generarAvatar(nickEntry.get())
            pop_up_msg("Usuario registrado, Bienvenido "+nickEntry.get())
        else:
            pop_up_msg("Las contraseñas deben coincidir")

    botonConfirmar = tk.Button(ventanaRegistro, text = "Cofirmar registro", command=confirmar)
    botonConfirmar.pack(pady=5)

    botonSalir = tk.Button(ventanaRegistro,text="Salir", command=ventanaRegistro.destroy)
    botonSalir.pack(pady=10)

    ventanaRegistro.mainloop()

    

    

    