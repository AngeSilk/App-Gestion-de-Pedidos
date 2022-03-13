from tkinter import *
from tkinter import ttk

gui = Tk()
gui.geometry("200x200+50+50") 

zona_c = Frame(gui, width = 200, height = 200) 
zona_c.config(background="cyan4")
zona_c.pack()

entry_text1 = StringVar() 
entry_text2 = StringVar() 
Entry(zona_c, width = 20, textvariable = entry_text1,justify=CENTER).pack()
Entry(zona_c, width = 20, textvariable = entry_text2,justify=CENTER).pack()
#zona_c.create_window(100, 100, window = entry_widget1)

#zona_c.bind_all("<Button-1>", lambda e: focus(e))

def focus(event):
    widget = zona_c.focus_get()
    #widget.trace("w", lambda *args: limitador(widget))
    print(widget, "has focus")

def limitador(widget, n):
    if len(widget.get()) > 0:
        #donde esta el :5 limitas la cantidad d caracteres
        widget.set(widget.get()[:n])

entry_text1.trace("w", lambda *args: limitador(entry_text1, 5))
gui.mainloop()