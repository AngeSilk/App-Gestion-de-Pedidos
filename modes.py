from database import DataBase

class Guest:
    def __init__(self,name:str, code:str):
        self.__name = name
        self.__sharecode = code
    
    def joinorder(self):
        pass

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

            datos=(client.name, client.lastname, client.dni, client.phone, client.password, client.address, client.avaliable)
            sql = 'INSERT INTO clients(name, lastname, dni, phone, password, address, available) VALUES (?,?,?,?,?,?,?)'
            db.execSql(sql,datos)
            print("Cliente Agregado")
            return True
        except:
            print("No se pudo cargar el cliente")
            return False
        finally:
            db.disconnect()
           
    def enableCient(self, client:object, value:bool):
        
        try:
            db = DataBase("./database.db")
            print("\nConexion establecida:", db.connect(), "\n")
            if value == True:
                sql=f'UPDATE clients SET available=1 WHERE dni="{client.dni}"'
            else:
                sql=f'UPDATE clients SET available=0 WHERE dni="{client.dni}"'
            db.execSql(sql)
            print("Cliente modificado")
        finally:
            db.disconnect()

    def addProduct(self, product:object): #grabar en la base de datos
            
        try:
            db = DataBase("./database.db")
            print("\nConexion establecida:", db.connect(), "\n")
            datos=(product.description, product.price)
            sql = 'INSERT INTO products(description, price, available) VALUES (?,?, 1)'
            db.execSql(sql, datos)
            print("Producto Agregado")
            return True
        except:
            print("E")
            return False
        finally:
            db.disconnect()

    def enableProduct(self, product:object, value:bool):
        
        try:
            db = DataBase("./database.db")
            print("\nConexion establecida:", db.connect(), "\n")
            if value == True:
                sql=f'UPDATE products SET available=1 WHERE id="{product.id}"'
            else:
                sql=f'UPDATE products SET available=0 WHERE id="{product.id}"'
            db.execSql(sql)
            print("Cliente modificado")
        finally:
            db.disconnect()

    def ModPrice(self, product:object, price):
        pass

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
    
    def takeorder(self):
        pass

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