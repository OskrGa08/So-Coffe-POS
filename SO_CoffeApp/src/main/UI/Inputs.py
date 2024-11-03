import pyodbc
from tkinter import *
from tkinter import Scrollbar
from tkinter import Menubutton
from tkinter import messagebox
from tkinter import ttk

# Configuration main window---------------------------
inp = Tk()
inp.geometry("1050x700")
inp.minsize(700, 500)
inp.maxsize(1500, 580)
inp.configure(bg="white")
inp.title("Gestion de Insumos")

#Top Bar-----------------------------------------------
topBar_frame = Frame(inp, bg="#CE7710")
topBar_frame.place(x=0, y=0, relwidth=1, height=30)

#Logica de los command para que habra resectivas ventanas cada opcion(abrir las ventanas respectivas a cada gestionar)---------------------------------------
# arreglar para poder navegar entre ventanas
def logout():
    inp.destroy()
    from LogIn import logIn
    logIn()

def managEmployees():
    from Employees import Employees
    Employees()

def managProducts():
    from Products import Products 
    Products()

def  managSupplier():
    from Suppliers import Suppliers 
    Suppliers()

# Load the image using PIL
MB_image = PhotoImage(file="SO_CoffeApp/src/main/resources/menu_bar.png")
# Create a label to display the background image
MenuButton_barFrame = Menubutton(topBar_frame, image=MB_image ,bg="#CE7710", width=30, height=30)
MenuButton_barFrame.place(x=0, y=0)
MenuButton_barFrame.menu = Menu(MenuButton_barFrame, tearoff=0, bg="#CE7710")
MenuButton_barFrame.menu.add_command(label="Configurar pa que salga el usuario", foreground="black", font=("New Times Roman", 12))
MenuButton_barFrame.menu.add_separator()
MenuButton_barFrame.menu.add_command(label="Gestion de ventas", foreground="white", font=("New Times Roman", 12))#
MenuButton_barFrame.menu.add_command(label="Gestion de compras", foreground="white", font=("New Times Roman", 12))#
MenuButton_barFrame.menu.add_command(label="Gestion de empleados", foreground="white", font=("New Times Roman", 12), command=managEmployees)
MenuButton_barFrame.menu.add_command(label="Gestion de proveedores", foreground="white", font=("New Times Roman", 12), command=managSupplier)
MenuButton_barFrame.menu.add_command(label="Gestion de productos", foreground="white", font=("New Times Roman", 12), command= managProducts)
MenuButton_barFrame.menu.add_command(label="Gestion de usuarios", foreground="white", font=("New Times Roman", 12))#
MenuButton_barFrame.menu.add_separator()
MenuButton_barFrame.menu.add_command(label="Cerrar Sesion", foreground="black", font=("New Times Roman", 12), command=logout)
MenuButton_barFrame["menu"]= MenuButton_barFrame.menu


Main_Label = Label(inp, text="INSUMOS", fg="black", bg="white", font=("Arial Black", 18))
Main_Label.place(x=480, y=55)

# Table to display products
inputs_columns = ("ID Insumo", "Nombre", "Existencia", "Descripcion", "Costo")
inputs_tree = ttk.Treeview(inp, columns=inputs_columns, show="headings", height=5)
for col in inputs_columns:
    inputs_tree.heading(col, text=col)
inputs_tree.place(x=20, y=162, height=300)

inputs_scrollbar = Scrollbar(inp, orient="vertical", command=inputs_tree.yview)
inputs_scrollbar.place(x=1000, y=165, height=290)
inputs_tree.configure(yscrollcommand=inputs_scrollbar.set)

# Function to open add product window
def Add_ProductWindow():
    ain = Toplevel(inp)
    ain.geometry("300x350")
    ain.configure(bg="white")
    ain.title("Agregar Insumo")
    #ap.iconbitmap('F:\\6to Semestre\\Gestión De Proyectos De Software\\S-O project\Extra\\icon sf.ico')

    ID_Input_Label = Label(ain, text="ID Insumo", fg="black", bg="white", font=("Arial Black", 9))
    ID_Input_Label.place(x=28, y=31)
    ID_Input_Value = Label(ain, text="01", fg="black", bg="lightgray", font=("Arial Black", 9), width=10)
    ID_Input_Value.place(x=115, y=35)

    Name_Label = Label(ain, text="Nombre", fg="black", bg="white", font=("Arial Black", 9))
    Name_Label.place(x=30, y=72)
    Name_Box = Entry(ain, width=20, bg="lightgray" )
    Name_Box.place(x=115, y=72)

    Existence_Label = Label(ain, text="Existencia ", fg="black", bg="white", font=("Arial Black", 9))
    Existence_Label.place(x=30, y=100)
    Existence_Box = Entry(ain, width=5, bg="lightgray" )
    Existence_Box.place(x=115, y=105)

    Description_Label = Label(ain, text="Descripcion", fg="black", bg="white", font=("Arial Black", 9))
    Description_Label.place(x=30, y=135)
    Description_Box = Entry(ain, width=20, bg="lightgray" )
    Description_Box.place(x=115, y=135)

    Precio_Label = Label(ain, text="Costo $", fg="black", bg="white", font=("Arial Black", 9))
    Precio_Label.place(x=30, y=165)
    Precio_Box = Entry(ain, width=5, bg="lightgray" )
    Precio_Box.place(x=115, y=165)
    
    Aceptar_Button = Button(ain, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9))
    Aceptar_Button.place(x=30, y=240)

    Cancelar_Button = Button(ain, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=ain.destroy)
    Cancelar_Button.place(x=100, y=240)

def Edit_ProductWindow():
    ain = Toplevel(inp)
    ain.geometry("300x350")
    ain.configure(bg="white")
    ain.title("Agregar Insumo")
    #ap.iconbitmap('F:\\6to Semestre\\Gestión De Proyectos De Software\\S-O project\Extra\\icon sf.ico')

    ID_Input_Label = Label(ain, text="ID Insumo", fg="black", bg="white", font=("Arial Black", 9))
    ID_Input_Label.place(x=28, y=31)
    ID_Input_Value = Label(ain, text="01", fg="black", bg="lightgray", font=("Arial Black", 9), width=10)
    ID_Input_Value.place(x=115, y=35)

    Name_Label = Label(ain, text="Nombre", fg="black", bg="white", font=("Arial Black", 9))
    Name_Label.place(x=30, y=72)
    Name_Box = Entry(ain, width=20, bg="lightgray" )
    Name_Box.place(x=115, y=72)

    Existence_Label = Label(ain, text="Existencia ", fg="black", bg="white", font=("Arial Black", 9))
    Existence_Label.place(x=30, y=100)
    Existence_Box = Entry(ain, width=5, bg="lightgray" )
    Existence_Box.place(x=115, y=105)

    Description_Label = Label(ain, text="Descripcion", fg="black", bg="white", font=("Arial Black", 9))
    Description_Label.place(x=30, y=135)
    Description_Box = Entry(ain, width=20, bg="lightgray" )
    Description_Box.place(x=115, y=135)

    Precio_Label = Label(ain, text="Costo $", fg="black", bg="white", font=("Arial Black", 9))
    Precio_Label.place(x=30, y=165)
    Precio_Box = Entry(ain, width=5, bg="lightgray" )
    Precio_Box.place(x=115, y=165)
    
    Aceptar_Button = Button(ain, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9))
    Aceptar_Button.place(x=30, y=240)

    Cancelar_Button = Button(ain, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=ain.destroy)
    Cancelar_Button.place(x=100, y=240)


Add_Product = Button(inp, text="Agregar Insumo", fg="black", bg="#CE7710", command=Add_ProductWindow, font=("Arial Black", 9))
Add_Product.place(x=30, y=120)

Edit_Product = Button(inp, text="Editar Insumo", fg="black", bg="#CE7710", command=Edit_ProductWindow, font=("Arial Black", 9))
Edit_Product.place(x=480, y=120)

Delete_Product = Button(inp, text="Desactivar Insumo", fg="black", bg="#CE7710", font=("Arial Black", 9))
Delete_Product.place(x=850, y=120)

inp.mainloop()