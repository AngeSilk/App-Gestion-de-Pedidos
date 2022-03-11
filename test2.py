from product import Product
from appV1 import App
from users import *

#Instancio la App
app=App("Gestion de Pedidos para Restaurante", "database.db")

#Instancio un administrador para la aplicacion
admin=Admin("Angelo","Silke","41632448", "12348578","3754436348")

#Ejecuto la aplicación  como administrador
#app.run(admin)

#Instancio un Cliente
cliente=Client("Angelo", "Silke", "41632448", "password", "3754436348","Sarratea371")

#Valido si un cliente está registrado

#Agrego el cliente a la base de datos
#admin.addClient(cliente)

#Habilitar Cliente
#admin.enableCient(cliente, True)

#Instancio un producto

#producto = Product("Pollo",120)

#Agregar Producto
#admin.addProduct(producto)

#Realizar un pedido
#cliente.makeorder()

#Traer productos
#app.run(cliente)

Mati=Guest("Mati", "111111111111")

app.run(Mati)
'''
Cliente2=App(cliente, password)

Guest1=App(guest, sharecode)
Guest2=App(guest, sharecode)

kitchen=(kitchen, )


Admin.run()
'''

