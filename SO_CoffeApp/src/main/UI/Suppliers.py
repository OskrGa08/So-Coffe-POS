from tkinter import messagebox
import pyodbc
from tkinter import *
from tkinter import ttk

# Configuration main window---------------------------
rprov = Tk()
rprov.geometry("840x530")
rprov.minsize(400, 400)
rprov.maxsize(1500, 580)
rprov.configure(bg="white")
rprov.title("Registrar nuevo Proveedor")

#Top Bar-----------------------------------------------
topBar_frame = Frame(rprov, bg="#CE7710")
topBar_frame.place(x=0, y=0, relwidth=1, height=30)

#Logica de los command para que habra resectivas ventanas cada opcion(abrir las ventanas respectivas a cada gestionar)---------------------------------------
def managEmployees():
    rprov.destroy()
    from Employees import Employees
    Employees()

def managInputs():
    rprov.destroy()
    from Inputs import Inputs
    Inputs()

def pontiOfSale():
    rprov.destroy()
    from POS import POS 
    POS()

def managPosition():
    rprov.destroy()
    from Position import Position
    Position()

def managProductCategory():
    rprov.destroy()
    from ProductCategory import ProductCategory
    ProductCategory()

def managProducts():
    rprov.destroy()
    from Products import Products 
    Products()

def managSells():
    rprov.destroy()
    from Sells import Sells 
    Sells()

def managShopping():
    rprov.destroy()
    from Shopping import Shopping
    Shopping()


# Load the image using PIL
MB_image = PhotoImage(file="SO_CoffeApp/src/main/resources/menu_bar.png")
# Create a label to display the background image
MenuButton_barFrame = Menubutton(topBar_frame, image=MB_image ,bg="#CE7710", width=30, height=30)
MenuButton_barFrame.place(x=0, y=0)
MenuButton_barFrame.menu = Menu(MenuButton_barFrame, tearoff=0, bg="#CE7710")
MenuButton_barFrame.menu.add_command(label="Configurar pa que salga el usuario", foreground="black", font=("New Times Roman", 12))
MenuButton_barFrame.menu.add_separator()
MenuButton_barFrame.menu.add_command(label="Gestion de Empleados", foreground="white", font=("New Times Roman", 12), command=managEmployees)
MenuButton_barFrame.menu.add_command(label="Gestion de Insumos", foreground="white", font=("New Times Roman", 12), command=managInputs)
MenuButton_barFrame.menu.add_command(label="Punto de Venta", foreground="white", font=("New Times Roman", 12), command=pontiOfSale)
MenuButton_barFrame.menu.add_command(label="Puestos de Empleados", foreground="white", font=("New Times Roman", 12), command=managPosition)
MenuButton_barFrame.menu.add_command(label="Categoria de Productos", foreground="white", font=("New Times Roman", 12), command= managProductCategory)
MenuButton_barFrame.menu.add_command(label="Gestion de Productos", foreground="white", font=("New Times Roman", 12), command=managProducts)
MenuButton_barFrame.menu.add_command(label="Gestion de Ventas", foreground="white", font=("New Times Roman", 12), command=managSells)
MenuButton_barFrame.menu.add_command(label="Gestion de Compras", foreground="white", font=("New Times Roman", 12), command=managShopping)
MenuButton_barFrame["menu"]= MenuButton_barFrame.menu

Main_Label = Label(rprov, text="PROVEEDOR", fg="black", bg="white", font=("Arial Black", 18))
Main_Label.place(x=350, y=45)

# Table to display suppliers
supplier_columns = ("Nombre", "Telefono", "RFC", "Correo")
supplier_tree = ttk.Treeview(rprov, columns=supplier_columns, show="headings", height=5)

supplier_scrollbar = Scrollbar(rprov, orient="vertical", command=supplier_tree.yview)
supplier_scrollbar.place(x=800, y=162, height=195)
supplier_tree.configure(yscrollcommand=supplier_scrollbar.set)

for col in supplier_columns:
    supplier_tree.heading(col, text=col)
supplier_tree.place(x=20, y=160, height=200)

# Connection db---------------------------------------------------------
def get_db_connection():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123;')
    return conn

#Load suppliers to show---------------------------------------------------
def load_suppliers():
    try:
        # Limpia el TreeView antes de recargar los registros
        supplier_tree.delete(*supplier_tree.get_children())
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC mostrar_proveedores_activos") 
        rows = cursor.fetchall()
        # Concatenate names directly in the loop for efficiency
        for row in rows:
            formatted_row = (
                row[1], #Nombre
                row[2], #Telefono
                row[3], #RFC
                row[4]) #Correo
            supplier_tree.insert("", "end", values=formatted_row)
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los proveedores: {e}")
load_suppliers()

# Function to open add suppliers window---------------------------------------------
def Add_SupplierWindow():
    ap = Toplevel(rprov)
    ap.geometry("400x550")
    ap.configure(bg="white")
    ap.title("Agregar Proveedor")
    #ap.iconbitmap('F:\\6to Semestre\\Gestión De Proyectos De Software\\S-O project\Extra\\icon sf.ico')

    def Aceptar_ButtonAction():
        # Obtener los valores ingresados por el usuario
        nombre = Name_Box.get()
        telefono = Number_Box.get()
        rfc = RFC_Box.get()
        correo = Mail_Box.get()

        # Agregar la información a la base de datos utilizando un procedimiento almacenado
        try:
            conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
            cursor = conn.cursor()
            cursor.execute("EXEC addProveedor ?, ?, ?, ?", nombre, telefono, rfc, correo)
            conn.commit()
            cursor.close()
            conn.close()

            # Mostrar la información obtenida en la ventana principal (rgp)
            supplier_tree.insert("", "end", values=(nombre, telefono, rfc, correo ))
            ap.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar el producto: {e}")

    Name_Label = Label(ap, text="Nombre", fg="black", bg="white", font=("Arial Black", 9))
    Name_Label.place(x=30, y=30)
    Name_Box = Entry(ap, width=20, bg="lightgray" )
    Name_Box.place(x=155, y=35)
    
    Number_Label = Label(ap, text="Telefono", fg="black", bg="white", font=("Arial Black", 9))
    Number_Label.place(x=30, y=75)
    Number_Box = Entry(ap, width=12, bg="lightgray" )
    Number_Box.place(x=155, y=75)

    RFC_Label = Label(ap, text="RFC", fg="black", bg="white", font=("Arial Black", 9))
    RFC_Label.place(x=30, y=115)
    RFC_Box = Entry(ap, width=15, bg="lightgray" )
    RFC_Box.place(x=155, y=115)

    Mail_Label = Label(ap, text="Correo", fg="black", bg="white", font=("Arial Black", 9))
    Mail_Label.place(x=30, y=150)
    Mail_Box = Entry(ap, width=30, bg="lightgray" )
    Mail_Box.place(x=155, y=150)

    Aceptar_Button = Button(ap, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=Aceptar_ButtonAction)
    Aceptar_Button.place(x=200, y=250)

    Cancelar_Button = Button(ap, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=ap.destroy)
    Cancelar_Button.place(x=280, y=250)

def obtener_id_proveedor_por_rfc(rfc):
    """Obtiene el id_proveedor a partir del RFC."""
    try:
        conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
        cursor = conn.cursor()
        cursor.execute("SELECT id_proveedor FROM proveedor WHERE rfc = ?", rfc)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        print(result)

        if result:
            return result[0]  # Regresa el id_empleado
        else:
            messagebox.showerror("Error", "Proveedor no encontrado")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener el ID del proveedor: {e}")
        return None

# Function to open edit employee window ---------------------------------------------
def Edit_SupplierWindow():
    selected_item = supplier_tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un Proveedor para editar")
        return
    
    item = supplier_tree.item(selected_item)
    values = item["values"]
    # Obtener el RFC del empleado seleccionado (suponiendo que es el valor en el índice 4)
    rfc_proveedor = values[2]  # Ajusta según el índice correcto de RFC
    
    # Obtener el id_proveedor usando el RFC
    id_proveedor = obtener_id_proveedor_por_rfc(rfc_proveedor)
    if id_proveedor is None:
        return  # Si no se encuentra el ID, no continuar con la edición

    load_suppliers()
    ep = Toplevel(rprov)
    ep.geometry("400x550")
    ep.configure(bg="white")
    ep.title("Editar Empleado")
    #ep.iconbitmap('F:\\6to Semestre\\Gestión De Proyectos De Software\\S-O project\Extra\\icon sf.ico')

    def Aceptar_ButtonAction():
        # Obtener los valores modificados por el usuario
        nombre = Name_Box.get()
        telefono = Number_Box.get()
        rfc = RFC_Box.get()
        correo = Mail_Box.get()

        load_suppliers()
        try:
            conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
            cursor = conn.cursor()
            cursor.execute("EXEC modProveedor ?, ?, ?, ?, ?", id_proveedor, nombre, telefono, rfc, correo)
            conn.commit()
            cursor.close()
            conn.close()

            # Actualizar la información en la tabla
            supplier_tree.insert("", "end", values=(nombre, telefono, rfc, correo))
            load_suppliers()
            ep.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el producto: {e}")
    
    Name_Label = Label(ep, text="Nombre", fg="black", bg="white", font=("Arial Black", 9))
    Name_Label.place(x=30, y=30)
    Name_Box = Entry(ep, width=20, bg="lightgray" )
    Name_Box.place(x=155, y=35)
    Name_Box.insert(0, values[0])
    
    Number_Label = Label(ep, text="Telefono", fg="black", bg="white", font=("Arial Black", 9))
    Number_Label.place(x=30, y=75)
    Number_Box = Entry(ep, width=12, bg="lightgray" )
    Number_Box.place(x=155, y=75)
    Number_Box.insert(0, values[1])

    RFC_Label = Label(ep, text="RFC", fg="black", bg="white", font=("Arial Black", 9))
    RFC_Label.place(x=30, y=115)
    RFC_Box = Entry(ep, width=15, bg="lightgray" )
    RFC_Box.place(x=155, y=115)
    RFC_Box.insert(0, values[2])

    Mail_Label = Label(ep, text="Correo", fg="black", bg="white", font=("Arial Black", 9))
    Mail_Label.place(x=30, y=150)
    Mail_Box = Entry(ep, width=30, bg="lightgray" )
    Mail_Box.place(x=155, y=150)
    Mail_Box.insert(0, values[3])

    Aceptar_Button = Button(ep, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=Aceptar_ButtonAction)
    Aceptar_Button.place(x=200, y=250)

    Cancelar_Button = Button(ep, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=ep.destroy)
    Cancelar_Button.place(x=280, y=250)

#Function to delete a employee
def Delete_Supplier():
    selected_item = supplier_tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un Proveedor para desactivar")
        return

    confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea Desactivar este Proveedor?")
    if not confirm:
        return
    
    item = supplier_tree.item(selected_item)
    values = item["values"]
    # Obtener el RFC del empleado seleccionado (suponiendo que es el valor en el índice 4)
    rfc_proveedor = values[2]  # Ajusta según el índice correcto de RFC
    
    # Obtener el id_proveedor usando el RFC
    id_proveedor = obtener_id_proveedor_por_rfc(rfc_proveedor)
    if id_proveedor is None:
        return  # Si no se encuentra el ID, no continuar con la edición

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC marcar_proveedor_inactivo @id_proveedor = ?", id_proveedor)
        conn.commit()
        cursor.close()
        conn.close()

        supplier_tree.delete(selected_item)
        messagebox.showinfo("Éxito", "Proveedor marcado como inactivo correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al marcar el Proveedor como inactivo: {e}")

def load_suppliersInactive():
    try:
        # Limpia el TreeView antes de recargar los registros
        supplier_tree.delete(*supplier_tree.get_children())
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC mostrar_proveedores_inactivos") 
        rows = cursor.fetchall()
        # Concatenate names directly in the loop for efficiency
        for row in rows:
            formatted_row = (
                row[1], #Nombre
                row[2], #Telefono
                row[3], #RFC
                row[4]) #Correo
            supplier_tree.insert("", "end", values=formatted_row)
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los proveedores Inactivos: {e}")

#Evento para la casilla de verificacion
def toggle_inactive_suppliers():
    if show_inactives_var.get():
        load_suppliersInactive()  # Cargar proveedores inactivos
    else:
        load_suppliers()  # Cargar proveedores activos

# Función para cargar empleados según el criterio de búsqueda
def load_suppliers_filter(query=None):
    try:
        # Limpiar el TreeView antes de cargar los registros
        supplier_tree.delete(*supplier_tree.get_children())

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si se hace una búsqueda o se cargan todos los proveedores activos
        if query:
            # Ejecutar el procedimiento almacenado para buscar por nombre
            cursor.execute("EXEC buscarProveedorNombre ?", query)
            rows = cursor.fetchall()
        else:
            # Ejecutar procedimiento para cargar todos los proveedores activos si no hay búsqueda
            load_suppliers()

        # Iterar sobre los resultados y formatear las filas para mostrar el puesto en lugar del ID
        for row in rows:
            formatted_row = (
                row[0], #Nombre
                row[1], #Telefono
                row[2], #RFC
                row[3]) #Correo
            supplier_tree.insert("", "end", values=formatted_row)
        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los empleados: {e}")

# Función para manejar el botón de búsqueda
def search_suppliers():
    query = search_entry.get()  # Obtener texto de búsqueda
    load_suppliers_filter(query=query)


#Buttons----------------------------------
# Barra de búsqueda
search_entry = Entry(rprov, width=30)
search_entry.place(x=70, y=40)

search_button = Button(rprov, text="Buscar", command=search_suppliers)
search_button.place(x=20, y=40)
# Variable para la casilla de verificación
show_inactives_var = BooleanVar()

# Casilla de verificación para mostrar proveedores inactivos
show_inactives_check = Checkbutton(rprov, text="Mostrar Proveedores inactivos", variable=show_inactives_var, bg="white", command=toggle_inactive_suppliers)
show_inactives_check.place(x=20, y=120)

Add_Supplier = Button(rprov, text="Agregar Proveedor", fg="black", bg="#CE7710", command=Add_SupplierWindow, font=("Arial Black", 9))
Add_Supplier.place(x=230, y=120)

Edit_Supplier = Button(rprov, text="Editar Proveedor", fg="black", bg="#CE7710", command=Edit_SupplierWindow, font=("Arial Black", 9))
Edit_Supplier.place(x=440, y=120)

Delete_Supplier = Button(rprov, text="Desactivar Proveedor", fg="black", bg="#CE7710", command=Delete_Supplier, font=("Arial Black", 9))
Delete_Supplier.place(x=640, y=120)


#END--------------------------------------------------
rprov.mainloop()