import os
from pathlib import Path
from tkinter import *
from tkinter import font
from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk

# Configuration main window---------------------------
root = Tk()
root.geometry("1003x556")
root.minsize(700, 500)
root.maxsize(1003, 550)
root.configure(bg="#D7CCC8")
root.title("Log In")

# Icon --------------------------
base_dir = Path(__file__).resolve().parent
icon_path = base_dir.parent / 'resources' / 'icon sf.ico'
icon_path_str = str(icon_path)
if icon_path.exists():
    try:
        root.iconbitmap(icon_path_str)
    except Exception as e:
        print(f"Error al cargar el icono: {e}")
else:
    print(f"El archivo de icono no se encuentra en la ruta especificada: {icon_path_str}")

# Background -----------------------------------
image_path = base_dir.parent /'resources' / 'background_LogIn.jpg'
image_path_str = str(image_path)

# Verificar la existencia de la imagen antes de cargarla
if image_path.exists():
    try:
        # Cargar imagen con PIL
        pil_image = Image.open(image_path_str)
        background_image = ImageTk.PhotoImage(pil_image)
        background_label = tk.Label(root, image=background_image)
        background_label.place(x=0, y=0)
        background_label.place(relx=0, rely=0, relheight=1, relwidth=1)
    except Exception as e:
        print(f"Error al cargar la imagen de fondo: {e}")
else:
    print(f"La imagen de fondo no se encuentra en la ruta especificada: {image_path_str}")
#Frame---------------------------------------------------------------------
LogIn_frame = Frame(root, bg="white", width=350, height=350, bd=10)
LogIn_frame.place(x=342, y=100)

# Labels Loggin----------------------------------------------------------------------
LabelNameCompany = Label(LogIn_frame, text="S-O Login", font=("Cambria", 22), bg="white", fg="black")
LabelNameCompany.place(x=165, y=40, anchor="center")
LabelDescrip = Label(LogIn_frame, text="Enter your details to get \n sign in to your account", font=("Cambria", 14), bg="white", fg="black")
LabelDescrip.place(x=160, y=100, anchor="center")
#TextBox User------------------------------------------------------------------
text_user = StringVar(value="Enter your User Name")
User_TextBox = Entry(LogIn_frame, textvariable=text_user, font=("Cambria", 9), justify=LEFT, bg="white", fg="grey", selectborderwidth=0, bd=0, highlightthickness=1, highlightcolor="black" ,borderwidth=0, width=25)
User_TextBox.place(x=160, y=150, anchor="center")

#TextBox Password-----------------------------------------------------------------
text_pass = StringVar(value="Password")
Password_TextBox = Entry(LogIn_frame, textvariable=text_pass, font=("Cambria", 9), justify=LEFT, bg="white", fg="grey", selectborderwidth=0, bd=0, highlightthickness=1, highlightcolor="black" ,borderwidth=0, width=25, show="*")
Password_TextBox.place(x=160, y=190, anchor="center")


#Button Join
Join_Button = Button(LogIn_frame, text="Log in", font=("Cambria", 9), fg="black", overrelief=FLAT, width=25)
Join_Button.config(bg="#E0A52D")
Join_Button.place(x=160, y=230, anchor="center")

#END-------------------------------------------------------------------------------
root.mainloop()
