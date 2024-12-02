from functools import partial
import pyodbc
from tkinter import *
from tkinter import Scrollbar
from tkinter import Menubutton
from tkinter import messagebox
from tkinter import ttk

# Configuration main window---------------------------
rgp = Tk()
rgp.geometry("1040x700")
rgp.minsize(700, 500)
rgp.maxsize(1500, 580)
rgp.configure(bg="white")
rgp.title("Registrar nuevo producto")

#Top Bar-----------------------------------------------
topBar_frame = Frame(rgp, bg="#CE7710")
topBar_frame.place(x=0, y=0, relwidth=1, height=30)


#Logica de los command para que habra resectivas ventanas cada opcion(abrir las ventanas respectivas a cada gestionar)---------------------------------------
def managEmployees():
    rgp.destroy()
    from Employees import Employees
    Employees()

def managInputs():
    rgp.destroy()
    from Inputs import Inputs
    Inputs()

def managOutPuts():
    rgp.destroy()
    from OutPuts import OutPuts
    OutPuts()

def pontiOfSale():
    rgp.destroy()
    from POS import POS 
    POS()

def managPosition():
    rgp.destroy()
    from Position import Position
    Position()

def managProductCategory():
    rgp.destroy()
    from ProductCategory import ProductCategory
    ProductCategory()

def managSells():
    rgp.destroy()
    from Sells import Sells 
    Sells()

def managShopping():
    rgp.destroy()
    from Shopping import Shopping
    Shopping()

def managShoppingView():
    rgp.destroy()
    from ShopingView import ShopingView
    ShopingView()

def  managSupplier():
    rgp.destroy()
    from Suppliers import Suppliers 
    Suppliers()

def reports():
    rgp.destroy()
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
MenuButton_barFrame.menu.add_command(label="Puesto de Empleados", foreground="white", font=("New Times Roman", 12), command=managPosition)
MenuButton_barFrame.menu.add_command(label="Categoria de Productos", foreground="white", font=("New Times Roman", 12), command= managProductCategory)
MenuButton_barFrame.menu.add_command(label="Vista de Ventas", foreground="white", font=("New Times Roman", 12), command=managSells)
MenuButton_barFrame.menu.add_command(label="Gestion de Compras", foreground="white", font=("New Times Roman", 12), command=managShopping)
MenuButton_barFrame.menu.add_command(label="Vista de Compras", foreground="white", font=("New Times Roman", 12), command=managShoppingView)
MenuButton_barFrame.menu.add_command(label="Gestion de Proveedores", foreground="white", font=("New Times Roman", 12), command=managSupplier)
MenuButton_barFrame.menu.add_command(label="Reportes", foreground="white", font=("New Times Roman", 12), command=reports)
MenuButton_barFrame["menu"]= MenuButton_barFrame.menu

Main_Label = Label(rgp, text="PRODUCTOS", fg="black", bg="white", font=("Arial Black", 18))
Main_Label.place(x=430, y=55)

# Table to display products
product_columns = ("Categoria", "Nombre", "Descripcion", "Costo", "Existencia")
product_tree = ttk.Treeview(rgp, columns=product_columns, show="headings", height=5)
for col in product_columns:
    product_tree.heading(col, text=col)
product_tree.place(x=20, y=160, height=300)

product_scrollbar = Scrollbar(rgp, orient="vertical", command=product_tree.yview)
product_scrollbar.place(x=1002, y=165, height=290)
product_tree.configure(yscrollcommand=product_scrollbar.set)


def get_db_connection():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123;')
    return conn

def load_products():
    try:
        product_tree.delete(*product_tree.get_children())
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC mostrar_productos_activos") #el metodo no imprime el noombre de ahi en mas todo bien 
        rows = cursor.fetchall()
        for row in rows:
            formatted_row = (
                row[2], 
                row[1], 
                row[3], 
                f"{row[4]:.2f}", 
                row[5])
            product_tree.insert("", "end", values=formatted_row)
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los productos: {e}")

# Function to open add product window
def Add_Normal_Product_Window():
    ap = Toplevel(rgp)
    ap.geometry("300x350")
    ap.configure(bg="white")
    ap.title("Agregar Producto")
    #ap.iconbitmap('F:\\6to Semestre\\Gestión De Proyectos De Software\\S-O project\Extra\\icon sf.ico')

    def Aceptar_ButtonAction():
        category_selected = Category_combobox.get()
        id_category = category_dict.get(category_selected, None)
        nombre = Name_Box.get()
        descripcion = Description_Box.get()
        costo = float(Precio_Box.get())
        existencia = Existence_Box.get()

        # Agregar la información a la base de datos utilizando un procedimiento almacenado
        try:
            conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
            cursor = conn.cursor()
            cursor.execute("EXEC addProducto ?, ?, ?, ?, ?", id_category, nombre, descripcion, costo, existencia)
            conn.commit()
            cursor.close()
            conn.close()

            # Mostrar la información obtenida en la ventana principal (rgp)
            product_tree.insert("", "end", values=(category_selected, nombre, descripcion, costo, existencia))
            ap.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar el producto: {e}")

    Category_Labael = Label(ap, text="Categoria", fg="black", bg="white", font=("Arial Black", 9))
    Category_Labael.place(x=30, y=30)
    Category_combobox = ttk.Combobox(ap, width=20)
    Category_combobox.place(x=115, y=35)

    # Cargar categoria con ID en el ComboBox
    def load_categories_combobox():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("EXEC mostrarCategorias")
            rows = cursor.fetchall()

            #Crear diccionario para almacenar {nombre: id}
            category_dict = {row[1]: row[0] for row in rows} # row[0]: id_categoria, row[1]: nombre de la categoria
            Category_combobox['values'] = list(category_dict.keys()) #Mostrar nombre de los puestos
            cursor.close()
            conn.close()
            return category_dict
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los puestos en ComboBox: {e}")

    # Llamar a la función para cargar los puestos en el ComboBox
    category_dict = load_categories_combobox()

    Name_Label = Label(ap, text="Nombre", fg="black", bg="white", font=("Arial Black", 9))
    Name_Label.place(x=30, y=75)
    Name_Box = Entry(ap, width=20, bg="lightgray" )
    Name_Box.place(x=115, y=75)

    Description_Label = Label(ap, text="Descripcion", fg="black", bg="white", font=("Arial Black", 9))
    Description_Label.place(x=30, y=115)
    Description_Box = Entry(ap, width=20, bg="lightgray" )
    Description_Box.place(x=115, y=115)

    Precio_Label = Label(ap, text="Costo $", fg="black", bg="white", font=("Arial Black", 9))
    Precio_Label.place(x=30, y=155)
    Precio_Box = Entry(ap, width=5, bg="lightgray" )
    Precio_Box.place(x=115, y=155)
    
    Existence_Label = Label(ap, text="Existencia ", fg="black", bg="white", font=("Arial Black", 9))
    Existence_Label.place(x=30, y=200)
    Existence_Box = Entry(ap, width=5, bg="lightgray" )
    Existence_Box.place(x=115, y=200)

    Aceptar_Button = Button(ap, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=Aceptar_ButtonAction)
    Aceptar_Button.place(x=30, y=240)

    Cancelar_Button = Button(ap, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=ap.destroy)
    Cancelar_Button.place(x=100, y=240)

# Function to open add product window kitchen
def Add_ProductWindow_Kitchen():
    apc = Toplevel(rgp)
    apc.geometry("300x350")
    apc.configure(bg="white")
    apc.title("Agregar Producto De Cocina")
    #ap.iconbitmap('F:\\6to Semestre\\Gestión De Proyectos De Software\\S-O project\Extra\\icon sf.ico')

    def Aceptar_ButtonAction():
        category_selected = Category_combobox.get()
        id_category = category_dict.get(category_selected, None)
        nombre = Name_Box.get()
        descripcion = Description_Box.get()
        costo = float(Precio_Box.get())

        # Agregar la información a la base de datos
        try:
            conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
            cursor = conn.cursor()
            cursor.execute("EXEC addProductoCocina ?, ?, ?, ?", id_category, nombre, descripcion, costo)
            
            # Obtener el ID del producto recién agregado para pasar a `Add_Ingredients`
            cursor.execute("SELECT id_producto FROM productos WHERE descripcion = ?", descripcion)
            id_producto = cursor.fetchone()[0]
            print(id_producto)

            conn.commit()
            cursor.close()
            conn.close()

            # Abre la ventana para añadir insumos y pasa `id_producto`
            Add_Ingredients(id_producto)
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar el producto: {e}")

    Category_Labael = Label(apc, text="Categoria", fg="black", bg="white", font=("Arial Black", 9))
    Category_Labael.place(x=30, y=30)
    Category_combobox = ttk.Combobox(apc, width=20)
    Category_combobox.place(x=115, y=35)
    
    # Cargar categoria con ID en el ComboBox
    def load_categories_combobox():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("EXEC mostrarCategorias")
            rows = cursor.fetchall()

            #Crear diccionario para almacenar {nombre: id}
            category_dict = {row[1]: row[0] for row in rows} # row[0]: id_categoria, row[1]: nombre de la categoria
            Category_combobox['values'] = list(category_dict.keys()) #Mostrar nombre de los puestos
            cursor.close()
            conn.close()
            return category_dict
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los puestos en ComboBox: {e}")

    # Llamar a la función para cargar los puestos en el ComboBox
    category_dict = load_categories_combobox()
    

    Name_Label = Label(apc, text="Nombre", fg="black", bg="white", font=("Arial Black", 9))
    Name_Label.place(x=30, y=75)
    Name_Box = Entry(apc, width=20, bg="lightgray" )
    Name_Box.place(x=115, y=75)

    Description_Label = Label(apc, text="Descripcion", fg="black", bg="white", font=("Arial Black", 9))
    Description_Label.place(x=30, y=115)
    Description_Box = Entry(apc, width=20, bg="lightgray" )
    Description_Box.place(x=115, y=115)

    Precio_Label = Label(apc, text="Costo $", fg="black", bg="white", font=("Arial Black", 9))
    Precio_Label.place(x=30, y=155)
    Precio_Box = Entry(apc, width=5, bg="lightgray" )
    Precio_Box.place(x=115, y=155)
    
    Aceptar_Button = Button(apc, text="Aceptar", bg="green", fg="black", font=("Arial Black", 9), command=Aceptar_ButtonAction)
    Aceptar_Button.place(x=30, y=240)

    Cancelar_Button = Button(apc, text="Cancelar", bg="red", fg="black", font=("Arial Black", 9), command=apc.destroy)
    Cancelar_Button.place(x=108, y=240)

def Add_Ingredients(id_producto):
    ai = Toplevel(rgp)
    ai.geometry("1050x600")
    ai.configure(bg="#C9C9C9")
    ai.title("Agregar Ingredientes")

    # Frames ----------------------------------------------
    bar_frame = Frame(ai, bg="#CE7710")
    ingredients_frame = Frame(ai, bg="white")
    list_frame = Frame(ai, bg="white")

    # Customize Frame
    ingredients_frame.place(x=30, y=60, width=700, height=450)
    list_frame.place(x=745, y=60, width=270, height=450)
    bar_frame.place(x=0, y=0, relwidth=1, height=30)
    
    def complete_detail_input():
        if not selected_inputs:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM productos WHERE id_producto = ?", (id_producto,))
                    conn.commit()
                    messagebox.showinfo("Cancelado", "Producto eliminado ya que no se agregaron insumos.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar el producto: {e}")
                finally:
                    ai.destroy()  # Cerrar la ventana después de la operación
            return

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                for insumo in selected_inputs:
                    id_input = insumo["id"]
                    cantidad = insumo["cantidad"]
                    print(f"Ejecutando query con id_producto: {id_producto}, id_input: {id_input}, cantidad: {cantidad}")  # Depuración
                    
                    cursor.execute(
                        "EXEC addDetalleInsumo ?, ?, ?",
                        (id_producto, id_input, cantidad)
                    )
                conn.commit()
                messagebox.showinfo("Éxito", "Producto e insumos agregados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar insumos: {e}")
        finally:
            ai.destroy()



    # Buttons and Labels main window
    CancelOrder_Button = Button(ai, text="Cancelar", font=("Katibeh", 15), fg="white", bg="red", overrelief=FLAT, width=25, highlightbackground="red")
    CancelOrder_Button.place(x=220, y=550, anchor="center", width=200)

    HoldOrder_Button = Button(ai, text="Aceptar", font=("Katibeh", 15), fg="white", bg="green", overrelief=FLAT, width=25, highlightbackground="green", command=complete_detail_input)
    HoldOrder_Button.place(x=440, y=550, anchor="center", width=200)

    # List to store selected ingredients
    selected_inputs = []

    # Method to retrieve inputs from the database
    def get_inputs():
        conn = get_db_connection()  
        if not conn:
            return []

        inputs = []
        cursor = conn.cursor()
        try:
            cursor.execute("EXEC mostrarInsumos")  # Call the stored procedure
            for row in cursor:
                inputs.append({
                    "id": row[0],  # ID del insumo (asegúrate de que sea la primera columna en el resultado)
                    "nombre": row[1],  # Nombre del insumo
                    "Descripcion": row[3],  # Descripción
                    "Existencia": row[2]  # Existencia
                })
        finally:
            if conn:
                conn.close()

        return inputs


    # Create buttons for each input item
    def create_inputs_buttons(inputs, inner_frame):
        column_count = 4  # Number of columns for the button grid
        current_column = 0
        current_row = 0

        for input_item in inputs:
            input_name = input_item["nombre"]
            input_description = input_item["Descripcion"]
            input_existence = input_item["Existencia"]

            button = Button(
                inner_frame,
                text=f"{input_name} \n {input_description} \n {input_existence}",
                command=partial(on_input_click, input_item["id"], input_name, input_description),
                width=20  # Set button width
            )


            # Use grid layout manager for positioning
            button.grid(row=current_row, column=current_column, padx=10, pady=20)

            # Move to the next column after creating a button
            current_column += 1

            # If all columns in a row are filled, move to the next row and reset column
            if current_column >= column_count:
                current_column = 0
                current_row += 1

    # Function executed when an ingredient button is clicked
    def on_input_click(id_input, input_name, input_description):
        print(f"Insumo seleccionado: {id_input} - {input_name} - {input_description}")
        
        # Pop-up para ingresar la cantidad del insumo seleccionado
        popup = Toplevel()
        popup.title("Cantidad")
        popup.geometry("300x150")

        Label_Cantidad = Label(popup, text="Cantidad") 
        Label_Cantidad.pack(pady=5)

        entry_cantidad = Entry(popup)
        entry_cantidad.pack(pady=5)
        entry_cantidad.insert(0, "1")  # Default quantity
        
        def confirmar_seleccion():
            cantidad = entry_cantidad.get()
            try:
                cantidad = int(cantidad)
            except ValueError:
                print("Por favor, ingresa una cantidad válida.")
                return
            
            selected_inputs.append({
                "id": id_input,  
                "name": input_name,
                "cantidad": cantidad,
            })
            popup.destroy()
            update_checkout_list()

        btn_confirm = Button(popup, text="Añadir al carrito", command=confirmar_seleccion)
        btn_confirm.pack(pady=10)


    # Scrollable canvas for the ingredients frame
    Canvas_scrollbar = Canvas(ingredients_frame)
    Canvas_scrollbar.pack(side=LEFT, fill=BOTH, expand=True)
    inner_frame = Frame(Canvas_scrollbar)
    Canvas_scrollbar.create_window((0, 0), window=inner_frame, anchor="nw")

    ScrollBar_Products = Scrollbar(Canvas_scrollbar, orient=VERTICAL, command=Canvas_scrollbar.yview)
    ScrollBar_Products.pack(side=RIGHT, fill=Y)
    Canvas_scrollbar.config(yscrollcommand=ScrollBar_Products.set)

    def configure_scrollregion(event):
        Canvas_scrollbar.configure(scrollregion=Canvas_scrollbar.bbox("all"))

    Canvas_scrollbar.bind("<Configure>", configure_scrollregion)

    # Customize Checkout_frame
    Checkout_Label = Label(list_frame, text="Ingredientes", font=("Playfair Display", 10), bg="white", fg="black", width=300)
    Checkout_Label.place(x=135, y=10, anchor="center", relwidth=1, height=10)

    Atributtes_Label = Label(list_frame, text="      Nombre                         Cantidad     ", font=("Arial", 8), bg="#d4d9d6", fg="black")
    Atributtes_Label.place(x=310, y=30, anchor="e", width=420, height=15)

    # Frame to show selected products in the checkout
    checkout_list_frame = Frame(list_frame, bg="white")
    checkout_list_frame.place(x=15, y=50, width=350, height=300)

    # Function to update the visual list of selected products
    def update_checkout_list():
        for widget in checkout_list_frame.winfo_children():
            widget.destroy()

        for index, product in enumerate(selected_inputs):
            product_label = Label(
                checkout_list_frame,
                text=f"{product['name']:15} {product['cantidad']}",
                font=("Arial", 10), bg="white", fg="black"
            )
            product_label.grid(row=index, column=0, sticky="w")

            modify_button = Button(checkout_list_frame, text="Modificar", command=lambda idx=index: modify_quantity(idx))
            modify_button.grid(row=index, column=1, padx=5, pady=3)
            
            delete_button = Button(checkout_list_frame, text="Eliminar", command=lambda idx=index: delete_product(idx))
            delete_button.grid(row=index, column=2, padx=5, pady=3)

    # Function to modify the quantity of a product
    def modify_quantity(index):
        popup = Toplevel()
        popup.title("Modificar cantidad")
        popup.geometry("300x150")

        Label(popup, text="Nueva cantidad:").pack(pady=5)
        entry_cantidad = Entry(popup)
        entry_cantidad.pack(pady=5)
        entry_cantidad.insert(0, str(selected_inputs[index]["cantidad"]))

        def confirmar_cambio():
            try:
                nueva_cantidad = int(entry_cantidad.get())
                if nueva_cantidad > 0:
                    selected_inputs[index]["cantidad"] = nueva_cantidad
                    update_checkout_list()
                popup.destroy()
            except ValueError:
                print("Por favor, ingrese un número válido.")

        confirmar_button = Button(popup, text="Confirmar", command=confirmar_cambio)
        confirmar_button.pack(pady=10)

    # Function to delete a product
    def delete_product(index):
        del selected_inputs[index]
        update_checkout_list()

    # Load inputs and create buttons
    inputs = get_inputs()
    create_inputs_buttons(inputs, inner_frame)


def obtener_id_producto_por_nombre(nombre):
    """Obtiene el id_producto a partir del nombre."""
    try:
        conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
        cursor = conn.cursor()
        cursor.execute("SELECT id_producto FROM productos WHERE nombre = ?", nombre)
        result = cursor.fetchone()
        print(f"Resultado obtenido de la BD: {result}")
        cursor.close()
        conn.close()

        if result:
            return result[0]  # Retorna solo el valor de la primera columna
        else:
            messagebox.showerror("Error", "Producto no encontrado")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener el ID del producto: {e}")
        return None



# Function to open edit product window
def Edit_ProductWindow():
    selected_item = product_tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un producto para editar")
        return

    item = product_tree.item(selected_item)
    values = item["values"]
    nombre_producto = values[1]
    id_producto = obtener_id_producto_por_nombre(nombre_producto)

    if id_producto is None: 
        return 

    load_products()
    ep = Toplevel(rgp)
    ep.geometry("300x350")
    ep.configure(bg="white")
    ep.title("Editar Producto")
    #ep.iconbitmap('F:\\6to Semestre\\Gestión De Proyectos De Software\\S-O project\Extra\\icon sf.ico')

    def Aceptar_ButtonAction():
        # Obtener los valores modificados por el usuario
        category_selected = Category_combobox.get()
        id_category = category_dict.get(category_selected, None)
        nombre = Name_Box.get()
        descripcion = Description_Box.get()
        costo = float(Precio_Box.get())
        load_products()

        # Actualizar la información en la base de datos (simulado)
        try:
            conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123')
            cursor = conn.cursor()
            cursor.execute("EXEC modProducto ?, ?, ?, ?, ?", id_producto, id_category, nombre, descripcion, costo)
            conn.commit()
            cursor.close()
            conn.close()
            load_products()

            # Actualizar la información en la tabla
            #product_tree.item(selected_item, values=(id_producto, nombre, descripcion, costo))
            load_products()
            messagebox.showinfo("Exito", "Producto Actualizado")
            ep.destroy()
        except Exception as e:
            messagebox.showerror("Actualizado con exito", f"Error al actualizar el producto: {e}")
    
    Category_Labael = Label(ep, text="Categoria", fg="black", bg="white", font=("Arial Black", 9))
    Category_Labael.place(x=30, y=30)
    Category_combobox = ttk.Combobox(ep, width=20)
    Category_combobox.place(x=115, y=35)
    Category_combobox.set(values[0])
    
    # Cargar categoria con ID en el ComboBox
    def load_categories_combobox():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("EXEC mostrarCategorias")
            rows = cursor.fetchall()

            #Crear diccionario para almacenar {nombre: id}
            category_dict = {row[1]: row[0] for row in rows} # row[0]: id_categoria, row[1]: nombre de la categoria
            Category_combobox['values'] = list(category_dict.keys()) #Mostrar nombre de los puestos
            cursor.close()
            conn.close()
            return category_dict
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los puestos en ComboBox: {e}")

    # Llamar a la función para cargar los puestos en el ComboBox
    category_dict = load_categories_combobox()
    
    Name_Label = Label(ep, text="Nombre", fg="black", bg="white", font=("Arial Black", 9))
    Name_Label.place(x=30, y=75)
    Name_Box = Entry(ep, width=20, bg="lightgray" )
    Name_Box.place(x=115, y=75)
    Name_Box.insert(0, values[1])

    Description_Label = Label(ep, text="Descripcion", fg="black", bg="white", font=("Arial Black", 9))
    Description_Label.place(x=30, y=115)
    Description_Box = Entry(ep, width=20, bg="lightgray" )
    Description_Box.place(x=115, y=115)
    Description_Box.insert(0, values[2])

    Precio_Label = Label(ep, text="Costo $", fg="black", bg="white", font=("Arial Black", 9))
    Precio_Label.place(x=30, y=155)
    Precio_Box = Entry(ep, width=5, bg="lightgray" )
    Precio_Box.place(x=115, y=155)
    Precio_Box.insert(0, values[3])
    
    Existence_Label = Label(ep, text="Existencia ", fg="black", bg="white", font=("Arial Black", 9))
    Existence_Label.place(x=30, y=200)
    Existence_Box = Label(ep, text=values[4], fg="black", bg="white", font=("Arial Black", 9))
    Existence_Box.place(x=115, y=200)

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
    values = item["values"]
    nombre_producto = values[1]
    id_producto = obtener_id_producto_por_nombre(nombre_producto)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC marcar_producto_inactivo @id_producto = ?", id_producto)
        conn.commit()
        cursor.close()
        conn.close()

        product_tree.delete(selected_item)
        messagebox.showinfo("Éxito", "Producto marcado como inactivo correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al marcar el producto como inactivo: {e}")

#Load employees inactives to show---------------------------------------------------
def load_productInactive():
    try:
        # Limpia el TreeView antes de recargar los registros
        product_tree.delete(*product_tree.get_children())

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC mostrar_productos_inactivos")
        rows = cursor.fetchall()
        # Concatenate names directly in the loop for efficiency
        for row in rows:
            formatted_row = ( 
                row[2], 
                row[1], 
                row[3], 
                f"{row[4]:.2f}", 
                row[5])
            product_tree.insert("", "end", values=formatted_row)
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los productos inactivos: {e}")

# Evento para la casilla de verificación
def toggle_product_inactive():
    if show_inactives_var.get():
        load_productInactive()  # Cargar productos inactivos
        Active_Product.place(x=840, y=120)
    else:
        Active_Product.place_forget()
        load_products()  # Cargar productos activos

def active_Product():
    selected_item = product_tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un producto para Activar")
        return

    confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea activar este producto?")
    if not confirm:
        return

    item = product_tree.item(selected_item)
    values = item["values"]
    item = product_tree.item(selected_item)
    nombre_producto = values[1]  
    
    # Obtener el id_empleado usando el RFC
    id_producto = obtener_id_producto_por_nombre(nombre_producto)
    if id_producto is None:
        return  # Si no se encuentra el ID, no continuar con la edición
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC marcar_producto_activo @id_producto = ?", id_producto)
        conn.commit()
        cursor.close()
        conn.close()

        product_tree.delete(selected_item)
        messagebox.showinfo("Éxito", "Producto marcado como activo correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al marcar el producto como activo: {e}")

def search_Products():
    query = search_entry.get().strip()  # Captura y limpia el texto ingresado
    if not query:  # Si la entrada está vacía, carga todos los productos
        load_products()
        return

    try:
        product_tree.delete(*product_tree.get_children())  # Limpia los datos actuales del Treeview
        conn = get_db_connection()  # Conecta a la base de datos
        cursor = conn.cursor()

       # Determinar el tipo de búsqueda y ejecutar el procedimiento almacenado correspondiente
        if query.isdigit():  # Búsqueda por ID (si decides implementarlo más adelante)
            cursor.execute("EXEC BuscarProductosCategoria ?", query)
        else:
            cursor.execute("EXEC BuscarProductosNombre ?", query)
            
        

        rows = cursor.fetchall()
        if not rows:
            messagebox.showinfo("Sin resultados", "No se encontraron productos que coincidan con el criterio de búsqueda.")
        else:
            for row in rows:
                # Ajusta el formato según las columnas del Treeview
                formatted_row = (
                    row[2], #Categoria
                    row[0], #Nombre
                    row[1], #Descripcion
                    row[3] #Costo
                    # f"{row[4]}" #Existencia
                )

            product_tree.insert("", "end", values=formatted_row)
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al buscar productos: {e}")

# Barra de búsqueda
search_entry = Entry(rgp, width=30)
search_entry.place(x=70, y=40)

search_button = Button(rgp, text="Buscar", command=search_Products)
search_button.place(x=20, y=40)
# Variable para la casilla de verificación
show_inactives_var = BooleanVar()

# Casilla de verificación para mostrar productos inactivos
show_inactives_check = Checkbutton(rgp, text="Mostrar productos inactivos", variable=show_inactives_var, bg="white", command=toggle_product_inactive)
show_inactives_check.place(x=20, y=90)

Add_Product = Button(rgp, text="Agregar producto", fg="black", bg="#CE7710", command=Add_Normal_Product_Window, font=("Arial Black", 9))
Add_Product.place(x=30, y=120)

Add_Product_kitchen = Button(rgp, text="Agregar Producto Cocina", fg="black", bg="#CE7710", command=Add_ProductWindow_Kitchen, font=("Arial Black", 9))
Add_Product_kitchen.place(x=290, y=120)

Edit_Product = Button(rgp, text="Editar Producto", fg="black", bg="#CE7710", command=Edit_ProductWindow, font=("Arial Black", 9))
Edit_Product.place(x=610, y=120)

Delete_Product = Button(rgp, text="Desactivar Producto", fg="black", bg="#CE7710", command=Delete_Product, font=("Arial Black", 9))
Delete_Product.place(x=840, y=120)

Active_Product = Button(rgp, text="Activar Producto", fg="black", background="#CE7710", command=active_Product, font=("Arial Black", 9))
Active_Product.config(width=20)

load_products()
rgp.mainloop()