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