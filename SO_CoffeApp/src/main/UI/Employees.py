import pyodbc
from tkinter import *
from tkinter import ttk

# Configuration main window---------------------------
remp = Tk()
remp.geometry("850x700")
remp.minsize(700, 500)
remp.maxsize(1500, 580)
remp.configure(bg="white")
remp.title("Registrar nuevo empleado")


Main_Label = Label(remp, text="EMPLEADOS", fg="black", bg="white", font=("Arial Black", 18))
Main_Label.place(x=330, y=75)

# Table to display products
product_columns = ("ID Empleado", "Nombre", "Apellido Paterno", "Apellido Materno", "Puesto", "Telefono", "Domicilio", "RFC", "Estado")
product_tree = ttk.Treeview(remp, columns=product_columns, show="headings", height=5)
for col in product_columns:
    product_tree.heading(col, text=col)
product_tree.place(x=20, y=160, height=200)


remp.mainloop()