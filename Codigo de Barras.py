from barcode import EAN13
from barcode.writer import ImageWriter
import random
import string
from barcode import Code39

# Establecemos el directorio donde será guardado
directorio = r'/home/angelo/Facultad/Programación/Gestion de Pedidos para Restaurante'

# Establecemos el numero del código de barras
# Importante: el modelo EAN debe tener 12 digitos
for id in range(20):
    numero = str(id).rjust(12, '0')
    print(numero)
#numero = "000000000003"
#numero = str(random.randint(111111111111, 999999999999))

#Generamos el código con un formato EAN13
mi_codigo = EAN13(numero, writer=ImageWriter())

#Guardamos la imagen en el directorio previamente declarado
mi_codigo.save(directorio+"/prueba")


states=("pendiente", "procesado","enviado","completado","cancelado")

print(states[1])

code = ""
for x in range(3):
    code = code + random.choice(string.ascii_letters).upper()
code = code + "-"
code = code + str(random.randint(111, 999))
print(code)

ean = Code39(code , writer=ImageWriter())
ean.save('barcode')
