from database import *
from users import *
import numpy as np

class App:

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
    
    def change_role(self):
        
        #Transforma un usuario Admin a Cliente 
        if isinstance(self.user, Admin):
            admin=Admin()
            admin
        '''
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
                print(f"El invitado {self.user.name} vinculado a la orden Nº: {order_id}")
            else:
                print("No se existe una orden con ese codigo")    
                
                
        elif isinstance(user, Delivery):
            pass
        '''

    def show_menu(self):
        
        for p in self.products:

            print(p[0])
    
    #Valida en la base de datos, si existe el objeto
    def validate_user(self, user:User):
        try:
            print("\nConexion establecida:", self.db.connect(), "\n")
            
            dni=user.dni
            passwd=user.password
    
            sql = f'SELECT id, name, lastname, dni, phone, role, address FROM user WHERE dni="{dni}" AND password="{passwd}"'
            info = self.db.selectAllSql(sql)
            #Devuelve el rol que cumple el usuario y su id.
            if len(info)!=0:
                user_info=info[0]
                return user_info
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

    #Eliminar de la base de datos
    def delete(self, object:object):
        pass
    
    #Modificar en la base de datos
    def modify(self,object:object, ):
        pass

    #Verificar en la base de datos
    def db_check(self, object:object):
        
        if isinstance(object, Client):
            if self.add(object): return True
            else: return False
        
        if isinstance(object, Guest):
            order_id = self.enable(object)
            if  order_id != False: return True
            else: return False

        if isinstance(object, User):
            user_info = self.validate_user(object)
            if user_info:
                id=int(user_info[0])
                name=str(user_info[1])
                lastname=str(user_info[2])
                dni=str(user_info[3])
                phone=str(user_info[4])
                role=int(user_info[5])
                address=str(user_info[6])
                user=User(id, name, lastname, dni, phone, role, address)
                self.user=user
                return True
            else: return False

    #Obtener los productos de la base de datos
    def get_products(self):
        try:
            print("\nConexion establecida:", self.db.connect(), "\n")
            
            sql='SELECT id, description, price FROM products WHERE available=1'     
            list=self.db.selectAllSql(sql)
            self.products.clear()
            for p in list:
                self.products.append(p)
        except:
            print("No se pudieron obtener los productos")
        finally:
            self.db.disconnect()

    '''
    def get_user(self, object):

        if isinstance(object, User):
            sql=f'SELECT * FROM user WHERE id={object.id}' 
            list=self.db.selectAllSql(sql)

        if object==
    '''
    def get_worker(self):
        try:
            print("\nConexion establecida:", self.db.connect(), "\n")
            sql=f'SELECT place FROM worker WHERE {self.user.id} AND available=1'     
            info=self.db.selectOneSql(sql)
            fun=info[0]
            return fun
        except:
            print("No se pudo obtener el trabajador")
        finally:
            self.db.disconnect()

    def generate_sharecode(self):
        pass

    def set_user(self, mode):
        user=self.user
        if mode=="Admin":
            print(user)
            admin=Admin(int(user.id),str(user.name),str(user.lastname),str(user.dni),str(user.phone),int(user.role),str(user.address))
            self.user=admin
        if mode=="Client":
            client=Client(user.id, user.name, user.lastname, user.dni, user.phone, user.role, user.address)
            self.user=client
        if mode=="Worker":
            print("Aqui estamos")
            fun=self.get_worker()
            worker=Worker(user.id, user.name, user.lastname, user.dni, user.phone, user.role, user.address, fun)
            self.user=worker
        print(self.user)  
       
'''         
    def ModPrice(self, product_id, price):
        
        try:
            sql=f'SELECT id FROM clients '
        finally:   
        pass
'''