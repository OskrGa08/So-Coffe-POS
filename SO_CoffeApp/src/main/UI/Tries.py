import tkinter as tk
from tkinter import messagebox
import pyodbc
import datetime

# Crear una ventana de la aplicación
root = tk.Tk()
root.title("Sistema de Punto de Venta")

# Crear una lista para el carrito
carrito = []

# Conexión a la base de datos
def obtener_conexion():
    return pyodbc.connect(
        'DRIVER={SQL Server};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123;')

# Función para obtener los productos de la base de datos
def obtener_productos():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id_producto, nombre, costo FROM productos WHERE activo = 1")
    productos = cursor.fetchall()
    conn.close()
    return productos

# Función para agregar productos automáticamente al carrito
def agregar_producto(id_producto, nombre, precio_unitario):
    cantidad = int(entry_cantidad.get())
    # Verificar si el producto ya está en el carrito
    for item in carrito:
        if item['id_producto'] == id_producto:
            item['cantidad'] += cantidad
            item['subtotal'] = item['cantidad'] * item['precio_unitario']
            actualizar_carrito()
            return
    # Si no está en el carrito, agregar como nuevo
    subtotal = cantidad * precio_unitario
    carrito.append({
        'id_producto': id_producto,
        'nombre': nombre,
        'cantidad': cantidad,
        'precio_unitario': precio_unitario,
        'subtotal': subtotal
    })
    actualizar_carrito()

# Función para actualizar la visualización del carrito
def actualizar_carrito():
    texto_carrito.delete(1.0, tk.END)  # Limpiar la visualización anterior
    for item in carrito:
        texto_carrito.insert(tk.END, f"Producto: {item['nombre']}, Cantidad: {item['cantidad']}, Subtotal: {item['subtotal']}\n")

# Función para confirmar la venta
def confirmar_venta():
    id_empleado = entry_id_empleado.get()
    if not carrito:
        messagebox.showwarning("Carrito vacío", "No hay productos en el carrito.")
        return
    if not id_empleado:
        messagebox.showwarning("Falta ID Empleado", "Debe ingresar un ID de empleado.")
        return
    try:
        # Llamar a la función que guarda la venta en la base de datos
        confirmar_venta_en_base_de_datos(id_empleado)
        messagebox.showinfo("Venta confirmada", "La venta ha sido registrada.")
        carrito.clear()
        actualizar_carrito()
    except Exception as e:
        messagebox.showerror("Error", f"Error al confirmar la venta: {e}")

# Función para guardar la venta y los detalles en la base de datos
def confirmar_venta_en_base_de_datos(id_empleado):
    conn = obtener_conexion()
    cursor = conn.cursor()

    try:
        cursor.execute("BEGIN TRANSACTION")

        # Calcular el total de la venta
        total_venta = sum(item['subtotal'] for item in carrito)

        # Llamar al procedimiento almacenado para insertar la venta
        cursor.execute("EXEC addVenta @id_empleado=?, @total=?", id_empleado, total_venta)

        # Obtener el ID de la venta recién creada usando una alternativa a SCOPE_IDENTITY()
        id_venta = cursor.execute("SELECT TOP 1 id_venta FROM ventas ORDER BY id_venta DESC").fetchval()
        if id_venta is None:
            raise Exception("No se pudo obtener el id_venta. Verifique la inserción en la tabla Ventas.")

        # Insertar cada producto del carrito usando el procedimiento almacenado addDetalleVenta
        for item in carrito:
            cursor.execute("""
                EXEC addDetalleVenta @id_venta=?, @id_producto=?, @cantidad=?, @subtotal=?
            """, id_venta, item['id_producto'], item['cantidad'], item['subtotal'])

        # Confirmar la transacción
        cursor.execute("COMMIT TRANSACTION")
        conn.commit()
        print("Transacción confirmada.")
    except Exception as e:
        cursor.execute("ROLLBACK TRANSACTION")
        print(f"Error durante la transacción: {e}")
        raise e
    finally:
        conn.close()

# Función para mostrar los productos desde la base de datos
def mostrar_productos():
    productos = obtener_productos()
    for index, producto in enumerate(productos):
        id_producto, nombre, costo = producto
        boton_producto = tk.Button(root, text=f"{nombre} (${costo})", command=lambda p=producto: agregar_producto(p[0], p[1], p[2]))
        boton_producto.grid(row=index + 1, column=0)

# Crear los widgets
label_producto = tk.Label(root, text="Producto")
label_producto.grid(row=0, column=0)
label_cantidad = tk.Label(root, text="Cantidad")
label_cantidad.grid(row=0, column=1)
label_id_empleado = tk.Label(root, text="ID Empleado")
label_id_empleado.grid(row=0, column=2)

# Entradas de cantidad y ID empleado
entry_cantidad = tk.Entry(root)
entry_cantidad.grid(row=1, column=1)
entry_id_empleado = tk.Entry(root)
entry_id_empleado.grid(row=1, column=2)

# Texto donde se mostrará el carrito
texto_carrito = tk.Text(root, height=10, width=50)
texto_carrito.grid(row=5, column=0, columnspan=3)

# Botón para confirmar la venta
boton_confirmar = tk.Button(root, text="Confirmar Venta", command=confirmar_venta)
boton_confirmar.grid(row=6, column=0, columnspan=3)

# Llamar a la función que muestra los productos al iniciar la aplicación
mostrar_productos()

# Ejecutar la ventana
root.mainloop()