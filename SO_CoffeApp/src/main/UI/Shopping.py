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
shp = Tk()
shp.geometry("1150x670")
shp.minsize(700, 500)
shp.maxsize(1224, 1280)
shp.configure(bg="#C9C9C9")
shp.title("Agregar Compra")

# Icon --------------------------
base_dir = Path(__file__).resolve().parent
icon_path = base_dir.parent / 'resources' / 'icon sf.ico'
icon_path_str = str(icon_path)
if icon_path.exists():
    try:
        shp.iconbitmap(icon_path_str)
    except Exception as e:
        print(f"Error al cargar el icono: {e}")
else:
    print(f"El archivo de icono no se encuentra en la ruta especificada: {icon_path_str}")

#Frames----------------------------------------------
bar_frame = Frame(shp, bg="#CE7710")
products_frame = Frame(shp, bg="#C9C9C9")
checkout_frame = Frame(shp, bg="white")

#Customize Frame
products_frame.place(x=30, y=60, width=700, height=500)
checkout_frame.place(x=745, y=60, width=370, height=500)
bar_frame.place(x=0, y=0, relwidth=1, height=30)


#Methods to nav amoung windows
def managInputs():
    shp.destroy()
    from Inputs import Inputs
    Inputs()

def managOutPuts():
    shp.destroy()
    from OutPuts import OutPuts
    OutPuts()

def pontiOfSale():
    shp.destroy()
    from POS import POS 
    POS()

def managPosition():
    shp.destroy()
    from Position import Position
    Position()

def managProductCategory():
    shp.destroy()
    from ProductCategory import ProductCategory
    ProductCategory()

def managProducts():
    shp.destroy()
    from Products import Products 
    Products()

def managSells():
    shp.destroy()
    from Sells import Sells 
    Sells()

def managEmployees():
    shp.destroy()
    from Employees import Employees
    Employees()

def managShoppingView():
    shp.destroy()
    from ShopingView import ShopingView
    ShopingView()

def  managSupplier():
    shp.destroy()
    from Suppliers import Suppliers 
    Suppliers()

def reports():
    shp.destroy()
    from Tries import Tries
    Tries()
#Option menu bar frame----------------------------------------------------------

MB_image1 = PhotoImage(file="SO_CoffeApp/src/main/resources/menu_bar.png")
# Create a label to display the background image
MenuButton_barFrame = Menubutton(bar_frame, image=MB_image1 ,bg="#CE7710", width=30, height=30)
MenuButton_barFrame.place(x=0, y=0)
MenuButton_barFrame.menu = Menu(MenuButton_barFrame, tearoff=0, bg="#CE7710")
MenuButton_barFrame.menu.add_command(label="Gestion de Insumos", foreground="white", font=("New Times Roman", 12), command=managInputs)
MenuButton_barFrame.menu.add_command(label="Gestion de Salidas", foreground="white", font=("New Times Roman", 12), command=managOutPuts)
MenuButton_barFrame.menu.add_command(label="Punto de Venta", foreground="white", font=("New Times Roman", 12), command=pontiOfSale)
MenuButton_barFrame.menu.add_command(label="Puestos de Empleados", foreground="white", font=("New Times Roman", 12), command=managPosition)
MenuButton_barFrame.menu.add_command(label="Categoria de Productos", foreground="white", font=("New Times Roman", 12), command=managProductCategory)
MenuButton_barFrame.menu.add_command(label="Gestion de Productos", foreground="white", font=("New Times Roman", 12), command=managProducts)
MenuButton_barFrame.menu.add_command(label="Vista de Ventas", foreground="white", font=("New Times Roman", 12), command= managSells)
MenuButton_barFrame.menu.add_command(label="Gestion de Empleados", foreground="white", font=("New Times Roman", 12), command=managEmployees)
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
def get_inputs_products():
    conn = get_db_connection()  
    if not conn:
        return []

    products = []
    cursor = conn.cursor()
    try:
        cursor.execute("EXEC MostrarProductosInsumos")  # Call the stored procedure
        for row in cursor:
            products.append({
                "id_producto": row[0],
                "nombre": row[1],
                "Categoria": row[2],
                "Descripcion": row[3],
                "Costo": row[4],
                "Existencia": row[5],
                "tipo": row[6]  # Asegúrate de que el procedimiento almacenado devuelve el tipo
            })
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
        product_price = product["Costo"]
        tipo = product["tipo"]

        button = Button(
            inner_frame,
            text=f"{product_name} \n {product_description} \n ${product_price}",
            command=partial(on_product_click, product["id_producto"] ,product_name, product_description, product_price, tipo),
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

def on_product_click(id_producto, product_name, product_description, product_price, tipo):
    print(f"Producto seleccionado: {id_producto} -  {product_name} - Precio: ${product_price:.2f} - Descripción: {product_description}")  # Replace with your desired action

    # Agregar cantidad del producto 
    popup = Toplevel()
    popup.title("Cantidad")
    popup.geometry("300x200")

    Label_Cantidad = Label(popup, text="Cantidad") 
    Label_Cantidad.pack(pady=5)

    entry_cantidad = Entry(popup)
    entry_cantidad.pack(pady=5)
    entry_cantidad.insert(0, "1")  # Valor predeterminado para cantidad

    Label_Precio = Label(popup, text="Costo")
    Label_Precio.pack(pady=5)

    entry_costo = Entry(popup)
    entry_costo.pack(pady=5)
    entry_costo.insert(0, product_price)

    # Confirmar selección de cantidad
    def confirmar_seleccion(product_price):  
        cantidad = entry_cantidad.get()
        try:
            cantidad = int(cantidad)
        except ValueError:
            print("Por favor, ingresa una cantidad válida.")
            return
        
        # Calcular el importe
        importe = Decimal(product_price) * Decimal(cantidad)
        
        # Obtener el nuevo costo desde el campo de entrada
        new_cost = entry_costo.get()
        try:
            new_cost = float(new_cost)
        except ValueError:
            print("El costo ingresado no es válido.")
            return

        # Actualizar datos en el array localmente
        selected_products.append({
            "id_producto": id_producto,
            "name": product_name,
            "costo": new_cost,  # Usar el costo actualizado
            "cantidad": cantidad,
            "importe": new_cost * cantidad,
            "tipo": tipo  
        })

        popup.destroy()
        update_checkout_list()  # Actualizar la lista visualmente

    # Botón para confirmar la selección
    btn_confirm = Button(popup, text="Añadir al carrito", command=lambda: confirmar_seleccion(product_price))  # Pasar product_price aquí
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
products = get_inputs_products()  # Call get_active_products before button creation
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
            text=f"{product['name']:15} ${product['costo']:.2f}   {product['cantidad']}   ${product['importe']:.2f}",
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
                selected_products[index]["importe"] = selected_products[index]["costo"] * nueva_cantidad
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
supplier_label = Label(shp, text="Proveedor", font=("Arial Black", 10), bg="#C9C9C9", fg="black")
supplier_label.place(x=745, y=35)
supplier_combobox = ttk.Combobox(shp, width=20)
supplier_combobox.place(x=830, y=35)

def load_Suppliers_combobox():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC mostrar_proveedores_activos")
        rows = cursor.fetchall()

        #Crear diccionario para almacenar {nombre: id}
        supplier_dict = {row[1]: row[0] for row in rows} # row[0]: id_categoria, row[1]: nombre de la categoria
        supplier_combobox['values'] = list(supplier_dict.keys()) #Mostrar nombre de los puestos
        cursor.close()
        conn.close()
        return supplier_dict
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los empleados en ComboBox: {e}")

# Llamar a la función para cargar los empleados en el ComboBox
supplier_dict = load_Suppliers_combobox()

# Función para confirmar la compra
def confirmar_compra():
    supplier_selected = supplier_combobox.get()
    id_proveedor = supplier_dict.get(supplier_selected, None)

    if not selected_products:
        messagebox.showwarning("Carrito vacío", "No hay productos en el carrito.")
        return
    if not id_proveedor:
        messagebox.showwarning("Falta ID Proveedor", "Debe seleccionar un proveedor.")
        return

    try:
        # Guardar la compra en la base de datos
        id_compra = confirmar_compra_en_base_de_datos(id_proveedor)
        
        # Actualizar costos y existencias en la base de datos después de confirmar la compra
        if id_compra is not None:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            for product in selected_products:
                if product["tipo"] == 1:  # Producto empaquetado
                    cursor.execute("UPDATE productos SET costo = ? WHERE id_producto = ?", 
                                   product["costo"], product["id_producto"])
                else:  # Insumo
                    cursor.execute("UPDATE insumos SET costo = ? WHERE id_insumo = ?", 
                                   product["costo"], product["id_producto"])

            conn.commit()
            conn.close()

            # Limpiar el carrito después de confirmar
            selected_products.clear()
            update_checkout_list()
            messagebox.showinfo("Compra confirmada", "La compra ha sido registrada y los costos actualizados.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al confirmar la compra: {e}")


# Función para guardar la compra y detalles en la base de datos
def confirmar_compra_en_base_de_datos(id_proveedor):
    conn = get_db_connection()
    cursor = conn.cursor()
    id_compra = None

    try:
        cursor.execute("BEGIN TRANSACTION")

        # Calcular el total de la compra
        total_compra = total_price

        # Llamar al procedimiento almacenado para insertar la compra
        cursor.execute("EXEC addCompras @id_proveedor=?, @total=?", id_proveedor, total_compra)

        # Obtener el ID de la compra recién creada
        id_compra = cursor.execute("SELECT TOP 1 id_compra FROM compras ORDER BY id_compra DESC").fetchval()
        if id_compra is None:
            raise Exception("No se pudo obtener el id_compra. Verifique la inserción en la tabla Compras.")

        # Insertar cada ítem del carrito usando addDetalleCompra o en compra_productos según tipo
        for item in selected_products:
            if item['tipo'] == 1:  # Producto empaquetado
                cursor.execute("EXEC addCompraProducto @id_compra=?, @id_producto=?, @cantidad=?, @costo=?", 
                               id_compra, item['id_producto'], item['cantidad'], item['costo'])
            else:  # Insumo
                cursor.execute("EXEC addDetalleCompra @id_compra=?, @id_insumo=?, @cantidad=?, @costo=?", 
                               id_compra, item['id_producto'], item['cantidad'], item['costo'])

        # Confirmar la transacción
        cursor.execute("COMMIT TRANSACTION")
        conn.commit()
        return id_compra
    except Exception as e:
        cursor.execute("ROLLBACK TRANSACTION")
        print(f"Error durante la transacción: {e}")
        raise e
    finally:
        conn.close()

def reload_buttons(products, inner_frame):
    # Limpiar el frame actual eliminando todos los widgets
    for widget in inner_frame.winfo_children():
        widget.destroy()

    # Crear los botones nuevamente con los productos actualizados
    create_product_buttons(products, inner_frame)

# Lógica para actualizar los productos y recargar los botones
def actualizar_productos_y_recargar():
    # Obtener la lista actualizada de productos desde la base de datos
    productos_actualizados = get_inputs_products()

    # Recargar los botones con los productos actualizados
    reload_buttons(productos_actualizados, inner_frame)

# Campo de entrada para la búsqueda
search_entry = Entry(shp, width=60)
search_entry.place(x=90, y=35)

def search_products():
    search_term = search_entry.get().strip()
    if not search_term:
        products = get_inputs_products()  # Mostrar todos los productos si la entrada está vacía
    else:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Intentar buscar por categoría
            cursor.execute("EXEC BuscarInsumosNombre ?", search_term)
            category_results = cursor.fetchall()
            
            if category_results:
                products = [
                    {"id_producto": row[0], "nombre": row[1], "Descripcion": row[2], "Costo": row[3], "tipo": row[4]}
                    for row in category_results
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
search_button = Button(shp, text="Buscar", command=search_products, bg="#CE7710", fg="white", font=("Arial", 8))
search_button.place(x=30, y=32)

# Configura la búsqueda automática al presionar Enter
search_entry.bind("<Return>", lambda event: search_products())

#Buttons and Labels main window
CancelShopping_Button = Button(text="Cancelar Compra", font=("Katibeh",15), fg="red", bg="SystemButtonFace", overrelief=FLAT, width=25, highlightbackground="red")
CancelShopping_Button.config(bg=shp.cget('bg'))
CancelShopping_Button.place(x=220, y=600, anchor="center", width=200)

HoldOrder_Button = Button(text="Completar Compra", font=("Katibeh",15), fg="green", bg="SystemButtonFace", overrelief=FLAT, width=25, highlightbackground="green", command=confirmar_compra)
HoldOrder_Button.config(bg=shp.cget('bg'))
HoldOrder_Button.place(x=440, y=600, anchor="center", width=200)

MB_image = PhotoImage(file="SO_CoffeApp/src/main/resources/reload.png")
reload_Bt = Button(bar_frame, image=MB_image, fg="black", bg="#CE7710", command=actualizar_productos_y_recargar, font=("Arial Black", 9), relief="flat")
reload_Bt.place(x=700, y=0)

shp.mainloop()
#modificar para que solo se actualice el array y en base de datos solo cuando se confirme