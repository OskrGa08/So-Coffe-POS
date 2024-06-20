from pathlib import Path
from tkinter import *
from tkinter import Scrollbar
from tkinter import Menubutton
from tkinter.ttk import Combobox
import pyodbc

# Configuration main window--------------------------------------
mw = Tk()
mw.geometry("1024x733")
mw.minsize(700, 500)
mw.maxsize(1024, 580)
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
checkout_frame.place(x=745, y=60, width=260, height=450)
bar_frame.place(x=0, y=0, relwidth=1, height=30)

#Buttons and Labels main window
CancelOrder_Button = Button(text="Cancelar Orden", font=("Katibeh",15), fg="red", bg="SystemButtonFace", overrelief=FLAT, width=25, highlightbackground="red")
CancelOrder_Button.config(bg=mw.cget('bg'))
CancelOrder_Button.place(x=220, y=550, anchor="center", width=200)

HoldOrder_Button = Button(text="Completar Orden", font=("Katibeh",15), fg="green", bg="SystemButtonFace", overrelief=FLAT, width=25, highlightbackground="green")
HoldOrder_Button.config(bg=mw.cget('bg'))
HoldOrder_Button.place(x=440, y=550, anchor="center", width=200)

Payment_Label = Label(text="configurar esta madre",font=("Katibeh", 10), bg="#309B15", fg="white")#hacer que el texto sea lo que arroje el total
Payment_Label.place(x=875, y=540, anchor="center", width=260, height=35)

#Customize Checkout_frame----------------------------------------
Checkout_Label = Label(checkout_frame, text="Cuenta", font=("Arial Black", 10), bg="white", fg="black")
Checkout_Label.place(x=135, y=10, anchor="center", relwidth=1, height=10)

Atributtes_Label = Label(checkout_frame, text="Nombre            Cantidad             Precio", font=("Arial", 10), bg="#d4d9d6", fg="black")
Atributtes_Label.place(x=260, y=30, anchor="e", relwidth=1, height=15)

#Logica de los command para que habra resectivas ventanas cada opcion(abrir las ventanas respectivas a cada gestionar)---------------------------------------
def managment_sales():
    mw.destroy()
    #from Sales_Management import Sales_Management
    #Sales_Management()

# Función para cerrar sesión
def logout():
    mw.destroy()
    from LogIn import logIn
    logIn()


#connection bd
def get_db_connection():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123;')
    return conn

def get_active_products():
    conn = get_db_connection()  
    if not conn:
        return []

    products = []
    cursor = conn.cursor()
    try:
        cursor.execute("EXEC mostrar_productos_activos")  # Call the stored procedure
        for row in cursor:
            products.append({"nombre": row[1], "Descripcion": row[2],  "costo": row[3]})  # Assuming the procedure returns name and price
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
            text=f"{product_name} \n {product_description} \n ${product_price:.2f}",
            command=lambda name=product_name, price=product_price, description=product_description: on_product_click(name, description, price),
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
def on_product_click(product_name, product_description, product_price):
    print(f"Producto seleccionado: {product_name} - Precio: ${product_price:.2f} - Descripción: {product_description}")  # Replace with your desired action

#ScrollBar products_frame  --------------------------------------------------- 
Canvas_scrollbar = Canvas(products_frame)
Canvas_scrollbar.pack(side=LEFT, fill=BOTH, expand=True)
inner_frame = Frame(Canvas_scrollbar)
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


#Configure Combobox----------------------------------------------------------------------
employee_combobox = Combobox(mw)
employee_combobox.place(x=745, y=35)

def get_mostrar_empleados_activos():
    conn = get_db_connection()  
    if not conn:
        return []

    employees = []
    cursor = conn.cursor()
    try:
        cursor.execute("EXEC mostrar_empleados_activos")  # Call the stored procedure
        for row in cursor:
            products.append({row[1]})  # Assuming the procedure returns name and price
    finally:
        if conn:
            conn.close()

    return employees


def configure_combobox():
    """Fetches employee names and populates the combobox."""
    employee_names = get_mostrar_empleados_activos()
   # employee_combobox.set_values(*employee_names)  # Set combobox values using unpacking

configure_combobox()

#END----------------------------
mw.mainloop()

            
