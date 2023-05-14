import random
individuo1 = [0,1,0,1,0,1,0,1]
individuo2 = [1,0,1,0,1,0,1,0]
individuo2.pop(0)
print(individuo2)

cruce = random.randint(1,len(individuo1)-1)
print(cruce)

mochila1 = individuo1[0:cruce]
print(mochila1)
mochila2 = individuo2[cruce:len(individuo2)-1]
print(mochila2)

print(random.randint(0, 9))

for i in range(len(individuo1)):
    print('lanzamiento ', i)
    print(random.uniform(0, 3))


def numeros():
    return 5, 6

a,b = numeros()

print(a)
print(b)

from threading import Timer
 
def foo(delay):
    print(f'foo() called after {delay}s delay')
 
if __name__ == '__main__':
 
    delay = 1        # en segundos
 
    print('Timer class demo')
 
    # llama a foo() después de 1 segundo
    t = Timer(delay, foo, [delay])
    t.start()
 
    print('foo() will be executed in 1 seconds…')