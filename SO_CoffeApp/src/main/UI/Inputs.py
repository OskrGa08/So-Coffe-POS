import pyodbc
from tkinter import *
from tkinter import Scrollbar
from tkinter import Menubutton
from tkinter import messagebox
from tkinter import ttk

# Configuration main window---------------------------
inp = Tk()
inp.geometry("850x700")
inp.minsize(700, 500)
inp.maxsize(1500, 580)
inp.configure(bg="white")
inp.title("Gestion de Insumos")

#Top Bar-----------------------------------------------
topBar_frame = Frame(inp, bg="#CE7710")
topBar_frame.place(x=0, y=0, relwidth=1, height=30)

#Logica de los command para que habra resectivas ventanas cada opcion(abrir las ventanas respectivas a cada gestionar)---------------------------------------
def managEmployees():
    inp.destroy()
    from Employees import Employees
    Employees()

def managOutPuts():
    inp.destroy()
    from OutPuts import OutPuts
    OutPuts()

def pontiOfSale():
    inp.destroy()
    from POS import POS 
    POS()

def managPosition():
    inp.destroy()
    from Position import Position
    Position()

def managProductCategory():
    inp.destroy()
    from ProductCategory import ProductCategory
    ProductCategory()

def managProducts():
    inp.destroy()
    from Products import Products 
    Products()

def managSells():
    inp.destroy()
    from Sells import Sells 
    Sells()

def managShopping():
    inp.destroy()
    from Shopping import Shopping
    Shopping()

def  managSupplier():
    inp.destroy()
    from Suppliers import Suppliers 
    Suppliers()


# Load the image using PIL
MB_image = PhotoImage(file="SO_CoffeApp/src/main/resources/menu_bar.png")
# Create a label to display the background image
MenuButton_barFrame = Menubutton(topBar_frame, image=MB_image ,bg="#CE7710", width=30, height=30)
MenuButton_barFrame.place(x=0, y=0)
MenuButton_barFrame.menu = Menu(MenuButton_barFrame, tearoff=0, bg="#CE7710")
MenuButton_barFrame.menu.add_command(label="Gestion de Empleados", foreground="white", font=("New Times Roman", 12), command=managEmployees)
MenuButton_barFrame.menu.add_command(label="Gestion de Salidas", foreground="white", font=("New Times Roman", 12), command=managOutPuts)
MenuButton_barFrame.menu.add_command(label="Punto de Venta", foreground="white", font=("New Times Roman", 12), command=pontiOfSale)
MenuButton_barFrame.menu.add_command(label="Puestos de Empleados", foreground="white", font=("New Times Roman", 12), command=managPosition)
MenuButton_barFrame.menu.add_command(label="Categorias de Productos", foreground="white", font=("New Times Roman", 12), command=managProductCategory)
MenuButton_barFrame.menu.add_command(label="Gestion de Productos", foreground="white", font=("New Times Roman", 12), command= managProducts)
MenuButton_barFrame.menu.add_command(label="Gestion de Ventas", foreground="white", font=("New Times Roman", 12), command=managSells)
MenuButton_barFrame.menu.add_command(label="Gestion de Compras", foreground="black", font=("New Times Roman", 12), command=managShopping)
MenuButton_barFrame.menu.add_command(label="Gestion de Proveedores", foreground="black", font=("New Times Roman", 12), command=managSupplier)
MenuButton_barFrame["menu"]= MenuButton_barFrame.menu

Main_Label = Label(inp, text="INSUMOS", fg="black", bg="white", font=("Arial Black", 18))
Main_Label.place(x=360, y=55)

# Table to display products
inputs_columns = ("Nombre", "Existencia", "Descripcion", "Costo")
inputs_tree = ttk.Treeview(inp, columns=inputs_columns, show="headings", height=5)
for col in inputs_columns:
    inputs_tree.heading(col, text=col)
inputs_tree.place(x=20, y=162, height=300)

inputs_scrollbar = Scrollbar(inp, orient="vertical", command=inputs_tree.yview)
inputs_scrollbar.place(x=800, y=165, height=290)
inputs_tree.configure(yscrollcommand=inputs_scrollbar.set)

# Connection db---------------------------------------------------------
def get_db_connection():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123;')
    return conn

#Load inputs to show---------------------------------------------------
def load_inputs():
    try:
        # Limpia el TreeView antes de recargar los registros
        inputs_tree.delete(*inputs_tree.get_children())
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC mostrarInsumos") 
        rows = cursor.fetchall()
        # Concatenate names directly in the loop for efficiency
        for row in rows:
            formatted_row = (
                row[1], #Nombre
                row[2], #Existencia
                row[3], #Descripcion
                row[4]) #Costo
            inputs_tree.insert("", "end", values=formatted_row)
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los insumos: {e}")
load_inputs()

# Function to open add product window
def Add_InputWindow():
    ain = Toplevel(inp)
    ain.geometry("300x350")
    ain.configure(bg="white")
    ain.title("Agregar Insumo")
    #ap.iconbitmap('F:\\6to Semestre\\Gestión De Proyectos De Software\\S-O project\Extra\\icon sf.ico')

    def Aceptar_ButtonAction():
        # Obtener los valores ingresados por el usuario
        nombre = Name_Box.get()
        existencia = Existence_Box.get()
        descripcion = Description_Box.get()
        costo = Precio_Box.get()

        # Agregar la información a la base de datos utilizando un procedimiento almacenado
        try:
            conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
            cursor = conn.cursor()
            cursor.execute("EXEC addInsumos ?, ?, ?, ?", nombre, existencia, descripcion, costo)
            conn.commit()
            cursor.close()
            conn.close()

            # Mostrar la información obtenida en la ventana principal (rgp)
            inputs_tree.insert("", "end", values=(nombre, existencia, descripcion, costo))
            ain.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar el insumo: {e}")


    Name_Label = Label(ain, text="Nombre", fg="black", bg="white", font=("Arial Black", 9))
    Name_Label.place(x=30, y=30)
    Name_Box = Entry(ain, width=20, bg="lightgray" )
    Name_Box.place(x=115, y=30)

    Existence_Label = Label(ain, text="Existencia ", fg="black", bg="white", font=("Arial Black", 9))
    Existence_Label.place(x=30, y=75)
    Existence_Box = Entry(ain, width=5, bg="lightgray" )
    Existence_Box.place(x=115, y=75)

    Description_Label = Label(ain, text="Descripcion", fg="black", bg="white", font=("Arial Black", 9))
    Description_Label.place(x=30, y=115)
    Description_Box = Entry(ain, width=20, bg="lightgray" )
    Description_Box.place(x=115, y=115)

    Precio_Label = Label(ain, text="Costo $", fg="black", bg="white", font=("Arial Black", 9))
    Precio_Label.place(x=30, y=150)
    Precio_Box = Entry(ain, width=5, bg="lightgray" )
    Precio_Box.place(x=115, y=150)
    
    Aceptar_Button = Button(ain, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=Aceptar_ButtonAction)
    Aceptar_Button.place(x=30, y=240)

    Cancelar_Button = Button(ain, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=ain.destroy)
    Cancelar_Button.place(x=100, y=240)


def obtener_id_input_por_nombre(nombre):
    """Obtiene el id_proveedor a partir del RFC."""
    try:
        conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
        cursor = conn.cursor()
        cursor.execute("SELECT id_insumo FROM insumos WHERE nombre = ?", nombre)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        print(result)

        if result:
            return result[0]  # Regresa el id_empleado
        else:
            messagebox.showerror("Error", "Insumo no encontrado")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener el ID del insumo: {e}")
        return None


# Function to open edit inputs window ---------------------------------------------
def Edit_InputWindow():
    selected_item = inputs_tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un Insumo para editar")
        return
    
    item = inputs_tree.item(selected_item)
    values = item["values"]
    # Obtener el RFC del empleado seleccionado (suponiendo que es el valor en el índice 4)
    nombre_insumo = values[0]  # Ajusta según el índice correcto de Nombre
    
    # Obtener el id_proveedor usando el RFC
    id_insumo = obtener_id_input_por_nombre(nombre_insumo)
    if id_insumo is None:
        return  # Si no se encuentra el ID, no continuar con la edición

    load_inputs()
    ei = Toplevel(inp)
    ei.geometry("400x550")
    ei.configure(bg="white")
    ei.title("Editar Insumo")
    #ep.iconbitmap('F:\\6to Semestre\\Gestión De Proyectos De Software\\S-O project\Extra\\icon sf.ico')

    def Aceptar_ButtonAction():
        # Obtener los valores modificados por el usuario
        nombre = Name_Box.get()
        existencia = values[1]
        descripcion = Description_Box.get()
        costo = Precio_Box.get()

        load_inputs()
        try:
            conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
            cursor = conn.cursor()
            cursor.execute("EXEC modInsumos ?, ?, ?, ?",id_insumo, nombre, descripcion, costo)
            conn.commit()
            cursor.close()
            conn.close()

            # Actualizar la información en la tabla
            # Mostrar la información obtenida en la ventana principal (rgp)
            inputs_tree.insert("", "end", values=(nombre, existencia, descripcion, costo))
            load_inputs()
            ei.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar el insumo: {e}")


    Name_Label = Label(ei, text="Nombre", fg="black", bg="white", font=("Arial Black", 9))
    Name_Label.place(x=30, y=30)
    Name_Box = Entry(ei, width=20, bg="lightgray" )
    Name_Box.place(x=115, y=30)
    Name_Box.insert(0, values[0])

    Existence_Label = Label(ei, text="Existencia ", fg="black", bg="white", font=("Arial Black", 9))
    Existence_Label.place(x=30, y=75)
    Existence_Label2 = Label(ei, text=values[1], fg="black", bg="white", font=("Arial Black", 9))
    Existence_Label2.place(x=115, y=75)

    Description_Label = Label(ei, text="Descripcion", fg="black", bg="white", font=("Arial Black", 9))
    Description_Label.place(x=30, y=115)
    Description_Box = Entry(ei, width=20, bg="lightgray" )
    Description_Box.place(x=115, y=115)
    Description_Box.insert(0, values[2])

    Precio_Label = Label(ei, text="Costo $", fg="black", bg="white", font=("Arial Black", 9))
    Precio_Label.place(x=30, y=150)
    Precio_Box = Entry(ei, width=5, bg="lightgray" )
    Precio_Box.place(x=115, y=150)
    Precio_Box.insert(0, values[3])
    
    Aceptar_Button = Button(ei, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=Aceptar_ButtonAction)
    Aceptar_Button.place(x=30, y=240)

    Cancelar_Button = Button(ei, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=ei.destroy)
    Cancelar_Button.place(x=100, y=240)

# Función para cargar empleados según el criterio de búsqueda
def load_inputs_filter(query=None):
    try:
        # Limpiar el TreeView antes de cargar los registros
        inputs_tree.delete(*inputs_tree.get_children())

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si se hace una búsqueda o se cargan todos los proveedores activos
        if query:
            # Ejecutar el procedimiento almacenado para buscar por nombre
            cursor.execute("EXEC BuscarInsumosNombre ?", query)
            rows = cursor.fetchall()
        else:
            # Ejecutar procedimiento para cargar todos los proveedores activos si no hay búsqueda
            load_inputs()

        # Iterar sobre los resultados y formatear las filas para mostrar el puesto en lugar del ID
        for row in rows:
            formatted_row = (
                row[0], #Nombre
                row[1], #Existencia
                row[2], #Descripcion
                row[3]) #Costo
            inputs_tree.insert("", "end", values=formatted_row)
        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los insumos: {e}")

# Función para manejar el botón de búsqueda
def search_inputs():
    query = search_entry.get()  # Obtener texto de búsqueda
    load_inputs_filter(query=query)


# Barra de búsqueda
search_entry = Entry(inp, width=30)
search_entry.place(x=70, y=120)

search_button = Button(inp, text="Buscar", command=search_inputs)
search_button.place(x=20, y=120)

#Buttons----------------------------------
Add_Input = Button(inp, text="Agregar Insumo", fg="black", bg="#CE7710", command=Add_InputWindow, font=("Arial Black", 9))
Add_Input.place(x=360, y=120)

Edit_Input = Button(inp, text="Editar Insumo", fg="black", bg="#CE7710", command=Edit_InputWindow, font=("Arial Black", 9))
Edit_Input.place(x=640, y=120)

inp.mainloop()