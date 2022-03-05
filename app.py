
from order import Order
from user import Client, Delivery


class App:
    def __init__(self, name) -> None:
        self.__name= name
        self.clients=[]
        self.delivery=[]
        self.waiters=[]
        self.orders=[]
    
    def __str__(self):
        return self.__name

    
#-Metodos para manejar las ordenes-#

    def takeorder(self, order):
        if isinstance(order, Order):
            self.orders.append(order)

#-Metodos para manejar clientes-#

    def addUser(self, user):
        
        if isinstance(user, Client):
            if Client.state == True:
                self.clients.append(user)
        
        if isinstance(user, Delivery):
            self.delivery.append(user)

