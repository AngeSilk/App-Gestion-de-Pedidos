
from order import Order
from modes import Client, Delivery


class App:
    def __init__(self, mode) -> None:
        self.__name= name
        self.clients=[]
        self.products=[]
        self.pendientorders=[]
        self.delivery=[]
        self.waiters=[]
    
    def __str__(self):
        return self.__name

    
#-Metodos para manejar las ordenes-#

    def takeorder(self, order):
        if isinstance(order, Order):
            self.orders.append(order)

#-Metodos para manejar clientes-#

    def add(self,)
    Client(self, ):
        
        if isinstance(user, Client):
            if Client.state == True:
                self.clients.append(user)
        
        if isinstance(user, Delivery):
            self.delivery.append(user)

