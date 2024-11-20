from tkinter import messagebox
import pyodbc
from tkinter import *
from tkinter import ttk

# Configuration main window---------------------------
remp = Tk()
remp.geometry("1440x530")
remp.minsize(400, 400)
remp.maxsize(1600, 680)
remp.configure(bg="white")
remp.title("Registrar nuevo empleado")

#Top Bar-----------------------------------------------
topBar_frame = Frame(remp, bg="#CE7710")
topBar_frame.place(x=0, y=0, relwidth=1, height=30)

#Methods to nav amoung windows
def managInputs():
    remp.destroy()
    from Inputs import Inputs
    Inputs()

def managOutPuts():
    remp.destroy()
    from OutPuts import OutPuts
    OutPuts()

def pontiOfSale():
    remp.destroy()
    from POS import POS 
    POS()

def managPosition():
    remp.destroy()
    from Position import Position
    Position()

def managProductCategory():
    remp.destroy()
    from ProductCategory import ProductCategory
    ProductCategory()

def managProducts():
    remp.destroy()
    from Products import Products 
    Products()

def managSells():
    remp.destroy()
    from Sells import Sells 
    Sells()

def managShopping():
    remp.destroy()
    from Shopping import Shopping
    Shopping()

def  managSupplier():
    remp.destroy()
    from Suppliers import Suppliers 
    Suppliers()



# Load the image using PIL
MB_image = PhotoImage(file="SO_CoffeApp/src/main/resources/menu_bar.png")
# Create a label to display the background image
MenuButton_barFrame = Menubutton(topBar_frame, image=MB_image ,bg="#CE7710", width=30, height=30)
MenuButton_barFrame.place(x=0, y=0)
MenuButton_barFrame.menu = Menu(MenuButton_barFrame, tearoff=0, bg="#CE7710")
MenuButton_barFrame.menu.add_command(label="Gestion de Insumos", foreground="white", font=("New Times Roman", 12), command=managInputs)
MenuButton_barFrame.menu.add_command(label="Gestion de Salidas", foreground="white", font=("New Times Roman", 12), command=managOutPuts)
MenuButton_barFrame.menu.add_command(label="Punto de Venta", foreground="white", font=("New Times Roman", 12), command=pontiOfSale)
MenuButton_barFrame.menu.add_command(label="Puestos de Empleados", foreground="white", font=("New Times Roman", 12), command=managPosition)
MenuButton_barFrame.menu.add_command(label="Categoria de Productos", foreground="white", font=("New Times Roman", 12), command=managProductCategory)
MenuButton_barFrame.menu.add_command(label="Gestion de Productos", foreground="white", font=("New Times Roman", 12), command=managProducts)
MenuButton_barFrame.menu.add_command(label="Gestion de Ventas", foreground="white", font=("New Times Roman", 12), command= managSells)
MenuButton_barFrame.menu.add_command(label="Gestion de Compras", foreground="white", font=("New Times Roman", 12), command=managShopping)
MenuButton_barFrame.menu.add_command(label="Gestion de Proveedores", foreground="white", font=("New Times Roman", 12), command=managSupplier)
MenuButton_barFrame["menu"]= MenuButton_barFrame.menu   

Main_Label = Label(remp, text="EMPLEADOS", fg="black", bg="white", font=("Arial Black", 18))
Main_Label.place(x=645, y=45)

# Table to display products
employee_columns = ("Nombre", "Apellido Paterno", "Apellido Materno", "Puesto", "RFC", "Domicilio", "Telefono")
employee_tree = ttk.Treeview(remp, columns=employee_columns, show="headings", height=5)

for col in employee_columns:
    employee_tree.heading(col, text=col)
employee_tree.place(x=20, y=160, height=200)

employee_scrollbar = Scrollbar(remp, orient="vertical", command=employee_tree.yview)
employee_scrollbar.place(x=1402, y=162, height=195)
employee_tree.configure(yscrollcommand=employee_scrollbar.set)


# Connection db---------------------------------------------------------
def get_db_connection():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123;')
    return conn
#Load employees to show---------------------------------------------------
def load_employees():
    try:
        # Limpia el TreeView antes de recargar los registros
        employee_tree.delete(*employee_tree.get_children())

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC mostrar_empleados_activos")
        rows = cursor.fetchall()
        # Concatenate names directly in the loop for efficiency
        for row in rows:
            formatted_row = ( 
                row[2], 
                row[3],
                row[4], 
                row[1],
                row[5],
                row[6],
                row[7])
            employee_tree.insert("", "end", values=formatted_row)
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los empleados: {e}")
load_employees()

# Function to open add employee window---------------------------------------------
def Add_EmployeeWindow():
    ap = Toplevel(remp)
    ap.geometry("400x550")
    ap.configure(bg="white")
    ap.title("Agregar Empleado")

    def Aceptar_ButtonAction():
        # Obtener los valores ingresados por el usuario
        # Obtener el `id_puesto` desde el ComboBox
        puesto_seleccionado = position_combobox.get()
        id_puesto = positions_dict.get(puesto_seleccionado, None)  # Obtener ID del puesto
        nombre = Name_Box.get()
        apeP = P_LastName_Box.get()
        apeM = M_LName_Box.get()
        rfc = RFC_Box.get()
        domicilio = Adress_Box.get()
        telefono = Number_Box.get()

        # Agregar la información a la base de datos utilizando un procedimiento almacenado
        try:
            conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
            cursor = conn.cursor()
            cursor.execute("EXEC addEmpleado ?, ?, ?, ?, ?, ?, ?",id_puesto, nombre, apeP, apeM, rfc, domicilio, telefono)
            conn.commit()
            cursor.close()
            conn.close()

            # Mostrar la información obtenida en la ventana principal 
            employee_tree.insert("", "end", values=(nombre, apeP, apeM, puesto_seleccionado, rfc, domicilio, telefono))
            load_employees()
            ap.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar el producto: {e}")

    Position_Label = Label(ap, text="Puesto", fg="black", bg="white", font=("Arial Black", 9))
    Position_Label.place(x=30, y=30)
    position_combobox = ttk.Combobox(ap, state="readonly", width=30)
    position_combobox.place(x=155, y=35)

    # Cargar puestos con ID en el ComboBox
    def load_positions_combobox():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("EXEC mostrarPuestos")
            rows = cursor.fetchall()
            
            # Crear diccionario para almacenar {nombre: id}
            positions_dict = {row[1]: row[0] for row in rows}  # row[0]: id_puesto, row[1]: nombre del puesto
            position_combobox['values'] = list(positions_dict.keys())  # Mostrar nombres de puestos

            cursor.close()
            conn.close()
            return positions_dict
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los puestos en ComboBox: {e}")

    # Llamar a la función para cargar los puestos en el ComboBox
    positions_dict = load_positions_combobox()
    
    Name_Label = Label(ap, text="Nombre", fg="black", bg="white", font=("Arial Black", 9))
    Name_Label.place(x=30, y=75)
    Name_Box = Entry(ap, width=20, bg="lightgray" )
    Name_Box.place(x=155, y=75)

    P_LastName_Label = Label(ap, text="Apellido Paterno", fg="black", bg="white", font=("Arial Black", 9))
    P_LastName_Label.place(x=30, y=115)
    P_LastName_Box = Entry(ap, width=20, bg="lightgray" )
    P_LastName_Box.place(x=155, y=115)

    M_LName_Label = Label(ap, text="Apellido Materno", fg="black", bg="white", font=("Arial Black", 9))
    M_LName_Label.place(x=30, y=155)
    M_LName_Box = Entry(ap, width=20, bg="lightgray" )
    M_LName_Box.place(x=155, y=155)

    RFC_Label = Label(ap, text="RFC", fg="black", bg="white", font=("Arial Black", 9))
    RFC_Label.place(x=30, y=200)
    RFC_Box = Entry(ap, width=15, bg="lightgray" )
    RFC_Box.place(x=155, y=200)

    Adress_Label = Label(ap, text="Domicilio", fg="black", bg="white", font=("Arial Black", 9))
    Adress_Label.place(x=30, y=240)
    Adress_Box = Entry(ap, width=30, bg="lightgray" )
    Adress_Box.place(x=155, y=240)

    Number_Label = Label(ap, text="Telefono", fg="black", bg="white", font=("Arial Black", 9))
    Number_Label.place(x=30, y=290)
    Number_Box = Entry(ap, width=12, bg="lightgray" )
    Number_Box.place(x=155, y=290)

    Aceptar_Button = Button(ap, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=Aceptar_ButtonAction)
    Aceptar_Button.place(x=200, y=330)

    Cancelar_Button = Button(ap, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=ap.destroy)
    Cancelar_Button.place(x=280, y=330)

def obtener_id_empleado_por_rfc(rfc):
    """Obtiene el id_empleado a partir del RFC."""
    try:
        conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
        cursor = conn.cursor()
        cursor.execute("SELECT id_empleado FROM empleado WHERE rfc = ?", rfc)
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            return result[0]  # Regresa el id_empleado
        else:
            messagebox.showerror("Error", "Empleado no encontrado")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener el ID del empleado: {e}")
        return None

# Function to open edit employee window ---------------------------------------------
def Edit_EmployeeWindow():
    selected_item = employee_tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un producto para editar")
        return

    item = employee_tree.item(selected_item)
    values = item["values"]
    # Obtener el RFC del empleado seleccionado (suponiendo que es el valor en el índice 4)
    rfc_empleado = values[4]  # Ajusta según el índice correcto de RFC
    
    # Obtener el id_empleado usando el RFC
    id_empleado = obtener_id_empleado_por_rfc(rfc_empleado)
    if id_empleado is None:
        return  # Si no se encuentra el ID, no continuar con la edición
    
    load_employees()
    ee = Toplevel(remp)
    ee.geometry("400x550")
    ee.configure(bg="white")
    ee.title("Editar Empleado")

    def Aceptar_ButtonAction():
        # Obtener los valores modificados por el usuario
        puesto_seleccionado = position_combobox.get()
        id_puesto = int(positions_dict.get(puesto_seleccionado))  # Asegurarse de que id_puesto sea un entero
        nombre = Name_Box.get()
        apeP = P_LastName_Box.get()
        apeM = M_LName_Box.get()
        rfc = RFC_Box.get()
        domicilio = Adress_Box.get()
        telefono = Number_Box.get()
        load_employees()
         # Validate id_puesto to ensure it's an integer
        if not isinstance(id_puesto, int):
            raise ValueError("Invalid puesto ID")
        
        try:
            print(id_empleado, id_puesto, nombre, apeP, apeM, rfc, domicilio, telefono)
            conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
            cursor = conn.cursor()
            cursor.execute("EXEC modEmpleado ?, ?, ?, ?, ?, ?, ?, ?", id_empleado, int(id_puesto), nombre, apeP, apeM, rfc, domicilio, telefono)
            conn.commit()
            cursor.close()
            conn.close()
            # Actualizar la información en la tabla
            employee_tree.insert("", "end", values=(nombre, apeP, apeM, puesto_seleccionado ,rfc, domicilio, telefono))
            load_employees()
            ee.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el empleado: {e}")
    
    Position_Label = Label(ee, text="Puesto", fg="black", bg="white", font=("Arial Black", 9))
    Position_Label.place(x=30, y=30)
    position_combobox = ttk.Combobox(ee, state="readonly", width=30)
    position_combobox.place(x=155, y=35)
    position_combobox.set(values[3])

    # Cargar puestos con ID en el ComboBox
    def load_positions_combobox():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("EXEC mostrarPuestos")
            rows = cursor.fetchall()
            
            # Crear diccionario para almacenar {nombre: id}
            positions_dict = {row[1]: row[0] for row in rows}  # row[0]: id_puesto, row[1]: nombre del puesto
            position_combobox['values'] = list(positions_dict.keys())  # Mostrar nombres de puestos
            print(rows)  # Verifica el contenido de las filas
            cursor.close()
            conn.close()
            return positions_dict
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los puestos en ComboBox: {e}")

    # Llamar a la función para cargar los puestos en el ComboBox
    positions_dict = load_positions_combobox()

    Name_Label = Label(ee, text="Nombre", fg="black", bg="white", font=("Arial Black", 9))
    Name_Label.place(x=30, y=75)
    Name_Box = Entry(ee, width=20, bg="lightgray" )
    Name_Box.place(x=155, y=75)
    Name_Box.insert(0, values[0])

    P_LastName_Label = Label(ee, text="Apellido Paterno", fg="black", bg="white", font=("Arial Black", 9))
    P_LastName_Label.place(x=30, y=115)
    P_LastName_Box = Entry(ee, width=20, bg="lightgray")
    P_LastName_Box.place(x=155, y=115)
    P_LastName_Box.insert(0, values[1])

    M_LName_Label = Label(ee, text="Apellido Materno", fg="black", bg="white", font=("Arial Black", 9))
    M_LName_Label.place(x=30, y=155)
    M_LName_Box = Entry(ee, width=20, bg="lightgray" )
    M_LName_Box.place(x=155, y=155)
    M_LName_Box.insert(0, values[2])

    RFC_Label = Label(ee, text="RFC", fg="black", bg="white", font=("Arial Black", 9))
    RFC_Label.place(x=30, y=200)
    RFC_Box = Entry(ee, width=15, bg="lightgray" )
    RFC_Box.place(x=155, y=200)
    RFC_Box.insert(0, values[4])

    Adress_Label = Label(ee, text="Domicilio", fg="black", bg="white", font=("Arial Black", 9))
    Adress_Label.place(x=30, y=240)
    Adress_Box = Entry(ee, width=30, bg="lightgray" )
    Adress_Box.place(x=155, y=240)
    Adress_Box.insert(0, values[5])

    Number_Label = Label(ee, text="Telefono", fg="black", bg="white", font=("Arial Black", 9))
    Number_Label.place(x=30, y=290)
    Number_Box = Entry(ee, width=12, bg="lightgray" )
    Number_Box.place(x=155, y=290)
    Number_Box.insert(0, values[6])

    Aceptar_Button = Button(ee, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=Aceptar_ButtonAction)
    Aceptar_Button.place(x=200, y=330)

    Cancelar_Button = Button(ee, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=ee.destroy)
    Cancelar_Button.place(x=280, y=330)

#Function to delete a employee
def Delete_Employee():
    selected_item = employee_tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un empleado para Desactivar")
        return

    confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea desactivar este empleado?")
    if not confirm:
        return

    item = employee_tree.item(selected_item)
    values = item["values"]
    item = employee_tree.item(selected_item)
    # Obtener el RFC del empleado seleccionado (suponiendo que es el valor en el índice 4)
    rfc_empleado = values[4]  # Ajusta según el índice correcto de RFC
    
    # Obtener el id_empleado usando el RFC
    id_empleado = obtener_id_empleado_por_rfc(rfc_empleado)
    if id_empleado is None:
        return  # Si no se encuentra el ID, no continuar con la edición

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC marcar_empleado_inactivo @id_empleado = ?", id_empleado)
        conn.commit()
        cursor.close()
        conn.close()

        employee_tree.delete(selected_item)
        messagebox.showinfo("Éxito", "Producto marcado como inactivo correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al marcar el producto como inactivo: {e}")

#Load employees inactives to show---------------------------------------------------
def load_employeeInactive():
    try:
        # Limpia el TreeView antes de recargar los registros
        employee_tree.delete(*employee_tree.get_children())

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC mostrar_empleados_inactivos")
        rows = cursor.fetchall()
        # Concatenate names directly in the loop for efficiency
        for row in rows:
            formatted_row = ( 
                row[2], 
                row[3],
                row[4], 
                row[1],
                row[5],
                row[6],
                row[7])
            employee_tree.insert("", "end", values=formatted_row)
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los empleados inactivos: {e}")

# Evento para la casilla de verificación
def toggle_inactive_employees():
    if show_inactives_var.get():
        load_employeeInactive()  # Cargar empleados inactivos
    else:
        load_employees()  # Cargar empleados activos


# Función para cargar empleados según el criterio de búsqueda
def load_employees_filter(query=None):
    try:
        # Limpiar el TreeView antes de cargar los registros
        employee_tree.delete(*employee_tree.get_children())

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si se hace una búsqueda o se cargan todos los empleados activos
        if query:
            # Ejecutar procedimientos almacenados para buscar en cada campo específico
            if query.isalpha():
                cursor.execute("EXEC buscarEmpleadoNombre ?", query)
            elif query.isdigit():
                cursor.execute("EXEC buscarEmpleadoApellidoP ?", query)
            elif len(query) == 1:  # Ajuste según el tipo de búsqueda o campo
                cursor.execute("EXEC buscarEmpleadoApellidoM ?", query)
            else:
                cursor.execute("EXEC buscarEmpleadoPuesto ?", query)

            rows = cursor.fetchall()
        else:
            # Ejecutar procedimiento para cargar todos los empleados activos si no hay búsqueda
            load_employees()

        # Iterar sobre los resultados y formatear las filas para mostrar el puesto en lugar del ID
        for row in rows:
            formatted_row = (
                row[1],  # Nombre
                row[2],  # Apellido Paterno
                row[3],  # Apellido Materno
                row[4],  # Nombre del Puesto en lugar del ID
                row[5],  # RFC
                row[6],  # Domicilio
                row[7]   # Teléfono
            )
            employee_tree.insert("", "end", values=formatted_row)

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los empleados: {e}")

# Función para manejar el botón de búsqueda
def search_employees():
    query = search_entry.get()  # Obtener texto de búsqueda
    load_employees_filter(query=query)



#Buttons----------------------------------
# Barra de búsqueda
search_entry = Entry(remp, width=30)
search_entry.place(x=70, y=40)

search_button = Button(remp, text="Buscar", command=search_employees)
search_button.place(x=20, y=40)

# Variable para la casilla de verificación
show_inactives_var = BooleanVar()

# Casilla de verificación para mostrar empleados inactivos
show_inactives_check = Checkbutton(remp, text="Mostrar empleados inactivos", variable=show_inactives_var, bg="white", command=toggle_inactive_employees)
show_inactives_check.place(x=20, y=120)

Add_Product = Button(remp, text="Agregar Empleado", fg="black", bg="#CE7710", command=Add_EmployeeWindow, font=("Arial Black", 9))
Add_Product.place(x=270, y=120)

Edit_Product = Button(remp, text="Editar Empleado", fg="black", bg="#CE7710", command=Edit_EmployeeWindow, font=("Arial Black", 9))
Edit_Product.place(x=690, y=120)

Delete_Product = Button(remp, text="Desactivar Empleado", fg="black", bg="#CE7710", command=Delete_Employee, font=("Arial Black", 9))
Delete_Product.place(x=1070, y=120)


#END--------------------------------------------------
remp.mainloop()