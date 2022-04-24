import tkinter as tk
from tkinter import *
from users import Client
from appV1 import *

class GUI(tk.Tk):

    def __init__(self, app:App):
        tk.Tk.__init__(self) 
        
        self.app = app
        self.title(app.name)

        master = tk.Frame(self)
        master.pack(side="top", fill="both", expand=True)
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
       
        #self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.frames = {}
        
        for F in (StartPage, Login, JoinOrder, Register, HomeGuest, EnterAs, AdminLogin):
            page_name = F.__name__
            frame = F(parent=master, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("StartPage")

    def on_closing(self):
        print("Chau puto")
        d = Closer(self)
        self.wait_window(d.top)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
    
    def db_check(self, object:object):
        
        if isinstance(object, Client):
            if self.app.addClient(object): return True
            else: return False
        
        if isinstance(object, Guest):
            
            order_id = self.app.enable_Guest(object)
            if  order_id != False: return True
            else: return False

        if isinstance(object, User):
            
            info = self.app.validate_user(object)
            if info:
                #id=info[0]
                #rolle=info[1]
                return info
            else: return False

    def run_app(self, info, user:User):
        
        role=info[0]
        user=info[1]

        if role == 0:
            self.app.run(user)
        if role == 1:
            pass

    def forguet_password(self):
        print("Sos un boludo")
        pass

class Closer:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.parent = parent
        self.top.title("Salir")

        tk.Label(self.top, text="¿Está seguro?").grid(row=0, column=0, columnspan=2)

        self.button1 = tk.Button(self.top, text="Si, salir de la app.", command=self.salir)
        self.button2 = tk.Button(self.top, text="No, solo minimizar.", command=self.minimizar)
        self.button1.grid(row=1, column=0, padx=5, pady=5)
        self.button2.grid(row=1, column=1, padx=5, pady=5)

    def salir(self):
        self.top.destroy()
        self.parent.destroy()

    def minimizar(self):
        self.top.destroy()
        self.parent.iconify()

class StartPage(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent, pady=10)
        self["text"]="Inicio"
        self.controller = controller
        #label = tk.Label(self, text="This is the start page", font=controller.title_font)
        #label.pack(side="top", fill="x", pady=10)
        
        tk.Button(self, text="Ingresar", command=lambda: controller.show_frame("Login"), height=5).pack(fill="both")
        tk.Button(self, text="Unirme a un Pedido", command=lambda: controller.show_frame("JoinOrder"), height=5).pack(fill="both")

class Login(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent, pady=20, padx=10)
        self["text"]="Iniciar Sesion"
        self.controller = controller
        
        self.dni = StringVar()
        self.passwd= StringVar()

        tk.Label(self, text="DNI:").grid(row=0, column=0)
        Digits(self, self.dni).grid(row=0, column=1)
        tk.Label(self, text="Contraseña:", pady=10).grid(row=1, column=0)
        tk.Entry(self, show="*", textvariable=self.passwd).grid(row=1, column=1)
        tk.Button(self, text="Olvidé la contraseña", command=lambda: controller.forguet_password()).grid(row=2, column=1)
        tk.Label(self, text="").grid(row=3, column=2)
        tk.Button(self, text="Ingresar", command=lambda: self.validate(self.controller)).grid(row=4, column=1)
        tk.Label(self, text="").grid(row=5, column=0)
        tk.Button(self, text="Atras", command=lambda: controller.show_frame("StartPage")).grid(row=6, column=0)
        tk.Button(self, text="Registrarme", command=lambda: controller.show_frame("Register")).grid(row=6, column=1)

        self.dni.trace("w", lambda *args: Limiter(self.dni, 8))

    def validate(self, controller:GUI):

        dni=self.dni.get()
        passwd=self.passwd.get()

        user=User("","",dni, passwd,"")
        
        info=controller.db_check(user)

        if info:
            controller.run_app(info)
            controller.show_frame("EnterAs")
            user_id=info[0]
            user_role=info[1]
            '''
            if user_role == 0:
                print("Roll = Administrador")
                controller.show_frame("AdminEnter")
            if user_role == 1:
                print("Roll = Cliente")
                controller.show_frame("HomeClient")
            if user_role == 2:
                print("Roll = Trabajador")
                controller.show_frame("WorkerEnter")
            '''
        else:
                print("Fallo el inicio de sesion")
                
class JoinOrder(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent, pady=20)
        self["text"]="Ingresar como invitado"
        
        self.controller = controller
        
        self.nick_tag=StringVar()
        self.code=StringVar()

        tk.Label(self, text="Nombre:").grid(row=0, column=1)
        tk.Entry(self).grid(row=0, column=2, columnspan=2)
        tk.Label(self, text="Codigo:").grid(row=1, column=1)
        Digits(self, self.code).grid(row=1, column=2, columnspan=2)
        tk.Label(self, text=" ").grid(row=4, column=0, columnspan=5)
        tk.Button(self, text="Atras", command=lambda: controller.show_frame("StartPage")).grid(row=5, column=2)
        tk.Button(self, text="Continuar", command=lambda: self.validate(self.controller)).grid(row=5, column=3)

    def validate(self, controller:GUI):

        nick=self.nick_tag.get()
        code=self.code.get()

        guest = Guest(nick, code)

        if controller.db_check(guest):
            controller.show_frame("HomeGuest")
        else:
            print("No se encontó usuario con ese codigo")

class Register(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
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
        
        tk.Label(self, textvariable=self.error, pady=10).grid(row=6, column=0, columnspan=13)

        tk.Button(self, text="Atras", command=lambda: controller.show_frame("Login")).grid(row=7, column=1, pady=20)
        tk.Button(self, text="Continuar", command=lambda: self.validate(self.controller), width=6).grid(row=7, column=2, columnspan=3)

        self.name_tag.trace("w", lambda *args: Limiter(self.name_tag, 20))
        self.lastname_tag.trace("w", lambda *args: Limiter(self.lastname_tag, 20))
        self.dni_tag.trace("w", lambda *args: Limiter(self.dni_tag, 8))
        self.pass_tag.trace("w", lambda *args: Limiter(self.pass_tag, 20))
        self.prefix.trace("w", lambda *args: Limiter(self.prefix, 4))
        self.number.trace("w", lambda *args: Limiter(self.number, 6))
        self.address_tag.trace("w", lambda *args: limitador(self.address_tag, 30))

        def limitador(widget:StringVar, n):
            if len(widget.get()) > 0:
                #Limita la cantidad a n caracteres
                widget.set(widget.get()[:n])
    
    def validate(self, controller:GUI):
            name=self.name_tag.get()
            lastname=self.lastname_tag.get()
            dni=self.dni_tag.get()
            passwd=self.pass_tag.get()
            prefix=self.prefix.get()
            number=self.number.get()
            address=self.address_tag.get()

            phone=prefix+number

            client = Client(name, lastname, dni, passwd, phone, address)

            if controller.db_check(client):
                controller.show_frame("")
                print("Registrado con exito")
            else:
                self.error.set("Error: \n\n El ususario ya está registrado")
        
class HomeGuest(tk.LabelFrame):
    def __init__(self, parent, controller):
        tk.LabelFrame.__init__(self, parent, pady=10, padx=10)
        self["text"]="Bienvenido"

class EnterAs(tk.LabelFrame):
    def __init__(self, parent, controller:GUI, user:object):
        tk.LabelFrame.__init__(self, parent, pady=10, padx=10)
        self["text"]="Ingresar Como"
        self.controller = controller
        
        tk.Button(self, text="Administrador", command=lambda: controller.run_app(), height=5).pack(fill="both")
        tk.Button(self, text="Cliente", command=lambda: controller.show_frame("WorkerEnter"), height=5).pack(fill="both")
     
class AdminLogin(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent, pady=10, padx=10)
        self["text"]="Pantalla Administrador"
        self.controller = controller

class Limiter:

    def __init__(self, widget:StringVar, n:int) -> None:
        self.__widget = widget
    
        if len(self.__widget.get()) > 0:
                    #Limita la cantidad a n caracteres
                    self.__widget.set(self.__widget.get()[:n])

        '''
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
        '''
    
class Letters(tk.Entry):
    def __init__(self, master=None, var=None, **kwargs):
        self.var = var
        #self.var = tk.StringVar()
        tk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.old_value = ''
        self.var.trace('w', self.check)
        self.get, self.set = self.var.get, self.var.set
        
      
        #self.bind("<BackSpace>", lambda _: self.reset(self.old_value))
    def check(self, *args):
        
        if len(self.old_value)== 1 and self.bind("<BackSpace>", lambda _: True):
            self.old_value=('')
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
    
        if len(self.old_value)== 1 and self.bind("<BackSpace>", lambda _: True):
            self.old_value=('')
        else:
            if self.get().isdigit(): 
                # the current value is only digits; allow this
                    self.old_value = self.get()
            else:
                # there's non-digit characters in the input; reject this 
                self.set(self.old_value)
    '''
    def reset(self, old_value):
        print(old_value)
        print(len(old_value))
        if len(old_value)==1:
            self.set=('')
    '''

def main():
    app=App("Gestion de Pedidos para Restaurante", "database.db")
    gui = GUI(app)
    gui.mainloop()
    return 0

if __name__ == '__main__':
    main()
