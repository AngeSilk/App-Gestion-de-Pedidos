from database import *
from users import *

class App:

    roles=("Administrador","Cliente","Invitado","Delivery","Cocina")

    def __init__(self, appname:str, db_name:str) -> None:
        self.__appname= appname
        self.__db = db_name
        self.products=[]
        

    @property
    def db(self):
        db_name = self.__db
        return DataBase(f"./{db_name}")
    
    @property
    def name(self):
        return self.__appname

    @property
    def product(self):
        self.get_products()
        return self.products

    def run(self, user:object):
        
        if isinstance(user, Admin):
            
            pass
        elif isinstance(user, Client):
            
            #Realizar Pedido
            #Traer productos disponibles
            self.get_products()
            self.addClient(user)
            self.show_menu()

            pass
        elif isinstance(user, Guest):

            order_id=self.enable_Guest(user)
            if order_id:
                print(f"El invitado {user.name} vinculado a la orden Nº: {order_id}")
            else:
                print("No se existe una orden con ese codigo")    
                
                
        elif isinstance(user, Delivery):
            pass


    def get_products(self):
        
        try:
            print("\nConexion establecida:", self.db.connect(), "\n")
            sql='SELECT id, description, price FROM products WHERE available=1'     
            list=self.db.selectAllSql(sql)
            self.products.clear()
            for p in list:
                self.products.append(p)
        except:
            print("Error al cargar los productos")
        finally:
            self.db.disconnect()
    
    def show_menu(self):
        
        for p in self.products:

            print(p[0])

    def enable_Guest(self, guest:Guest):
        
        #Comprobar si existe una orden activa con el codigo compartido
        try:
            print("\nConexion establecida:", self.db.connect(), "\n")
            print(guest.sharecode)
            sql = f'SELECT id FROM orders WHERE sharecode="{guest.sharecode}"'     
            tupla=self.db.selectAllSql(sql)
            vector=tupla[0]
            id=int(vector[0])
            print(id)
            if id != None:
                print(id)
                return id 
        except:
            print("Error al validar el invitado")
            return False
        finally:
            self.db.disconnect()
    
    def addClient(self, client:Client): #grabar en la base de datos
            
        try:
            print("\nConexion establecida:", self.db.connect(), "\n")
            #datos=(client.name, client.lastname, client.dni, client.phone, client.password, client.address, client.avaliable)
            datos=client.current()
            sql = 'INSERT INTO user(name, lastname, dni, phone, password, address, available, role) VALUES (?,?,?,?,?,?,?, 1)'
            self.db.execSql(sql,datos)
            print("Cliente Agregado")
            return True
        except:
            print("No se pudo cargar el cliente")
            return False
        finally:
            self.db.disconnect()

    #Validar en la base de datos, si existe, envía el rol que cumple el usuario
    def validate_user(self, user:User):
        
        try:
            print("\nConexion establecida:", self.db.connect(), "\n")
            
            dni=user.dni
            passwd=user.password
    
            sql = f'SELECT id, role FROM user WHERE dni="{dni}" AND password="{passwd}"'
            tupla=self.db.selectAllSql(sql)
            if tupla:
                print("Se encontró el usuario")
                info=tupla[0]
                return info
            else:
                print("Los datos no coinciden con los usuarios registrados")
                return False
        finally:
            self.db.disconnect()