import os
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.ticker as plticker
 
#Código para modificar grilla de ploteo
fig,ax=plt.subplots()
intervals = float(0.1)
loc = plticker.MultipleLocator(base=intervals)
ax.xaxis.set_major_locator(loc)
ax.yaxis.set_major_locator(loc)
ax.grid(which='major', axis='both', linestyle='-')
#
 
def rand(tamaño, semilla):
    return gcl(tamaño,semilla,2**31 - 1,7**5,0)
 
def randu (tamaño, semilla):
    return gcl(tamaño,semilla,2**31 ,2**16+3,0)
 
def gcl(tamaño, semilla, m=None, a=None, c=None):
    if m == None:
        m = (2**31-1)
        a = 1103515245
        c = 12345
    suces = [semilla]
    for i in range(tamaño):
        suces.append((a*suces[i] +c ) % m)
    suces = normalizar(suces,m)
    return suces
 
 
def cutCenter(number):
    center = number//100
    center =center-((center)//10000)*10000
    return center
 
def middleSquare(size, semilla):
    if (semilla <= 9999):
        x = [semilla]
        for i in range(size):
            x.append(cutCenter(x[i]*x[i]))
        x = normalizar(x,9999)
        return x
 
 
def comparar(numero, c):
    if 0.1*c <= numero <= 0.1*(c+1):
        return True
    else:
        return False
 
def normalizar(lista, factor):
    array = []
    for i in range(len(lista)):
        array.append(lista[i]/factor)
    return array
 
def calcularIndice(numero):
    indice = 0
    while (indice<10):
        if comparar(numero, indice):
            break
        indice+=1
    return indice
 
def calcularFrecuencias(lista):
    frecuencias = [0,0,0,0,0,0,0,0,0,0]
    for i in range(len(lista)):
        frecuencias[calcularIndice(lista[i])]+=1
    return frecuencias
 
def testChiCuad(f_obs, f_esp, alpha):
    chi2 = 0
    k = len(f_obs)
    for i in (range(k)):
        chi2 += ((f_obs[i] - f_esp)**2)/f_esp
    chiTabla = stats.chi2.ppf(1-alpha,k-1)
    print ("=== Chi Calculado ===")
    print(chi2)
    print("")
    print("=== Chi Tabla ===")
    print(chiTabla)
     
    if chi2<chiTabla:
        print ("Al ser el chi2 calculado menor al valor de tabla, la hipótesis nula de que no existe diferencia entre la distribución de la muestra y la distribución uniforme se acepta")  
    else:
        print ("Al ser el chi2 calculado mayor al valor de tabla, la hipótesis nula de que no existe diferencia entre la distribución de la muestra y la distribución uniforme se rechaza")  
 
def kstest(lista, alpha):
    lista.sort()
    dmax = 0
    n = len(lista)
    for j in range(n):
        if (((j+1)/n - lista[j]) > dmax):
            dmax = (j+1)/n - lista[j]
        if ((lista[j] - j/n) > dmax):
            dmax = (j+1)/n - lista[j]
    dtabla = stats.ksone.ppf((1-alpha/2),n)
    print ("=== Desviación máxima ===")
    print(dmax)
    print("")
    print ("=== Desviación tabla ===")
    print(dtabla)
    if dmax<dtabla:
        print ("Al ser el desvío calculado menor al valor de tabla, la hipótesis nula de que no existe diferencia entre la distribución de la muestra y la distribución uniforme se acepta")  
    else:
        print ("Al ser el desvío calculado mayor al valor de tabla, la hipótesis nula de que no existe diferencia entre la distribución de la muestra y la distribución uniforme se rechaza")

def corridasArAb(nums):
    bits=[]
    for i in range(len(nums)-1):
            if nums[i+1]<=nums[i]:
                bits.append(0)
            else:
                bits.append(1)
    corridas=1
    for i in range(1,len(bits)):
        if bits[i] != bits[i-1]:
            corridas+=1
    media= (2*len(nums)-1)/3
    print('media= ',media)
    varianza= (16*len(nums)-29)/90
    print('var= ',varianza)
    zo=(corridas-media)/(varianza**(1/2))
    if zo<0:
        zo=zo*-1
    print('zo= ', zo)
    z= stats.norm.ppf(1-alpha/2)
    print('z= ', z)
    zn=z*-1
    if ((zn < zo) & (zo < z)):
        print("Al ser el desvío calculado menor al valor de tabla, la hipótesis de que los números son independientes se acepta")
    else:
        print("Al ser el desvío calculado mayor al valor de tabla, la hipótesis de que los números son independientes se rechaza")         


def pruebaSerial(lista, alpha):
    results = []
    resultsUnidimen = []
    for i in range(10):
        results.append([])
        for j in range(10):
            results[i].append(0)
    listaBidimen = [[],[]]
    for i in range(len(lista)//2):
        listaBidimen[0].append(lista[i*2])
        listaBidimen[1].append(lista[i*2+1])
    for i in range(len(listaBidimen[0])):
        calcularIndice(listaBidimen[0][i])
        results[calcularIndice(listaBidimen[0][i])][calcularIndice(listaBidimen[1][i])] += 1
    for i in range(10):
        for j in range(10):
            resultsUnidimen.append(results[i][j])
    plt.plot(listaBidimen[0],listaBidimen[1],'o',markersize=1)
    plt.grid(True)
    plt.show()
    testChiCuad(resultsUnidimen, tam/len(resultsUnidimen)/2, alpha)
 
def menu():
    print(" ")    
    print ("MENÚ PRINCIPAL - Selecciona una opción")
    print ("1 - Rand")
    print ("2 - RandU")
    print ("3 - GCL")
    print ("4 - MiddleSquare")
    print ("5 - Prueba de chi-cuadrado")
    print ("6 - Prueba de Kolmogorov-Smirnov")
    print ("7 - Prueba serial")
    print ("8 - Prueba de corridas arriba-abajo")
    print ("9 - Salir")
 
 
 
tam = 100000
alpha = 0.05
while True:
    os.system('cls')
    print("Tamaño de la sucesion:", tam)
    sem = int(input("Inserte la semilla:"))
    menu()
   
    opcionMenu = input("Inserte su opcion >> ")
    print(" ")
 
    if opcionMenu=="1":
        print(rand(tam, sem))
        input("Pulsa una tecla para continuar")
   
    elif opcionMenu=="2":
        print(randu(tam, sem))
        input("Pulsa una tecla para continuar")
 
    elif opcionMenu=="3":
        print(gcl(tam, sem))
        input("Pulsa una tecla para continuar")
 
    elif opcionMenu=="4":
        while (sem>9999 or sem<1000):
            print("Este método requiere semillas de 4 cifras, se recomienda un número alto")
            sem = int(input("Inserte la semilla:"))
        print(middleSquare(tam, sem))
        input("Pulsa una tecla para continuar")
   
    elif opcionMenu=="5":
        os.system('cls')
        nums = gcl(tam,sem)
        f_obs = calcularFrecuencias(nums)
        f_esp = tam/len(f_obs)
        testChiCuad(f_obs, f_esp, alpha)
        input("Pulsa una tecla para continuar")
 
    elif opcionMenu=="6":
        os.system('cls')
        nums = gcl(tam,sem)
        kstest(nums, alpha)
        input("Pulsa una tecla para continuar")
 
    elif opcionMenu=="7":
        os.system('cls')
        nums = gcl(tam,sem)
        pruebaSerial(suces, alpha)
        input("Pulsa una tecla para continuar")
   
    elif opcionMenu=="8":
        os.system('cls')
        nums = gcl(tam,sem)
        corridasArAb(nums)
        input("Pulsa una tecla para continuar")
 
    elif opcionMenu=="9":
        break
   
    else:
        print(" ")
        input("No has pulsado ninguna opción correcta... \n Pulsa una tecla para continuar")
    os.system('cls')