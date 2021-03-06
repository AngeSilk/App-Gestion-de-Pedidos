import tkinter as tk
from tkinter import *
from users import Client
from appV1 import *

#Ventana Principal
class GUI(tk.Tk):

    def __init__(self, app:App):
        tk.Tk.__init__(self) 
        
        self.__app = app
        self.title(app.name)

        self.__user_name=StringVar()

        master = tk.Frame(self)
        master.pack(side="top", fill="both", expand=True)
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        
        ancho_ventana = 400
        alto_ventana = 400

        x_ventana = self.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = self.winfo_screenheight() // 2 - alto_ventana // 2

        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        self.geometry(posicion)

        #self.resizable(0,0)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
       
        #self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.frames = {}
        
        for F in (StartPage, Login, Register, AdminEnter, WorkerEnter, HomeAdmin, 
                HomeDelivery, HomeKitcken, HomeClient, HomeGuest, JoinOrder, Menu, ShowProducts):
            page_name = F.__name__
            frame = F(parent=master, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("StartPage")

    @property
    def app(self):
        return self.__app

    @property
    def user_name(self):
        self.__user_name.set(f'Bienvenido, {self.app.user.name}')
        return self.__user_name

    def on_closing(self):
        d = Closer(self)
        self.wait_window(d.top)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def forguet_password(self):
        print("Opcion no programada")
        pass
    
    def update_products(self):
        self.app.get_products()  

    def share(self):
        pass
    
    def set_mode(self, mode):
        self.app.set_user(mode)
        self.user_name

    def back(self, frame):
        if isinstance(frame, ShowProducts):
            if isinstance(self.app.user, Admin):
                self.show_frame("HomeAdmin")
            if isinstance(self.app.user, Client):
                self.show_frame("HomeClient")
            if isinstance(self.app.user, Worker):
                self.show_frame("HomeWorker")
    
#Ventanas que se mostraran

class Closer:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.parent = parent
        
        ancho_ventana = 235
        alto_ventana = 70

        x_ventana = self.top.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = self.top.winfo_screenheight() // 2 - alto_ventana // 2
        
        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        self.top.geometry(posicion)
        self.top.title("Salir")
    
        tk.Label(self.top, text="??Est?? seguro?").grid(row=0, column=0, columnspan=2)

        self.button1 = tk.Button(self.top, text="Si, salir de la app.", command=self.salir)
        self.button2 = tk.Button(self.top, text="No, solo minimizar.", command=self.minimizar)
        self.button1.grid(row=1, column=0, padx=5, pady=5)
        self.button2.grid(row=1, column=1, padx=5, pady=5)

    def salir(self):
        print("Gracias por usar nuestro programa. SILTECK")
        self.top.destroy()
        self.parent.destroy()

    def minimizar(self):
        self.top.destroy()
        self.parent.iconify()

class StartPage(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent, pady=10, text="Inicio")
        
        self.controller = controller
        #label = tk.Label(self, text="This is the start page", font=controller.title_font)
        #label.pack(side="top", fill="x", pady=10)
        
        tk.Button(self, text="Ingresar", command=lambda: controller.show_frame("Login"), height=5, width=40).pack(padx=10)
        tk.Button(self, text="Unirme a un Pedido", command=lambda: controller.show_frame("JoinOrder"), height=5, width=40).pack()
        tk.Button(self, text="Salir", command=lambda: controller.on_closing(), height=3, width=10).pack(pady=20)

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
        tk.Label(self, text="Contrase??a:").grid(row=3, column=0)
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

            if controller.app.db_check(client):
                controller.show_frame("Login")
                print("Registrado con exito")
            else:
                self.error.set("Error: \n\n El ususario ya est?? registrado")

class Login(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent)

        tk.Label(self).pack(fill="x")

        frm2=tk.LabelFrame(self, pady=20, padx=90, text="Iniciar Sesion")
        frm2.pack(pady=10)
        self.controller = controller
        #self.parent = parent
        self.dni = StringVar()
        self.passwd= StringVar()
        
        frm1=Label(frm2)
        frm1.pack()
        tk.Label(frm1, text="DNI:").grid(row=0, column=0)
        Digits(frm1, self.dni).grid(row=0, column=1)
        tk.Label(frm1, text="Contrase??a:", pady=10).grid(row=1, column=0)
        tk.Entry(frm1, show="*", textvariable=self.passwd).grid(row=1, column=1)
        tk.Button(frm1, text="Olvid?? la contrase??a", command=lambda: controller.forguet_password()).grid(row=2, column=1)
        tk.Label(frm1, text="").grid(row=3, column=2)
        tk.Button(frm1, text="Ingresar", command=lambda: self.validate(self.controller), width=10, pady=5).grid(row=4, column=1)
        #tk.Label(frm1, text="").grid(row=5, column=0)
        frm4=Label(self)
        frm4.pack(fill="x")
        tk.Button(frm4, text="Atras", command=lambda: controller.show_frame("StartPage"), width=20, pady=8).grid(column=2, row=0, padx=20, pady=15)
        tk.Button(frm4, text="Registrarme", command=lambda: controller.show_frame("Register"),width=20, pady=8).grid(column=4, row=0, padx=25, pady=15)
        
        frm3=Label(self)
        frm3.pack(fill="x")
        self.errorframe=tk.LabelFrame(frm3, text="Error")
        tk.Label(self.errorframe, text="Los datos NO coinciden con un usuario registrado", fg="red").pack(fill="both", pady=10)

        self.dni.trace("w", lambda *args: Limiter(self.dni, 8))

        self.bind_all("<Button-1>", lambda e: self.focus())

    def validate(self, controller:GUI):

        #self.errorframe.grid_remove()
        dni=self.dni.get() #Se obtienen los valores ingresados en el campo de dni
        passwd=self.passwd.get() 
        
        self.dni.set("")
        self.passwd.set("")
        
        user=User(dni, passwd) #Se instancia un objeto del tipo user
        
        if controller.app.db_check(user):
            user=controller.app.user
            if user.role == 0:
                controller.show_frame("AdminEnter")
            if user.role == 2:
                controller.show_frame("WorkerEnter")
            if user.role == 1:
                controller.show_frame("HomeClient")
        else:
            self.errorframe.pack(fill="x")
            print("Fallo el inicio de sesion")

    def focus(self):
        self.errorframe.pack_forget()
       
class AdminEnter(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent, pady=20, padx=10)
        self["text"]="Ingresar como"
        self.controller = controller

        tk.Button(self, text="Administrador", command=lambda: [controller.show_frame("HomeAdmin"), controller.set_mode("Admin")], height=5).pack(fill="x")
        tk.Button(self, text="Cliente", command=lambda: [controller.show_frame("HomeClient"), controller.set_mode("Client")], height=5).pack(fill="x")
        tk.Button(self, text="Atras", command=lambda: controller.show_frame("Login"), height=3, width=10).pack(pady=20)

class WorkerEnter(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent, pady=10, padx=10)
        self["text"]="Ingresar como"
        self.controller = controller

        tk.Button(self, text="Trabajador", command=lambda: controller.set_mode("Worker"), height=5).pack(fill="both")
        tk.Button(self, text="Cliente", command=lambda: [controller.show_frame("HomeClient"), controller.set_mode("Client")], height=5).pack(fill="both")
        tk.Button(self, text="Atras", command=lambda: controller.show_frame("Login"), height=3, width=10).pack(pady=20)

class HomeAdmin(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent, text="Administrador")
        self.controller = controller
        
        #self.__client_name=StringVar()
        
        tk.Label(self,justify='right', textvariable=controller.user_name, pady=10).pack(fill="x")

        #Pedidos
        self.labelframe1=tk.LabelFrame(self, text="Pedidos")
        tk.Button(self.labelframe1,text="Recientes",justify='center', width=20, pady=8).grid(column=2, row=0, padx=20, pady=15)
        tk.Button(self.labelframe1, text="Ver Historial",justify='center',width=20, pady=8).grid(column=4, row=0, padx=25, pady=15)
        self.labelframe1.pack(fill="both")
        
        #Productos
        self.labelframe2=tk.LabelFrame(self, text="Productos")
        tk.Button(self.labelframe2,text="Mostrar",justify='center', command=lambda: [controller.update_products(),controller.show_frame("ShowProducts")], width=20, pady=8).grid(column=2, row=0, padx=20, pady=15)
        tk.Button(self.labelframe2, text="Modificar",justify='center',width=20, pady=8).grid(column=4, row=0, padx=25, pady=15)
        self.labelframe2.pack(fill="both")
        
        #Clientes
        self.labelframe3=tk.LabelFrame(self, text="Clientes")

        self.labelframe3.pack(fill="both")
        
        #Trabajadores
        self.labelframe4=tk.LabelFrame(self, text="Trabajadores")
    
        self.labelframe4.pack(fill="both")
        
        tk.Button(self, text="Atras", command=lambda: controller.show_frame("Login"), height=3, width=10).pack(pady=20)

class HomeClient(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent, text="Cliente")
        self.controller = controller
        
        tk.Label(self,justify='right', textvariable=controller.user_name, pady=10).pack(fill="x")

        #Menu
        self.labelframe1=tk.LabelFrame(self, text="Menu")
        tk.Button(self.labelframe1,text="Mostrar",command=lambda: [controller.update_products(), controller.show_frame("ShowProducts")],justify='center', width=20, pady=8).grid(column=2, row=0, padx=20, pady=15)
        self.labelframe1.pack(fill="both")

        #Pedidos
        self.labelframe1=tk.LabelFrame(self, text="Pedidos")
        tk.Button(self.labelframe1,text="Nuevo", command=lambda: [controller.update_products(), controller.show_frame()], justify='center', width=20, pady=8).grid(column=2, row=0, padx=20, pady=15)
        tk.Button(self.labelframe1, text="Ver Historial",justify='center',width=20, pady=8).grid(column=4, row=0, padx=25, pady=15)
        self.labelframe1.pack(fill="both")

        #Usuario
        self.labelframe2=tk.LabelFrame(self, text="Configuracion")
        tk.Button(self.labelframe2,text="Modificar mis datos", justify='center', width=30, pady=8).grid(column=2, row=0, padx=40, pady=15)
        #tk.Button(self.labelframe2, text="Ver Historial",justify='center',width=20, pady=8).grid(column=4, row=0, padx=25, pady=15)
        self.labelframe2.pack(fill="both")
        
        #Control
        frm2=Label(self)
        Button(frm2, text="Salir", command=lambda: controller.on_closing() ,justify='center', width=20, pady=8).grid(column=2, row=0, padx=20, pady=15)
        Button(frm2, text="Atras", command=lambda: controller.show_frame("Login"), justify='center',width=20, pady=8).grid(column=4, row=0, padx=25, pady=15)
        frm2.pack()

class HomeDelivery(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent)
        frm0=tk.LabelFrame(self, parent, pady=10, padx=10, text="Delivery")
        frm0.pack()
        self.controller = controller

        #Opciones de un delivery

        #Control
        frm_control=Label(self)
        Button(frm_control, text="Salir", command=lambda: controller.on_closing() ,justify='center', width=20, pady=8).grid(column=2, row=0, padx=20, pady=15)
        Button(frm_control, text="Atras", command=lambda: controller.show_frame("Login"), justify='center',width=20, pady=8).grid(column=4, row=0, padx=25, pady=15)
        frm_control.pack()

class HomeKitcken(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent)
        frm0=tk.LabelFrame(self, parent, pady=10, padx=10, text="Cocina")
        frm0.pack()
        self.controller = controller

        #Opciones de la cocina

        #Control
        frm_control=Label(self)
        Button(frm_control, text="Salir", command=lambda: controller.on_closing() ,justify='center', width=20, pady=8).grid(column=2, row=0, padx=20, pady=15)
        Button(frm_control, text="Atras", command=lambda: controller.show_frame("Login"), justify='center',width=20, pady=8).grid(column=4, row=0, padx=25, pady=15)
        frm_control.pack()
    
class HomeGuest(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent, pady=10, padx=10, text="Invitadi")
        #self.__controller = controller
        tk.Label(self,justify='right', textvariable=controller.user_name, pady=10).pack(fill="x")

class JoinOrder(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent, pady=40, padx=100)
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

        if controller.app.db_check(guest):
            controller.show_frame("HomeGuest")
        else:
            print("No se encont?? usuario con ese codigo")

class Menu(tk.Label):
    def __init__(self, parent, controller:GUI):
        tk.Label.__init__(self, parent)

        self.__products=[]
        self.__amount=StringVar()
        
        frm0=Label(self, text="Realizar un Pedido", font=("Bahnschrift", 15), pady=10)
        frm0.pack()
        frm1 = LabelFrame(frm0, text="Menu", pady=10, padx=20, font=("Courrier", 10))
        frm1.pack()
        
        self.__products=controller.app.product
        self.__amount.set("$0")
        a=[]
        e=[]
        Label(frm1, text="Variedades", justify=LEFT, font=("Bahnschrift", 10)).grid(column=1, row=0)
        Label(frm1, text="Precio      \nUnitario      ", justify="center", font=("Bahnschrift", 10)).grid(column=2, row=0)
        Label(frm1, text="Cant.", font=("Bahnschrift", 10)).grid(column=3, row=0)
        for i in range(len(self.__products)):
            Label(frm1, text=f"     {self.__products[i][1]}     ", font=("Bahnschrift", 14)).grid(column=1, row=i+1)
            Label(frm1, text=f"${self.__products[i][2]}   ", font=("Bahnschrift", 14)).grid(column=2, row=i+1)
            e.append(StringVar())
            a.append(Spinbox(frm1, textvariable=e[i], from_=0, to=48, width=5, command=lambda i=i: change(i)))
            a[i].grid(column=3, row=i+1)
        
        frm3=LabelFrame(frm0, text="Total a Pagar", pady=5, padx=5)
        Label(frm3, textvariable=self.__amount, font=("Bahnschrift", 15), width=20).grid(column=2,row=i+2)
        frm3.pack()
        
        frm2=LabelFrame(frm0, text="Acciones", pady=10)
        frm2.pack()

        Button(frm2, text="Volver Atras", command=lambda: [controller.show_frame("HomeClient"), reset()], width=10).grid(column=0, row=0, padx=4)
        Button(frm2, text="Compartir", command=lambda: [controller.share()], width=10).grid(column=1, row=0, padx=4)
        Button(frm2, text="Continuar", command=lambda: take_order(), width=10).grid(column=2, row=0, padx=4)
    

        def change(i):
            total=0
            cants=0
            for i in range(len(self.__products)):
                subtotal=0
                price=int(self.__products[i][2])
                cant=int(a[i].get())
                cants+=cant
                subtotal=price*cant
                total+=subtotal
            self.__amount.set(f'${total}')
        
        def reset():
            self.__amount.set("$0")
            for i in range(len(e)):
                e[i].set(0)

class ShowProducts(tk.Label):
    
    def __init__(self, parent, controller:GUI):
        tk.Label.__init__(self, parent)
        #frm0=Label(self)
        self.__products=[]
        self.__products=controller.app.product
        
        frm1 = LabelFrame(self, text="Productos", pady=10, padx=20, font=("Courrier", 10))
        frm1.pack()
        
        Label(frm1, text="Variedades", justify=LEFT, font=("Bahnschrift", 10)).grid(column=1, row=0)
        Label(frm1, text="Precio      \nUnitario      ", justify="center", font=("Bahnschrift", 10)).grid(column=2, row=0)
        for i in range(len(self.__products)):
            Label(frm1, text=f"     {self.__products[i][1]}     ", font=("Bahnschrift", 14)).grid(column=1, row=i+1)
            Label(frm1, text=f"${self.__products[i][2]}   ", font=("Bahnschrift", 14)).grid(column=2, row=i+1)
        frm2 = Label(self)
        frm2.pack()
        Button(frm2, text="Volver Atras", command=lambda: controller.back(self), width=10).pack()

''' 
class EnterAs(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent, pady=10, padx=10)
        self["text"]="Ingresar Como"
        self.controller = controller
        self.__user=controller.app.user

    def chose(self):
        print(self.__user.role)
        if self.__user.role == 0:
            print("Roll = Administrador")
            tk.Button(self, text="Administrador", command=lambda: controller.show_frame("AdminEnter"), height=5).pack(fill="both")
            tk.Button(self, text="Cliente", command=lambda: controller.show_frame("HomeClient"), height=5).pack(fill="both")
            #controller.show_frame("AdminEnter")
        if self.__user.role == 1:
            print("Roll = Cliente")
            controller.show_frame("HomeClient")
        if self.__user.role == 2:
            print("Roll = Trabajador")
            tk.Button(self, text="Trabajador", command=lambda: controller.show_frame("WorkerEnter"), height=5).pack(fill="both")
            tk.Button(self, text="Cliente", command=lambda: controller.show_frame("HomeClient"), height=5).pack(fill="both")
'''

#Limitadores

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
    
        if len(passwd) < 6: error.append("- La contrase??a debe tener al menos 6 caracteres\n")
        if len(passwd) > 20: error.append("- La contrase??a no puede tener mas de 20 caracteres\n")
        if not any(char.isdigit() for char in passwd): error.append("- La contrase??a debe tener almenos un numero\n")
        if not any(char.isupper() for char in passwd): error.append("- La contrase??a debe tener almenos una MAYUSCULA\n")
        if not any(char.islower() for char in passwd): error.append("- La contrase??a debe tener almenos una minuscula\n")    

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
