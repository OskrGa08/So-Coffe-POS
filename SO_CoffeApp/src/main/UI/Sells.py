import pyodbc
from tkinter import *
from tkinter import Scrollbar
from tkinter import Menubutton
from tkinter import messagebox
from tkinter import ttk

# Configuration main window---------------------------
sells = Tk()
sells.geometry("850x700")
sells.minsize(700, 500)
sells.maxsize(1500, 580)
sells.configure(bg="white")
sells.title("Gestion de ventas")

#Top Bar-----------------------------------------------
topBar_frame = Frame(sells, bg="#CE7710")
topBar_frame.place(x=0, y=0, relwidth=1, height=30)

#Logica de los command para que habra resectivas ventanas cada opcion(abrir las ventanas respectivas a cada gestionar)---------------------------------------
# arreglar para poder navegar entre ventanas
def logout():
    sells.destroy()
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


Main_Label = Label(sells, text="VENTAS", fg="black", bg="white", font=("Arial Black", 18))
Main_Label.place(x=330, y=55)

# Table to display products
sells_columns = ("ID Venta", "Empleado", "Fecha", "Total")
sells_tree = ttk.Treeview(sells, columns=sells_columns, show="headings", height=5)
for col in sells_columns:
    sells_tree.heading(col, text=col)
sells_tree.place(x=20, y=160, height=300)

sells_scrollbar = Scrollbar(sells, orient="vertical", command=sells_tree.yview)
sells_scrollbar.place(x=802, y=165, height=290)
sells_tree.configure(yscrollcommand=sells_scrollbar.set)


sells.mainloop()