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

#Top Bar-----------------------------------------------
topBar_frame = Frame(rgp, bg="#CE7710")
topBar_frame.place(x=0, y=0, relwidth=1, height=30)

#Logica de los command para que habra resectivas ventanas cada opcion(abrir las ventanas respectivas a cada gestionar)---------------------------------------
# arreglar para poder navegar entre ventanas
def logout():
    rgp.destroy()
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


Main_Label = Label(rgp, text="PRODUCTOS", fg="black", bg="white", font=("Arial Black", 18))
Main_Label.place(x=330, y=55)

# Table to display products
product_columns = ("ID Producto", "Categoria", "Nombre", "Costo")
product_tree = ttk.Treeview(rgp, columns=product_columns, show="headings", height=5)
for col in product_columns:
    product_tree.heading(col, text=col)
product_tree.place(x=20, y=160, height=300)

product_scrollbar = Scrollbar(rgp, orient="vertical", command=product_tree.yview)
product_scrollbar.place(x=802, y=165, height=290)
product_tree.configure(yscrollcommand=product_scrollbar.set)


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
    ap.geometry("300x350")
    ap.configure(bg="white")
    ap.title("Agregar Producto")
    #ap.iconbitmap('F:\\6to Semestre\\Gestión De Proyectos De Software\\S-O project\Extra\\icon sf.ico')

    def Aceptar_ButtonAction():
        values = "Configurar para obtener id"
        # Obtener los valores ingresados por el usuario
        id_producto = values
        category = Category_combobox.get()
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
    ID_Product_Label.place(x=28, y=31)
    ID_Product_Value = Label(ap, text="01", fg="black", bg="lightgray", font=("Arial Black", 9), width=10)
    ID_Product_Value.place(x=115, y=35)

    Category_Labael = Label(ap, text="Categoria", fg="black", bg="white", font=("Arial Black", 9))
    Category_Labael.place(x=30, y=72)
    Category_combobox = ttk.Combobox(ap, width=20)
    Category_combobox.place(x=115, y=72) 

    Name_Label = Label(ap, text="Nombre", fg="black", bg="white", font=("Arial Black", 9))
    Name_Label.place(x=30, y=100)
    Name_Box = Entry(ap, width=20, bg="lightgray" )
    Name_Box.place(x=115, y=105)

    Description_Label = Label(ap, text="Descripcion", fg="black", bg="white", font=("Arial Black", 9))
    Description_Label.place(x=30, y=135)
    Description_Box = Entry(ap, width=20, bg="lightgray" )
    Description_Box.place(x=115, y=135)

    Precio_Label = Label(ap, text="Costo $", fg="black", bg="white", font=("Arial Black", 9))
    Precio_Label.place(x=30, y=165)
    Precio_Box = Entry(ap, width=5, bg="lightgray" )
    Precio_Box.place(x=115, y=165)
    
    Existence_Label = Label(ap, text="Existencia ", fg="black", bg="white", font=("Arial Black", 9))
    Existence_Label.place(x=30, y=192)
    Existence_Box = Entry(ap, width=5, bg="lightgray" )
    Existence_Box.place(x=115, y=192)

    Aceptar_Button = Button(ap, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=Aceptar_ButtonAction)
    Aceptar_Button.place(x=30, y=240)

    Cancelar_Button = Button(ap, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=ap.destroy)
    Cancelar_Button.place(x=100, y=240)

# Function to open add product window kitchen
def Add_ProductWindow_Kitchen():
    apc = Toplevel(rgp)
    apc.geometry("500x350")
    apc.configure(bg="white")
    apc.title("Agregar Producto De Cocina")
    #ap.iconbitmap('F:\\6to Semestre\\Gestión De Proyectos De Software\\S-O project\Extra\\icon sf.ico')

    def Aceptar_ButtonAction():
        values = "Configurar para obtener id"
        # Obtener los valores ingresados por el usuario
        id_producto = values
        category = Category_combobox.get()
        nombre = Name_Box.get()
        descripcion = Description_Box.get()
        costo = float(Precio_Box.get())

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
            apc.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar el producto: {e}")


    ID_Product_Label = Label(apc, text="ID Producto", fg="black", bg="white", font=("Arial Black", 9))
    ID_Product_Label.place(x=28, y=31)
    ID_Product_Value = Label(apc, text="01", fg="black", bg="lightgray", font=("Arial Black", 9), width=10)
    ID_Product_Value.place(x=115, y=35)

    Category_Labael = Label(apc, text="Categoria", fg="black", bg="white", font=("Arial Black", 9))
    Category_Labael.place(x=30, y=72)
    Category_combobox = ttk.Combobox(apc, width=20)
    Category_combobox.place(x=115, y=72) 

    Name_Label = Label(apc, text="Nombre", fg="black", bg="white", font=("Arial Black", 9))
    Name_Label.place(x=30, y=100)
    Name_Box = Entry(apc, width=20, bg="lightgray" )
    Name_Box.place(x=115, y=105)

    Description_Label = Label(apc, text="Descripcion", fg="black", bg="white", font=("Arial Black", 9))
    Description_Label.place(x=30, y=135)
    Description_Box = Entry(apc, width=20, bg="lightgray" )
    Description_Box.place(x=115, y=135)

    Precio_Label = Label(apc, text="Costo $", fg="black", bg="white", font=("Arial Black", 9))
    Precio_Label.place(x=30, y=165)
    Precio_Box = Entry(apc, width=5, bg="lightgray" )
    Precio_Box.place(x=115, y=165)
    
    Aceptar_Button = Button(apc, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=Aceptar_ButtonAction)
    Aceptar_Button.place(x=30, y=240)

    Cancelar_Button = Button(apc, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=apc.destroy)
    Cancelar_Button.place(x=100, y=240)

    Agregar_Ingredientes = Button(apc, text="Agregar Ingredientes", bg="#D9D9D9", fg="black", font=("Arial Black", 9), command=Add_Ingredients)
    Agregar_Ingredientes.place(x=310, y=40)


def Add_Ingredients(): 
    ai = Toplevel(rgp)
    ai.geometry("1150x733")
    ai.configure(bg="#C9C9C9")
    ai.title("Agregar Ingredientes")
    #Frames----------------------------------------------
    bar_frame = Frame(ai, bg="#CE7710")
    ingredients_frame = Frame(ai, bg="white")
    list_frame = Frame(ai, bg="white")

    #Customize Frame
    ingredients_frame.place(x=30, y=60, width=700, height=450)
    list_frame.place(x=745, y=60, width=370, height=450)
    bar_frame.place(x=0, y=0, relwidth=1, height=30)


    #Buttons and Labels main window
    CancelOrder_Button = Button(ai, text="Cancelar", font=("Katibeh",15), fg="red", bg="SystemButtonFace", overrelief=FLAT, width=25, highlightbackground="red")
    CancelOrder_Button.config(bg=ai.cget('bg'))
    CancelOrder_Button.place(x=220, y=550, anchor="center", width=200)

    HoldOrder_Button = Button(ai, text="Aceptar", font=("Katibeh",15), fg="green", bg="SystemButtonFace", overrelief=FLAT, width=25, highlightbackground="green")
    HoldOrder_Button.config(bg=ai.cget('bg'))
    HoldOrder_Button.place(x=440, y=550, anchor="center", width=200)

    #ScrollBar products_frame  --------------------------------------------------- 
    Canvas_scrollbar = Canvas(ingredients_frame)
    Canvas_scrollbar.pack(side=LEFT, fill=BOTH, expand=True)
    inner_frame = Frame(Canvas_scrollbar)
    Canvas_scrollbar.create_window((0, 0), window=inner_frame, anchor="nw")

    ScrollBar_Products = Scrollbar(Canvas_scrollbar, orient=VERTICAL, command=Canvas_scrollbar.yview)
    ScrollBar_Products.pack(side=RIGHT, fill=Y)
    Canvas_scrollbar.config(yscrollcommand = ScrollBar_Products.set)

    def configure_scrollregion(event):
        Canvas_scrollbar.configure(scrollregion=Canvas_scrollbar.bbox("all"))

    Canvas_scrollbar.bind("<Configure>", configure_scrollregion)

    #Customize Checkout_frame----------------------------------------
    Checkout_Label = Label(list_frame, text="Ingredientes", font=("Playfair Display", 10), bg="white", fg="black", width=300)
    Checkout_Label.place(x=135, y=10, anchor="center", relwidth=1, height=10)

    Atributtes_Label = Label(list_frame, text="      Nombre          Cantidad", font=("Arial", 8), bg="#d4d9d6", fg="black")
    Atributtes_Label.place(x=310, y=30, anchor="e", width=420, height=15)

    #Configure Combobox----------------------------------------------------------------------
    employee_label = Label(ai, text="Producto", font=("Arial Black", 10), bg="#C9C9C9", fg="black")
    employee_label.place(x=745, y=35)
    employee_combobox = Entry(ai)
    employee_combobox.place(x=830, y=35)


# Function to open edit product window
def Edit_ProductWindow():
    selected_item = product_tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un producto para editar")
        return

    item = product_tree.item(selected_item)
    values = item["values"]

    ep = Toplevel(rgp)
    ep.geometry("300x350")
    ep.configure(bg="white")
    ep.title("Editar Producto")
    #ep.iconbitmap('F:\\6to Semestre\\Gestión De Proyectos De Software\\S-O project\Extra\\icon sf.ico')

    def Aceptar_ButtonAction():
        # Obtener los valores modificados por el usuario
        id_producto = values[0]
        category = Category_combobox.get()
        nombre = Name_Box.get()
        descripcion = Description_Box.get()
        costo = float(Precio_Box.get())
        existencia = Existence_Box.get()

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
    ID_Product_Label.place(x=28, y=31)
    ID_Product_Value = Label(ep, text="01", fg="black", bg="lightgray", font=("Arial Black", 9), width=10)
    ID_Product_Value.place(x=115, y=35)

    Category_Labael = Label(ep, text="Categoria", fg="black", bg="white", font=("Arial Black", 9))
    Category_Labael.place(x=30, y=72)
    Category_combobox = ttk.Combobox(ep, width=20)
    Category_combobox.place(x=115, y=72) 

    Name_Label = Label(ep, text="Nombre", fg="black", bg="white", font=("Arial Black", 9))
    Name_Label.place(x=30, y=100)
    Name_Box = Entry(ep, width=20, bg="lightgray" )
    Name_Box.place(x=115, y=105)

    Description_Label = Label(ep, text="Descripcion", fg="black", bg="white", font=("Arial Black", 9))
    Description_Label.place(x=30, y=135)
    Description_Box = Entry(ep, width=20, bg="lightgray" )
    Description_Box.place(x=115, y=135)

    Precio_Label = Label(ep, text="Costo $", fg="black", bg="white", font=("Arial Black", 9))
    Precio_Label.place(x=30, y=165)
    Precio_Box = Entry(ep, width=5, bg="lightgray" )
    Precio_Box.place(x=115, y=165)
    
    Existence_Label = Label(ep, text="Existencia ", fg="black", bg="white", font=("Arial Black", 9))
    Existence_Label.place(x=30, y=192)
    Existence_Box = Entry(ep, width=5, bg="lightgray" )
    Existence_Box.place(x=115, y=192)

    Aceptar_Button = Button(ep, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=Aceptar_ButtonAction)
    Aceptar_Button.place(x=30, y=240)

    Cancelar_Button = Button(ep, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=ep.destroy)
    Cancelar_Button.place(x=100, y=240)

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
Add_Product.place(x=30, y=120)

Add_Product_kitchen = Button(rgp, text="Producto Cocina", fg="black", bg="#CE7710", command=Add_ProductWindow_Kitchen, font=("Arial Black", 9))
Add_Product_kitchen.place(x=250, y=120)

Edit_Product = Button(rgp, text="Editar producto", fg="black", bg="#CE7710", command=Edit_ProductWindow, font=("Arial Black", 9))
Edit_Product.place(x=460, y=120)

Delete_Product = Button(rgp, text="Desactivar Producto", fg="black", bg="#CE7710", command=Delete_Product, font=("Arial Black", 9))
Delete_Product.place(x=640, y=120)

load_products()
rgp.mainloop()