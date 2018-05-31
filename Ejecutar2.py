from Simulacion import *

grafo=np.array([[13,34],[12,70]])
grafo1=np.array([[18,44],[7,60]])
gragrafofo = np.array([grafo,grafo1])
LR = np.genfromtxt("LR",delimiter=",")


def mtot(gragrafofox,q):
    aux = 0
    for j in range(0,bach):
        eleccion =  selector( np.array([q[j][0],q[j][1]]) , np.array([q[j][2],q[j][3]]) , gragrafofox)[1]
        aux = aux + eleccion

    return(aux)

def variador(gragrafofox):
    pares = []
    for j in range(0,9):
        for i in range(0,9):
            auxilio = np.array( [gragrafofox[0][0]+versores[j],gragrafofox[0][1]+versores[i]] ) 
            pares.append([auxilio,gragrafofox[1]]) 

    for j in range(0,9):
        for i in range(0,9):
            auxilio = np.array( [gragrafofox[1][0]+versores[j],gragrafofox[1][1]+versores[i]] ) 
            pares.append([gragrafofox[0],auxilio])

    return(pares)


def final(gragrafofox):
    minimo = []
    juntar = []
    for t in range(0,162):
#        print("Voy pasada",t)
        juntar.append( variador(gragrafofox)[t] )
        tiempo = mtot( juntar[t],LR )
        minimo.append( tiempo )
        tn = min(minimo)
        indice = minimo.index(tn)

    return(juntar[indice])



Datos = open("Prueba2","w")

Datos.write(str(gragrafofo[0][0][0]) + "," + str(gragrafofo[0][0][1]) + "," + str(gragrafofo[0][1][0]) + "," + str(gragrafofo[0][1][1]))
Datos.write("\n")
Datos.write( str(gragrafofo[1][0][0]) + "," + str(gragrafofo[1][0][1]) + "," + str(gragrafofo[1][1][0]) + "," + str(gragrafofo[1][1][1]))
Datos.write("\n")

time.clock()
for w in range(0,10):
    print(time.clock())
    print("voy por la pasada",w)
    gragrafofo = final(gragrafofo)

    Datos.write(str(gragrafofo[0][0][0]) + "," + str(gragrafofo[0][0][1]) + "," + str(gragrafofo[0][1][0]) + "," + str(gragrafofo[0][1][1]))
    Datos.write("\n")
    Datos.write( str(gragrafofo[1][0][0]) + "," + str(gragrafofo[1][0][1]) + "," + str(gragrafofo[1][1][0]) + "," + str(gragrafofo[1][1][1]))
    Datos.write("\n")



Datos.write("\n")
Datos.write("Aca la configuracion inicial es [[[13,34],[12,70],[[18,44],[7,60]]] , tiene un bach de 1000 y le aplique 1 iteracion")


print("termino")









