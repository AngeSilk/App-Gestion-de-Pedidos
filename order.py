
states=("Pendiente","Procesando","Enviado","Completado","Cancelado")
services=("Waiter","Take Away","Delivery")

class Order:
    
    def __init__(self, client:object, service:int, state:int=0):
        self.__client = client
        self.__sharecode = 0
        self.__state
        self.__service = service

    @property
    def sharcode(self):
        return self.__sharecode

    @property
    def state(self):
        return self.__state
    
    @state.setter
    def state(self, state:int):
        self.__state = state

        
        
        
        