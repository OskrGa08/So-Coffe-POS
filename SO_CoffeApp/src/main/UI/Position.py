import pyodbc
from tkinter import *
from tkinter import Scrollbar
from tkinter import Menubutton
from tkinter import messagebox
from tkinter import ttk

# Configuration main window---------------------------
posistion = Tk()
posistion.geometry("600x500")
posistion.maxsize(700,580)
posistion.minsize(700,500)
posistion.configure(bg="white")
posistion.title("Puestos de Empleados")

#Top Bar-----------------------------------------------
topBar_frame = Frame(posistion, bg="#CE7710")
topBar_frame.place(x=0, y=0, relwidth=1, height=30)

#Methods to nav amoung windows
def managEmployees():
    posistion.destroy()
    from Employees import Employees
    Employees()

def managInputs():
    posistion.destroy()
    from Inputs import Inputs
    Inputs()

def managOutPuts():
    posistion.destroy()
    from OutPuts import OutPuts
    OutPuts()

def pontiOfSale():
    posistion.destroy()
    from POS import POS 
    POS()

def managProductCategory():
    posistion.destroy()
    from ProductCategory import ProductCategory
    ProductCategory()

def managProducts():
    posistion.destroy()
    from Products import Products 
    Products()

def managSells():
    posistion.destroy()
    from Sells import Sells 
    Sells()

def managShopping():
    posistion.destroy()
    from Shopping import Shopping
    Shopping()

def managShoppingView():
    posistion.destroy()
    from ShopingView import ShopingView
    ShopingView()

def  managSupplier():
    posistion.destroy()
    from Suppliers import Suppliers 
    Suppliers()

def reports():
    posistion.destroy()
    from Tries import Tries
    Tries()

# Load the image using PIL
MB_image = PhotoImage(file="SO_CoffeApp/src/main/resources/menu_bar.png")
# Create a label to display the background image
MenuButton_barFrame = Menubutton(topBar_frame, image=MB_image ,bg="#CE7710", width=30, height=30)
MenuButton_barFrame.place(x=0, y=0)
MenuButton_barFrame.menu = Menu(MenuButton_barFrame, tearoff=0, bg="#CE7710")
MenuButton_barFrame.menu.add_command(label="Gestion de Empleados", foreground="white", font=("New Times Roman", 12), command=managEmployees)
MenuButton_barFrame.menu.add_command(label="Gestion de Insumos", foreground="white", font=("New Times Roman", 12), command=managInputs)
MenuButton_barFrame.menu.add_command(label="Gestion de Salidas", foreground="white", font=("New Times Roman", 12), command=managOutPuts)
MenuButton_barFrame.menu.add_command(label="Punto de Venta", foreground="white", font=("New Times Roman", 12), command=pontiOfSale)
MenuButton_barFrame.menu.add_command(label="Categoria de Productos", foreground="white", font=("New Times Roman", 12), command=managProductCategory)
MenuButton_barFrame.menu.add_command(label="Gestion de Productos", foreground="white", font=("New Times Roman", 12), command=managProducts)
MenuButton_barFrame.menu.add_command(label="Vista de Ventas", foreground="white", font=("New Times Roman", 12), command=managSells)
MenuButton_barFrame.menu.add_command(label="Gestion de Compras", foreground="white", font=("New Times Roman", 12), command= managShopping)
MenuButton_barFrame.menu.add_command(label="Vista de Compras", foreground="white", font=("New Times Roman", 12), command= managShoppingView)
MenuButton_barFrame.menu.add_command(label="Gestion de Proveedores", foreground="white", font=("New Times Roman", 12), command=managSupplier)
MenuButton_barFrame.menu.add_command(label="Gestion de Compras", foreground="white", font=("New Times Roman", 12), command= managShopping)
MenuButton_barFrame.menu.add_command(label="Reportes", foreground="white", font=("New Times Roman", 12), command=reports)
MenuButton_barFrame["menu"]= MenuButton_barFrame.menu

Main_Label = Label(posistion, text="Puesto Empleado", fg="black", bg="white", font=("Arial Black", 18))
Main_Label.place(x=240, y=55)

# Table to display positions
position_columns = ("ID Puesto", "Puesto")
position_tree = ttk.Treeview(posistion, columns=position_columns, show="headings", height=5)
for col in position_columns:
    position_tree.heading(col, text=col)
position_tree.place(x=150, y=142, height=300)

position_scrollbar = Scrollbar(posistion, orient="vertical", command=position_tree.yview)
position_scrollbar.place(x=532, y=145, height=295)
position_tree.configure(yscrollcommand=position_scrollbar.set)

#Connection with DB
def get_db_connection():
    return pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123;')

def load_positions():
    try:
        # Limpia el TreeView antes de recargar los registros
        position_tree.delete(*position_tree.get_children())

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC mostrarPuestos")
        rows = cursor.fetchall()
        # Inserta cada fila en el TreeView
        for row in rows:
            formatted_row = (row[0], row[1])
            position_tree.insert("", "end", values=formatted_row)  # row[0]: ID, row[1]: Nombre del puesto 
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los puestos: {e}")
load_positions()

#Function to open addPosition window
def add_PositionWindow():
    adpo = Toplevel(posistion)
    adpo.geometry("300x300")
    adpo.configure(bg="white")
    adpo.title("Agregar Puesto")
    
    Position_Label = Label(adpo, text="Puesto", fg="black", bg="white", font=("Arial Black", 9))
    Position_Label.place(x=30, y=72)
    Position_Box = Entry(adpo, width=20, bg="lightgray" )
    Position_Box.place(x=115, y=72)
    
    def accept_ButtomAction():
        positionEmployee = Position_Box.get()

        try: 
            conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
            cursor = conn.cursor()
            cursor.execute("EXEC addPuesto ?", positionEmployee) 
            conn.commit()
            cursor.close()
            conn.close()
            # Mostrar la información obtenida en la ventana principal (position)
            position_tree.insert("", "end", values=(positionEmployee))
            load_positions()
            adpo.destroy() 
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar el puesto: {e}")

    Aceptar_Button = Button(adpo, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=accept_ButtomAction)
    Aceptar_Button.place(x=30, y=200)

    Cancelar_Button = Button(adpo, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=adpo.destroy)
    Cancelar_Button.place(x=100, y=200)

Add_Position = Button(posistion, text="Agregar Posicion", fg="black", bg="#CE7710", command=add_PositionWindow, font=("Arial Black", 9))
Add_Position.place(x=20, y=60)

posistion.mainloop()