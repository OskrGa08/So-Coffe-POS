import pyodbc
from tkinter import *
from tkinter import Scrollbar
from tkinter import Menubutton
from tkinter import messagebox
from tkinter import ttk

# Configuration main window---------------------------
sells = Tk()
sells.geometry("1440x700")
sells.minsize(700, 500)
sells.maxsize(1500, 580)
sells.configure(bg="white")
sells.title("Gestion de ventas")

#Top Bar-----------------------------------------------
topBar_frame = Frame(sells, bg="#CE7710")
topBar_frame.place(x=0, y=0, relwidth=1, height=30)

#Frames--------------------------------------------------
detail_Frame = Frame(sells, bg="#D2D2D2")
detail_Frame.place(x=1040, y=60, width=340, height=460)

#Logica de los command para que habra resectivas ventanas cada opcion(abrir las ventanas respectivas a cada gestionar)---------------------------------------
def managEmployees():
    sells.destroy()
    from Employees import Employees
    Employees()

def managInputs():
    sells.destroy()
    from Inputs import Inputs
    Inputs()

def pontiOfSale():
    sells.destroy()
    from POS import POS 
    POS()

def managPosition():
    sells.destroy()
    from Position import Position
    Position()

def managProductCategory():
    sells.destroy()
    from ProductCategory import ProductCategory
    ProductCategory()

def managProducts():
    sells.destroy()
    from Products import Products 
    Products()

def managOutPuts():
    sells.destroy()
    from OutPuts import OutPuts 
    OutPuts()

def managShopping():
    sells.destroy()
    from Shopping import Shopping
    Shopping()

def managShoppingView():
    sells.destroy()
    from ShopingView import ShopingView
    ShopingView()

def  managSupplier():
    sells.destroy()
    from Suppliers import Suppliers 
    Suppliers()

def reports():
    sells.destroy()
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
MenuButton_barFrame.menu.add_command(label="Vista de Compras", foreground="white", font=("New Times Roman", 12), command=managShoppingView)
MenuButton_barFrame.menu.add_command(label="Gestion de Proveedores", foreground="white", font=("New Times Roman", 12), command=managSupplier)
MenuButton_barFrame.menu.add_command(label="Reportes", foreground="white", font=("New Times Roman", 12), command=reports)
MenuButton_barFrame["menu"]= MenuButton_barFrame.menu

Main_Label = Label(sells, text="VENTAS", fg="black", bg="white", font=("Arial Black", 18))
Main_Label.place(x=430, y=55)

# Table to display products
sells_columns = ("ID Venta", "Empleado", "Fecha", "Hora", "Total")
sells_tree = ttk.Treeview(sells, columns=sells_columns, show="headings", height=5)
for col in sells_columns:
    sells_tree.heading(col, text=col)
sells_tree.place(x=20, y=160, height=300)

sells_scrollbar = Scrollbar(sells, orient="vertical", command=sells_tree.yview)
sells_scrollbar.place(x=1002, y=165, height=290)
sells_tree.configure(yscrollcommand=sells_scrollbar.set)

#connection bd---------------------------------------------------------------------------------------------------------------------
def get_db_connection():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123;')
    return conn

def load_Sells():
    try:
        sells_tree.delete(*sells_tree.get_children())
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC MostrarVentas") #el metodo no imprime el noombre de ahi en mas todo bien 
        rows = cursor.fetchall()
        for row in rows:
            formatted_row = (
                row[0], 
                row[1],
                row[2],
                row[3],
                f"{row[4]}")
            sells_tree.insert("", "end", values=formatted_row)
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar las ventas: {e}")
load_Sells()

def on_select_output(event):
    # Obtener el ID de la salida seleccionada
    selected_item = sells_tree.selection()
    if not selected_item:
        return  # Si no hay selección, salir

    item = sells_tree.item(selected_item)
    venta_id = item["values"][0]  # El ID está en la primera columna

    # Limpiar el frame de detalles
    for widget in detail_Frame.winfo_children():
        widget.destroy()

    try:
        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ejecutar el procedimiento almacenado con el ID de la venta
        cursor.execute("EXEC ObtenerDetallesVenta ?", venta_id)
        detalles = cursor.fetchall()
        
        # Mostrar los detalles en el frame
        Label(detail_Frame, text="Detalles de la Venta", bg="#D2D2D2", font=("Arial Black", 10)).pack(pady=5)
        
        for detalle in detalles:
            texto = f"Nombre: {detalle[1]}, Costo: {detalle[2]}, Cantidad: {detalle[3]}, Importe: {detalle[4]}"
            Label(detail_Frame, text=texto, bg="#D2D2D2", anchor="w").pack(fill="x", padx=10, pady=2)
        
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los detalles de la venta: {e}")

# Vincular el evento de selección al treeview
sells_tree.bind("<<TreeviewSelect>>", on_select_output)

sells.mainloop()