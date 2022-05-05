class User:
    def __init__(self,nombre, variable):
        self.__nombre = nombre
        self.__variable = variable

    def do_something(self):
        print("do something A")

    @property
    def nombre(self):
        return self.__nombre

class Client(User):

    def __init__(self, nombre, variable):
        super().__init__(nombre, variable)
        self.__address =""
    
    @property
    def address(self):
        return self.__address
    
    @address.setter
    def address(self, address):
        self.__address = address

    @classmethod
    def from_User(cls, user:User, address):
        # Create new b_obj
        client_obj = cls(user.nombre, address)
        # Copy all values of A to B
        # It does not have any problem since they have common template
        for key, value in user.__dict__.items():
            client_obj.__dict__[key] = value
        client_obj.address=address
        return client_obj

if __name__ == "__main__":
    user = User("Hola","something")
    user = Client.from_User(user, "Sarratea 371")

    print(user.__dict__)
    print(user.address)
    #print(client.__dict__)
    #client.do_something()
    #print(type(client))