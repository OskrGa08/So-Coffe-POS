from functools import partial
from pathlib import Path
import pyodbc
from tkinter import *
from tkinter import Scrollbar
from tkinter import Menubutton
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage
# Configuration main window--------------------------------------
mw = Tk()
mw.geometry("870x620")
mw.minsize(650, 500)
mw.maxsize(1024, 900)
mw.configure(bg="white")
mw.title("Salidas")
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

#Top Bar-----------------------------------------------
topBar_frame = Frame(mw, bg="#CE7710")
topBar_frame.place(x=0, y=0, relwidth=1, height=30)

#Frames--------------------------------------------------
detail_Frame = Frame(mw, bg="#D2D2D2")
detail_Frame.place(x=545, y=60, width=270, height=450)


#Logica de los command para que habra resectivas ventanas cada opcion(abrir las ventanas respectivas a cada gestionar)---------------------------------------
def managEmployees():
    mw.destroy()
    from Employees import Employees
    Employees()

def managInputs():
    mw.destroy()
    from Inputs import Inputs
    Inputs()

def pontiOfSale():
    mw.destroy()
    from POS import POS 
    POS()

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

def managShopping():
    mw.destroy()
    from Shopping import Shopping
    Shopping()

def managShoppingView():
    mw.destroy()
    from ShopingView import ShopingView
    ShopingView()

def  managSupplier():
    mw.destroy()
    from Suppliers import Suppliers 
    Suppliers()

def reports():
    mw.destroy()
    from Tries import Tries
    Tries()

#Option menu bar frame----------------------------------------------------------

# Load the image using PIL
#MB_image = PhotoImage(file="SO_CoffeApp/src/main/resources/menu_bar.png")
# Create a label to display the background image
MenuButton_barFrame = Menubutton(topBar_frame, bg="#CE7710", width=30, height=30)
MenuButton_barFrame.place(x=0, y=0)
MenuButton_barFrame.menu = Menu(MenuButton_barFrame, tearoff=0, bg="#CE7710")
MenuButton_barFrame.menu.add_command(label="Gestion de Insumos", foreground="white", font=("New Times Roman", 12), command=managInputs)
MenuButton_barFrame.menu.add_command(label="Gestion de Insumos", foreground="white", font=("New Times Roman", 12), command=managInputs)
MenuButton_barFrame.menu.add_command(label="Punto de Venta", foreground="white", font=("New Times Roman", 12), command=pontiOfSale)
MenuButton_barFrame.menu.add_command(label="Puestos de Empleados", foreground="white", font=("New Times Roman", 12), command=managPosition)
MenuButton_barFrame.menu.add_command(label="Categoria de Productos", foreground="white", font=("New Times Roman", 12), command=managProductCategory)
MenuButton_barFrame.menu.add_command(label="Gestion de Productos", foreground="white", font=("New Times Roman", 12), command=managProducts)
MenuButton_barFrame.menu.add_command(label="Vista de Ventas", foreground="white", font=("New Times Roman", 12), command= managSells)
MenuButton_barFrame.menu.add_command(label="Gestion de Compras", foreground="white", font=("New Times Roman", 12), command=managShopping)
MenuButton_barFrame.menu.add_command(label="Vista de Compras", foreground="white", font=("New Times Roman", 12), command=managShoppingView)
MenuButton_barFrame.menu.add_command(label="Gestion de Proveedores", foreground="white", font=("New Times Roman", 12), command=managSupplier)
MenuButton_barFrame.menu.add_command(label="Reportes", foreground="white", font=("New Times Roman", 12), command=reports)
MenuButton_barFrame["menu"] = MenuButton_barFrame.menu
 

Main_Label = Label(mw, text="SALIDAS", fg="black", bg="white", font=("Arial Black", 18))
Main_Label.place(x=200, y=55)

# Table to display products
product_columns = ("ID Salida", "Fecha / Hora")
product_tree = ttk.Treeview(mw, columns=product_columns, show="headings", height=5)
for col in product_columns:
    product_tree.heading(col, text=col)
product_tree.place(x=50, y=160, height=300)

product_scrollbar = Scrollbar(mw, orient="vertical", command=product_tree.yview)
product_scrollbar.place(x=432, y=165, height=290)
product_tree.configure(yscrollcommand=product_scrollbar.set)

# List to store selected ingredients
selected_inputs = []

#connection bd---------------------------------------------------------------------------------------------------------------------
def get_db_connection():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123;')
    return conn

def load_Outputs():
    try:
        product_tree.delete(*product_tree.get_children())
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC mostrar_salidas") #el metodo no imprime el noombre de ahi en mas todo bien 
        rows = cursor.fetchall()
        for row in rows:
            formatted_row = (
                row[0], 
                f"{row[1]}")
            product_tree.insert("", "end", values=formatted_row)
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar las salidas: {e}")
load_Outputs()

def on_select_output(event):
    # Obtener el ID de la salida seleccionada
    selected_item = product_tree.selection()
    if not selected_item:
        return  # Si no hay selección, salir

    item = product_tree.item(selected_item)
    salida_id = item["values"][0]  # El ID está en la primera columna

    # Limpiar el frame de detalles
    for widget in detail_Frame.winfo_children():
        widget.destroy()

    try:
        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ejecutar el procedimiento almacenado con el ID de la salida
        cursor.execute("EXEC mostrarDetalleSalida ?", salida_id)
        detalles = cursor.fetchall()
        
        # Mostrar los detalles en el frame
        Label(detail_Frame, text="Detalles de la Salida", bg="#D2D2D2", font=("Arial Black", 10)).pack(pady=5)
        
        for detalle in detalles:
            texto = f"Insumo: {detalle[0]}, Cantidad: {detalle[1]}"
            Label(detail_Frame, text=texto, bg="#D2D2D2", anchor="w").pack(fill="x", padx=10, pady=2)
        
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los detalles de la salida: {e}")

# Vincular el evento de selección al treeview
product_tree.bind("<<TreeviewSelect>>", on_select_output)

#Acomodar------------------------------------------
def Add_Output():
    try:
        with pyodbc.connect('DRIVER={SQL SERVER};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123') as conn:
            cursor = conn.cursor()

            # Ejecutar el procedimiento almacenado
            cursor.execute("INSERT INTO salidas (fecha_hora) VALUES (GETDATE())")
            id_salida = cursor.execute("SELECT SCOPE_IDENTITY()").fetchval()
            if id_salida is not None:
                print(f"ID de la salida recién insertada: {id_salida}")
            else:
                print("No se pudo obtener el ID de la salida.")
            # Llama a la función para manejar los detalles de la salida
            add_Content_Outputs(id_salida)

    except Exception as e:
        print(f"Error al insertar la salida: {e}")


def add_Content_Outputs(id_salida):
    ai = Toplevel(mw)
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
        if not id_salida or id_salida <= 0:
            messagebox.showerror("Error", "ID de salida no válido.")
            return

        if not selected_inputs:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM salidas WHERE id_salida = ?", (id_salida,))
                    conn.commit()
                    messagebox.showinfo("Cancelado", "Salida eliminada ya que no se agregaron insumos.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar la salida: {e}")
                finally:
                    ai.destroy()
            return

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                for insumo in selected_inputs:
                    id_input = insumo["id"]
                    cantidad = insumo["cantidad"]
                    if not id_input or cantidad <= 0:
                        raise ValueError("Datos de insumo no válidos.")
                    
                    cursor.execute(
                        "EXEC addDetalleSalida ?, ?, ?",
                        (id_salida, id_input, cantidad)
                    )
                conn.commit()
                messagebox.showinfo("Éxito", "Salida e insumos agregados correctamente.")
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


Add_Output = Button(mw, text="Agregar Nueva Salida", fg="black", bg="#CE7710", command=Add_Output, font=("Arial Black", 9))
Add_Output.place(x=50, y=120)


MB_image = PhotoImage(file="SO_CoffeApp/src/main/resources/reload.png")
reload_Bt = Button(mw, image=MB_image, fg="black", bg="#CE7710", command=load_Outputs, font=("Arial Black", 9))
reload_Bt.place(x=420, y=120)

mw.mainloop()