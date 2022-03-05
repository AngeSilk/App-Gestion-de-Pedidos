from appV1 import App
from modes import *

#Instancio una App
App_Admin=App("Vista de Ususario")

#Instancio un administrador para la aplicacion
admin=Admin("Angelo","Silke","41632448", "12348578","3754436348")

#Ejecuto la aplicación  como administrador
App_Admin.run(admin)

#Instancio un Cliente
cliente=Client("Angelo", "Silke", "41632448", "password", "3754436348","Sarratea371")

#Agrego el cliente a la base de datos
admin.addClient(cliente)


'''
Cliente2=App(cliente, password)

Guest1=App(guest, sharecode)
Guest2=App(guest, sharecode)

kitchen=(kitchen, )


Admin.run()
'''

