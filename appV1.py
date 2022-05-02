from database import *
from users import *
import numpy as np

class App:

    roles=("Administrador","Cliente","Invitado","Delivery","Cocina")

    def __init__(self, appname:str, db_name:str) -> None:
        self.__appname= appname
        self.__db = db_name
        self.products=[]
        self.__user = User("","")
    
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

    @property
    def user(self):
        return self.__user
    
    @user.setter
    def user(self, user:User):
        self.__user=user
    
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

    def get(self, object:object):
        
        try:
            print("\nConexion establecida:", self.db.connect(), "\n")
            #Productos
            if isinstance(object, Product):
                sql='SELECT id, description, price FROM products WHERE available=1'     
                list=self.db.selectAllSql(sql)
                self.products.clear()
                for p in list:
                    self.products.append(p)
            #Ususario
            if isinstance(object, User):
                sql=f'SELECT * FROM user WHERE id={object.id}' 
                list=self.db.selectAllSql(sql)
        except:
            print("Error al obtener")
        finally:
            self.db.disconnect()
    
    def show_menu(self):
        
        for p in self.products:

            print(p[0])
    
    #Valida en la base de datos, si existe el objeto
    def validate_user(self, user:User):
        try:
            print("\nConexion establecida:", self.db.connect(), "\n")
            
            dni=user.dni
            passwd=user.password
    
            sql = f'SELECT id, name, lastname, dni, phone, role FROM user WHERE dni="{dni}" AND password="{passwd}"'
            info = self.db.selectAllSql(sql)
            
            #Devuelve el rol que cumple el usuario y su id.
            if info!=None:
                u=info[0]
                print("Se encontró el usuario")      
                user=User(int(u[0]), str(u[1]), str(u[2]), str(u[3]), str(u[4]), int(u[5]))
                self.user=user
                print(self.user)
                #info=tupla[0]
                #user_id=info[0]
                #user_role=info[1]
                return True
            else:
                print("Los datos no coinciden con los usuarios registrados")
                return False
        finally:
            self.db.disconnect()

    #Habilitar o deshabilitar
    def enable(self, object:object, value:bool):
        try:
            print("\nConexion establecida:", self.db.connect(), "\n")
            #Cliente
            if isinstance(object, Client):
                if value:
                    sql=f'UPDATE clients SET available=1 WHERE dni="{object.dni}"'
                    print("Cliente habilitado")
                else:
                    sql=f'UPDATE clients SET available=0 WHERE dni="{object.dni}"'
                    print("Cliente deshabilitado")
                self.db.execSql(sql)
            #Producto
            if isinstance(object, Product):
                if value == True:
                    sql=f'UPDATE products SET available=1 WHERE id="{object.id}"'
                    print("Producto deshabilitado")
                else:
                    sql=f'UPDATE products SET available=0 WHERE id="{object.id}"'
                self.db.execSql(sql)
                print("Producto habilitado")
            #Invitado
            if isinstance(object, Guest):
                print(object.sharecode)
                sql = f'SELECT id FROM orders WHERE sharecode="{object.sharecode}"'     
                tupla=self.db.selectAllSql(sql)
                vector=tupla[0]
                id=int(vector[0])
                print(id)
                if id != None:
                    print(id)
                    return id
        except:
            print("No se pudo ejecutar la operacion")
            return False
        finally:
            self.db.disconnect()

    #Añadir en la base de datos
    def add(self, object:object): 
        try:
            print("\nConexion establecida:", self.db.connect(), "\n")
            #Cliente
            if isinstance(object, Client):
                datos=object.current()
                sql = 'INSERT INTO user(name, lastname, dni, phone, password, address, available, role) VALUES (?,?,?,?,?,?,?, 1)'
                self.db.execSql(sql,datos)
                print("Cliente Agregado")
                return True
            #Producto
            if isinstance(object, Product):
                datos=(object.description, object.price)
                sql = 'INSERT INTO products(description, price, available) VALUES (?,?, 1)'
                self.db.execSql(sql, datos)
                print("Producto Agregado")
                return True
            #Trabajador
            if isinstance(object, Worker):
                pass
        except:
            print("No se pudo ejecutar la operacion")
            return False
        finally:
            self.db.disconnect()

    def delete(self, object:object):
        pass

    def db_check(self, object:object):
        
        if isinstance(object, Client):
            if self.add(object): return True
            else: return False
        
        if isinstance(object, Guest):
            order_id = self.enable(object)
            if  order_id != False: return True
            else: return False

        if isinstance(object, User):
            user = self.validate_user(object)
            if user:
                #app.get(user)
                user:User
                return user
            else: return False

'''
    def ModPrice(self, product_id, price):
        
        try:
            sql=f'SELECT id FROM clients '
        finally:   
        pass
'''