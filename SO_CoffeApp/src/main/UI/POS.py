from decimal import Decimal
from functools import partial
from pathlib import Path
from tkinter import *
from tkinter import Scrollbar
from tkinter import Menubutton
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Combobox
import pyodbc
from PIL import Image, ImageTk
import tkinter as tk
# Configuration main window--------------------------------------
mw = Tk()
mw.geometry("1150x733")
mw.minsize(700, 500)
mw.maxsize(1224, 580)
mw.configure(bg="#C9C9C9")
mw.title("Punto de Venta")
# Icon --------------------------
base_dir = Path(__file__).resolve().parent
icon_path = base_dir.parent / 'resources' / 'icon sf.ico'
icon_path_str = str(icon_path)
if icon_path.exists():
    try:
        mw.iconbitmap(icon_path_str)
    except Exception as e:
        print(f"Error al cargar el icono: {e}")
else:
    print(f"El archivo de icono no se encuentra en la ruta especificada: {icon_path_str}")

#Frames----------------------------------------------
bar_frame = Frame(mw, bg="#CE7710")
products_frame = Frame(mw, bg="white")
checkout_frame = Frame(mw, bg="white")

#Customize Frame
products_frame.place(x=30, y=60, width=700, height=450)
checkout_frame.place(x=745, y=60, width=370, height=450)
bar_frame.place(x=0, y=0, relwidth=1, height=30)

#Logica de los command para que habra resectivas ventanas cada opcion(abrir las ventanas respectivas a cada gestionar)---------------------------------------
def managEmployees():
    mw.destroy()
    from Employees import Employees
    Employees()

def managInputs():
    mw.destroy()
    from Inputs import Inputs
    Inputs()

def managOutPuts():
    mw.destroy()
    from OutPuts import OutPuts
    OutPuts()

def managPosition():
    mw.destroy()
    from Position import Position
    Position()

def managProductCategory():
    mw.destroy()
    from ProductCategory import ProductCategory
    ProductCategory()

def managProducts():
    mw.destroy()
    from Products import Products 
    Products()

def managSells():
    mw.destroy()
    from Sells import Sells 
    Sells()

def managShoppingView():
    mw.destroy()
    from ShopingView import ShopingView
    ShopingView()

def managShopping():
    mw.destroy()
    from Shopping import Shopping
    Shopping()

def managSupplier():
    mw.destroy()
    from Suppliers import Suppliers 
    Suppliers()

def reports():
    mw.destroy()
    from Tries import Tries 
    Tries()

#Option menu bar frame----------------------------------------------------------

# Load the image using PIL
MB_image = PhotoImage(file="SO_CoffeApp/src/main/resources/menu_bar.png")
# Create a label to display the background image
MenuButton_barFrame = Menubutton(bar_frame, image=MB_image ,bg="#CE7710", width=30, height=30)
MenuButton_barFrame.place(x=0, y=0)
MenuButton_barFrame.menu = Menu(MenuButton_barFrame, tearoff=0, bg="#CE7710")
MenuButton_barFrame.menu.add_command(label="Gestion de Insumos", foreground="white", font=("New Times Roman", 12), command=managInputs)
MenuButton_barFrame.menu.add_command(label="Gestion de Salidas", foreground="white", font=("New Times Roman", 12), command=managOutPuts)
MenuButton_barFrame.menu.add_command(label="Gestion de Empleados", foreground="white", font=("New Times Roman", 12), command=managEmployees)
MenuButton_barFrame.menu.add_command(label="Puestos de Empleados", foreground="white", font=("New Times Roman", 12), command=managPosition)
MenuButton_barFrame.menu.add_command(label="Categoria de Productos", foreground="white", font=("New Times Roman", 12), command=managProductCategory)
MenuButton_barFrame.menu.add_command(label="Gestion de Productos", foreground="white", font=("New Times Roman", 12), command=managProducts)
MenuButton_barFrame.menu.add_command(label="Vista de Ventas", foreground="white", font=("New Times Roman", 12), command= managSells)
MenuButton_barFrame.menu.add_command(label="Gestion de Compras", foreground="white", font=("New Times Roman", 12), command=managShopping)
MenuButton_barFrame.menu.add_command(label="Vista de Compras", foreground="white", font=("New Times Roman", 12), command=managShoppingView)
MenuButton_barFrame.menu.add_command(label="Gestion de Proveedores", foreground="white", font=("New Times Roman", 12), command=managSupplier)
MenuButton_barFrame.menu.add_command(label="Reportes", foreground="white", font=("New Times Roman", 12), command=reports)
MenuButton_barFrame["menu"]= MenuButton_barFrame.menu 

#Bar_list search product------------------------------------------------
product_list = []  # List to store retrieved products
current_selection = StringVar()  # String variable to hold the selected product

 
#connection bd---------------------------------------------------------------------------------------------------------------------
def get_db_connection():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123;')
    return conn

#Method get products to show in scroll_bar_frame
def get_active_products():
    conn = get_db_connection()  
    if not conn:
        return []

    products = []
    cursor = conn.cursor()
    try:
        cursor.execute("EXEC mostrar_productos_activos")  # Call the stored procedure
        for row in cursor:
            products.append({"id_producto": row[0], "nombre": row[1], "Descripcion": row[3],  "costo": row[4]})  # Assuming the procedure returns name and price
    finally:
        if conn:
            conn.close()

    return products

def create_product_buttons(products, inner_frame):
    column_count = 4  # Number of columns for the button grid
    current_column = 0
    current_row = 0

    for product in products:
        product_name = product["nombre"]
        product_description = product["Descripcion"]
        product_price = product["costo"]

        button = Button(
            inner_frame,
            text=f"{product_name} \n {product_description} \n ${product_price}",
            command=partial(on_product_click, product["id_producto"] ,product_name, product_description, product_price),
            width=20,  # Set button width
            bg="white"
        )

        # Use grid layout manager for positioning
        button.grid(row=current_row, column=current_column, padx=10, pady=20)

        # Move to the next column after creating a button
        current_column += 1

        # If all columns in a row are filled, move to the next row and reset column
        if current_column >= column_count:
            current_column = 0
            current_row += 1

def on_product_click(id_producto, product_name, product_description, product_price):
    print(f"Producto seleccionado: {id_producto} -  {product_name} - Precio: ${product_price:.2f} - Descripción: {product_description}")  # Replace with your desired action

    #Agregar cantidad del producto 
    popup = Toplevel()
    popup.title("Cantidad")
    popup.geometry("300x150")

    Label_Cantidad = Label(popup, text="Cantidad") 
    Label_Cantidad.pack(pady=5)

    entry_cantidad = Entry(popup)
    entry_cantidad.pack(pady=5)
    entry_cantidad.insert(0, "1")  # Valor predeterminado para cantidad
    

    # Confirmar selección de cantidad
    def confirmar_seleccion():
        cantidad = entry_cantidad.get()
        try:
            cantidad = int(cantidad)
        except ValueError:
            print("Por favor, ingresa una cantidad válida.")
            return
        
        importe = Decimal(product_price) * Decimal(cantidad)  # Asegura que importe sea Decimal
        selected_products.append({
            "id_producto": id_producto,  # Agregar esta línea
            "name": product_name,
            "price": float(product_price),
            "cantidad": cantidad,
            "importe": float(importe)
        })

        # Actualizar el total usando floats
        global total_price
        total_price += float(importe)
        total_label.config(text=f"Total: ${total_price:.2f}")

        popup.destroy()
        update_checkout_list()
    btn_confirm = Button(popup, text="Añadir al carrito", command=confirmar_seleccion)
    btn_confirm.pack(pady=10)


#ScrollBar products_frame  --------------------------------------------------- 
Canvas_scrollbar = Canvas(products_frame)
Canvas_scrollbar.pack(side=LEFT, fill=BOTH, expand=True)
inner_frame = Frame(Canvas_scrollbar)
inner_frame.config(background="white")
Canvas_scrollbar.create_window((0, 0), window=inner_frame, anchor="nw")

ScrollBar_Products = Scrollbar(Canvas_scrollbar, orient=VERTICAL, command=Canvas_scrollbar.yview)
ScrollBar_Products.pack(side=RIGHT, fill=Y)
Canvas_scrollbar.config(yscrollcommand = ScrollBar_Products.set)

def configure_scrollregion(event):
    Canvas_scrollbar.configure(scrollregion=Canvas_scrollbar.bbox("all"))

Canvas_scrollbar.bind("<Configure>", configure_scrollregion)

# Get active products and create buttons
products = get_active_products()  # Call get_active_products before button creation
create_product_buttons(products, inner_frame)


#Customize Checkout_frame----------------------------------------
Checkout_Label = Label(checkout_frame, text="Cuenta", font=("Playfair Display", 10), bg="white", fg="black", width=300)
Checkout_Label.place(x=135, y=10, anchor="center", relwidth=1, height=20)

Atributtes_Label = Label(checkout_frame, text="Nombre   Precio   QYT   Importe", font=("Arial", 9), bg="#d4d9d6", fg="black")
Atributtes_Label.place(x=370, y=30, anchor="e", width=500, height=15)

selected_products = []
total_price = 0.0

# Frame para mostrar los productos seleccionados en el checkout--------------------
checkout_list_frame = Frame(checkout_frame, bg="white")
checkout_list_frame.place(x=15, y=50, width=350, height=300)

# Label para mostrar el total
total_label = Label(checkout_frame, text="Total: $0.00", font=("Arial", 12), bg="white", fg="black")
total_label.place(x=5, y=425)

# Función para actualizar la lista de productos seleccionados visualmente
def update_checkout_list():
    global total_price
    total_price = sum(product['importe'] for product in selected_products)  # Recalcular total
    for widget in checkout_list_frame.winfo_children():
        widget.destroy()

    for index, product in enumerate(selected_products):
        product_label = Label(
            checkout_list_frame,
            text=f"{product['name']:15} ${product['price']:.2f}   {product['cantidad']}   ${product['importe']:.2f}",
            font=("Arial", 10), bg="white", fg="black"
        )
        product_label.grid(row=index, column=0, sticky="w")

        modify_button = Button(checkout_list_frame, text="Modificar", command=lambda idx=index: modify_quantity(idx))
        modify_button.grid(row=index, column=1, padx=5, pady=3)
        
        delete_button = Button(checkout_list_frame, text="Eliminar", command=lambda idx=index: delete_product(idx))
        delete_button.grid(row=index, column=2, padx=5, pady=3)

    total_label.config(text=f"Total: ${total_price:.2f}")


# Función para modificar la cantidad de un producto
def modify_quantity(index):
    popup = Toplevel()
    popup.title("Modificar cantidad")
    popup.geometry("300x150")

    Label(popup, text="Nueva cantidad:").pack(pady=5)
    entry_cantidad = Entry(popup)
    entry_cantidad.pack(pady=5)
    entry_cantidad.insert(0, str(selected_products[index]["cantidad"]))

    def confirmar_cambio():
        try:
            nueva_cantidad = int(entry_cantidad.get())
            if nueva_cantidad > 0:
                selected_products[index]["cantidad"] = nueva_cantidad
                selected_products[index]["importe"] = selected_products[index]["price"] * nueva_cantidad
                update_checkout_list()
            popup.destroy()
        except ValueError:
            print("Por favor, ingrese un número válido.")

    confirmar_button = Button(popup, text="Confirmar", command=confirmar_cambio)
    confirmar_button.pack(pady=10)

# Función para eliminar un producto
def delete_product(index):
    del selected_products[index]
    update_checkout_list()

#Configure Combobox----------------------------------------------------------------------
employee_label = Label(mw, text="Empleado", font=("Arial Black", 10), bg="#C9C9C9", fg="black")
employee_label.place(x=745, y=35)
employee_combobox = ttk.Combobox(mw, width=20)
employee_combobox.place(x=830, y=35)

def load_Employees_combobox():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC mostrar_empleados_activos")
        rows = cursor.fetchall()

        #Crear diccionario para almacenar {nombre: id}
        employee_dict = {row[2]: row[0] for row in rows} # row[0]: id_categoria, row[1]: nombre de la categoria
        employee_combobox['values'] = list(employee_dict.keys()) #Mostrar nombre de los puestos
        cursor.close()
        conn.close()
        return employee_dict
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los empleados en ComboBox: {e}")

# Llamar a la función para cargar los empleados en el ComboBox
employee_dict = load_Employees_combobox()

#Logic HoldOrder_Button
def addSell_DetailSell():
    try: 
        employee_selected = employee_combobox.get()
        id_empleado = employee_dict.get(employee_selected, None)
        total_venta = total_price
        conn = get_db_connection()
        cursor = conn.cursor()

        if not selected_products:
            messagebox.showwarning("Carrito vacío", "No hay productos en el carrito.")

        if not id_empleado:
            messagebox.showwarning("Falta el Empleado", "Debe ingresar un empleado.")

        # Llamar al procedimiento almacenado para insertar la venta
        cursor.execute("EXEC addVenta @id_empleado=?, @total=?", id_empleado, total_venta)
        id_venta = cursor.execute("SELECT TOP 1 id_venta FROM ventas ORDER BY id_venta DESC").fetchval()
        print(id_venta)
        if id_venta is None:
            raise Exception("No se pudo obtener el id_venta. Verifique la inserción en la tabla Ventas.")

        # Insertar cada producto del carrito usando el procedimiento almacenado addDetalleVenta
        for item in selected_products:
            cursor.execute(
                "EXEC addDetalleVenta @id_venta=?, @id_producto=?, @cantidad=?, @subtotal=?",
                id_venta, item["id_producto"], item["cantidad"], item["importe"]
            )
        # Confirmar la transacción
        conn.commit()
        messagebox.showinfo("Exito", "Venta y Detalle Venta añadidos con exito")

        actualizar_existencias(id_venta)
        selected_products.clear()
        update_checkout_list()
        total_label.config(text="Total: $0.00")

        
        return id_venta
    except Exception as e:
        print(f"Error durante la transacción: {e}")
    finally:
        conn.close()

def actualizar_existencias(id_venta):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("EXEC registrarVentaConExistencias @id_venta=?", id_venta)
        conn.commit()
        print("Existencias actualizadas.")
    except Exception as e:
        conn.rollback()
        print(f"Error al actualizar existencias: {e}")
        raise e
    finally:
        conn.close()

# Campo de entrada para la búsqueda
search_entry = Entry(mw, width=60)
search_entry.place(x=90, y=35)

# Función de búsqueda
def search_products():
    search_term = search_entry.get().strip()
    if not search_term:
        products = get_active_products()  # Mostrar todos los productos si la entrada está vacía
    else:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Intentar buscar por categoría
            cursor.execute("EXEC BuscarProductosCategoria ?", search_term)
            category_results = cursor.fetchall()
            
            if category_results:
                products = [
                    {"id_producto": row[0], "nombre": row[1], "Descripcion": row[2], "costo": row[3]}
                    for row in category_results
                ]
            else:
                # Si no hay resultados por categoría, buscar por nombre
                cursor.execute("EXEC BuscarProductosNombre ?", search_term)
                name_results = cursor.fetchall()
                products = [
                    {"id_producto": row[0], "nombre": row[1], "Descripcion": row[2], "costo": row[3]}
                    for row in name_results
                ]
        except Exception as e:
            print(f"Error durante la búsqueda: {e}")
            products = []
        finally:
            conn.close()

    # Actualizar botones con los productos encontrados
    for widget in inner_frame.winfo_children():
        widget.destroy()
    create_product_buttons(products, inner_frame)

# Botón para realizar la búsqueda
search_button = Button(mw, text="Buscar", command=search_products, bg="#CE7710", fg="white", font=("Arial", 8))
search_button.place(x=30, y=32)

# Configura la búsqueda automática al presionar Enter
search_entry.bind("<Return>", lambda event: search_products())


#Buttons and Labels main window
CancelOrder_Button = Button(text="Cancelar Orden", font=("Katibeh",15), fg="red", bg="SystemButtonFace", overrelief=FLAT, width=25, highlightbackground="red")
CancelOrder_Button.config(bg=mw.cget('bg'))
CancelOrder_Button.place(x=220, y=550, anchor="center", width=200)

HoldOrder_Button = Button(text="Completar Orden", font=("Katibeh",15), fg="green", bg="SystemButtonFace", overrelief=FLAT, width=25, highlightbackground="green", command=addSell_DetailSell)
HoldOrder_Button.config(bg=mw.cget('bg'))
HoldOrder_Button.place(x=440, y=550, anchor="center", width=200)

#END----------------------------
mw.mainloop()

            
