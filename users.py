from numpy import product
from product import *
from plum import dispatch

class User:
    
    #Sobre carga del metodo init de user
    @dispatch
    def __init__(self, DNI:str, password:str):
        self.__DNI = DNI
        self.__password = password
        self.__role = None
    
    @dispatch
    def __init__(self, id:int, name:str, lastname:str, DNI:str, phone:str, role:int) -> None:
       self.__id = id
       self.__name = name
       self.__lastname = lastname
       self.__DNI = DNI
       #self.__password = password
       self.__phone = phone
       self.__state = True
       self.__role = role
    
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, id):
        self.__id = id
    
    @property
    def name(self):
        return self.__name
    
    @property
    def lastname(self):
        return self.__lastname
    
    @property 
    def dni(self):
        return self.__DNI
    
    @property 
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password 
    
    @property 
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        self.__phone = phone

    @property
    def state(self):
        return self.__state

    @property 
    def avaliable(self):
        if self.__state==True:
            return 1
        else: 
            return 0
    
    @state.setter
    def state(self, state):
        self.__state = state

    @property
    def role(self):
        return self.__role
    
    @role.setter
    def role(self, role):
        self.__role=role

    def __str__(self) -> str:
        user_info=f"Informacion del usuario:{self.id}, {self.name}, {self.lastname}, {self.dni}, {self.phone}, {self.role}"
        return user_info

class Admin(User):

    def __init__(self, name:str, lastname:str, DNI:str, password:str, phone:str):
        User.__init__(self, name, lastname, DNI, password, phone)

class Client(User):
    
    def __init__(self, name:str, lastname:str, DNI:str, password:str, phone:str, address):
        User.__init__(self, name, lastname, DNI, password, phone)
        self.__address = address
    
    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        self.__address = address
    
    def current(self):
        tupla=(self.name, self.lastname, self.dni, self.phone, self.password, self.address, self.avaliable)
        print(tupla)
        return tupla
    
    def makeorder(self, cliente:object, producto:object, quantity):
        
        pass
        
    def addedGuest(self, guest:object ,order:object):
        pass
        
class Worker(User):
    def __init__(self):
        self.__state = True

class Delivery(Worker):
    
    pass

class Kitchen(Worker):

    pass
        
class Guest:
    def __init__(self,name:str, code:str):
        self.__name = name
        self.__sharecode = code
    
    @property
    def name(self):
        return self.__name
        
    @property
    def sharecode(self):
        return self.__sharecode

    def joinorder(self):
        pass