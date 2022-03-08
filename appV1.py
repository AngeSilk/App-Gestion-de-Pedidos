import tkinter as tk
from tkinter import ttk
from database import *
from modes import *

class App:

    
    def __init__(self, appname) -> None:
        self.__appname= appname
        

    def run(self, mode:object):
        
        if isinstance(mode, Admin):
            
            pass
        elif isinstance(mode, Client):
            
            #Realizar Pedido
            
            #Traer productos disponibles
            self.get_products()  
                           
            pass
        elif isinstance(mode, Guest):
            pass
        elif isinstance(mode, Waiter):
            pass
        elif isinstance(mode, Delivery):
            pass


    def get_products(self):
        
        try:
            db = DataBase("./database.db")
            print("\nConexion establecida:", db.connect(), "\n")
            sql='SELECT id, description, price FROM products WHERE available=1'     
            list=db.selectAllSql(sql)
            self.products.clear()
            for p in list:
                self.products.append(p)
        except:
            print("Error al cargar los productos")
        finally:
            db.disconnect()
    
    def show_menu(self):
        
        for p in products:
            