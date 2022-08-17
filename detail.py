
class Detail:

    def __init__(self, order:int, product:int, guest:str, qty:int):
        self.__ref_order = order
        self.__ref_product = product
        self.__guest = guest
        self.__qty = qty
        self.__subtotal = 0.0
        self.__available = True

    @property
    def ref_order(self):
        return self.__ref_order

    @property
    def ref_product(self):
        return self.__ref_product

    @property
    def guest(self):
        return self.__guest

    @property
    def qty(self):
        return self.__qty

    @property
    def subtotal(self):
        return self.__subtotal

    @property
    def available(self):
        return self.__available

    @available.setter
    def available(self, available:bool):
        self.__available = available



