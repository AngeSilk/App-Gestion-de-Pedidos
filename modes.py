from database import DataBase


class Guest:
    def __init__(self,name:str, code:str):
        self.__name = name
        self.__sharecode = code

class User:
    def __init__(self, name:str, lastname:str, DNI:str, password:str, phone:str) -> None:
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

class Admin(User):

    def __init__(self, name:str, lastname:str, DNI:str, password:str, phone:str):
        User.__init__(self, name, lastname, DNI, password, phone)
    
    def addClient(self, client:object): #grabar en la base de datos
            
            try:
                db = DataBase("./database.db")
                print("\nConexion establecida:", db.connect(), "\n")
                print()
                sql = f'INSERT INTO client (name, lastname, dni, phone, password, address, available) VALUES ("{client.name}","{client.lastname}","{client.dni}","{client.phone}","{client.password}","{client.address}","{client.avaliable}")'
                print(sql)
                db.insert(sql)
                print(client.name)
                print("Cliente Agregado")
            finally:
                db.disconnect()
           
            
            


class Client(User):
    
    def __init__(self, name:str, lastname:str, DNI:str, password:str, phone:str, address):
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
        pass
        

class Waiter(User):

    waiter_ID = 0 #Seguir contador de la tabla SQL

    def __init__(self):
        Waiter.waiter_ID =+ 1
        self.__state = "on_hold"

class Delivery(User):

    delivery_ID = 0 #Seguir contador de la tabla SQL

    def __init__(self):
        Delivery.delivery_ID =+ 1
        self.__state = "on_hold"