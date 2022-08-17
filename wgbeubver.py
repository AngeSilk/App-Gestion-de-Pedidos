diccionario={'Lunes':[],'Miercoles':[],'Jueves':[]}

for d in diccionario.items():
    temp=[]
    print('Temp dia ', d[0])
    tem = float(input('Ingrese la temperatura: '))
    for x in range(3):
        if -8< tem <50:
            temp.append(tem)
        else:
            x = x-1
        diccionario[x] = temp

print(diccionario)