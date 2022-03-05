from modes import *

class App:

    def __init__(self, appname) -> None:
        self.__appname= appname

    def run(self, mode:object):
        
        if isinstance(mode, Admin):
            pass
        elif isinstance(mode, Client):
            pass
        elif isinstance(mode, Guest):
            pass
        elif isinstance(mode, Waiter):
            pass
        elif isinstance(mode, Delivery):
            pass
