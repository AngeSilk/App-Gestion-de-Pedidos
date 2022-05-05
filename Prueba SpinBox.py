from ast import Lambda
from tkinter import *

w=Tk()
frm1 = LabelFrame(w, text="Menu", font=("Courrier", 10))
frm1.pack(fill='both',expand=1)

productos=[(1,"Humita", 120),(3,"Pollo",220),(5,"Salame",500)]

a=[]
e=[]

Label(frm1, text="Variedad", justify=LEFT, font=("Bahnschrift", 10)).grid(column=1, row=0)
Label(frm1, text="Precio      \nUnitario      ", justify="center", font=("Bahnschrift", 10)).grid(column=2, row=0)
Label(frm1, text="Cant.", font=("Bahnschrift", 10)).grid(column=3, row=0)
for i in range(len(productos)):
    Nombre=Label(frm1, text=f"     {productos[i][1]}     ", font=("Bahnschrift", 14)).grid(column=1, row=i+1)
    Precio=Label(frm1, text=f"${productos[i][2]}   ", font=("Bahnschrift", 14)).grid(column=2, row=i+1)
    e.append(StringVar())
    a.append(Spinbox(frm1, textvariable=e[i], from_=1, to=10, width=5))
    a[i].grid(column=3, row=i+1)

frm2=LabelFrame(w, text="Acciones").pack(fill="both", expand=1)

Button(frm2, text="Aceptar", command=lambda: take_order()).pack()
Button(frm2, text="Cancelar", command=lambda: ).pack()

def take_order():
    for i in range(len(productos)):
        print(a[i].get())

w.mainloop()