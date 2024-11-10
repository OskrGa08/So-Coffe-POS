from decimal import Decimal
from functools import partial
from pathlib import Path
from tkinter import *
from tkinter import Scrollbar
from tkinter import Menubutton
from tkinter import ttk
from tkinter.ttk import Combobox
import pyodbc
from PIL import Image, ImageTk
import tkinter as tk

# Configuration main window--------------------------------------
shp = Tk()
shp.geometry("1150x670")
shp.minsize(700, 500)
shp.maxsize(1224, 1280)
shp.configure(bg="#C9C9C9")
shp.title("Agregar Compra")

# Icon --------------------------
base_dir = Path(__file__).resolve().parent
icon_path = base_dir.parent / 'resources' / 'icon sf.ico'
icon_path_str = str(icon_path)
if icon_path.exists():
    try:
        shp.iconbitmap(icon_path_str)
    except Exception as e:
        print(f"Error al cargar el icono: {e}")
else:
    print(f"El archivo de icono no se encuentra en la ruta especificada: {icon_path_str}")

#Frames----------------------------------------------
bar_frame = Frame(shp, bg="#CE7710")
products_frame = Frame(shp, bg="#C9C9C9")
checkout_frame = Frame(shp, bg="white")

#Customize Frame
products_frame.place(x=30, y=60, width=700, height=500)
checkout_frame.place(x=745, y=60, width=370, height=500)
bar_frame.place(x=0, y=0, relwidth=1, height=30)

#Logic CancelOrder_Button-------------------------------------
#
#
#
#

#Logic HoldOrder_Button
#
#
#
#
#

#Buttons and Labels main window
CancelShopping_Button = Button(text="Cancelar Compra", font=("Katibeh",15), fg="red", bg="SystemButtonFace", overrelief=FLAT, width=25, highlightbackground="red")
CancelShopping_Button.config(bg=shp.cget('bg'))
CancelShopping_Button.place(x=220, y=600, anchor="center", width=200)

HoldOrder_Button = Button(text="Completar Compra", font=("Katibeh",15), fg="green", bg="SystemButtonFace", overrelief=FLAT, width=25, highlightbackground="green")
HoldOrder_Button.config(bg=shp.cget('bg'))
HoldOrder_Button.place(x=440, y=600, anchor="center", width=200)

#Logica de los command para que habra resectivas ventanas cada opcion(abrir las ventanas respectivas a cada gestionar)---------------------------------------
# arreglar para poder navegar entre ventanas
def logout():
    shp.destroy()
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
#Option menu bar frame----------------------------------------------------------

# Load the image using PIL
MB_image = PhotoImage(file="SO_CoffeApp/src/main/resources/menu_bar.png")
# Create a label to display the background image
MenuButton_barFrame = Menubutton(bar_frame, image=MB_image ,bg="#CE7710", width=30, height=30)
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


# ScrollBar products_frame para productos enteros
Canvas_scrollbar1 = Canvas(products_frame, height=200)
Canvas_scrollbar1.pack(side=TOP, fill=BOTH, expand=True, pady=(0, 10))  # Ajuste a side=TOP para apilarlos verticalmente
inner_frame1 = Frame(Canvas_scrollbar1)
Canvas_scrollbar1.create_window((0, 0), window=inner_frame1, anchor="nw")

ScrollBar_Products1 = Scrollbar(Canvas_scrollbar1, orient=VERTICAL, command=Canvas_scrollbar1.yview)
ScrollBar_Products1.pack(side=RIGHT, fill=Y)
Canvas_scrollbar1.config(yscrollcommand=ScrollBar_Products1.set)

# Configuración para ajustar la región desplazable de productos enteros
def configure_scrollregion1(event):
    Canvas_scrollbar1.configure(scrollregion=Canvas_scrollbar1.bbox("all"))

Canvas_scrollbar1.bind("<Configure>", configure_scrollregion1)



#Customize Checkout_frame----------------------------------------
Checkout_Label = Label(checkout_frame, text="Lista", font=("Playfair Display", 10), bg="white", fg="black", width=300)
Checkout_Label.place(x=135, y=10, anchor="center", relwidth=1, height=10)

Atributtes_Label = Label(checkout_frame, text="      Nombre            Precio   QYT   Importe", font=("Arial", 8), bg="#d4d9d6", fg="black")
Atributtes_Label.place(x=310, y=30, anchor="e", width=420, height=15)


#Configure Combobox----------------------------------------------------------------------
supplier_label = Label(shp, text="Proveedor", font=("Arial Black", 10), bg="#C9C9C9", fg="black")
supplier_label.place(x=745, y=35)
supplier_combobox = Entry(shp)
supplier_combobox.place(x=830, y=35)

shp.mainloop()