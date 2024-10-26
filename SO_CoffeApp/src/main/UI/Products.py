import pyodbc
from tkinter import *
from tkinter import Scrollbar
from tkinter import Menubutton
from tkinter import messagebox
from tkinter import ttk

# Configuration main window---------------------------
rgp = Tk()
rgp.geometry("850x700")
rgp.minsize(700, 500)
rgp.maxsize(1500, 580)
rgp.configure(bg="white")
rgp.title("Registrar nuevo producto")


Main_Label = Label(rgp, text="PRODUCTOS", fg="black", bg="white", font=("Arial Black", 18))
Main_Label.place(x=330, y=75)

# Table to display products
product_columns = ("ID Producto", "Nombre", "Descripcion", "Precio")
product_tree = ttk.Treeview(rgp, columns=product_columns, show="headings", height=5)
for col in product_columns:
    product_tree.heading(col, text=col)
product_tree.place(x=20, y=160, height=200)

def get_db_connection():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123;')
    return conn

def load_products():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC mostrar_productos_activos")
        rows = cursor.fetchall()
        for row in rows:
            formatted_row = (row[0], row[1], row[2], f"{row[3]:.2f}")
            product_tree.insert("", "end", values=formatted_row)
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los productos: {e}")

# Function to open add product window
def Add_ProductWindow():
    ap = Toplevel(rgp)
    ap.geometry("400x250")
    ap.configure(bg="white")
    ap.title("Agregar Producto")
    #ap.iconbitmap('F:\\6to Semestre\\Gestión De Proyectos De Software\\S-O project\Extra\\icon sf.ico')

    def Aceptar_ButtonAction():
        # Obtener los valores ingresados por el usuario
        id_producto = Id_Product_Box.get()
        nombre = Name_Box.get()
        descripcion = Description_Box.get()
        costo = float(Precio_Box.get())
        existencia = Existence_Box.get()

        # Agregar la información a la base de datos utilizando un procedimiento almacenado
        try:
            conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
            cursor = conn.cursor()
            cursor.execute("EXEC addProducto ?, ?, ?, ?", id_producto, nombre, descripcion, costo)
            conn.commit()
            cursor.close()
            conn.close()

            # Mostrar la información obtenida en la ventana principal (rgp)
            product_tree.insert("", "end", values=(id_producto, nombre, descripcion, costo))
            ap.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar el producto: {e}")


    ID_Product_Label = Label(ap, text="ID Producto", fg="black", bg="white", font=("Arial Black", 9))
    ID_Product_Label.place(x=30, y=30)
    Id_Product_Box = Entry(ap, width=5, bg="lightgray" )
    Id_Product_Box.place(x=115, y=35)

    Name_Label = Label(ap, text="Nombre", fg="black", bg="white", font=("Arial Black", 9))
    Name_Label.place(x=30, y=75)
    Name_Box = Entry(ap, width=20, bg="lightgray" )
    Name_Box.place(x=115, y=75)

    Description_Label = Label(ap, text="Descripcion", fg="black", bg="white", font=("Arial Black", 9))
    Description_Label.place(x=30, y=115)
    Description_Box = Entry(ap, width=20, bg="lightgray" )
    Description_Box.place(x=115, y=115)

    Precio_Label = Label(ap, text="Precio $", fg="black", bg="white", font=("Arial Black", 9))
    Precio_Label.place(x=30, y=145)
    Precio_Box = Entry(ap, width=5, bg="lightgray" )
    Precio_Box.place(x=115, y=145)
    
    Existence_Label = Label(ap, text="Existencia $", fg="black", bg="white", font=("Arial Black", 9))
    Existence_Label.place(x=30, y=145)
    Existence_Box = Entry(ap, width=5, bg="lightgray" )
    Existence_Box.place(x=115, y=145)

    Aceptar_Button = Button(ap, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=Aceptar_ButtonAction)
    Aceptar_Button.place(x=300, y=70)

    Cancelar_Button = Button(ap, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=ap.destroy)
    Cancelar_Button.place(x=300, y=120)

# Function to open edit product window
def Edit_ProductWindow():
    selected_item = product_tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un producto para editar")
        return

    item = product_tree.item(selected_item)
    values = item["values"]

    ep = Toplevel(rgp)
    ep.geometry("400x250")
    ep.configure(bg="white")
    ep.title("Editar Producto")
    #ep.iconbitmap('F:\\6to Semestre\\Gestión De Proyectos De Software\\S-O project\Extra\\icon sf.ico')

    def Aceptar_ButtonAction():
        # Obtener los valores modificados por el usuario
        id_producto = values[0]
        nombre = Name_Box.get()
        descripcion = Description_Box.get()
        costo = float(Precio_Box.get())

        # Actualizar la información en la base de datos (simulado)
        try:
            conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
            cursor = conn.cursor()
            cursor.execute("EXEC modProducto ?, ?, ?, ?", id_producto, nombre, descripcion, costo)
            conn.commit()
            cursor.close()
            conn.close()

            # Actualizar la información en la tabla
            product_tree.item(selected_item, values=(id_producto, nombre, descripcion, costo))
            ep.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el producto: {e}")
    ID_Product_Label = Label(ep, text="ID Producto", fg="black", bg="white", font=("Arial Black", 9))
    ID_Product_Label.place(x=30, y=30)
    ID_Product_Value = Label(ep, text=values[0], fg="black", bg="lightgray", font=("Arial Black", 9), width=10)
    ID_Product_Value.place(x=115, y=35)

    Name_Label = Label(ep, text="Nombre", fg="black", bg="white", font=("Arial Black", 9))
    Name_Label.place(x=30, y=75)
    Name_Box = Entry(ep, width=20, bg="lightgray")
    Name_Box.place(x=115, y=75)
    Name_Box.insert(0, values[1])

    Description_Label = Label(ep, text="Descripcion", fg="black", bg="white", font=("Arial Black", 9))
    Description_Label.place(x=30, y=115)
    Description_Box = Entry(ep, width=20, bg="lightgray")
    Description_Box.place(x=115, y=115)
    Description_Box.insert(0, values[2])

    Precio_Label = Label(ep, text="Precio $", fg="black", bg="white", font=("Arial Black", 9))
    Precio_Label.place(x=30, y=145)
    Precio_Box = Entry(ep, width=5, bg="lightgray")
    Precio_Box.place(x=115, y=145)
    Precio_Box.insert(0, values[3])

    Aceptar_Button = Button(ep, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=Aceptar_ButtonAction)
    Aceptar_Button.place(x=300, y=70)

    Cancelar_Button = Button(ep, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=ep.destroy)
    Cancelar_Button.place(x=300, y=120)

# Function to delete a product
def Delete_Product():
    selected_item = product_tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
        return

    confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este producto?")
    if not confirm:
        return

    item = product_tree.item(selected_item)
    ID_producto = item["values"][0]

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC marcar_producto_inactivo @id_producto = ?", ID_producto)
        conn.commit()
        cursor.close()
        conn.close()

        product_tree.delete(selected_item)
        messagebox.showinfo("Éxito", "Producto marcado como inactivo correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al marcar el producto como inactivo: {e}")

Add_Product = Button(rgp, text="Agregar producto", fg="black", bg="#CE7710", command=Add_ProductWindow, font=("Arial Black", 9))
Add_Product.place(x=650, y=40)

Edit_Product = Button(rgp, text="Editar producto", fg="black", bg="#CE7710", command=Edit_ProductWindow, font=("Arial Black", 9))
Edit_Product.place(x=650, y=80)

Delete_Product = Button(rgp, text="Eliminar producto", fg="black", bg="#CE7710", command=Delete_Product, font=("Arial Black", 9))
Delete_Product.place(x=650, y=120)

load_products()
rgp.mainloop()