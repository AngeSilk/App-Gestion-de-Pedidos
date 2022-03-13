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

    def db_check(self, values):
        print(values)

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
        self.lastname_tag = tk.StringVar()
        self.dni_tag = tk.StringVar()
        self.pass_tag = tk.StringVar()
        self.prefix = tk.StringVar()
        self.number = tk.StringVar()
        self.address_tag = tk.StringVar()

        self.error = tk.StringVar()

        tk.Label(self, text="Nombre:").grid(row=0, column=0)
        Letters(self, self.name_tag).grid(row=0, column=1, columnspan=12, ipadx=15, padx=10)
        tk.Label(self, text="Apellido:").grid(row=1, column=0)
        Letters(self, self.lastname_tag).grid(row=1, column=1, columnspan=12, ipadx=15, padx=10)
        tk.Label(self, text="DNI:", justify="left").grid(row=2, column=0)
        Digits(self, self.dni_tag).grid(row=2, column=1, columnspan=12, ipadx=15, padx=10)
        tk.Label(self, text="Contraseña:").grid(row=3, column=0)
        tk.Entry(self, textvariable=self.pass_tag).grid(row=3, column=1, columnspan=5, ipadx=15, padx=10)
        tk.Label(self, text="Telefono:").grid(row=4, column=0)
        tk.Label(self, text="+54", width=3).grid(row=4, column=1, columnspan=1)
        Digits(self, self.prefix, width=4).grid(row=4, column=2)
        tk.Label(self, text="-").grid(row=4, column=3)
        Digits(self, self.number, width=6).grid(row=4, column=4)
    
        tk.Label(self, text="Direccion:").grid(row=5, column=0)
        tk.Entry(self, textvariable=self.address_tag).grid(row=5, column=1, columnspan=12, ipadx=15, padx=10)
        
        tk.Label(self, textvariable=self.error).grid(row=6, column=0, columnspan=13)

        tk.Button(self, text="Atras", command=lambda: controller.show_frame("Login")).grid(row=7, column=1, pady=20)
        tk.Button(self, text="Continuar", command=lambda: self.validate(), width=6).grid(row=7, column=2, columnspan=3)

        self.name_tag.trace("w", lambda *args: limitador(self.name_tag, 20))
        self.lastname_tag.trace("w", lambda *args: limitador(self.lastname_tag, 20))
        self.dni_tag.trace("w", lambda *args: limitador(self.dni_tag, 8))
        self.pass_tag.trace("w", lambda *args: limitador(self.pass_tag, 20))
        self.prefix.trace("w", lambda *args: limitador(self.prefix, 4))
        self.number.trace("w", lambda *args: limitador(self.number, 6))
        self.address_tag.trace("w", lambda *args: limitador(self.address_tag, 30))


        def limitador(widget, n):
            if len(widget.get()) > 0:
                #Limita la cantidad a n caracteres
                widget.set(widget.get()[:n])

    def validate(self):
        name=self.name_tag.get()
        lastname=self.lastname_tag.get()
        dni=self.dni_tag.get()
        passwd=self.pass_tag.get()
        prefix=self.prefix.get()
        number=self.number.get()
        address=self.address_tag.get()
        
        error=["Error \n"]

        if not name.isalpha(): error.append("- El nombre no puede contener numeros\n")
        if not lastname.isalpha(): error.append("- El Appelido no puede contener numeros\n")
        if dni.isnumeric(): 
            if len(dni) != 8: error.append("- El Dni debe tener 8 digitos\n")
        else: error.append("- El Dni no puede contener letras\n")
        if not prefix.isnumeric(): error.append("- El Prefijo Telefonico no puede contener letras\n")
        if not number.isnumeric(): error.append("- El Numero Telefonico es invalido\n")
        if not address.isalnum(): error.append("- La direccion solo debe contener lestras y numeros\n")
    
        if len(passwd) < 6: error.append("- La contraseña debe tener al menos 6 caracteres\n")
        if len(passwd) > 20: error.append("- La contraseña no puede tener mas de 20 caracteres\n")
        if not any(char.isdigit() for char in passwd): error.append("- La contraseña debe tener almenos un numero\n")
        if not any(char.isupper() for char in passwd): error.append("- La contraseña debe tener almenos una MAYUSCULA\n")
        if not any(char.islower() for char in passwd): error.append("- La contraseña debe tener almenos una minuscula\n")    

        self.error.set("")        
        for e in error:
            val1= self.error.get()
            val2= str(e)
            string=val1 + val2
            self.error.set(string)


        #self.controller.db_check()
        
class Letters(tk.Entry):
    def __init__(self, master=None, var=None, **kwargs):
        self.var = var
        #self.var = tk.StringVar()
        tk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.old_value = ''
        self.var.trace('w', self.check)
        self.get, self.set = self.var.get, self.var.set
        
        #self.bind("<BackSpace>", lambda _: self.reset(self.old_value))
    '''
    def reset(self, old_value):
        print(old_value)
        print(len(old_value))
        if len(old_value)==1:
            self.set=('')
    '''
    def check(self, *args):
        
        if len(self.old_value)== 1 and self.bind("<BackSpace>", lambda _: True):
            self.set=('')
        else:
            if self.get().isalpha(): 
                # the current value is only digits; allow this
                    self.old_value = self.get()
            else:
                # there's non-digit characters in the input; reject this 
                self.set(self.old_value)
        
    
        
        
    

class Digits(tk.Entry):
    def __init__(self, master=None, var=None, **kwargs):
        self.var = var
        #self.var = tk.StringVar()
        tk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.old_value = ''
        self.var.trace('w', self.check)
        self.get, self.set = self.var.get, self.var.set

    def check(self, *args):
        if self.get().isdigit(): 
            # the current value is only digits; allow this
            self.old_value = self.get()
        else:
            # there's non-digit characters in the input; reject this 
            self.set(self.old_value)


def main():
    app=App("Gestion de Pedidos para Restaurante", "database.db")
    gui = GUI(app)
    gui.mainloop()
    return 0

if __name__ == '__main__':
    main()
