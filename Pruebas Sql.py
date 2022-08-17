from database import *
from datetime import datetime
from order import *
import random

db = DataBase("database.db")
user_id = 5


def max_value():
    try:
        print("\nConexion establecida:", db.connect(), "\n")
        sql=f'SELECT MAX(id) FROM user'
        info=db.selectOneSql(sql)
        fun=info[0]
        print(fun)
    except:
        print("No se pudo obtener el trabajador")
    finally:
        db.disconnect()

def generate_sharecode():
    numero = str(random.randint(111111111111, 999999999999))
    print(numero)
    return numero

def generate_order():

    try:
        print("\nConexion establecida:", db.connect(), "\n")
        sharecode = 957932682977
        '''
        sharecode=generate_sharecode()
        now=datetime.now()
        datos=(user_id, sharecode, now)
        sql = 'INSERT INTO orders (ref_client,sharecode,timestamp,state) VALUES (?,?,?,0)'
        db.execSql(sql,datos)
        '''
        sql=f'SELECT MAX(id) FROM orders WHERE ref_client={user_id} AND state=0'
        info=db.selectOneSql(sql)
        order_id=info[0]
        print(order_id)
        order = Order(order_id, sharecode)
        return order

    except:
        print("No se pudo generar la nueva orden")
    finally:
        db.disconnect()

details = []

ref_order = 41


def get_details(id=False):

    details = []

    try:
        print("\nObteniendo detalles de la orden", db.connect(), "\n")
        if id:
            print(id)
            sql=f'SELECT description, sum(qty), sum(subtotal) FROM details INNER JOIN products ON products.id=ref_product WHERE ref_order={id} AND details.available=1 GROUP BY ref_product'
        else:
            print(ref_order)
            sql=f'SELECT ref_user, SUM(subtotal) FROM details WHERE ref_order={ref_order} AND available=1 GROUP BY ref_user'
        list=db.selectAllSql(sql)
        details.clear()
        if list:
            print('Esta es la lista: ', list)
            for p in list:
                details.append(p)
        return details
    except:
        print("No se pudieron obtener los detalles de la orden")
    finally:
        db.disconnect()

def get_request(index):

    participants = ['1', 'Julio', 'Pedro', 'Roberto', 'Zamani']
    ref_user = participants[index]
    print(ref_user)

    try:
        print("\nObteniendo pedidos del usuario", db.connect(), "\n")

        sql=f'SELECT ref_product, SUM(qty), SUM(subtotal) FROM details WHERE ref_user=1 AND ref_order=42 AND available=1 GROUP BY ref_product'
        list=db.selectAllSql(sql)
        print(list)
        if list:
            for e in list:
                print(e[0])
        else:
            print()
    except:
        print("No se pudieron obtener los detalles de la orden")
    finally:
        db.disconnect()

time = datetime

def get_orders():

    pending = []
    inprogress = []
    data = time.now().date()
    print(data)
    try:
        print("\nObteniendo ordenes del dia", db.connect(), "\n")
        sql=f'SELECT orders.id, ref_client, timestamp, state FROM orders INNER JOIN user ON user.id = orders.ref_client WHERE date(timestamp)="{data}" AND (state = 3 OR state =2)'
        list=db.selectAllSql(sql)
        print(list)
        if list:
            for o in list:
                print(o)
                order = (o[0],o[1],o[2])
                if o[3] == 2:
                    pending.append(order)
                else:
                    inprogress.append(order)
                print('pendientes: ', pending)
                print('en proceso: ', inprogress)
        else:
            print('No hay ordenes todavia')

        #self.order.participants = self.participants
        #print(f'Ordenes del momento: {self.order.id}: ', self.order.participants)

    except:
        print("No se pudieron obtener las ordenes")
    finally:
        db.disconnect()

print(get_details(42))