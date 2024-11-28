import datetime
import tkinter as tk
from tkinter import Menu, Menubutton, PhotoImage, messagebox
from tkinter import ttk
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

# Clase para manejar los reportes
class SocoffeReportes:
    def __init__(self, server, database, username, password):
        self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123;')

    def ejecutar_query(self, query):
        return pd.read_sql(query, self.conn)

    # RF003 - Ventas Totales Anuales y Mensuales, Ventas por Empleado
    def ventas_totales_anuales_y_mensuales(self):
        query_annual = """
        SELECT YEAR(fecha) AS año, SUM(total) AS total_ventas
        FROM ventas
        GROUP BY YEAR(fecha)
        ORDER BY año;
        """
        query_monthly = """
        SELECT MONTH(fecha) AS mes, SUM(total) AS total_ventas
        FROM ventas
        GROUP BY MONTH(fecha)
        ORDER BY mes;
        """
        df_annual = self.ejecutar_query(query_annual)
        df_monthly = self.ejecutar_query(query_monthly)

        # Crear gráficos
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,6))

        # Ventas Totales Anuales
        ax1.plot(df_annual['año'], df_annual['total_ventas'], marker='o', color='blue')
        ax1.set_title('Ventas Totales Anuales')
        ax1.set_xlabel('Año')
        ax1.set_ylabel('Ventas Totales ($)')

        # Ventas Totales Mensuales
        ax2.plot(df_monthly['mes'], df_monthly['total_ventas'], marker='o', color='orange')
        ax2.set_title('Ventas Totales Mensuales')
        ax2.set_xlabel('Mes')
        ax2.set_ylabel('Ventas Totales ($)')

        plt.tight_layout()
        plt.show()

    # RF003 - Ventas por Empleado
    def ventas_por_empleado(self, fecha_inicio=None, fecha_fin=None):
        filtro_fecha = ""
        if fecha_inicio and fecha_fin:
            filtro_fecha = f"WHERE v.fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'"

        query = f"""
        SELECT e.nombre, SUM(v.total) AS total_ventas
        FROM ventas v
        JOIN empleado e ON v.id_empleado = e.id_empleado
        {filtro_fecha}
        GROUP BY e.nombre
        ORDER BY total_ventas DESC;
        """
        df = self.ejecutar_query(query)
        
        # Mostrar un gráfico de ventas por empleado
        plt.figure(figsize=(10, 6))
        plt.barh(df['nombre'], df['total_ventas'], color='skyblue')
        plt.title(f'Ventas por Empleado ({fecha_inicio} a {fecha_fin})' if fecha_inicio and fecha_fin else 'Ventas por Empleado')
        plt.xlabel('Total Ventas ($)')
        plt.ylabel('Empleado')
        plt.tight_layout()
        plt.show()



    # RF004 - Compras Totales Mensuales y Anuales
    def compras_totales_anuales_y_mensuales(self):
        query_annual = """
        SELECT YEAR(fecha) AS año, SUM(total) AS total_compras
        FROM compras
        GROUP BY YEAR(fecha)
        ORDER BY año;
        """
        query_monthly = """
        SELECT MONTH(fecha) AS mes, SUM(total) AS total_compras
        FROM compras
        GROUP BY MONTH(fecha)
        ORDER BY mes;
        """
        df_annual = self.ejecutar_query(query_annual)
        df_monthly = self.ejecutar_query(query_monthly)

        # Crear gráficos
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,6))

        # Compras Totales Anuales
        ax1.plot(df_annual['año'], df_annual['total_compras'], marker='o', color='green')
        ax1.set_title('Compras Totales Anuales')
        ax1.set_xlabel('Año')
        ax1.set_ylabel('Compras Totales ($)')

        # Compras Totales Mensuales
        ax2.plot(df_monthly['mes'], df_monthly['total_compras'], marker='o', color='red')
        ax2.set_title('Compras Totales Mensuales')
        ax2.set_xlabel('Mes')
        ax2.set_ylabel('Compras Totales ($)')

        plt.tight_layout()
        plt.show()

    # RF005 - Inventario de Productos
    def inventario_de_productos(self):
        query = """
        SELECT p.nombre, p.existencia
        FROM productos p
        WHERE p.activo = 1 AND p.existencia > 0;
        """
        df = self.ejecutar_query(query)
        
        if not df.empty:
            plt.figure(figsize=(10, 6))
            plt.bar(df['nombre'], df['existencia'], color='lightcoral')
            plt.title('Inventario de Productos (con Existencias)')
            plt.xlabel('Producto')
            plt.ylabel('Existencia')
            plt.xticks(rotation=90)
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showinfo("Inventario de Productos", "No hay productos con existencias disponibles.")

    # RF005 - Salidas de Productos
    def salidas_por_producto(self):
        query = """
        SELECT i.nombre, SUM(ds.cantidad) AS cantidad_salidas
        FROM detalle_salidas ds
        JOIN insumos i ON ds.id_insumo = i.id_insumo
        GROUP BY i.nombre
        ORDER BY cantidad_salidas DESC;
        """
        df = self.ejecutar_query(query)
        plt.figure(figsize=(10,6))
        plt.barh(df['nombre'], df['cantidad_salidas'], color='salmon')
        plt.title('Salidas de Insumos por Producto')
        plt.xlabel('Cantidad Salidas')
        plt.ylabel('Producto')
        plt.tight_layout()
        plt.show()

    def ventas_del_dia(self, ventas_label):
        # Obtener la fecha actual
        today = datetime.date.today()

        # Consultar las ventas del día actual
        query = f"""
        SELECT fecha, SUM(total) as total_ventas
        FROM ventas
        WHERE CAST(fecha AS DATE) = '{today}'
        GROUP BY fecha;
        """
        df = self.ejecutar_query(query)

        # Mostrar un gráfico con las ventas del día
        plt.figure(figsize=(10, 6))
        if not df.empty:
            plt.plot(df['fecha'], df['total_ventas'], marker='o', color='green')
            plt.title(f'Ventas del Día ({today})')
            plt.xlabel('Fecha')
            plt.ylabel('Total Ventas ($)')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            plt.show()

            # Actualizar el Label con el total de ventas
            total_ventas = df['total_ventas'].iloc[0]
            ventas_label.config(text=f"Total Ventas del Día: ${total_ventas:.2f}")
        else:
            # Mostrar mensaje de que no hay ventas
            ventas_label.config(text="No hay ventas registradas para el día de hoy.")

    # RF005 - Inventario de Insumos
    def inventario_de_insumos(self):
        query = """
        SELECT i.nombre, i.existencia
        FROM insumos i
        WHERE i.activo = 1;
        """
        df = self.ejecutar_query(query)
        
        # Verificar si hay datos para mostrar
        if not df.empty:
            plt.figure(figsize=(10, 6))
            plt.bar(df['nombre'], df['existencia'], color='lightblue')
            plt.title('Inventario de Insumos')
            plt.xlabel('Insumo')
            plt.ylabel('Existencia')
            plt.xticks(rotation=90)
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showinfo("Inventario de Insumos", "No hay insumos activos en el inventario.")

def show_daily_sales_report():
    # Mostrar las ventas del día
    reportes.ventas_del_dia()

    # Mostrar las ventas del día en un messagebox
    today = datetime.date.today()
    
    query = f"""
    SELECT fecha, SUM(total) as total_ventas
    FROM ventas
    WHERE CAST(fecha AS DATE) = '{today}'
    GROUP BY fecha;
    """
    df = reportes.ejecutar_query(query)
    
    if not df.empty:
        total_ventas = df['total_ventas'].iloc[0]
        messagebox.showinfo("Ventas del Día", f"Total de ventas del día {today}: ${total_ventas:.2f}")
    else:
        messagebox.showinfo("Ventas del Día", f"No hay ventas registradas para el día {today}.")

def show_sales_by_employee_report():
    # Crear ventana emergente para rango de fechas
    def generar_reporte():
        fecha_inicio = start_date.get()
        fecha_fin = end_date.get()
        reportes.ventas_por_empleado(fecha_inicio, fecha_fin)

    popup = tk.Toplevel()
    popup.title("Seleccionar Periodo")
    tk.Label(popup, text="Fecha Inicio (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5)
    start_date = tk.Entry(popup)
    start_date.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(popup, text="Fecha Fin (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5)
    end_date = tk.Entry(popup)
    end_date.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Button(popup, text="Generar Reporte", command=generar_reporte).grid(row=2, column=0, columnspan=2, pady=10)

# Funciones para los botones
def show_sales_report():
    reportes.ventas_totales_anuales_y_mensuales()

def show_purchases_report():
    reportes.compras_totales_anuales_y_mensuales()

def show_inventory_report():
    reportes.inventario_de_productos()
    #mostrar solo los que tienen existencias

def show_sales_exits_report():
    reportes.salidas_por_producto()  
    
def show_daily_sales_report():
    reportes.ventas_del_dia(total_label)

def show_insumos_inventory():
    reportes.inventario_de_insumos()


# Crear la ventana principal del Dashboard
root = tk.Tk()
root.title("Dashboard de Reportes")
root.geometry("800x600")

#Logica de los command para que habra resectivas ventanas cada opcion(abrir las ventanas respectivas a cada gestionar)---------------------------------------
def managEmployees():
    root.destroy()
    from Employees import Employees
    Employees()

def managInputs():
    root.destroy()
    from Inputs import Inputs
    Inputs()

def managOutPuts():
    root.destroy()
    from OutPuts import OutPuts
    OutPuts()

def pontiOfSale():
    root.destroy()
    from POS import POS 
    POS()

def managPosition():
    root.destroy()
    from Position import Position
    Position()

def managProductCategory():
    root.destroy()
    from ProductCategory import ProductCategory
    ProductCategory()

def managProducts():
    root.destroy()
    from Products import Products 
    Products()

def managSells():
    root.destroy()
    from Sells import Sells 
    Sells()

def managShopping():
    root.destroy()
    from Shopping import Shopping
    Shopping()

def managShoppingView():
    root.destroy()
    from ShopingView import ShopingView
    ShopingView()

def  managSupplier():
    root.destroy()
    from Suppliers import Suppliers 
    Suppliers()


# Load the image using PIL
MB_image = PhotoImage(file="SO_CoffeApp/src/main/resources/menu_bar.png")
# Create a label to display the background image
MenuButton_barFrame = Menubutton(root, image=MB_image ,bg="#4CAF50", width=30, height=30)
MenuButton_barFrame.place(x=0, y=13)
MenuButton_barFrame.menu = Menu(MenuButton_barFrame, tearoff=0, bg="#4CAF50")
MenuButton_barFrame.menu.add_command(label="Gestion de Empleados", foreground="white", font=("New Times Roman", 12), command=managEmployees)
MenuButton_barFrame.menu.add_command(label="Gestion de Salidas", foreground="white", font=("New Times Roman", 12), command=managOutPuts)
MenuButton_barFrame.menu.add_command(label="Gestion de Insumos", foreground="white", font=("New Times Roman", 12), command=managInputs)
MenuButton_barFrame.menu.add_command(label="Punto de Venta", foreground="white", font=("New Times Roman", 12), command=pontiOfSale)
MenuButton_barFrame.menu.add_command(label="Puestos de Empleados", foreground="white", font=("New Times Roman", 12), command=managPosition)
MenuButton_barFrame.menu.add_command(label="Categorias de Productos", foreground="white", font=("New Times Roman", 12), command=managProductCategory)
MenuButton_barFrame.menu.add_command(label="Gestion de Productos", foreground="white", font=("New Times Roman", 12), command= managProducts)
MenuButton_barFrame.menu.add_command(label="Vista de Ventas", foreground="white", font=("New Times Roman", 12), command=managSells)
MenuButton_barFrame.menu.add_command(label="Gestion de Compras", foreground="white", font=("New Times Roman", 12), command=managShopping)
MenuButton_barFrame.menu.add_command(label="Vista de Compras", foreground="white", font=("New Times Roman", 12), command=managShoppingView)
MenuButton_barFrame.menu.add_command(label="Gestion de Proveedores", foreground="white", font=("New Times Roman", 12), command=managSupplier)
MenuButton_barFrame["menu"]= MenuButton_barFrame.menu

# Título
title_label = tk.Label(root, text="Dashboard de Reportes", font=("Arial", 20, "bold"), bg="#4CAF50", fg="white")
title_label.pack(fill=tk.X, pady=10)
title_label.lower()

# Crear un frame para organizar los botones
frame = tk.Frame(root)
frame.pack(pady=20)

# Botones para los reportes
sales_report_button = tk.Button(frame, text="Ventas Anuales y Mensuales", width=25, font=("Arial", 12), command=show_sales_report)
sales_report_button.grid(row=0, column=0, padx=10, pady=10)

sales_by_employee_button = tk.Button(frame, text="Ventas por Empleado", width=25, font=("Arial", 12), command=show_sales_by_employee_report)
sales_by_employee_button.grid(row=0, column=1, padx=10, pady=10)

purchases_report_button = tk.Button(frame, text="Compras Anuales y Mensuales", width=25, font=("Arial", 12), command=show_purchases_report)
purchases_report_button.grid(row=1, column=0, padx=10, pady=10)

inventory_report_button = tk.Button(frame, text="Inventario de Productos", width=25, font=("Arial", 12), command=show_inventory_report)
inventory_report_button.grid(row=1, column=1, padx=10, pady=10)

sales_exits_report_button = tk.Button(frame, text="Salidas de Productos", width=25, font=("Arial", 12), command=show_sales_exits_report)
sales_exits_report_button.grid(row=2, column=0, padx=10, pady=10)

daily_sales_button = tk.Button(frame, text="Corte de Caja (Ventas del Día)", width=25, font=("Arial", 12), command=show_daily_sales_report)
daily_sales_button.grid(row=2, column=1, padx=10, pady=10)

insumos_inventory_button = tk.Button(frame, text="Existencias de Insumos", width=25, font=("Arial", 12), command=show_insumos_inventory)
insumos_inventory_button.grid(row=3, column=0, padx=10, pady=10)

# Etiqueta para mostrar el total de ventas
total_label = tk.Label(root, text="Total Ventas del Día: $0.00", font=("Arial", 16))
total_label.pack(pady=20)

# Barra de navegación adicional (si es necesario)
navigation_frame = tk.Frame(root)
navigation_frame.pack(pady=20)

# Salir
exit_button = tk.Button(root, text="Salir", font=("Arial", 12), bg="red", fg="white", command=root.quit)
exit_button.pack(pady=20)

# Iniciar la conexión a la base de datos
server = 'localhost'
database = 'Socoffe'
username = 'sa'
password = 'sistemas123'
reportes = SocoffeReportes(server, database, username, password)

# Ejecutar la aplicación
root.mainloop()
