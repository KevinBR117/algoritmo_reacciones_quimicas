import random
# leer archivo txt
archivo = open('./productos.txt', 'r')

# crear lista de productos
lista_productos = []
for linea in archivo:
    lista_productos.append(linea.replace('\n', '').split(' '))
print(f'lista de productos: {lista_productos} \n')

poblacion = []
numero_moleculas = 1000
mejor_molecula = []
buffer = 0
ratio_perdidaKE = 0.4
max_colisiones = 1000
calorias_min = 800
peso_max = 1.5


def crear_poblacion_inicial(numero_moleculas):
    for i in range(numero_moleculas):
        mochila = [0] * len(lista_productos)
        puntuacion = [0] * 4
        for j in range(len(mochila)):
            # generar seleccion de productos aleatoria
            cargo_producto = random.randint(0, 1)
            if(cargo_producto == 1):
                mochila[j] = 1
                # peso
                puntuacion[0] += float(lista_productos[j][1])
                # caloria
                puntuacion[1] += int(lista_productos[j][2])
        puntuacion[0] = round(puntuacion[0], 2)
        # energia potencial
        puntuacion[2] = round(float(puntuacion[1]/puntuacion[0]), 2)
        # energia cinetica
        puntuacion[3] = 0
        # añadir puntuacion
        mochila.extend(puntuacion)
        # añadir a la poblacion
        poblacion.append(mochila)

    print(f'poblacion inicial: {poblacion} \n')


def energia_potencial_total(poblacion):
    ept = 0
    for i in range(len(poblacion)):
        ept += poblacion[i][len(poblacion[i])-2]
    return round(ept*0.15, 2)


def mostrar_mejor_molecula():
    mejor_molecula = poblacion[0]
    for i in range(len(poblacion)):
        molecula = poblacion[i]
        # print(len(individuo), len(mejor_molecula))
        if(molecula[len(molecula)-2] >= mejor_molecula[len(mejor_molecula)-2]):
            # print(f'mochila anterior: {mejor_molecula}')
            if (molecula[len(molecula)-4] <= peso_max) and (molecula[len(molecula)-3] >= calorias_min):
                # print('nueva mejor mochila')
                mejor_molecula = molecula
    print(f'mejor molecula: {mejor_molecula} \n')


def col_ineficaz_contra_pared(w, buffer):
    molecula = poblacion[w]
    molecula_prima = mutar_molecula(molecula.copy())
    print('molécula_original: ', molecula)
    print('molécula_prima: ', molecula_prima)

    if((molecula[len(molecula)-2] + molecula[len(molecula)-1]) >= molecula_prima[len(molecula_prima)-2]):
        q = random.uniform(ratio_perdidaKE, 1)
        # energia cinetica
        molecula_prima[len(molecula_prima)-1] = round((molecula[len(molecula)-2] +
                                                         molecula[len(molecula)-1] - molecula_prima[len(molecula_prima)-2]) * q, 2)
        buffer = round(buffer + (molecula[len(molecula)-2] + molecula[len(
            molecula)-1] - molecula_prima[len(molecula_prima)-2]) * (1-q), 2)
        print('buffer actualizado: ', buffer)
        # print(f'PEw: {molecula[len(molecula)-2]}, KEw: {molecula[len(molecula)-1]}')
        # print(f'PEw_prima: {molecula_prima[len(molecula_prima)-2]}, KEw_prima: {molecula_prima[len(molecula_prima)-1]}')
        # print('molecula anterior: ', poblacion[w])
        poblacion[w] = molecula_prima
        print('molécula w ahora es w_prima: ', poblacion[w] , '\n')
    else:
        print('no hay cambios en la estrucutra interna de la molécula\n')


def mutar_molecula(molecula):
    producto_mutado = random.randint(0, len(lista_productos))

    for i in range(len(molecula)):
        if(producto_mutado == i):
            if(molecula[i] == 0):
                molecula[i] = 1
            else:
                molecula[i] = 0

    puntuacion = [0] * 4
    for i in range(len(molecula)-4):
        if(molecula[i] == 1):
            # print('true')
            # peso
            puntuacion[0] += float(lista_productos[i][1])
            # caloria
            puntuacion[1] += int(lista_productos[i][2])
    puntuacion[0] = round(puntuacion[0], 2)
    # energia potencial
    puntuacion[2] = round(float(puntuacion[1]/puntuacion[0]), 2)
    # energia cinetica
    puntuacion[3] = 0
    # añadir puntuacion
    molecula[len(molecula)-4] = puntuacion[0]
    molecula[len(molecula)-3] = puntuacion[1]
    molecula[len(molecula)-2] = puntuacion[2]
    molecula[len(molecula)-1] = puntuacion[3]

    return molecula


def descomposicion(w, buffer):
    molecula = poblacion[w]
    print('molécula_original: ', molecula)
    molecula_prima1, molecula_prima2 = descomponer_molecula(
        molecula.copy())
    print('molécula_prima1: ', molecula_prima1)
    print('molécula_prima2: ', molecula_prima2)

    temp = molecula[len(molecula)-2] + molecula[len(molecula)-1] - molecula_prima1[len(molecula_prima1)-2] - molecula_prima2[len(molecula_prima2)-2]
    print('temp: ', temp)
    if (temp >= 0):
        # print('temp mayor que 0: verdadero')
        k = random.uniform(0, 1)
        # energias cineticas
        molecula_prima1[len(molecula_prima1)-1] = round(temp * k, 2)
        molecula_prima2[len(molecula_prima2)-1] = round(temp * (1-k), 2)

        poblacion.pop(w)
        print('se añaden las moléculas ala población')
        print('molécula_prima1: ', molecula_prima1)
        print('molécula_prima2: ', molecula_prima2 , '\n')
        poblacion.append(molecula_prima1)
        poblacion.append(molecula_prima2)
    
    elif((temp + buffer) >= 0 ):
        # print('temp + buffer mayor igual que 0: verdadero')
        m1 = random.uniform(0, 1)
        m2 = random.uniform(0, 1)
        m3 = random.uniform(0, 1)
        m4 = random.uniform(0, 1)
        # energias cineticas
        molecula_prima1[len(molecula_prima1)-1] = round((temp + buffer)*(m1)*(m2), 2)
        molecula_prima2[len(molecula_prima2)-1] = round((temp + buffer - molecula_prima1[len(molecula_prima1)-1])*(m3)*(m4), 2)
        # actualizar buffer
        buffer = round(temp + buffer - molecula_prima1[len(molecula_prima1)-1] - molecula_prima2[len(molecula_prima2)-1], 2)
        print('buffer actualizdo: ', buffer)
        poblacion.pop(w)
        print('se añaden las moléculas ala población')
        print('molécula_prima1: ', molecula_prima1)
        print('molécula_prima2: ', molecula_prima2 , '\n')
        poblacion.append(molecula_prima1)
        poblacion.append(molecula_prima2)
    
    else:
        print('la descomposición no se lleva a cabo\n')

def descomponer_molecula(molecula):
    # cruzar partes molecula
    corte = random.randint(1, len(lista_productos)-1)
    # corte = int(len(individuo1)/2)
    # print("corte", corte)
    mochila = molecula[corte:len(lista_productos)]
    mochila.extend(molecula[0:corte])
    puntuacion = [0] * 4
    # generar puntuacion
    for i in range(len(mochila)):
        # print(i)
        if(mochila[i] == 1):
            # peso
            puntuacion[0] += float(lista_productos[i][1])
            # caloria
            puntuacion[1] += int(lista_productos[i][2])
    puntuacion[0] = round(puntuacion[0], 2)
    # energia potencial
    puntuacion[2] = round(float(puntuacion[1]/puntuacion[0]), 2)
    #  energia cinetica
    puntuacion[3] = 0
    # añadir puntuacion
    mochila.extend(puntuacion)

    mochila1 = mutar_molecula(molecula)

    return mochila, mochila1


def col_intermolecular_ineficaz(w, w1, buffer):
    molecula1 = poblacion[w]
    molecula2 = poblacion[w1]
    molecula_prima1 = mutar_molecula(molecula1.copy())
    molecula_prima2 = mutar_molecula(molecula2.copy())
    print('molécula1: ', molecula1)
    print('molécula_prima1: ', molecula_prima1)
    print('molécula2: ', molecula2)
    print('molécula_prima2: ', molecula_prima2)

    temp = (molecula1[len(molecula1)-2] + molecula2[len(molecula2)-2] + molecula1[len(molecula1)-1] + molecula2[len(molecula2)-1]) - (molecula_prima1[len(molecula_prima1)-2] + molecula_prima2[len(molecula_prima2)-2])
    print('temp: ', temp)
    if(temp >= 0):
        p = random.uniform(0, 1)
        # energias cineticas
        molecula_prima1[len(molecula_prima1)-1] = round(temp * p, 2)
        molecula_prima2[len(molecula_prima2)-1] = round(temp * (1-p), 2)
        # actualizar particulas
        print('se actualizan las moléculas en la población')
        print(molecula_prima1)
        print(molecula_prima2,'\n')
        poblacion[w] = molecula_prima1
        poblacion[w1] = molecula_prima2
    else:
        print('no hay cambios en la estructura interna de las moléculas\n')


def col_sintesis(w, w1, buffer):
    molecula1 = poblacion[w]
    molecula2 = poblacion[w1]
    molecula_prima = fusionar_moleculas(molecula1.copy(), molecula2.copy())
    print('molécula1: ', molecula1)
    print('molécula2: ', molecula2)
    print('molécula_prima: ', molecula_prima)

    if((molecula1[len(molecula1)-2] + molecula2[len(molecula2)-2] + molecula1[len(molecula1)-1] + molecula2[len(molecula2)-1]) >= (molecula_prima[len(molecula_prima)-2])):
        # energia cinetica
        molecula_prima[len(molecula_prima)-1] = round((molecula1[len(molecula1)-2] + molecula2[len(molecula2)-2] + molecula1[len(molecula1)-1] + molecula2[len(molecula2)-1] - molecula_prima[len(molecula_prima)-2]), 2)
        print('se fusionan las moléculas y se crea una nueva')
        print(molecula_prima , '\n')
        poblacion.pop(w)
        if(w1 == 0):
            poblacion.pop(w1)
        else:
            poblacion.pop(w1-1)
        poblacion.append(molecula_prima)

    else:
        print('la síntesis no se lleva a cabo\n')

def fusionar_moleculas(molecula1, molecula2):
    # cruzar particulas
    corte = random.randint(1, len(lista_productos)-1)
    mochila = molecula1[0:corte]
    mochila.extend(molecula2[corte:len(lista_productos)])

    puntuacion = [0] * 4
    # generar puntuacion
    for i in range(len(mochila)):
        # print(i)
        if(mochila[i] == 1):
            # peso
            puntuacion[0] += float(lista_productos[i][1])
            # caloria
            puntuacion[1] += int(lista_productos[i][2])
    puntuacion[0] = round(puntuacion[0], 2)
    # energia potencial
    puntuacion[2] = round(float(puntuacion[1]/puntuacion[0]), 2)
    #  energia cinetica
    puntuacion[3] = 0
    # añadir puntuacion
    mochila.extend(puntuacion)

    return mochila


def main():
    # estado inicial del sistema
    crear_poblacion_inicial(numero_moleculas)
    buffer = energia_potencial_total(poblacion)
    print(f"buffer: {buffer} \n")
    mostrar_mejor_molecula()

    colisiones = 0
    while (colisiones < max_colisiones):
        tipo_colision = random.randint(0, 3)
        # tipo_colision = 3
        w = random.randint(0, len(poblacion)-1)
        if (tipo_colision == 0):
            print(f'colisión ineficaz contra la pared\n')
            col_ineficaz_contra_pared(w, buffer)
        elif(tipo_colision == 1):
            print(f'colisión descomposición\n')
            descomposicion(w, buffer)
        elif(tipo_colision == 2):
            w1  = random.randint(0, len(poblacion)-1)
            while(w == w1):
                w1 = random.randint(0, len(poblacion)-1)
            print(f'colisión intermolecular ineficaz\n')
            col_intermolecular_ineficaz(w, w1, buffer)
        else:
            w1 = random.randint(0, len(poblacion)-1)
            while(w == w1):
                w1 = random.randint(0, len(poblacion)-1)
            print(f'colisión síntesis\n')
            col_sintesis(w, w1, buffer)
        colisiones += 1
    mostrar_mejor_molecula()


if __name__ == '__main__':
    main()
