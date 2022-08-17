import tkinter as tk
from tkinter import *
from users import Client
from appV1 import *
from PIL import ImageTk, Image
from datetime import datetime
import math

#Ventana Principaldeta
class GUI(tk.Tk):

    def __init__(self, app:App):
        tk.Tk.__init__(self)

        self.__app = app
        self.title(app.name)

        self.__barcode = self.update_barcode()

        self.__n_order = StringVar()
        self.__user_name = StringVar()

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

        self.states=("Cancelado","Pendiente","Procesando","Enviado","Completado")

        self.frames = {}

        self.pages = (StartPage,
                Login, Register,
                AdminEnter, WorkerEnter,
                HomeAdmin, HomeDelivery, Kitchen, HomeClient, HomeGuest,
                JoinOrder, Menu, ShowProducts, Share, ShowOrder, ShowDetail,OrderState)

        for F in self.pages:
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

    @property
    def n_order(self):
        self.__n_order.set(f'Orden N° {self.app.order.id}')
        return self.__n_order

    @property
    def barcode(self):
        return(self.__barcode)

    @property
    def update(self):
       self.pages[14].update

    @barcode.setter
    def barcode(self, barcode):
        self.__barcode = barcode

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

    def update_barcode(self):
        img = Image.open('barcode.png')
        self.barcode = ImageTk.PhotoImage(img)
        return self.barcode

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

        if isinstance(frame, Share):
            pass

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

        tk.Label(self.top, text="¿Está seguro?").grid(row=0, column=0, columnspan=2)

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

            if controller.app.db_check(client):
                controller.show_frame("Login")
                print("Registrado con exito")
            else:
                self.error.set("Error: \n\n El ususario ya está registrado")

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
        tk.Label(frm1, text="Contraseña:", pady=10).grid(row=1, column=0)
        tk.Entry(frm1, show="*", textvariable=self.passwd).grid(row=1, column=1)
        tk.Button(frm1, text="Olvidé la contraseña", command=lambda: controller.forguet_password()).grid(row=2, column=1)
        tk.Label(frm1, text="").grid(row=3, column=2)
        tk.Button(frm1, text="Ingresar", command=lambda: self.validate(self.controller), width=10, pady=5).grid(row=4, column=1)
        #tk.Label(frm1, text="").grid(row=5, column=0)
        frm4=Label(self)
        frm4.pack(fill="x")
        tk.Button(frm4, text="Atras", command=lambda: controller.show_frame("StartPage"), width=20, pady=8).grid(column=2, row=0, padx=20, pady=15)
        tk.Button(frm4, text="Registrarme", command=lambda: controller.show_frame("Register"),width=20, pady=8).grid(column=4, row=0, padx=25, pady=15)

        self.frm3=Label(self)
        self.errorframe=tk.LabelFrame(self.frm3, text="Error")
        self.errorframe.pack(fill="x")
        tk.Label(self.errorframe, text="Los datos NO coinciden con un usuario registrado", fg="red").pack(fill="both", pady=10)

        self.bind("<Button-1>", lambda e: self.focus())

        self.dni.trace("w", lambda *args: Limiter(self.dni, 8))

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
                controller.set_mode("Client")
                controller.show_frame("HomeClient")
        else:
            self.frm3.pack(fill="x")
            print("Fallo el inicio de sesion")

    def focus(self):
        self.frm3.pack_forget()

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

        tk.Button(self, text="Trabajador", command=lambda: self.worker(), height=5).pack(fill="both")
        tk.Button(self, text="Cliente", command=lambda: [controller.show_frame("HomeClient"), controller.set_mode("Client")], height=5).pack(fill="both")
        tk.Button(self, text="Atras", command=lambda: controller.show_frame("Login"), height=3, width=10).pack(pady=20)

    def worker(self):
        self.controller.set_mode("Worker")
        worker:Worker = self.controller.app.user
        if worker.place =="Kitchen":
            self.controller.show_frame("Kitchen")
        if worker.place == "Delivery":
            self.controller.show_frame("Delivery")

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
        tk.Button(self.labelframe1,text="Mostrar",command=lambda: self.show_prodcuts() ,anchor='center', width=30, pady=8).grid(column=4, row=0, columnspan=2, padx=85, pady=15)
        self.labelframe1.pack(fill="both")

        #Pedidos
        self.labelframe1=tk.LabelFrame(self, text="Pedidos")
        tk.Button(self.labelframe1,text="Nuevo", command=lambda: [controller.update_products(), self.new_order()], justify='center', width=20, pady=8).grid(column=2, row=0, padx=20, pady=15)
        tk.Button(self.labelframe1, text="Ver Historial",justify='center',width=20, pady=8).grid(column=4, row=0, padx=25, pady=15)
        self.labelframe1.pack(fill="both")

        #Usuario
        self.labelframe2=tk.LabelFrame(self, text="Configuracion")
        tk.Button(self.labelframe2,text="Modificar mis datos", justify='center', width=30, pady=8).grid(column=2, row=0, padx=40, pady=15)
        self.labelframe2.pack(fill="both")

        #Control
        frm2=Label(self)
        Button(frm2, text="Salir", command=lambda: controller.on_closing() ,justify='center', width=20, pady=8).grid(column=2, row=0, padx=20, pady=15)
        Button(frm2, text="Atras", command=lambda: controller.show_frame("Login"), justify='center',width=20, pady=8).grid(column=4, row=0, padx=25, pady=15)
        frm2.pack()

    def show_prodcuts(self):
        self.controller.update_products()
        self.controller.show_frame("ShowProducts")

    def new_order(self):
        self.top = tk.Toplevel(self.controller)

        ancho_ventana = 235
        alto_ventana = 70

        x_ventana = self.top.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = self.top.winfo_screenheight() // 2 - alto_ventana // 2

        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        self.top.geometry(posicion)
        self.top.title("Nuevo Pedido")

        tk.Label(self.top, text="Realizar un nuevo pedido?").grid(row=0, column=0, columnspan=2)

        self.button1 = tk.Button(self.top, text="Si, continuar.", command=lambda: keep())
        self.button2 = tk.Button(self.top, text="No, volver atras.", command=lambda: minimizar())
        self.button1.grid(row=1, column=0, padx=5, pady=5)
        self.button2.grid(row=1, column=1, padx=5, pady=5)

        def keep():
            self.top.destroy()
            self.controller.app.new_order()
            self.controller.n_order
            self.controller.update_barcode()
            self.controller.show_frame("Menu")

        def minimizar():
            self.top.destroy()

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
        tk.LabelFrame.__init__(self, parent, pady=10, padx=10, text="Invitado")
        #self.__controller = controller
        tk.Label(self,justify='right', textvariable=controller.user_name, pady=10).pack(fill="x")

class JoinOrder(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent, pady=40, padx=100)
        self["text"]="Ingresar como invitado"

        self.controller = controller

        self.nick_tag=StringVar()
        self.code=StringVar()
        self.letters=StringVar()
        self.digits=StringVar()

        frm1=tk.LabelFrame(self, text="Nombre")
        Letters(frm1, self.nick_tag, font=("", 15), width=15).grid(row=0, column=1, padx=10, pady=15)
        frm1.pack()

        frm5 = tk.Label(self)
        frm5.pack()

        frm2 = tk.LabelFrame(self, text="Codigo")
        Letters(frm2, self.letters, True, width=4, font=("Bahnschrift", 15)).grid(row=0, column=1, padx=5, pady=10)
        tk.Label(frm2, text="  -  ", font=("Bahnschrift", 15)).grid(row=0, column=2, padx=5, pady=10)
        Digits(frm2, self.digits, width=4, font=("Bahnschrift", 15)).grid(row=0, column=3, padx=5, pady=10)
        frm2.pack(pady=20)

        frm4 = tk.Label(self)
        frm4.pack()

        frm3 = tk.Label(self)
        tk.Button(frm3, text="Volver Atras", command=lambda: controller.show_frame("StartPage")).grid(row=0, column=2, padx=10)
        tk.Button(frm3, text="Continuar", command=lambda: self.validate()).grid(row=0, column=4, padx=10)
        frm3.pack(pady=10)

        self.errorframe1=tk.Label(frm5, text="El nombre ingresado ya esta en uso.\nPorfavor intente con otro.", fg="red")
        self.errorframe2=tk.Label(frm4, text="El codigo ingresado no es valido", fg="red")

        self.letters.trace("w", lambda *args: Limiter(self.letters, 3, True))
        self.digits.trace("w", lambda *args: Limiter(self.digits, 3))

        self.bind("<Button-1>", lambda e: focus())

        def focus():
            self.errorframe1.pack_forget()
            self.errorframe2.pack_forget()

    def validate(self):

        nick=self.nick_tag.get()
        nick = nick.capitalize()

        digits=self.digits.get()
        letters=self.letters.get()

        code = letters + '-' + digits

        if len(code) == 7:

            guest = Guest(nick, code)

            value = self.controller.app.db_check(guest)

            if value == 0:
                self.controller.app.user = guest
                self.controller.n_order
                self.controller.update_barcode()
                self.controller.show_frame("Menu")
            elif value == 1:
                self.errorframe1.pack()
                self.nick_tag.set(" ")
                print('Intente con otro nombre')
            else:
                print("No se encontó una orden valida")
                self.errorframe2.pack()
        else:
            self.errorframe2.pack()

class Menu(tk.LabelFrame):

    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent)
        self.controller = controller
        self.__detail={}
        self.__products=[]
        self.__amount=StringVar()

        tk.Label(self, textvariable=self.controller.n_order, font=("Bahnschrift", 15), justify='right', pady=10).pack()

        #Error

        self.errorframe=tk.Label(self, text="Para continuar aguegue almenos un producto a la orden", fg="red")

        frm1 = tk.LabelFrame(self, text="Menu", pady=10, padx=20, font=("Courrier", 10))
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

        #Total a Pagar
        frm3=LabelFrame(self, text="Total a Pagar", pady=5, padx=5)
        Label(frm3, textvariable=self.__amount, font=("Bahnschrift", 15), width=20).grid(column=2,row=i+2)
        frm3.pack()

        #Acciones
        frm2=LabelFrame(self, text="Acciones", pady=10)
        frm2.pack()

        #Control
        Button(frm2, text="Volver Atras", command=lambda: [controller.show_frame("HomeClient"), reset()], width=10).grid(column=0, row=0, padx=4)
        Button(frm2, text="Compartir", command=lambda: [controller.show_frame("Share"), controller.update_barcode()], width=10).grid(column=1, row=0, padx=4)
        Button(frm2, text="Continuar", command=lambda: take_order(), width=10).grid(column=2, row=0, padx=4)


        self.bind("<Button-1>", lambda e: focus())

        def focus():
            self.errorframe.pack_forget()

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

        def take_order():

            total_cant = 0

            for i in range(len(self.__products)):
                cant=int(a[i].get())
                total_cant = total_cant + cant
                price=int(self.__products[i][2])
                subtotal=price*cant
                id = self.__products[i][0]
                self.__detail[id] = (cant, subtotal)

            if total_cant != 0:
                self.controller.app.add_details(self.__detail)
                reset()
                self.controller.show_frame("ShowOrder")
            else:
                self.errorframe.pack(fill="x")
                print("No hay ordenes disponibles")

class ShowProducts(tk.Label):

    def __init__(self, parent, controller:GUI):
        tk.Label.__init__(self, parent)
        #frm0=Label(self)
        self.__products=[]
        self.__products=controller.app.product

        frm1 = LabelFrame(self, text="Menu", pady=10, padx=20, font=("Courrier", 10))
        frm1.pack(pady=30)

        Label(frm1, text="Variedades", justify=LEFT, font=("Bahnschrift", 10)).grid(column=1, row=0)
        Label(frm1, text="Precio      \nUnitario      ", justify="center", font=("Bahnschrift", 10)).grid(column=2, row=0)
        for i in range(len(self.__products)):
            Label(frm1, text=f"     {self.__products[i][1]}     ", font=("Bahnschrift", 14)).grid(column=1, row=i+1)
            Label(frm1, text=f"${self.__products[i][2]}   ", font=("Bahnschrift", 14)).grid(column=2, row=i+1)
        frm2 = Label(self)
        frm2.pack()
        Button(frm2, text="Volver Atras", command=lambda: controller.back(self), width=10).pack()

class Share(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent)

        self.controller = controller

        self.frm1 = LabelFrame(self, text="Compartir Orden", pady=10, padx=20, font=("Courrier", 10))
        self.frm1.pack()
        self.but1 = tk.Button(self.frm1, text="Compartir", command=lambda: self.change_img(), height=3, width=40)
        self.but1.pack()
        frm2 = Label(self)
        frm2.pack(pady=10)
        Button(frm2, text="Volver Atras", command=lambda: [controller.show_frame("Menu"), self.reset()], height = 2, width=20).pack()

    def change_img(self):
        self.but1.pack_forget()
        self.img_code=Label(self.frm1, image = self.controller.barcode)
        self.img_code.pack()

    def reset(self):
        self.img_code.pack_forget()
        self.but1.pack()

class ShowOrder(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.b1=[]
        self.b2=[]
        self.lbl1 = []
        self.lbl2 = []
        self.lbl3 = []

        self.__cont = 0

        self.__details=[('Hola', 500)]

        self.name = StringVar()
        self.__amount=StringVar()
        self.__amount.set("$0")


        tk.Label(self, textvariable=self.controller.n_order, font=("Bahnschrift", 15), justify='right', pady=10).pack()
        self.frm1 = tk.LabelFrame(self, text="Pedidos", pady=10, padx=20, font=("Courrier", 10))
        self.frm1.pack()

        frm3=LabelFrame(self, text="Total a Pagar", pady=5, padx=5)
        Label(frm3, textvariable=self.__amount, font=("Bahnschrift", 15), width=20).grid(column=2, row=self.cont+1)
        frm3.pack()

        frm2 = Label(self)
        frm2.pack(pady=20)

        #Control
        Button(frm2, text="Volver Atras", command=lambda: controller.show_frame("HomeClient"), width=15).grid(column=0, row=0, padx=4)

        if self.controller.app.order.state == 1:
            self.btn1=Button(frm2, text="Confirmar", command=lambda: self.confirm(), width=15)
            self.btn1.grid(column=1, row=0, padx=4)

        self.bind("<Enter>", lambda e: self.update_order())
        self.bind("<Leave>", lambda e: self.cancel())

    def cancel(self):
        self.frm1.after_cancel(self.__upfrm)

    def update_order(self):
        self.__details = self.controller.app.get_details()
        #print('Hola se ejecuto esto, la lista tiene: ', self.__details)
        i=0
        self.cont = 0
        total = 0

        #print(self.__details)

        for i in range(len(self.__details)):

            value = str(self.__details[i][0])

            if value.isalpha():
                print('Invitado: ', value)
            if value.isdigit():
                value = self.controller.app.get_username(value)
                print('Cliente: ', value)

            lbl1 = tk.Label(self.frm1, text=f"     {value}     ", font=("Bahnschrift", 14))
            lbl1.grid(column=1, row=i+1)
            self.lbl1.append(lbl1)
            self.b1.append(tk.Button(self.frm1, text='Ver', width=5, command= lambda i=i: self.show_detail(i)))
            self.b1[i].grid(column=2, row=i+1)
            self.b2.append(tk.Button(self.frm1, text="X", command= lambda i=i: self.delete(i)))
            self.b2[i].grid(column=3, row=i+1)
            lbl2 = tk.Label(self.frm1, text=f"     ", font=("Bahnschrift", 14))
            lbl2.grid(column=4, row=i+1)
            self.lbl2.append(lbl2)
            lbl3 = tk.Label(self.frm1, text=f"${self.__details[i][1]}   ", font=("Bahnschrift", 14))
            lbl3.grid(column=5, row=i+1)
            self.lbl3.append(lbl3)
            total = total + self.__details[i][1]

        self.lbls = [self.lbl1, self.lbl2, self.lbl3, self.b1, self.b2]

        self.cont = i
        self.__amount.set('$'+str(total))
        self.__upfrm = self.frm1.after(5000, self.update_order)

    def delete(self, x):
        self.top = tk.Toplevel(self.controller)

        ancho_ventana = 240
        alto_ventana = 70

        x_ventana = self.top.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = self.top.winfo_screenheight() // 2 - alto_ventana // 2

        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        self.top.geometry(posicion)
        self.top.title("Eliminar pedido")

        lblfrm1 = tk.LabelFrame(self.top)
        lblfrm1.pack()
        tk.Label(lblfrm1, text="Esta segugo que desea eliminar este pedido?", justify='center').grid(row=0, column=0, columnspan=2)

        tk.Button(lblfrm1, text="Si, continuar.", command=lambda: keep()).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(lblfrm1, text="No, volver atras.", command= lambda: minimizar()).grid(row=1, column=1, padx=5, pady=5)

        def keep():
            self.top.destroy()
            if self.controller.app.delete_detail(x):
                for list in self.lbls:
                    for label in list:
                        label.destroy()
                self.lbl1.clear()
                self.lbl2.clear()
                self.lbl3.clear()
                self.b1.clear()
                self.b2.clear()
                print('Eliminado correctamente')

            else:
                print('No se pudo eliminar')
            #self.controller.show_frame("")

        def minimizar():
            self.top.destroy()

    def show_detail(self, x):
        self.top = tk.Toplevel(self.controller)

        ancho_ventana = 300
        alto_ventana = 350

        x_ventana = self.top.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = self.top.winfo_screenheight() // 2 - alto_ventana // 2

        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        self.top.geometry(posicion)
        self.top.title("Detalle de la orden")

        total = 0
        subamount=StringVar()
        subamount.set("$0")

        username = str(self.__details[x][0])

        if username.isdigit():
            username = self.controller.app.get_username(username)

        self.name.set(f"Pedido de {username}")

        request = self.controller.app.get_request(x)

        lblfrm1 = tk.LabelFrame(self.top)
        lblfrm1.pack(pady=20)
        tk.Label(lblfrm1, textvariable=self.name, anchor="center", font=("Bahnschrift", 16)).grid(row=0, column=0, columnspan=4)
        tk.Label(lblfrm1, text='').grid(row=1)

        for i in range(len(request)):
            lbl1 = tk.Label(lblfrm1, text=f"{request[i][1]}     ", font=("Bahnschrift", 13))
            lbl1.grid(column=1, row=i+3)
            #self.lbl1.append(lbl1)
            lbl2 = tk.Label(lblfrm1, text=f"{request[i][0]}    ", font=("Bahnschrift", 13))
            lbl2.grid(column=2, row=i+3)
            #self.lbl2.append(lbl2)
            lbl3 = tk.Label(lblfrm1, text=f"${request[i][2]}   ", font=("Bahnschrift", 13))
            lbl3.grid(column=3, row=i+3)
            #self.lbl3.append(lbl3)
            total = total + request[i][2]

        subamount.set('$'+str(total))

        lblfrm2=LabelFrame(self.top, text="Total a Pagar", pady=5, padx=5)
        Label(lblfrm2, textvariable=subamount, anchor="center", font=("Bahnschrift", 15), width=20).pack()
        lblfrm2.pack()

        lblfrm3 = tk.LabelFrame(self.top)
        lblfrm3.pack(pady=10)

        if username == self.controller.app.user.name:
            Button(lblfrm3, text="Volver Atras", command=lambda: minimizar(), width=15).grid(column=0, row=0, padx=6, pady=6)
            Button(lblfrm3, text="Modificar", command=lambda: modify(), width=15).grid(column=1, row=0, padx=6, pady=6)
        else:
            Button(lblfrm3, text="Volver Atras", command=lambda: minimizar(), width=15).grid(column=0, row=0, padx=6, pady=6)

        def modify():
            print("Funcion no programada")

        def minimizar():
            self.top.destroy()

    def confirm(self):
        self.btn1.destroy()
        self.controller.app.update_order(2)
        self.controller.show_frame("OrderState")

    @property
    def cont(self):
        return self.__cont

    @cont.setter
    def cont(self, cont):
        self.__cont=cont

class OrderState(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent)
        self.controller = controller

        self.state = StringVar()

        tk.Label(self, textvariable=self.controller.n_order, font=("Bahnschrift", 15), justify='right', pady=10).pack()

        lblfrm1=tk.LabelFrame(self, text="Pedido")
        Button(lblfrm1,text="Ver",command=lambda: controller.show_frame("ShowOrder"), width=20, pady=8).grid(column=2, row=0, padx=20, pady=15)
        lblfrm1.pack()

        lblfrm2=tk.LabelFrame(self, text="Estado")
        Label(lblfrm2,textvariable=self.state).grid(column=2, row=0, padx=20, pady=15)
        lblfrm2.pack()

        self.bind("<Enter>", lambda e: self.update_state())
        self.bind("<Leave>", lambda e: self.cancel())

    def cancel(self):
        self.after_cancel(self.__refresh_frm)

    def update_state(self):
        print('Se actualizo el estado')
        self.controller.app.update_order()
        self.state.set(self.controller.states[self.controller.app.order.state])
        print(self.controller.states[self.controller.app.order.state])
        self.__refresh_frm = self.after(5000, self.update_state)

class ShowDetail(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent)
        self.controller = controller

class Records(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent)
        self.controller = controller

class Kitchen(tk.LabelFrame):
    def __init__(self, parent, controller:GUI):
        tk.LabelFrame.__init__(self, parent, text="Cocina", font=("Bahnschrift", 12))
        self.controller = controller
        self.parent = parent
        #Pedidos en espera
        #self.pending = [Order(41),Order(42)]

        self.b1=[]
        self.lbl1 = []
        self.lbl2 = []
        self.lbl3 = []
        self.lbl4 = []
        self.lbl5 = []
        self.frms = []
        self.chkboxes = []
        self.lbl7 = []

        self.time = StringVar()

        #Fecha y hora

        Label(self, textvariable=self.time, font=("Bahnschrift", 15)).pack(padx=1, pady=2)

        #En espera

        self.frm1 = LabelFrame(self, text="En espera", height=30)
        self.frm1.pack(padx=15, pady=12)

        frm1_canvas = Canvas(self.frm1)
        self.frame1 = Frame(frm1_canvas)
        scrollbar1 = Scrollbar(self.frm1, orient="vertical", command=frm1_canvas.yview)
        frm1_canvas.configure(yscrollcommand=scrollbar1.set, heigh=80)

        scrollbar1.pack(side=RIGHT, fill="y")
        frm1_canvas.pack(side="left", fill="both", expand=True)
        frm1_canvas.create_window((0,0), window=self.frame1, anchor="nw", tags="frame1")

        self.frame1.bind("<Configure>", lambda event, canvas=frm1_canvas: OnFrameConfigure(canvas))

        #En Proceso

        self.frm2 = LabelFrame(self, text="En Proceso", height=120)
        self.frm2.pack(padx=15, pady=5)

        frm2_canvas = Canvas(self.frm2)
        self.frame2 = Frame(frm2_canvas)
        scrollbar2 = Scrollbar(self.frm2, orient="vertical", command=frm2_canvas.yview)
        frm2_canvas.configure(yscrollcommand=scrollbar2.set, heigh=240)

        scrollbar2.pack(side=RIGHT, fill="y")
        frm2_canvas.pack(side="left", fill="both", expand=True)
        frm2_canvas.create_window((0,0), window=self.frame2, anchor="nw", tags="frame2")

        self.frame2.bind("<Configure>", lambda event, canvas=frm2_canvas: OnFrameConfigure(canvas))

        tk.Button(self, text="Salir", command=lambda: controller.on_closing(), height=2, width=10).pack(pady=10)

        #Funciones
        self.bind("<Enter>", lambda e: self.update_kitcken())
        self.bind("<Leave>", lambda e: self.cancel())

        def OnFrameConfigure(canvas):
            canvas.configure(scrollregion=canvas.bbox("all"))

    def update_kitcken(self):

        #Redimensionar ventana
        self.controller.geometry("400x500")

        #Actualizar fecha y hora
        datetimes = self.controller.app.time.now()
        date = datetimes.date().strftime("%d-%m-%y")
        time = datetimes.time().isoformat(timespec='minutes')
        datetime_str = date +'                             '+time
        self.time.set(f'{datetime_str}')

        #Obtener el estado de las ordenes
        self.controller.app.get_orders()
        self.pending = self.controller.app.pending
        self.inprogress = self.controller.app.inprogress

        #Mostrar ordenes pendientes
        for i in range(len(self.pending)):

            lbl1 = tk.Label(self.frame1, text=f"  #{self.pending[i][0]}      ", font=("Bahnschrift", 15))
            lbl1.grid(column=1, row=i+1)
            self.lbl1.append(lbl1)
            lbl2 = tk.Label(self.frame1, text=f"{self.controller.app.get_username(self.pending[i][1])}    ", font=("Bahnschrift", 15))
            lbl2.grid(column=2, row=i+1)
            self.lbl2.append(lbl2)
            self.b1.append(tk.Button(self.frame1, text='Preparar', width=6, height=2, command= lambda i=i: self.prepare(i)))
            self.b1[i].grid(column=3, row=i+1)
            lbl3 = tk.Label(self.frame1, text=f"       {self.pending[i][2]}  ", font=("Bahnschrift", 15))
            lbl3.grid(column=4, row=i+1)
            self.lbl3.append(lbl3)

        for i in range(len(self.inprogress)):

            lbl_frame1 = tk.LabelFrame(self.frame2, width=100)
            lbl_frame1.grid(column=0, row=i, padx=40, pady=10)
            self.frms.append(lbl_frame1)

            lbl4 = tk.Label(lbl_frame1, text=f"#{self.inprogress[i][0]}   {self.controller.app.get_username(self.inprogress[i][1])}", font=("Bahnschrift", 15), width=23, anchor='center')
            lbl4.pack(pady=5)
            self.lbl4.append(lbl4)
            lbl_frame2 = tk.LabelFrame(lbl_frame1)
            lbl_frame2.pack(pady=3, fill='both', padx=20)

            detail = self.controller.app.get_details(self.inprogress[i][0])

            for j in range(len(detail)):
                lbl5 = Label(lbl_frame2, text=f"  {detail[j][0]}  ", font=("Bahnschrift", 15))
                lbl5.grid(column=0, row=j)
                Label(lbl_frame2, text=f"      {detail[j][1]}       ", font=("Bahnschrift", 15)).grid(column=1, row=j)
                self.lbl5.append(lbl5)
                chkbox = Checkbox(lbl_frame2, command=lambda j=j: check_clicked(j))
                chkbox.grid(column=2, row=j)
                self.chkboxes.append(chkbox)

            lbl7=tk.Label(lbl_frame1)
            lbl7.pack()
            self.lbl7.append(lbl7)
            btn = tk.Button(lbl7, text='Terminado', width=10, height=2, command= lambda i=i: self.prepare(i))
            btn.grid(column=0, row=0)
            timestamp:datetime = self.inprogress[i][2]
            minutes_diff = (datetimes - timestamp).total_seconds() / 60.0
            parte_decimal, parte_entera = math.modf(minutes_diff)
            timer = str(int(parte_entera))+':'+str(int(parte_decimal*60)).rjust(2, '0')
            lbl6 = Label(lbl7, text=f"  {timer}", font=("Bahnschrift", 15))
            lbl6.grid(column=1, row=0)
            #self.lbl5.append(lbl6)

        self.lbls1 = [self.lbl1, self.lbl2, self.lbl3, self.lbl4, self.lbl5, self.lbl7, self.b1, self.frms, self.chkboxes]

        def check_clicked(x):
            print(self.checkboxes[x].checked())

        self.__upfrm = self.after(3000, self.update_kitcken)

    def cancel(self):
        self.after_cancel(self.__upfrm)

    def prepare(self, x):
        self.top = tk.Toplevel(self.controller)

        ancho_ventana = 240
        alto_ventana = 70

        x_ventana = self.top.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = self.top.winfo_screenheight() // 2 - alto_ventana // 2

        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        self.top.geometry(posicion)
        self.top.title("Preparar")

        lblfrm1 = tk.LabelFrame(self.top)
        lblfrm1.pack()
        tk.Label(lblfrm1, text="Preparar este pedido?", justify='center').grid(row=0, column=0, columnspan=2)

        tk.Button(lblfrm1, text="Si, continuar.", command=lambda: keep()).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(lblfrm1, text="No, volver atras.", command= lambda: minimizar()).grid(row=1, column=1, padx=5, pady=5)

        def keep():
            self.top.destroy()
            order_id = self.pending[x][0]
            if self.controller.app.update_order(3, order_id):
                self.clear()
                print('Pedido en preparacion')

            else:
                print('No se pudo ejecutar la accion')

        def minimizar():
            self.top.destroy()

    def finish(self, x):
        self.top = tk.Toplevel(self.controller)

        ancho_ventana = 240
        alto_ventana = 70

        x_ventana = self.top.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = self.top.winfo_screenheight() // 2 - alto_ventana // 2

        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        self.top.geometry(posicion)
        self.top.title("Terminar")

        lblfrm1 = tk.LabelFrame(self.top)
        lblfrm1.pack()
        tk.Label(lblfrm1, text="Termino este pedido?", justify='center').grid(row=0, column=0, columnspan=2)

        tk.Button(lblfrm1, text="Si, continuar.", command=lambda: keep()).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(lblfrm1, text="No, volver atras.", command= lambda: minimizar()).grid(row=1, column=1, padx=5, pady=5)

        def keep():
            self.top.destroy()
            order_id = self.pending[x][0]
            if self.controller.app.update_order(3, order_id):
                self.clear()
                print('Pedido terminado')
            else:
                print('No se pudo ejecutar la accion')

        def minimizar():
            self.top.destroy()

    def clear(self):
        for list in self.lbls1:
            for label in list:
                label.destroy()
        for lbls in self.frms:
            lbls.destroy()
        self.b1.clear()
        self.lbl1.clear()
        self.lbl2.clear()
        self.lbl3.clear()
        self.frms.clear()
        self.lbl4.clear()
        self.lbl5.clear()
        self.lbl7.clear()
        self.chkboxes.clear()

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

class Checkbox(Checkbutton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variable = tk.BooleanVar(self)
        self.configure(variable=self.variable)

    def checked(self):
        return self.variable.get()

    def check(self):
        self.variable.set(True)

    def uncheck(self):
        self.variable.set(False)

#Limitadores

class Limiter:

    def __init__(self, widget:StringVar, n:int, upper = False) -> None:
        self.__widget = widget
        self.upper = upper
        if len(self.__widget.get()) > 0:
            #Limita la cantidad a n caracteres
            if upper:
                self.__widget.set(self.__widget.get()[:n].upper())
            else:
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
    def __init__(self, master=None, var:StringVar=None, upper=False, **args):
        self.var = var
        self.upper = upper
        #self.var = tk.StringVar()
        tk.Entry.__init__(self, master, textvariable=self.var, **args)
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
                if self.upper:
                    self.old_value = self.get().upper()
                else:
                    self.old_value = self.get()
            else:
                # there's non-digit characters in the input; reject this
                if self.upper :
                    self.set(self.old_value.upper())
                else:
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