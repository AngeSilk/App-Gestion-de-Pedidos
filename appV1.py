from datetime import datetime
from database import *
from users import *
from barcode.writer import ImageWriter
from barcode import Code39
import random
import numpy as np
import string


class App:

    def __init__(self, appname:str, db_name:str) -> None:
        self.__appname= appname
        self.__db = db_name
        self.__products=[]
        self.__orders={"Confirmadas":[], "En proceso":[]}
        self.__order = Order(0)
        self.__user = User("","")
        self.time  = datetime

        self.generate_barcode()

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
        return self.__products

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user:User):
        self.__user=user

    @property
    def order(self):
        return self.__order

    @order.setter
    def order(self, order:Order):
        self.__order=order

    @property
    def pending(self):
        print("Ordenes pendientes: ", self.__orders[0])
        return self.__orders[0]

    @property
    def inprogress(self):
        print("Ordenes en progreso: ", self.__orders[1])
        return self.__orders[1]

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
        for p in self.__products:
            print(p[0])

    #Valida en la base de datos, si existe el objeto
    def validate(self, object):

        try:
            print("\nConexion establecida:", self.db.connect(), "\n")

            #User
            if isinstance(object, User):
                user=object
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

            #Invitado
            if isinstance(object, Guest):
                sql = f'SELECT id FROM orders WHERE sharecode="{object.sharecode}" AND state = 1'
                tupla=self.db.selectAllSql(sql)
                if tupla:
                    vector=tupla[0]
                    id = int(vector[0])
                    return id
                else: return False
        finally:
            self.db.disconnect()

    #Habilitar o deshabilitar
    def enable(self, object:object, value:bool=True):
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
    def disable(self, object:object):
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
            order_id = self.validate(object)
            if  order_id != False:
                order=Order(order_id, "", object.sharecode, None)
                self.order=order
                self.get_participats()
                if object.name in order.participants:
                    return 1
                else:
                    self.generate_barcode()
                    return 0
            else: return 2

        if isinstance(object, User):
            user_info = self.validate(object)
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
            self.__products.clear()
            for p in list:
                self.__products.append(p)
        except:
            print("No se pudieron obtener los productos")
        finally:
            self.db.disconnect()

    #Obtener los detalles de una orden
    def get_details(self, id=False):

        details = []

        try:
            print("\nObteniendo detalles de la orden", self.db.connect(), "\n")
            if id:
                sql=f'SELECT sum(qty), description FROM details INNER JOIN products ON products.id=ref_product WHERE ref_order={id} AND details.available=1 GROUP BY ref_product'
            else:
                sql=f'SELECT ref_user, SUM(subtotal) FROM details WHERE ref_order={self.order.id} AND available=1 GROUP BY ref_user'
            list=self.db.selectAllSql(sql)
            details.clear()
            if list:
                #print('Esta es la lista: ', list)
                for p in list:
                    details.append(p)
            self.order.detail = details
            return details
        except:
            print("No se pudieron obtener los detalles de la orden")
        finally:
            self.db.disconnect()

    #Obtener los pedidos de los participantes de una orden
    def get_request(self, index):

        self.get_participats()

        ref_user = self.order.participants[index]
        print(ref_user)
        try:
            print("\nObteniendo pedidos del usuario", self.db.connect(), "\n")

            sql=f'SELECT ref_product, SUM(qty), SUM(subtotal) FROM details WHERE ref_user="{ref_user}" AND ref_order={self.order.id} AND available=1 GROUP BY ref_product'
            list=self.db.selectAllSql(sql)
            print(list)
            if list:
                request = []
                for e in list:
                    ref_product = e[0]
                    for p in self.product:
                        if p[0] == ref_product:
                            request.append((p[1],e[1],e[2]))
                return request
            else:
                print('No existen pedidos del usuario')
        except:
            print("No se pudieron obtener los detalles de la orden")
        finally:
            self.db.disconnect()

    #Eliminar un detalle de la orden
    def delete_detail(self, index):

        self.get_participats()
        print(self.order.participants[index])
        self.participant = self.order.participants[index]
        try:
            print("\nConexion establecida:", self.db.connect(), "\n")
            sql=f'UPDATE details SET available=0 WHERE ref_user="{self.participant}" AND ref_order={self.order.id}'
            self.db.execSql(sql)
            return True
        except:
            print("No se pudo ejecutar la operacion")
            return False
        finally:
            self.db.disconnect()

    #Obtener los participantes de una orden
    def get_participats(self):

        self.participants = []
        try:
            print("\nObteniendo participantes de la orden", self.db.connect(), "\n")

            sql=f'SELECT ref_user FROM details WHERE ref_order={self.order.id} AND available = 1 GROUP BY ref_user'
            list=self.db.selectAllSql(sql)
            for p in list:

                value = str(p[0])
                self.participants.append(value)

            self.order.participants = self.participants
            print(f'Participantes de la orden N° {self.order.id}: ', self.order.participants)

        except:
            print("No se pudieron obtener los detalles de la orden")
        finally:
            self.db.disconnect()

    #Obtener el nombre de usuario
    def get_username(self, id):
        try:
            print("\nObteniendo nombre de usuario", self.db.connect(), "\n")
            sql=f'SELECT name FROM user WHERE id={id} AND available = 1'
            info = self.db.selectOneSql(sql)
            value = info[0]
            return value
        except:
            print("No se pudieron obtener los detalles de la orden")
        finally:
            self.db.disconnect()

    #Obtener el trabajador y puesto
    def get_worker(self):
        try:
            print("\nConexion establecida:", self.db.connect(), "\n")
            sql=f'SELECT place FROM worker WHERE id_user={self.user.id} AND available=1'
            info=self.db.selectOneSql(sql)
            place=info[0]
            return place
        except:
            print("No se pudo obtener el trabajador")
        finally:
            self.db.disconnect()

    #Cambiar roll de usuario en la App
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
            place=self.get_worker()
            print(place)
            worker=Worker(user.id, user.name, user.lastname, user.dni, user.phone, user.role, user.address, place)
            self.user=worker
        print(self.user)

    #Generar un codigo para compartir
    def generate_sharecode(self):

        code = ""
        for x in range(3):
            code = code + random.choice(string.ascii_letters).upper()
        code = code + "-"
        code = code + str(random.randint(111, 999))
        print(code)

        return code

    #Generar un codigo de barras
    def generate_barcode(self):
        ean = Code39(self.order.sharecode, writer=ImageWriter(), add_checksum=False)
        ean.save('barcode')
        print('Codigo de barras generado: ',self.order.sharecode)

    #Generar orden en la base de datos
    def generate_order(self):

        sharecode=self.generate_sharecode()

        try:
            print("\nGenerando nueva orden:", self.db.connect(), "\n")

            datos=(self.user.id, sharecode, self.time.now())
            sql = 'INSERT INTO orders(ref_client,sharecode,timestamp,state) VALUES (?,?,?,1)'
            self.db.execSql(sql,datos)
            sql=f'SELECT MAX(id) FROM orders WHERE ref_client={self.user.id} AND state=1'
            info=self.db.selectOneSql(sql)
            info = info[0]
            return info #Retorna el id de la orden
        except:
            print("No se pudo generar la nueva orden")
        finally:
            self.db.disconnect()

    #Genera nueva orden
    def new_order(self):

        try:
            print("\nObteniendo ordenes:", self.db.connect(), "\n")
            #Obtener el id de la orden pendiente mas reciente del cliente.
            sql=f'SELECT MAX(id) FROM orders WHERE ref_client={self.user.id} AND state=1'
            info=self.db.selectOneSql(sql)
            info = info[0]
            print("Esto es info: ", info)
            if info == None:
                #Se crea una nueva orden
                order_id = self.generate_order()
            else:
                order_id=info
        except:
            print("No se pudo obtener la nueva orden")
        finally:
            self.db.disconnect()

        try:
            print("\nObter orden mas reciente: ", self.db.connect(), "\n")
            print(order_id)
            sql=f'SELECT sharecode, timestamp FROM orders WHERE id={order_id}'
            info=self.db.selectOneSql(sql)
            print(info)
            sharecode = info[0]
            timestamp = info[1]
            order=Order(order_id, self.user.id, sharecode, timestamp)
            self.order=order
            self.generate_barcode()
        except:
            print("No se pudo obtener la orden mas reciente")
        finally:
            self.db.disconnect()

    #Obetenr las ordenes del dia
    def get_orders(self, id=False):

        if id:
            print("Llego un id")
        else:

            pending = []
            inprogress = []

            try:
                print("\nObteniendo ordenes del dia", self.db.connect(), "\n")
                sql=f'SELECT orders.id, ref_client, timestamp, state FROM orders INNER JOIN user ON user.id = orders.ref_client WHERE date(timestamp)="{self.time.now().date()}" AND (state = 3 OR state =2)'
                #sql=f'SELECT ref_client FROM details WHERE ref_order={self.order.id} AND available = 1 GROUP BY ref_user'
                list=self.db.selectAllSql(sql)
                if list:
                    for o in list:
                        timestamp = datetime.fromisoformat(o[2])
                        if o[3] == 2:
                            time = timestamp.time().isoformat(timespec='minutes')
                            order = (o[0],o[1],time)
                            pending.append(order)
                        if o[3] == 3:
                            #time = timestamp.time().isoformat(timespec='seconds')
                            order = (o[0],o[1],timestamp)
                            inprogress.append(order)
                    self.__orders[0] = pending
                    self.__orders[1] = inprogress
                else:
                    print("No hay ordenes pendientes")
            except:
                print("No se pudieron obtener las ordenes")
            finally:
                self.db.disconnect()

    #Actualizar el estado de una orden
    def update_order(self, state=False, id=False):

        try:
            print(f"\nActualizando el estado de la orden a {state}:", self.db.connect(), "\n")
            if id:
                print('Entro aca')
                sql=f'UPDATE orders SET state={state}, timestamp ="{self.time.now()}" WHERE id={id}'
                print(sql)
            else:
                sql=f'UPDATE orders SET state={state}, timestamp ="{self.time.now()}" WHERE id={self.order.id}'
                self.order.state=state
            self.db.execSql(sql)
            return True
        except:
            print("No se pudo actualizar el estado de la orden")
        finally:
            self.db.disconnect()
    '''
    def get_order_state(self):
        try:
            print(f"\nObtener el estado de la orden a {state}:", self.db.connect(), "\n")
            sql=f'SELECT orders SET state={state}, timestamp ="{self.time.now()}" WHERE id={id}'

            self.db.SelectOneSql(sql)
            return True
        except:
            print("No se pudo actualizar el estado de la orden")
        finally:
            self.db.disconnect()
    '''

    #Insertar detalles de una orden
    def add_details(self, details:dict):

        try:
            print("\nAgregando detalles:", self.db.connect(), "\n")
            for d in details.items():
                product_id = d[0]
                qty = d[1][0]
                subtotal = d[1][1]
                print('Id: ',product_id,'   Cant: ',qty,'    Subtotal: ',subtotal)

                if isinstance(self.user, Guest):
                    ref_user = self.user.name
                if isinstance(self.user, Client):
                    ref_user = self.user.id

                if qty > 0:
                    datos=(self.order.id, product_id, ref_user, qty, subtotal)
                    sql = 'INSERT INTO details(ref_order,ref_product,ref_user,qty,subtotal, available) VALUES (?,?,?,?,?,1)'
                    self.db.execSql(sql,datos)
        except:
            print("No se pudo agregar los detalles")
        finally:
            self.db.disconnect()

'''
    def ModPrice(self, product_id, price):

        try:
            sql=f'SELECT id FROM clients '
        finally:
        pass
'''