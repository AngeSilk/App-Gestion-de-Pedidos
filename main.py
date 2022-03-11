from easygui import *


message = "What does she say?"
title = "Inicio"


result = indexbox(msg="Ingresar como", title="Hola cara de bola", choices=("Opcion 1","Opcion 2","Opcion 3"), cancel_choice="No")
if  result == 0:
    print("Opcion 1")
if result == 1:
    print("Opcion 2")
if result == 2:
    print("Opcion 3")

'''
msg ="Ingresar como"
title = "Inicio"
choices = ["Administrador", "Cliente", "Invitado", "Delivery"]
choice = choicebox(msg, title, choices)
'''