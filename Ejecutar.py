from Simulacion import *


"""Esta es la segunda version del optimizador donde tiro los numeros random una sola vez"""

grafo = np.array([[11,35],[12,70]])
print("wewer")
print()
Datos = open("Prueba2","w")
Datos.write("Aca la configuracion inicial es [[11,35],[12,70]], tiene un bach de 100000 y le aplique 10 iteraciones")
Datos.write("\n")

Datos.write( str(grafo[0][0]) + "," + str(grafo[0][1])  + ","  + str(grafo[1][0]) + "," + str(grafo[1][1]) )
Datos.write("\n")
for j in range(0,iteracion):
    grafo = optimizador0(grafo,LR)[0]
    Datos.write( str(grafo[0][0]) + "," + str(grafo[0][1])  + ","  + str(grafo[1][0]) + "," + str(grafo[1][1])   )
    if (j != iteracion - 1):
        Datos.write( str("\n") )

    print(time.clock())
    print("pasada" ,j+1,"De", iteracion )


print("Aca termina la simulacion")



"""Esto fue un experimento para optimizar cuando tengo varios grafos, pero fue cualquier cosa, tendria que ver que es lo que hace"""

"""
grafo=np.array([[13,34],[12,70]])
grafo1=np.array([[18,44],[7,60]])
gragrafofo = np.array([grafo,grafo1])

print("Empezo")
print()
Datos = open("Prueba5","w")

Datos.write( str(gragrafofo[0][0][0]) + "," + str(gragrafofo[0][0][1])  + ","  + 
str(gragrafofo[0][1][0]) + "," + str(gragrafofo[0][1][1]) )

Datos.write("\n")

Datos.write( str(gragrafofo[1][0][0]) + "," + str(gragrafofo[1][0][1])  + ","  + 
str(gragrafofo[1][1][0]) + "," + str(gragrafofo[1][1][1]) )

Datos.write("\n")

for j in range(0,iteracion):
    grafo = optimizador20(gragrafofo,LR)

    Datos.write( str(gragrafofo[0][0][0]) + "," + str(gragrafofo[0][0][1])  + ","  + 
    str(gragrafofo[0][1][0]) + "," + str(gragrafofo[0][1][1]) )

    Datos.write("\n")

    Datos.write( str(gragrafofo[1][0][0]) + "," + str(gragrafofo[1][0][1])  + ","  + 
    str(gragrafofo[1][1][0]) + "," + str(gragrafofo[1][1][1]) )

    Datos.write("\n")

    print(time.clock())
    print("pasada" ,j+1,"De", iteracion )

Datos.write("Aca la configuracion inicial es [[[13,34],[12,70]],[[18,44],[7,60]]], tiene un bach de 1000 y le aplique 10 iteraciones")

print("termino") """

