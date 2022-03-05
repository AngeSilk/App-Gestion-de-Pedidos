from tkinter import ttk
from tkinter import *

import sqlite3


class Order:

    db_name = "database.db"

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            results = cursor.execute(query, parameters)
            conn.commit()
            conn.close()
        return results
    
    def get_orders(self):
        query = 'SELECT * FROM orders ORDER BY id DESC'
        db_rows = self.run_query(query)
        print(db_rows)

order = Order()
order.get_orders()