import tkinter as tk
from tkinter import *
from users import Client
from appV1 import *

class GUI(tk.Tk):

    def __init__(self, app:App):
        tk.Tk.__init__(self) 
        
        self.title(app.name)

        master = tk.Frame(self)
        master.pack(side="top", fill="both", expand=True)
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        
        #self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.frames = {}
        for F in (StartPage, Login, JoinOrder, Register):
            page_name = F.__name__
            frame = F(parent=master, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def validate(self):
        pass

    def forguet_password(self):
        print("Sos un boludo")
        pass

class StartPage(tk.LabelFrame):
    def __init__(self, parent, controller):
        tk.LabelFrame.__init__(self, parent, pady=10)
        self["text"]="Inicio"
        self.controller = controller
        #label = tk.Label(self, text="This is the start page", font=controller.title_font)
        #label.pack(side="top", fill="x", pady=10)
        
        tk.Button(self, text="Ingresar", command=lambda: controller.show_frame("Login"), height=5).pack(fill="both")
        tk.Button(self, text="Unirme a un Pedido", command=lambda: controller.show_frame("JoinOrder"), height=5).pack(fill="both")

class Login(tk.LabelFrame):
    def __init__(self, parent, controller):
        tk.LabelFrame.__init__(self, parent, pady=20, padx=10)
        self["text"]="Iniciar Sesion"
        self.controller = controller
        
 
        label=tk.Label(self, text="DNI:").grid(row=0, column=0)
        name=tk.Entry(self).grid(row=0, column=1)
        label=tk.Label(self, text="Contraseña:", pady=10).grid(row=1, column=0)
        password=tk.Entry(self).grid(row=1, column=1)
        tk.Button(self, text="Olvidé la contraseña", command=lambda: controller.forguet_password()).grid(row=2, column=1)
        tk.Label(self, text="").grid(row=3, column=2)
        tk.Button(self, text="Ingresar", command=lambda: controller.validate()).grid(row=4, column=1)
        tk.Label(self, text="").grid(row=5, column=0)
        tk.Button(self, text="Atras", command=lambda: controller.show_frame("StartPage")).grid(row=6, column=0)
        tk.Button(self, text="Registrarme", command=lambda: controller.show_frame("Register")).grid(row=6, column=1)


class JoinOrder(tk.LabelFrame):
    def __init__(self, parent, controller):
        tk.LabelFrame.__init__(self, parent, pady=20)
        self["text"]="Ingresar como invitado"
        self.controller = controller
        label=tk.Label(self, text="Nombre:").grid(row=0, column=1)
        nick_tag=tk.Entry(self).grid(row=0, column=2, columnspan=2)
        label=tk.Label(self, text="Codigo:").grid(row=1, column=1)
        code=tk.Entry(self).grid(row=1, column=2, columnspan=2)
        tk.Label(self, text=" ").grid(row=4, column=0, columnspan=5)
        tk.Button(self, text="Atras", command=lambda: controller.show_frame("StartPage")).grid(row=5, column=2)
        tk.Button(self, text="Continuar", command=lambda: controller.show_frame("HomeGuest")).grid(row=5, column=3)

class Register(tk.LabelFrame):
    def __init__(self, parent, controller):
        tk.LabelFrame.__init__(self, parent, pady=10, padx=10)
        self["text"]="Registrarse"
        self.controller = controller

        
        self.name_tag = tk.StringVar()
        lastname_tag = tk.StringVar()
        dni_tag = tk.StringVar()
        pass_tag = tk.StringVar()
        prefix = tk.StringVar()
        number = tk.StringVar()
        address_tag = tk.StringVar()

        tk.Label(self, text="Nombre:").grid(row=0, column=0)
        tk.Entry(self, textvariable= self.name_tag).grid(row=0, column=1, columnspan=12, ipadx=15, padx=10)
        tk.Label(self, text="Apellido:").grid(row=1, column=0)
        tk.Entry(self, textvariable=lastname_tag).grid(row=1, column=1, columnspan=12, ipadx=15, padx=10)
        tk.Label(self, text="DNI:", justify="left").grid(row=2, column=0)
        tk.Entry(self, textvariable=dni_tag).grid(row=2, column=1, columnspan=12, ipadx=15, padx=10)
        tk.Label(self, text="Contraseña:").grid(row=3, column=0)
        tk.Entry(self, textvariable=pass_tag).grid(row=3, column=1, columnspan=5, ipadx=15, padx=10)
        tk.Label(self, text="Telefono:").grid(row=4, column=0)
        tk.Label(self, text="+54", width=3).grid(row=4, column=1, columnspan=1)
        tk.Entry(self, width=4, textvariable=prefix).grid(row=4, column=2)
        tk.Label(self, text="-").grid(row=4, column=3)
        tk.Entry(self, width=6, textvariable=number).grid(row=4, column=4)
        
        #phone_tag= prefix + number
        tk.Label(self, text="Direccion:").grid(row=5, column=0)
        tk.Entry(self, textvariable=address_tag).grid(row=5, column=1, columnspan=12, ipadx=15, padx=10)
        
        
        tk.Button(self, text="Atras", command=lambda: controller.show_frame("Login")).grid(row=6, column=1, pady=20)
        tk.Button(self, text="Continuar", command=lambda: self.get_values(), width=6).grid(row=6, column=2, columnspan=3)

    def get_values(self):
        print(self.name_tag.get())
        
    


def main():
    app=App("Gestion de Pedidos para Restaurante", "database.db")
    gui = GUI(app)
    gui.mainloop()
    return 0

if __name__ == '__main__':
    main()
