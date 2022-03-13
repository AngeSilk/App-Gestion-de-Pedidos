import tkinter as tk


class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        #INTEGER
        self.integer = tk.IntVar()
        self.integer.set(0)
        
        tk.Label(self, text='Menu', font=("Courier", 20)).pack()

        tk.Button(self, text='+', command=self.plus_one).pack(side=tk.RIGHT)
        tk.Button(self, text='-', command=self.take_one).pack(side=tk.LEFT)
        tk.Button(self, text='Quit', command=self.destroy).pack()
        tk.Button(self, text='Continue', command=self.take_order).pack()
        #ENTRY
        tk.Entry(self, textvariable=str(self.integer), justify="center", width=4).pack()
        
        

    def plus_one(self):
        x =  self.integer.get() + 1
        self.integer.set(x)

    def take_one(self):
        x =  self.integer.get() - 1
        if(x<=0):
            self.integer.set(0)
            return x
        else:
            self.integer.set(x)

    def take_order(self):
        print(str(self.integer.get()))

app = Main()
app.mainloop()