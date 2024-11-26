import tkinter as tk
from tkinter import messagebox
import pyodbc

# Crear una ventana de la aplicación
root = tk.Tk()
root.title("Sistema de Compras")

# Crear una lista para el carrito
carrito = []

# Conexión a la base de datos
def obtener_conexion():
    return pyodbc.connect(
        'DRIVER={SQL Server};SERVER=DESKTOP-M8N9242;DATABASE=Socoffe;UID=sa;PWD=sistemas123;')

# Función para obtener productos e insumos
def obtener_productos_insumos():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("EXEC MostrarProductosInsumos")
    productos = cursor.fetchall()
    conn.close()
    return productos

def agregar_producto(id_producto, nombre, precio_unitario, tipo):
    cantidad = int(entry_cantidad.get())
    
    # Verificar si el producto/insumo ya está en el carrito
    producto_existente = None
    for item in carrito:
        # Aquí verificamos tanto el id_producto como el tipo (producto o insumo)
        if item['id_producto'] == id_producto and item['tipo'] == tipo:
            producto_existente = item
            break
    
    if producto_existente:
        # Si ya existe, actualizamos la cantidad y el costo
        producto_existente['cantidad'] += cantidad
        producto_existente['costo'] = producto_existente['cantidad'] * producto_existente['precio_unitario']
    else:
        # Si no está en el carrito, lo agregamos como nuevo
        costo = cantidad * precio_unitario
        carrito.append({
            'id_producto': id_producto,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio_unitario': precio_unitario,
            'costo': costo,
            'tipo': tipo  # Guardamos el tipo (producto o insumo)
        })
    
    # Actualizar la visualización del carrito después de agregar el producto
    actualizar_carrito()



# Función para actualizar la visualización del carrito
def actualizar_carrito():
    texto_carrito.delete(1.0, tk.END)  # Limpiar la visualización anterior
    for item in carrito:
        texto_carrito.insert(tk.END, f"Producto: {item['nombre']}, Cantidad: {item['cantidad']}, costo: {item['costo']}\n")

# Función para confirmar la compra
def confirmar_compra():
    id_proveedor = entry_id_proveedor.get()
    if not carrito:
        messagebox.showwarning("Carrito vacío", "No hay productos en el carrito.")
        return
    if not id_proveedor:
        messagebox.showwarning("Falta ID Proveedor", "Debe ingresar un ID de proveedor.")
        return
    try:
        # Guardar la compra en la base de datos
        id_compra = confirmar_compra_en_base_de_datos(id_proveedor)
        
        # Actualizar existencias de productos e insumos
        if id_compra is not None:
            messagebox.showinfo("Compra confirmada", "La compra ha sido registrada y las existencias actualizadas.")
            carrito.clear()
            actualizar_carrito()
    except Exception as e:
        messagebox.showerror("Error", f"Error al confirmar la compra: {e}")

# Función para guardar la compra y detalles en la base de datos
def confirmar_compra_en_base_de_datos(id_proveedor):
    conn = obtener_conexion()
    cursor = conn.cursor()
    id_compra = None

    try:
        cursor.execute("BEGIN TRANSACTION")

        # Calcular el total de la compra
        total_compra = sum(item['costo'] for item in carrito)

        # Llamar al procedimiento almacenado para insertar la compra
        cursor.execute("EXEC addCompras @id_proveedor=?, @total=?", id_proveedor, total_compra)

        # Obtener el ID de la compra recién creada
        id_compra = cursor.execute("SELECT TOP 1 id_compra FROM compras ORDER BY id_compra DESC").fetchval()
        if id_compra is None:
            raise Exception("No se pudo obtener el id_compra. Verifique la inserción en la tabla Compras.")

        # Insertar cada ítem del carrito usando addDetalleCompra o en compra_productos según tipo
        for item in carrito:
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


# Función para mostrar los productos e insumos desde la base de datos
def mostrar_productos_insumos():
    productos_insumos = obtener_productos_insumos()
    for index, item in enumerate(productos_insumos):
        id_producto, nombre, categoria, descripcion, costo, existencia, tipo = item
        
        # Mostrar productos empaquetados (tipo 1) y insumos (tipo 0)
        boton_item = tk.Button(root, text=f"{nombre} (${costo})", command=lambda i=item: agregar_producto(i[0], i[1], i[4], i[6]))
        boton_item.grid(row=index + 1, column=0)


# Crear los widgets
label_producto = tk.Label(root, text="Producto/Insumo")
label_producto.grid(row=0, column=0)
label_cantidad = tk.Label(root, text="Cantidad")
label_cantidad.grid(row=0, column=1)
label_id_proveedor = tk.Label(root, text="ID Proveedor")
label_id_proveedor.grid(row=0, column=2)

# Entradas de cantidad y ID proveedor
entry_cantidad = tk.Entry(root)
entry_cantidad.grid(row=1, column=1)
entry_id_proveedor = tk.Entry(root)
entry_id_proveedor.grid(row=1, column=2)

# Texto donde se mostrará el carrito
texto_carrito = tk.Text(root, height=10, width=50)
texto_carrito.grid(row=5, column=0, columnspan=3)

# Botón para confirmar la compra
boton_confirmar = tk.Button(root, text="Confirmar Compra", command=confirmar_compra)
boton_confirmar.grid(row=6, column=0, columnspan=3)

# Llamar a la función que muestra los productos e insumos al iniciar la aplicación
mostrar_productos_insumos()

# Ejecutar la ventana
root.mainloop()