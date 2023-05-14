import random
# leer archivo txt
archivo = open('./productos.txt', 'r')

# crear lista de productos
lista_productos = []
for linea in archivo:
    lista_productos.append(linea.replace('\n', '').split(' '))
print(f'lista de productos: {lista_productos} \n')

poblacion = []
nueva_poblacion = []
numero_particulas = 10
mejor_particula = []
buffer = 0
ratio_perdidaKE = 0.4
# mutacion = 0.5
max_colisiones = 100
calorias_min = 800
peso_max = 1.5


def crear_poblacion_inicial(numero_particulas):
    for i in range(numero_particulas):
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


def mostrar_mejor_particula():
    mejor_particula = poblacion[0]
    for i in range(len(poblacion)):
        particula = poblacion[i]
        # print(len(individuo), len(mejor_particula))
        if(particula[len(particula)-2] >= mejor_particula[len(mejor_particula)-2]):
            # print(f'mochila anterior: {mejor_particula}')
            if (particula[len(particula)-4] <= peso_max) and (particula[len(particula)-3] >= calorias_min):
                # print('nueva mejor mochila')
                mejor_particula = particula
    print(f'mejor particula: {mejor_particula} \n')


def col_ineficaz_contra_pared(w, buffer):
    particula = poblacion[w]
    particula_prima = mutar_particula(particula.copy())
    print('particula: ', particula)
    print('particula_prima: ', particula_prima)
    if((particula[len(particula)-2] + particula[len(particula)-1]) >= particula_prima[len(particula_prima)-2]):
        q = random.uniform(ratio_perdidaKE, 1)
        # energia cinetica
        particula_prima[len(particula_prima)-1] = round((particula[len(particula)-2] +
                                                         particula[len(particula)-1] - particula_prima[len(particula_prima)-2]) * q, 2)
        buffer = round(buffer + (particula[len(particula)-2] + particula[len(
            particula)-1] - particula_prima[len(particula_prima)-2]) * (1-q), 2)
        print('buffer actualizado: ', buffer)
        # print(f'PEw: {particula[len(particula)-2]}, KEw: {particula[len(particula)-1]}')
        # print(f'PEw_prima: {particula_prima[len(particula_prima)-2]}, KEw_prima: {particula_prima[len(particula_prima)-1]}')
        # print('particula anterior: ', poblacion[w])
        poblacion[w] = particula_prima
        print('particula w ahora es w_prima: ', poblacion[w] , '\n')
    else:
        print('no hay cambios en la estrucutra interna de la partícula\n')


def mutar_particula(particula):
    producto_mutado = random.randint(0, len(lista_productos))

    for i in range(len(particula)):
        if(producto_mutado == i):
            if(particula[i] == 0):
                particula[i] = 1
            else:
                particula[i] = 0

    puntuacion = [0] * 4
    for i in range(len(particula)-4):
        if(particula[i] == 1):
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
    particula[len(particula)-4] = puntuacion[0]
    particula[len(particula)-3] = puntuacion[1]
    particula[len(particula)-2] = puntuacion[2]
    particula[len(particula)-1] = puntuacion[3]

    return particula


def descomposicion(w, buffer):
    particula = poblacion[w]
    print('particula_original: ', particula)
    particula_prima1, particula_prima2 = descomponer_particula(
        particula.copy())
    print('particula_prima1: ', particula_prima1)
    print('particula_prima2: ', particula_prima2)

    temp = particula[len(particula)-2] + particula[len(particula)-1] - particula_prima1[len(particula_prima1)-2] - particula_prima2[len(particula_prima2)-2]
    print('temp: ', temp)
    if (temp >= 0):
        # print('temp mayor que 0: verdadero')
        k = random.uniform(0, 1)
        # energias cineticas
        particula_prima1[len(particula_prima1)-1] = round(temp * k, 2)
        particula_prima2[len(particula_prima2)-1] = round(temp * (1-k), 2)

        poblacion.pop(w)
        print('se añaden las partículas ala población')
        print('particula_prima1: ', particula_prima1)
        print('particula_prima2: ', particula_prima2 , '\n')
        poblacion.append(particula_prima1)
        poblacion.append(particula_prima2)
    
    elif((temp + buffer) >= 0 ):
        # print('temp + buffer mayor igual que 0: verdadero')
        m1 = random.uniform(0, 1)
        m2 = random.uniform(0, 1)
        m3 = random.uniform(0, 1)
        m4 = random.uniform(0, 1)
        # energias cineticas
        particula_prima1[len(particula_prima1)-1] = round((temp + buffer)*(m1)*(m2), 2)
        particula_prima2[len(particula_prima2)-1] = round((temp + buffer - particula_prima1[len(particula_prima1)-1])*(m3)*(m4), 2)
        # actualizar buffer
        buffer = round(temp + buffer - particula_prima1[len(particula_prima1)-1] - particula_prima2[len(particula_prima2)-1], 2)
        print('buffer actualizdo: ', buffer)
        poblacion.pop(w)
        print('se añaden las partículas ala población')
        print('particula_prima1: ', particula_prima1)
        print('particula_prima2: ', particula_prima2 , '\n')
        poblacion.append(particula_prima1)
        poblacion.append(particula_prima2)
    
    else:
        print('la descomposición no se lleva a cabo\n')

def descomponer_particula(particula):
    # cruzar partes particula
    corte = random.randint(1, len(lista_productos)-1)
    # corte = int(len(individuo1)/2)
    # print("corte", corte)
    mochila = particula[corte:len(lista_productos)]
    mochila.extend(particula[0:corte])
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

    mochila1 = mutar_particula(particula)

    return mochila, mochila1


def col_intermolecular_ineficaz(w, w1, buffer):
    particula1 = poblacion[w]
    particula2 = poblacion[w1]
    particula_prima1 = mutar_particula(particula1.copy())
    particula_prima2 = mutar_particula(particula2.copy())
    print('particula1: ', particula1)
    print('particula_prima1: ', particula_prima1)
    print('particula2: ', particula2)
    print('particula_prima2: ', particula_prima2)

    temp = (particula1[len(particula1)-2] + particula2[len(particula2)-2] + particula1[len(particula1)-1] + particula2[len(particula2)-1]) - (particula_prima1[len(particula_prima1)-2] + particula_prima2[len(particula_prima2)-2])
    print('temp: ', temp)
    if(temp >= 0):
        p = random.uniform(0, 1)
        # energias cineticas
        particula_prima1[len(particula_prima1)-1] = round(temp * p, 2)
        particula_prima2[len(particula_prima2)-1] = round(temp * (1-p), 2)
        # actualizar particulas
        print('se actualizan partículas en la población')
        print(particula_prima1)
        print(particula_prima2,'\n')
        poblacion[w] = particula_prima1
        poblacion[w1] = particula_prima2
    else:
        print('no hay cambios en la estructura interna de las partículas\n')


def col_sintesis(w, w1, buffer):
    particula1 = poblacion[w]
    particula2 = poblacion[w1]
    particula_prima = fusionar_particulas(particula1.copy(), particula2.copy())
    print('particula1: ', particula1)
    print('particula2: ', particula2)
    print('particula_prima: ', particula_prima)

    if((particula1[len(particula1)-2] + particula2[len(particula2)-2] + particula1[len(particula1)-1] + particula2[len(particula2)-1]) >= (particula_prima[len(particula_prima)-2])):
        # energia cinetica
        particula_prima[len(particula_prima)-1] = round((particula1[len(particula1)-2] + particula2[len(particula2)-2] + particula1[len(particula1)-1] + particula2[len(particula2)-1] - particula_prima[len(particula_prima)-2]), 2)
        print('se fusionan las partículas y se crea una nueva')
        print(particula_prima , '\n')
        poblacion.pop(w)
        if(w1 == 0):
            poblacion.pop(w1)
        else:
            poblacion.pop(w1-1)
        poblacion.append(particula_prima)

    else:
        print('la síntesis no se lleva a cabo\n')

def fusionar_particulas(particula1, particula2):
    # cruzar particulas
    corte = random.randint(1, len(lista_productos)-1)
    mochila = particula1[0:corte]
    mochila.extend(particula2[corte:len(lista_productos)])

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
    crear_poblacion_inicial(numero_particulas)
    buffer = energia_potencial_total(poblacion)
    print(f"buffer: {buffer} \n")
    mostrar_mejor_particula()

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
    mostrar_mejor_particula()


if __name__ == '__main__':
    main()
