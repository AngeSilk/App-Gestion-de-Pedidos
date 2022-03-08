
class Product:
    def __init__(self, description:str, price:float):
        self.__description = description
        self.__price = price
        self.__available = True

    @property 
    def id(self):
        return self.__id

    @property
    def description(self):
        return self.__description
    
    @description.setter
    def description(self, description:str):
        self.__description = description
    
    @property
    def price(self):
        return self.__price
    
    @price.setter
    def price(self, price:float):
        self.__price = price
    
    @property
    def available(self):
        return self.__available

    @available.setter
    def available(self, available:bool):
        self.__available = available
    
        
