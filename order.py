^
states=("Pendiente","Procesando","Enviado","Completado","Cancelado")

class Order:
    
    def __init__(self, client, service):
        self.__elements=[]
        self.__sharecode = 0
        self.__state = 0
        self.__client = client
        self.__service = service

    def addelement(self, element):
        self.__elements.append(element)
        
        
        
        