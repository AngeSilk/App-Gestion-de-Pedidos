from appV1 import *
import tkinter as tk
from tkinter import *
from tkinter import ttk

class GUI():
    
    def __init__(self,window, app):
        super().__init__(window)
        self.window = window
        self.window.title(app.name)
        self.products =[(1,"Humita", 120),(3,"Pollo",220),(5,"Salame",500)]
        self.window.title("Inicio")
        tk.Button(window, text="Ingresar", width=30, height=5, command=self.show_menu).grid(row=0, column=0)
        tk.Button(window, text="Unirme a un pediodo", width=30, height=5, command=self.join).grid(row=1, column=0)


    def login(self):
        tk.Entry(window)
        pass

    def join(self):
        pass

    def show_menu(self, products):
        print("Se está ejecutando")
        tk.Label(self.window, text="Menu:", font=("Courier", 20)).grid(row=0, column=0)
        tk.Label(self.window, text="Precio Unitario", font=("Courier", 10)).grid(row=1, column=6)

        self.count=2
        for p in products:
            tk.Label(self, text=f"{p[1]}     ", font=("Bahnschrift", 14)).grid(row=self.count, column=1, columnspan=2)
            tk.Spinbox(self, from_=0, to=99, justify="center", width=3).grid(row=self.count, column=4)
            tk.Label(self, text=f"${p[2]}", font=("Bahnschrift", 14)).grid(row=self.count, column=6)
            self.count = self.count + 1
        tk.Label(self).grid(row=self.count)
        tk.Button(self, text='Quit', command=self.destroy).grid(row=self.count+1, column=2)
        tk.Button(self, text='Continue', command=self.take_order).grid(row=self.count+1, column=4)

    def take_order(self):
        print()

window = tk.Tk()
app=App("Gestion de Pedidos para Restaurante", "database.db")
gui = GUI(window, app)
gui.mainloop()


'''
class ():
    def __init__(self):
        self.main = Tk()

        #INTEGER
        self.integer = 0

        #BUTTONS
        Button(self.main,text='Quit',command=self.main.destroy).pack()
        Button(self.main,text='+',command=self.plus_one).pack()
        Button(self.main,text='-',command=self.take_one).pack()

        #ENTRY
        Entry(self.main,textvariable=self.integer,justify=CENTER,width=4).pack()

        #MAINLOOP
        mainloop()

    def plus_one(self):
        self.integer = self.integer + 1
        self.entry0.delete(0,END)
        self.entry0.insert(0,self.integer)

    def take_one(self):
        self.integer = self.integer - 1
        self.entry0.delete(0,END)
        self.entry0.insert(0,self.integer)

'''