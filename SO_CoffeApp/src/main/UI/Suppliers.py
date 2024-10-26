from tkinter import messagebox
import pyodbc
from tkinter import *
from tkinter import ttk

# Configuration main window---------------------------
rprov = Tk()
rprov.geometry("650x430")
rprov.minsize(400, 400)
rprov.maxsize(1500, 580)
rprov.configure(bg="white")
rprov.title("Registrar nuevo Proveedor")


Main_Label = Label(rprov, text="PROVEEDOR", fg="black", bg="white", font=("Arial Black", 18))
Main_Label.place(x=250, y=75)

# Table to display suppliers
product_columns = ("ID Proveedores", "Nombre", "Apellidos")
product_tree = ttk.Treeview(rprov, columns=product_columns, show="headings", height=5)

for col in product_columns:
    product_tree.heading(col, text=col)
product_tree.place(x=20, y=160, height=200)

# Connection db---------------------------------------------------------
def get_db_connection():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123;')
    return conn

#Load suppliers to show---------------------------------------------------
def load_suppliers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # cursor.execute("EXEC mostrar_empleados_activos") Modificar
        rows = cursor.fetchall()
        # Concatenate names directly in the loop for efficiency
        for row in rows:
            full_name = f"{row[2]} {row[3]}"  # Combine all names
            formatted_row = (row[0], row[1], full_name)
            product_tree.insert("", "end", values=formatted_row)
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los proveedores: {e}")
load_suppliers()

# Function to open add suppliers window---------------------------------------------
def Add_ProductWindow():
    ap = Toplevel(rprov)
    ap.geometry("400x550")
    ap.configure(bg="white")
    ap.title("Agregar Proveedor")
    #ap.iconbitmap('F:\\6to Semestre\\Gestión De Proyectos De Software\\S-O project\Extra\\icon sf.ico')

    def Aceptar_ButtonAction():
        # Obtener los valores ingresados por el usuario
        id_proveedor = Id_Supplier_Box.get()
        nombre = Name_Box.get()
        rfc = RFC_Box.get()
        correo = Mail_Box.get()
        telefono = Number_Box.get()

        # Agregar la información a la base de datos utilizando un procedimiento almacenado
        try:
            conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
            cursor = conn.cursor()
            cursor.execute("EXEC addEmpleado ?, ?, ?, ?, ?", id_proveedor, nombre, rfc, correo, telefono)
            conn.commit()
            cursor.close()
            conn.close()

            # Mostrar la información obtenida en la ventana principal (rgp)
            product_tree.insert("", "end", values=(id_proveedor, nombre, rfc, correo, telefono))
            ap.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar el producto: {e}")

    ID_Supplier_Label = Label(ap, text="ID Proveedor", fg="black", bg="white", font=("Arial Black", 9))
    ID_Supplier_Label.place(x=30, y=30)
    Id_Supplier_Box = Entry(ap, width=5, bg="lightgray" )
    Id_Supplier_Box.place(x=155, y=35)

    Name_Label = Label(ap, text="Nombre", fg="black", bg="white", font=("Arial Black", 9))
    Name_Label.place(x=30, y=75)
    Name_Box = Entry(ap, width=20, bg="lightgray" )
    Name_Box.place(x=155, y=75)

    RFC_Label = Label(ap, text="RFC", fg="black", bg="white", font=("Arial Black", 9))
    RFC_Label.place(x=30, y=115)
    RFC_Box = Entry(ap, width=15, bg="lightgray" )
    RFC_Box.place(x=155, y=115)

    Mail_Label = Label(ap, text="Correo", fg="black", bg="white", font=("Arial Black", 9))
    Mail_Label.place(x=30, y=150)
    Mail_Box = Entry(ap, width=30, bg="lightgray" )
    Mail_Box.place(x=155, y=150)

    Number_Label = Label(ap, text="Telefono", fg="black", bg="white", font=("Arial Black", 9))
    Number_Label.place(x=30, y=190)
    Number_Box = Entry(ap, width=12, bg="lightgray" )
    Number_Box.place(x=155, y=190)

    Aceptar_Button = Button(ap, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=Aceptar_ButtonAction)
    Aceptar_Button.place(x=300, y=50)

    Cancelar_Button = Button(ap, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=ap.destroy)
    Cancelar_Button.place(x=300, y=90)

# Function to open edit employee window ---------------------------------------------
def Edit_EmployeeWindow():
    selected_item = product_tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un Proveedor para editar")
        return

    item = product_tree.item(selected_item)
    values = item["values"]

    ee = Toplevel(rprov)
    ee.geometry("400x550")
    ee.configure(bg="white")
    ee.title("Editar Empleado")
    #ep.iconbitmap('F:\\6to Semestre\\Gestión De Proyectos De Software\\S-O project\Extra\\icon sf.ico')

    def Aceptar_ButtonAction():
        # Obtener los valores modificados por el usuario
        id_proveedor = values[0]
        nombre = Name_Box.get()
        rfc = RFC_Box.get()
        correo = Mail_Box.get()
        telefono = Number_Box.get()
        # Actualizar la información en la base de datos (simulado)
        try:
            conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
            cursor = conn.cursor()
            cursor.execute("EXEC modEmpleado ?, ?, ?, ?, ?", id_proveedor, nombre, rfc, correo, telefono)
            conn.commit()
            cursor.close()
            conn.close()

            # Actualizar la información en la tabla
            product_tree.insert("", "end", values=(id_proveedor, nombre, rfc, correo, telefono))
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

    RFC_Label = Label(ee, text="RFC", fg="black", bg="white", font=("Arial Black", 9))
    RFC_Label.place(x=30, y=115)
    RFC_Box = Entry(ee, width=15, bg="lightgray" )
    RFC_Box.place(x=155, y=115)

    Mail_Label = Label(ee, text="Correo", fg="black", bg="white", font=("Arial Black", 9))
    Mail_Label.place(x=30, y=150)
    Mail_Box = Entry(ee, width=30, bg="lightgray" )
    Mail_Box.place(x=155, y=150)

    Number_Label = Label(ee, text="Telefono", fg="black", bg="white", font=("Arial Black", 9))
    Number_Label.place(x=30, y=190)
    Number_Box = Entry(ee, width=12, bg="lightgray" )
    Number_Box.place(x=155, y=190)

    Aceptar_Button = Button(ee, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=Aceptar_ButtonAction)
    Aceptar_Button.place(x=300, y=50)

    Cancelar_Button = Button(ee, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=ee.destroy)
    Cancelar_Button.place(x=300, y=90)

#Function to delete a employee
def Delete_Employee():
    selected_item = product_tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un Proveedor para eliminar")
        return

    confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este Proveedor?")
    if not confirm:
        return

    item = product_tree.item(selected_item)
    id_proveedor = item["values"][0]

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC marcar_empleado_inactivo @id_empleado = ?", id_proveedor)
        conn.commit()
        cursor.close()
        conn.close()

        product_tree.delete(selected_item)
        messagebox.showinfo("Éxito", "Proveedor marcado como inactivo correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al marcar el Proveedor como inactivo: {e}")



#Buttons----------------------------------
Add_Supplier = Button(rprov, text="Agregar Proveedor", fg="black", bg="#CE7710", command=Add_ProductWindow, font=("Arial Black", 9))
Add_Supplier.place(x=500, y=30)

Edit_Supplier = Button(rprov, text="Editar Proveedor", fg="black", bg="#CE7710", command=Edit_EmployeeWindow, font=("Arial Black", 9))
Edit_Supplier.place(x=500, y=70)

Delete_Supplier = Button(rprov, text="Eliminar Proveedor", fg="black", bg="#CE7710", command=Delete_Employee, font=("Arial Black", 9))
Delete_Supplier.place(x=500, y=110)


#END--------------------------------------------------
rprov.mainloop()