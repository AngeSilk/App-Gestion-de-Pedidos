class Guest:
    def __init__(self,name, code):
        self.__name = name
        self.__sharecode = code
        self.__elements = ""

class User:
    def __init__(self, name, lastname, DNI, password, phone) -> None:
       self.__name = name
       self.__lastname = lastname
       self.__DNI = DNI
       self.__password = password
       self.__phone = phone
       self.__state = True
    
    @property
    def name(self):
        return self.__name
    
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
    
    @state.setter
    def state(self, state):
        self.__state = state


    
class Client(User):
    
    def __init__(self, name, lastname, DNI, password, phone, address):
        User.__init__(self, name, lastname, DNI, password, phone)
        self.__address = address
    
    @property
    def id(self):
        return self.__
    
    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        self.__address = address
        
    def addGuest(self):
        


'''
class Waiter(User):

    waiter_ID = 0 #Seguir contador de la tabla SQL

    def __init__(self):
        Waiter.waiter_ID =+ 1
        self.__state = "on_hold"
'''

class Delivery(User):

    delivery_ID = 0 #Seguir contador de la tabla SQL

    def __init__(self):
        Delivery.delivery_ID =+ 1
        self.__state = "on_hold"

class Admin(User):

    def __init__(self, name, lastname, DNI, password, phone):
        User.__init__(self, name, lastname, DNI, password, phone)
        
        

