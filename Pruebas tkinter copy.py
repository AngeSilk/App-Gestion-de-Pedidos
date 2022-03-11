import tkinter as tk

class Menu(tk.Tk):
    
    def __init__(self, products):
        tk.Tk.__init__(self)

        tk.Label(self, text="Menu:", font=("Courier", 20)).grid(row=0, column=0)
        tk.Label(self, text="Precio Unitario", font=("Courier", 10)).grid(row=1, column=6)

        self.count=2
        for p in products:
            tk.Label(self, text=f"{p[1]}     ", font=("Bahnschrift", 14)).grid(row=self.count, column=1, columnspan=2)
            #tk.Button(self, text='-', command=self.take_one(id)).grid(row=self.count, column=3)
            tk.Spinbox(self, from_=0, to=99, justify="center", width=3).grid(row=self.count, column=4)
            #tk.Button(self, text='+', command=self.plus_one(id)).grid(row=self.count, column=5)
            tk.Label(self, text=f"${p[2]}", font=("Bahnschrift", 14)).grid(row=self.count, column=6)
            self.count = self.count + 1
        tk.Label(self).grid(row=self.count)
        tk.Button(self, text='Quit', command=self.destroy).grid(row=self.count+1, column=2)
        tk.Button(self, text='Continue', command=self.take_order).grid(row=self.count+1, column=4)

    def take_order(self):
        pre_order={}
        pass



productos=[(1,"Humita", 120),(3,"Pollo",220),(5,"Salame",500)]

Menu(productos).mainloop()
    

