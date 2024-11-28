import pyodbc
from tkinter import *
from tkinter import Scrollbar
from tkinter import Menubutton
from tkinter import messagebox
from tkinter import ttk

#Configuration main window------------
category = Tk()
category.geometry("600x500")
category.maxsize(700, 580)
category.minsize(700, 500)
category.configure(bg="white")
category.title("Categoria Productos")

#Top Bar-----------------------------------------------
topBar_frame = Frame(category, bg="#CE7710")
topBar_frame.place(x=0, y=0, relwidth=1, height=30)

#Methods to nav amoung windows
def managEmployees():
    category.destroy()
    from Employees import Employees
    Employees()

def managInputs():
    category.destroy()
    from Inputs import Inputs
    Inputs()

def managOutPuts():
    category.destroy()
    from OutPuts import OutPuts
    OutPuts()

def pontiOfSale():
    category.destroy()
    from POS import POS 
    POS()

def managPosition():
    category.destroy()
    from Position import Position 
    Position()

def managProducts():
    category.destroy()
    from Products import Products 
    Products()

def managSells():
    category.destroy()
    from Sells import Sells 
    Sells()

def managShopping():
    category.destroy()
    from Shopping import Shopping
    Shopping()

def managShoppingView():
    category.destroy()
    from ShopingView import ShopingView
    ShopingView()

def  managSupplier():
    category.destroy()
    from Suppliers import Suppliers 
    Suppliers()

def reports():
    category.destroy()
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
MenuButton_barFrame.menu.add_command(label="Puestos de Empelados", foreground="white", font=("New Times Roman", 12), command=managPosition)
MenuButton_barFrame.menu.add_command(label="Gestion de Productos", foreground="white", font=("New Times Roman", 12), command=managProducts)
MenuButton_barFrame.menu.add_command(label="Vista de Ventas", foreground="white", font=("New Times Roman", 12), command=managSells)
MenuButton_barFrame.menu.add_command(label="Gestion de Compras", foreground="white", font=("New Times Roman", 12), command= managShopping)
MenuButton_barFrame.menu.add_command(label="Vista de Compras", foreground="white", font=("New Times Roman", 12), command= managShoppingView)
MenuButton_barFrame.menu.add_command(label="Gestion de Proveedores", foreground="white", font=("New Times Roman", 12), command=managSupplier)
MenuButton_barFrame.menu.add_command(label="Reportes", foreground="white", font=("New Times Roman", 12), command= reports)
MenuButton_barFrame["menu"]= MenuButton_barFrame.menu

Main_Label = Label(category, text="Categorias Productos", fg="black", bg="white", font=("Arial Black", 18))
Main_Label.place(x=240, y=55)

#Table to display categories 
category_columns = ("Id_Categoria", "Categoria")
category_tree = ttk.Treeview(category, columns=category_columns, show="headings", height=5)
for col in category_columns:
    category_tree.heading(col, text=col)
category_tree.place(x=150, y=142, height=300)

#Connection with DB
def get_db_connection():
    return pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123;')

def load_Categories():
    try:
        # Limpia el TreeView antes de recargar los registros
        category_tree.delete(*category_tree.get_children())

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC mostrarCategorias")
        rows = cursor.fetchall()
        # Inserta cada fila en el TreeView
        for row in rows:
            formatted_row = (row[0], row[1])
            category_tree.insert("", "end", values=formatted_row)  # row[0]: ID, row[1]: Nombre del puesto 
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar las categoirias: {e}")
load_Categories()

#Add Category Window
def add_CategoryWindow():
    adca = Toplevel(category)
    adca.geometry("300x300")
    adca.configure(bg="white")
    adca.title("Agregar Categoria")
    
    Category_Label = Label(adca, text="Categoria", fg="black", bg="white", font=("Arial Black", 9))
    Category_Label.place(x=30, y=72)
    Category_Box = Entry(adca, width=20, bg="lightgray" )
    Category_Box.place(x=115, y=72)
    
    def accept_ButtomAction():
        category_Product = Category_Box.get()

        try: 
            conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
            cursor = conn.cursor()
            cursor.execute("EXEC addCategoria ?", category_Product) 
            conn.commit()
            cursor.close()
            conn.close()
            # Mostrar la información obtenida en la ventana principal (category)
            category_tree.insert("", "end", values=(category_Product))
            load_Categories()
            adca.destroy() 
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar la categoria: {e}")

    Aceptar_Button = Button(adca, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=accept_ButtomAction)
    Aceptar_Button.place(x=30, y=200)

    Cancelar_Button = Button(adca, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=adca.destroy)
    Cancelar_Button.place(x=100, y=200)

Add_CategoryBt = Button(category, text="Agregar Categoria", fg="black", bg="#CE7710", command=add_CategoryWindow, font=("Arial Black", 9))
Add_CategoryBt.place(x=20, y=60)

category.mainloop()