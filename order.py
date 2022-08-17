from datetime import datetime
from plum import dispatch

#states=("Cancelado","Pendiente","Procesando","Enviado","Completado")
services=("Waiter","Take Away","Delivery")

class Order:

    @dispatch
    def __init__(self, id):
        self.__id = id
        self.__sharecode = "AAA-000"
        self.__state = 1

    @dispatch
    def __init__(self, id:int, ref_client, sharecode, timestamp, service:int=2):

        self.__id = id
        self.__ref_client = ref_client
        self.__sharecode = sharecode
        self.__state = 1
        self.__service = service
        self.__participants = []
        self.__detail = []
        self.__timestamp:datetime = timestamp

    @property
    def id(self):
        return self.__id

    @property
    def sharecode(self):
        return self.__sharecode

    @property
    def state(self):
        return self.__state

    @property
    def service(self):
        return self.__service

    @state.setter
    def state(self, state:int):
        self.__state = state

    @property
    def participants(self):
        return self.__participants

    @participants.setter
    def participants(self, participants:list):
        self.__participants = participants

    @property
    def ref_client(self):
        return self.__ref_client

    @property
    def time(self):
        return self.__timestamp.time().isoformat(timespec='seconds')

    @property
    def date(self):
        return self.__timestamp.date().strftime("%d/%m/%y")

    @property
    def detail(self):
        return self.__detail

    @detail.setter
    def detail(self, details):
        self.__detail = details

'''
    def current(self):
        tupla=(self.client_id, self.sharecode, self.state, self.service)
        print(tupla)
        return tupla
'''