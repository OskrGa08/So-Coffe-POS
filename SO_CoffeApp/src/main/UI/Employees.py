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

#Logica de los command para que habra resectivas ventanas cada opcion(abrir las ventanas respectivas a cada gestionar)---------------------------------------
# arreglar para poder navegar entre ventanas
def logout():
    remp.destroy()
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


Main_Label = Label(remp, text="EMPLEADOS", fg="black", bg="white", font=("Arial Black", 18))
Main_Label.place(x=645, y=45)

# Table to display products
employee_columns = ("ID Empleado", "Nombre", "Apellidos", "Puesto", "RFC", "Domicilio", "Telefono")
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
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC mostrar_empleados_activos")
        rows = cursor.fetchall()
        # Concatenate names directly in the loop for efficiency
        for row in rows:
            full_name = f"{row[2]} {row[3]}"  # Combine all names
            formatted_row = (
                row[0], 
                row[1], 
                full_name, 
                row[4],
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
def Add_ProductWindow():
    ap = Toplevel(remp)
    ap.geometry("400x550")
    ap.configure(bg="white")
    ap.title("Agregar Empleado")
    #ap.iconbitmap('F:\\6to Semestre\\Gestión De Proyectos De Software\\S-O project\Extra\\icon sf.ico')

    def Aceptar_ButtonAction():
        # Obtener los valores ingresados por el usuario
        id_empleado = Id_Employee_Box.get()
        nombre = Name_Box.get()
        apeP = P_LastName_Box.get()
        apeM = M_LName_Box.get()
        puesto = Puesto_Box.get()
        rfc = RFC_Box.get()
        domicilio = Adress_Box.get()
        telefono = Number_Box.get()

        # Agregar la información a la base de datos utilizando un procedimiento almacenado
        try:
            conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
            cursor = conn.cursor()
            cursor.execute("EXEC addEmpleado ?, ?, ?, ?, ?, ?, ?, ?", id_empleado, nombre, apeP, apeM, puesto, rfc, domicilio, telefono)
            conn.commit()
            cursor.close()
            conn.close()

            # Mostrar la información obtenida en la ventana principal (rgp)
            employee_tree.insert("", "end", values=(id_empleado, nombre, apeP, apeM, puesto, rfc, domicilio, telefono))
            ap.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar el producto: {e}")

    ID_Employee_Label = Label(ap, text="ID Empleado", fg="black", bg="white", font=("Arial Black", 9))
    ID_Employee_Label.place(x=30, y=30)
    Id_Employee_Box = Entry(ap, width=5, bg="lightgray" )
    Id_Employee_Box.place(x=155, y=35)

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

    Puesto_Label = Label(ap, text="Puesto", fg="black", bg="white", font=("Arial Black", 9))
    Puesto_Label.place(x=30, y=200)
    Puesto_Box = Entry(ap, width=15, bg="lightgray" )
    Puesto_Box.place(x=155, y=200)

    RFC_Label = Label(ap, text="RFC", fg="black", bg="white", font=("Arial Black", 9))
    RFC_Label.place(x=30, y=240)
    RFC_Box = Entry(ap, width=15, bg="lightgray" )
    RFC_Box.place(x=155, y=240)

    Adress_Label = Label(ap, text="Domicilio", fg="black", bg="white", font=("Arial Black", 9))
    Adress_Label.place(x=30, y=290)
    Adress_Box = Entry(ap, width=30, bg="lightgray" )
    Adress_Box.place(x=155, y=290)

    Number_Label = Label(ap, text="Telefono", fg="black", bg="white", font=("Arial Black", 9))
    Number_Label.place(x=30, y=330)
    Number_Box = Entry(ap, width=12, bg="lightgray" )
    Number_Box.place(x=155, y=330)

    Aceptar_Button = Button(ap, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=Aceptar_ButtonAction)
    Aceptar_Button.place(x=300, y=70)

    Cancelar_Button = Button(ap, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=ap.destroy)
    Cancelar_Button.place(x=300, y=120)

# Function to open edit employee window ---------------------------------------------
def Edit_EmployeeWindow():
    selected_item = employee_tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un producto para editar")
        return

    item = employee_tree.item(selected_item)
    values = item["values"]

    ee = Toplevel(remp)
    ee.geometry("400x550")
    ee.configure(bg="white")
    ee.title("Editar Empleado")
    #ep.iconbitmap('F:\\6to Semestre\\Gestión De Proyectos De Software\\S-O project\Extra\\icon sf.ico')

    def Aceptar_ButtonAction():
        # Obtener los valores modificados por el usuario
        id_empleado = values[0]
        nombre = Name_Box.get()
        apeP = P_LastName_Box.get()
        apeM = M_LName_Box.get()
        puesto = Puesto_Box.get()
        rfc = RFC_Box.get()
        domicilio = Adress_Box.get()
        telefono = Number_Box.get()
        # Actualizar la información en la base de datos (simulado)
        try:
            conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
            cursor = conn.cursor()
            cursor.execute("EXEC modEmpleado ?, ?, ?, ?, ?, ?, ?, ?", id_empleado, nombre, apeP, apeM, puesto, rfc, domicilio, telefono)
            conn.commit()
            cursor.close()
            conn.close()

            # Actualizar la información en la tabla
            employee_tree.item(selected_item, values=(id_empleado, nombre, apeP, apeM, puesto, rfc, domicilio, telefono))
            ee.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el producto: {e}")
    ID_Employee_Label = Label(ee, text="ID Producto", fg="black", bg="white", font=("Arial Black", 9))
    ID_Employee_Label.place(x=30, y=30)
    ID_Empleado_Value = Label(ee, text=values[0], fg="black", bg="lightgray", font=("Arial Black", 9), width=10)
    ID_Empleado_Value.place(x=115, y=35)

    Name_Label = Label(ee, text="Nombre", fg="black", bg="white", font=("Arial Black", 9))
    Name_Label.place(x=30, y=75)
    Name_Box = Entry(ee, width=20, bg="lightgray" )
    Name_Box.place(x=155, y=75)

    P_LastName_Label = Label(ee, text="Apellido Paterno", fg="black", bg="white", font=("Arial Black", 9))
    P_LastName_Label.place(x=30, y=115)
    P_LastName_Box = Entry(ee, width=20, bg="lightgray" )
    P_LastName_Box.place(x=155, y=115)

    M_LName_Label = Label(ee, text="Apellido Materno", fg="black", bg="white", font=("Arial Black", 9))
    M_LName_Label.place(x=30, y=155)
    M_LName_Box = Entry(ee, width=20, bg="lightgray" )
    M_LName_Box.place(x=155, y=155)

    Puesto_Label = Label(ee, text="Puesto", fg="black", bg="white", font=("Arial Black", 9))
    Puesto_Label.place(x=30, y=200)
    Puesto_Box = Entry(ee, width=15, bg="lightgray" )
    Puesto_Box.place(x=155, y=200)

    RFC_Label = Label(ee, text="RFC", fg="black", bg="white", font=("Arial Black", 9))
    RFC_Label.place(x=30, y=240)
    RFC_Box = Entry(ee, width=15, bg="lightgray" )
    RFC_Box.place(x=155, y=240)

    Adress_Label = Label(ee, text="Domicilio", fg="black", bg="white", font=("Arial Black", 9))
    Adress_Label.place(x=30, y=290)
    Adress_Box = Entry(ee, width=30, bg="lightgray" )
    Adress_Box.place(x=155, y=290)

    Number_Label = Label(ee, text="Telefono", fg="black", bg="white", font=("Arial Black", 9))
    Number_Label.place(x=30, y=330)
    Number_Box = Entry(ee, width=12, bg="lightgray" )
    Number_Box.place(x=155, y=330)

    Aceptar_Button = Button(ee, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=Aceptar_ButtonAction)
    Aceptar_Button.place(x=300, y=70)

    Cancelar_Button = Button(ee, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=ee.destroy)
    Cancelar_Button.place(x=300, y=120)

#Function to delete a employee
def Delete_Employee():
    selected_item = employee_tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
        return

    confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este producto?")
    if not confirm:
        return

    item = employee_tree.item(selected_item)
    id_empleado = item["values"][0]

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

#Buttons----------------------------------
Add_Product = Button(remp, text="Agregar Empleado", fg="black", bg="#CE7710", command=Add_ProductWindow, font=("Arial Black", 9))
Add_Product.place(x=250, y=120)

Edit_Product = Button(remp, text="Editar Empleado", fg="black", bg="#CE7710", command=Edit_EmployeeWindow, font=("Arial Black", 9))
Edit_Product.place(x=670, y=120)

Delete_Product = Button(remp, text="Eliminar Empleado", fg="black", bg="#CE7710", command=Delete_Employee, font=("Arial Black", 9))
Delete_Product.place(x=1050, y=120)


#END--------------------------------------------------
remp.mainloop()