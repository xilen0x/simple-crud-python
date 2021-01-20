from tkinter import *
from tkinter import messagebox
from conexion_db import *
import sqlite3

root = Tk()
miMenu = Menu(root)
root.config(menu = miMenu)
miFrame = Frame(root)
miFrame.pack()

root.geometry('500x400')
root.resizable(0,0)
root.title("My CRUD in Python")
#-----------------------------Funciones Menú:-------------------------------------
def ventanaEmergenteInfo():
    messagebox.showinfo("titulo ventana","Mensaje de Información")

def ErrorConexion():
    messagebox.showwarning("Error de conexión", "Tabla USUARIOS ya existe")

def limpiarCampos():
    miId.set("")
    miNombre.set("")
    miPass.set("")
    miDirec.set("")
    entryComentario.delete(1.0, END)

def salir():
    valor = messagebox.askquestion("Salir", "Estas seguro de salir?")
    if valor == "yes":
        root.destroy()

def createData():
    miConexion = sqlite3.connect("Usuarios")
    miCursor=miConexion.cursor()
    #opcion q me gustó:
    datos = miNombre.get(),miPass.get(),miDirec.get(),entryComentario.get(1.0,END)
    miCursor.execute("INSERT INTO DATOSUSUARIOS VALUES(NULL,?,?,?,?)",(datos))
    #Otra opcion:
    # miCursor.execute("INSERT INTO DATOSUSUARIOS (NOMBRE_USUARIO,PASSWORD,DIRECCION,COMENTARIO) VALUES (?,?,?,?)",(miNombre.get(),miPass.get(),miDirec.get(),entryComentario.get(1.0,END)))    
    
    miConexion.commit()
    messagebox.showinfo("Conexión DB","Registro ingresado con éxito!")

def readData():
    miConexion = sqlite3.connect("Usuarios")
    miCursor=miConexion.cursor()
    
    miCursor.execute("SELECT * FROM DATOSUSUARIOS WHERE ID="+ miId.get())
    datosUsuario = miCursor.fetchall() # fetchall devuelve una lista y para recorrer esa lista usamos un for

    for e in datosUsuario:
        miId.set(e[0])
        miNombre.set(e[1])
        miPass.set(e[2])
        miDirec.set(e[3])
        entryComentario.insert(1.0, e[4])

    miConexion.commit()

def updateData():
    miConexion = sqlite3.connect("Usuarios")
    miCursor=miConexion.cursor()
    datos = miNombre.get(),miPass.get(),miDirec.get(),entryComentario.get(1.0,END)
    miCursor.execute("UPDATE DATOSUSUARIOS SET NOMBRE_USUARIO=?,PASSWORD=?,DIRECCION=?,COMENTARIO=? WHERE ID=" + miId.get(),(datos))

    """ miCursor.execute("UPDATE DATOSUSUARIOS SET NOMBRE_USUARIO='" + miNombre.get() +
        "', PASSWORD='" + miPass.get() +
        "', DIRECCION='" + miDirec.get() +
        "', COMENTARIO='" + entryComentario.get("1.0", END) +
        "' WHERE ID=" + miId.get()) """    
    
    miConexion.commit()
    messagebox.showinfo("Conexión DB","Actualización de registro con éxito!")

def deleteData():
    miConexion = sqlite3.connect("Usuarios")
    miCursor=miConexion.cursor()
    miCursor.execute("DELETE FROM DATOSUSUARIOS WHERE ID=" + miId.get())

    miConexion.commit()
    limpiarCampos()
    messagebox.showinfo("Conexión DB","Eliminación de registro con éxito!")

#----------------------------Función conexión-------------------------------------
def conexionBBDD():
        
    miConexion = sqlite3.connect("Usuarios")
    miCursor = miConexion.cursor()

    try:
        miCursor.execute('''
            CREATE TABLE DATOSUSUARIOS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE_USUARIO VARCHAR(50) UNIQUE,
            PASSWORD VARCHAR(50),
            DIRECCION VARCHAR(100),
            COMENTARIO VARCHAR(200))
            ''')
        messagebox.showinfo("Conexión DB","DB creada con éxito!")


    except:
        ErrorConexion()


#-----------------------------CREACIÓN DE MENUS(SUBMENUS):-------------------------------------

conectarDB = Menu(miMenu, tearoff=0) #tearoff=0 para eliminar submenu vacío o rayitas--
conectarDB.add_command(label="Conectar", command=conexionBBDD)
conectarDB.add_command(label="Salir", command=salir)

limpiarMenu = Menu(miMenu, tearoff=0)
limpiarMenu.add_command(label="Limpiar campos", command=limpiarCampos)

crudMenu = Menu(miMenu, tearoff=0)
crudMenu.add_command(label="Crear", command=createData)
crudMenu.add_command(label="Leer", command=readData)
crudMenu.add_command(label="Actualizar", command=updateData)
crudMenu.add_command(label="Borrar", command=deleteData)

ayudaMenu = Menu(miMenu, tearoff=0)
ayudaMenu.add_command(label="Ventana Emergente Info", command=ventanaEmergenteInfo)

#-----------------------------ANEXAR LOS MENÚS CREADOS A LA BARRA DE MENU: miMenu:-------------------------------------

miMenu.add_cascade(label="BBDD", menu=conectarDB)
miMenu.add_cascade(label="Limpiar", menu=limpiarMenu)
miMenu.add_cascade(label="CRUD", menu=crudMenu)
miMenu.add_cascade(label="Ayuda", menu=ayudaMenu)

#---------------------Entries------------------------------------------Entries:
miId=StringVar()
entryID = Entry(miFrame, textvariable=miId)
entryID.grid(row=0, column=1, padx=20, pady=10)
entryID.config(fg="red") 

miNombre=StringVar()
entryNombre = Entry(miFrame, textvariable=miNombre)
entryNombre.grid(row=1, column=1, padx=10, pady=10)

miPass=StringVar()
entryPass = Entry(miFrame, textvariable=miPass)
entryPass.grid(row=2, column=1, padx=10, pady=10)
entryPass.config(show="*") # para reemplazar el password por asteriscos

miDirec=StringVar()
entryDireccion = Entry(miFrame, textvariable=miDirec)
entryDireccion.grid(row=3, column=1, padx=10, pady=10)

entryComentario=Text(miFrame, width=23, height=5)
entryComentario.grid(row=4, column=1, padx=10, pady=10)
scrollVert = Scrollbar(miFrame, command=entryComentario.yview)
scrollVert.grid(row=4, column=2, sticky="nsew")
entryComentario.config(yscrollcommand=scrollVert.set)

#----------------------Labels-------------------------------------------:
labelID= Label(miFrame, text="ID: ")
labelID.grid(row=0, column=0, sticky="e")

labelNombre = Label(miFrame, text="Nombre: ")
labelNombre.grid(row=1, column=0, sticky="e") # sticky se utliza para alinear, en este caso el label, a la derecha o este(e)...otras opciones: n, s, e, w, ne, nw, se, sw

labelPass = Label(miFrame, text="Password: ")
labelPass.grid(row=2, column=0, sticky="e") 

labelDireccion = Label(miFrame, text="Dirección: ")
labelDireccion.grid(row=3, column=0, sticky="e") 

labelComentario = Label(miFrame, text="Comentario: ")
labelComentario.grid(row=4, column=0, sticky="e") 

#------------new frame for buttons-----#
buttonFrame = Frame(root)
buttonFrame.pack()

# ---***********************--Button-CREAR---***********************---
botonCrear = Button(buttonFrame, text="Guardar", command=createData)
botonCrear.grid(row=1, column=0, sticky="e", padx=10, pady=10)

# ---***********************--Button-LEER---***********************---
botonLeer = Button(buttonFrame, text="Listar", command=readData)
botonLeer.grid(row=1, column=1, sticky="e", padx=10, pady=10)

# ---***********************--Button-ACTUALIZAR---***********************---
botonActualizar = Button(buttonFrame, text="Actualizar", command=updateData)
botonActualizar.grid(row=1, column=2, sticky="e", padx=10, pady=10)

# ---***********************--Button-BORRAR---***********************---
botonBorrar = Button(buttonFrame, text="Borrar", command=deleteData) 
botonBorrar.grid(row=1, column=3, sticky="e", padx=10, pady=10)

root.mainloop()