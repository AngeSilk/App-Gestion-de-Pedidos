from app import App
from order import Order
from users import Client
#from order import Order



App1=App("Gestion de Pedidos")

Cliente = Client("Angelo", "Silke", 41632448, "12345678", 3754436348, "Sarratea 371")

Pedido=Order(Client.id, service)

'''
print (Cliente.name)
Cliente.state="on hold"
print (Cliente.state)
'''



