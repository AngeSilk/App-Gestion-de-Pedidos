from appV1 import *
import tkinter as tk
from tkinter import *
from tkinter import ttk

class GUI():
    
    def __init__(self, app:App):
        self.window = Tk()
        self.window.title("Aplicacion")
        self.app = app
        
        self.inicio_frame=Frame(self.window)
        
        self.menu = Frame(self.window)
        
        ttk.Button(self.inicio_frame, text="Ingresar", command= lambda: self.show_menu).grid(row=0, column=0)
        ttk.Button(self.inicio_frame, text="Unirme a un pediodo", command=self.join).grid(row=1, column=0)

        tk.Label(self.menu, text="Menu:", font=("Courier", 20)).grid(row=0, column=0)
        tk.Label(self.menu, text="Precio Unitario", font=("Courier", 10)).grid(row=1, column=6)

        self.count=2
        for p in app.products:
            tk.Label(self.menu, text=f"{p[1]}     ", font=("Bahnschrift", 14)).grid(row=self.count, column=1, columnspan=2)
            tk.Spinbox(self.menu, from_=0, to=99, justify="center", width=3).grid(row=self.count, column=4)
            tk.Label(self.menu, text=f"${p[2]}", font=("Bahnschrift", 14)).grid(row=self.count, column=6)
            self.count = self.count + 1
        tk.Label(self.menu).grid(row=self.count)
        tk.Button(self.menu, text='Quit', command=self.window.destroy).grid(row=self.count+1, column=2)
        tk.Button(self.menu, text='Continue', command=self.take_order).grid(row=self.count+1, column=4)

        self.inicio()
        self.window.mainloop()
        
    
    def inicio(self):
        self.hide_frames()
        self.inicio_frame.grid(row=0, column=0)

    def show_menu(self):
        self.hide_frames()
        self.menu.grid(row=0, column=0)
        
        
    def hide_frames(self):
        self.menu.grid_forget()
        self.inicio_frame.grid_forget()
    
    def join(self):
        print("Cara de bola")

    def take_order():
        pass

    
    
    
def main():
    app=App("Gestion de Pedidos para Restaurante", "database.db")
    gui = GUI(app)
    gui.inicio()
    return 0

if __name__ == '__main__':
    main()