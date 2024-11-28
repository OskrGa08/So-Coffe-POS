import pyodbc
from tkinter import *
from tkinter import Scrollbar
from tkinter import Menubutton
from tkinter import messagebox
from tkinter import ttk

# Configuration main window---------------------------
sh = Tk()
sh.geometry("1220x700")
sh.minsize(700, 500)
sh.maxsize(1500, 580)
sh.configure(bg="white")
sh.title("Gestion de Compras")

#Top Bar-----------------------------------------------
topBar_frame = Frame(sh, bg="#CE7710")
topBar_frame.place(x=0, y=0, relwidth=1, height=30)

#Frames--------------------------------------------------
detail_Frame = Frame(sh, bg="#D2D2D2")
detail_Frame.place(x=850, y=60, width=340, height=460)

#Logica de los command para que habra resectivas ventanas cada opcion(abrir las ventanas respectivas a cada gestionar)---------------------------------------
def managEmployees():
    sh.destroy()
    from Employees import Employees
    Employees()

def managInputs():
    sh.destroy()
    from Inputs import Inputs
    Inputs()

def pontiOfSale():
    sh.destroy()
    from POS import POS 
    POS()

def managPosition():
    sh.destroy()
    from Position import Position
    Position()

def managProductCategory():
    sh.destroy()
    from ProductCategory import ProductCategory
    ProductCategory()

def managProducts():
    sh.destroy()
    from Products import Products 
    Products()

def managSells():
    sh.destroy()
    from Sells import Sells 
    Sells()

def managOutPuts():
    sh.destroy()
    from OutPuts import OutPuts 
    OutPuts()

def managShopping():
    sh.destroy()
    from Shopping import Shopping
    Shopping()

def managShoppingView():
    sh.destroy()
    from ShopingView import ShopingView
    ShopingView()

def  managSupplier():
    sh.destroy()
    from Suppliers import Suppliers 
    Suppliers()

def reports():
    sh.destroy()
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
MenuButton_barFrame.menu.add_command(label="Punto de Venta", foreground="white", font=("New Times Roman", 12), command=pontiOfSale)
MenuButton_barFrame.menu.add_command(label="Puestos de Empleados", foreground="white", font=("New Times Roman", 12), command=managPosition)
MenuButton_barFrame.menu.add_command(label="Categorias de Productos", foreground="white", font=("New Times Roman", 12), command= managProductCategory)
MenuButton_barFrame.menu.add_command(label="Gestion de Productos", foreground="white", font=("New Times Roman", 12), command=managProducts)
MenuButton_barFrame.menu.add_command(label="Gestion de Salidas", foreground="white", font=("New Times Roman", 12), command=managOutPuts)
MenuButton_barFrame.menu.add_command(label="Gestion de Compras", foreground="white", font=("New Times Roman", 12), command=managShopping)
MenuButton_barFrame.menu.add_command(label="Vistas de Compras", foreground="white", font=("New Times Roman", 12), command=managShoppingView)
MenuButton_barFrame.menu.add_command(label="Gestion de Proveedores", foreground="white", font=("New Times Roman", 12), command=managSupplier)
MenuButton_barFrame.menu.add_command(label="Vista de Ventas", foreground="white", font=("New Times Roman", 12), command=managSells)
MenuButton_barFrame.menu.add_command(label="Reportes", foreground="white", font=("New Times Roman", 12), command=reports)
MenuButton_barFrame["menu"]= MenuButton_barFrame.menu

Main_Label = Label(sh, text="COMPRAS", fg="black", bg="white", font=("Arial Black", 18))
Main_Label.place(x=350, y=75)

# Table to display 
sh_columns = ("ID Compra", "Proveedor", "Fecha", "Total")
sh_tree = ttk.Treeview(sh, columns=sh_columns, show="headings", height=5)
for col in sh_columns:
    sh_tree.heading(col, text=col)
sh_tree.place(x=20, y=160, height=300)

sh_scrollbar = Scrollbar(sh, orient="vertical", command=sh_tree.yview)
sh_scrollbar.place(x=802, y=165, height=290)
sh_tree.configure(yscrollcommand=sh_scrollbar.set)

#connection bd---------------------------------------------------------------------------------------------------------------------
def get_db_connection():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123;')
    return conn

def load_Sh():
    try:
        sh_tree.delete(*sh_tree.get_children())
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC mostrar_compras")
        rows = cursor.fetchall()
        for row in rows:
            formatted_row = (
                row[0], 
                row[1],
                row[2],
                f"{row[3]}")
            sh_tree.insert("", "end", values=formatted_row)
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar las compras: {e}")
load_Sh()

def on_select_output(event):
    # Obtener el ID de la salida seleccionada
    selected_item = sh_tree.selection()
    if not selected_item:
        return  # Si no hay selección, salir

    item = sh_tree.item(selected_item)
    compra_id = item["values"][0]  # El ID está en la primera columna

    # Limpiar el frame de detalles
    for widget in detail_Frame.winfo_children():
        widget.destroy()

    try:
        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ejecutar el procedimiento almacenado con el ID de la compra
        cursor.execute("EXEC obtenerDetalleCompra ?", compra_id)
        detalles = cursor.fetchall()
        
        # Mostrar los detalles en el frame
        Label(detail_Frame, text="Detalles de la Compra", bg="#D2D2D2", font=("Arial Black", 10)).pack(pady=5)
        
        for detalle in detalles:
            texto = f"Insumo: {detalle[0]}, Cantidad: {detalle[1]}, Costo: {detalle[2]}"
            Label(detail_Frame, text=texto, bg="#D2D2D2", anchor="w").pack(fill="x", padx=10, pady=2)
        
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los detalles de la compra: {e}")

# Vincular el evento de selección al treeview
sh_tree.bind("<<TreeviewSelect>>", on_select_output)

sh.mainloop()