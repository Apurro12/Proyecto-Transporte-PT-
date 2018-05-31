
# coding: utf-8

# In[15]:


import numpy as np
from numpy import linalg as LA
from random import randint as RI
import time


a= 4
bach = 1000
iteracion = 10

LR = np.genfromtxt("LR",delimiter=",")


def d(p1,p2,q):
    t=np.dot((p2-p1),(q-p1))/(LA.norm(p2-p1)**2)
    if t<0:
        x=p1
    elif t>1:
        x=p2
    else:
        x=(p2-p1)*t+p1
    return x

def dlist(grafo,punto):
    return [d(grafo[i],grafo[i+1],punto) for i in range(0,len(grafo)-1)]  

def nodelenght(i,j,grafo):
    lenght=0
    if i<j:
        for i in range(i,j):
            lenght+=LA.norm(grafo[i+1]-grafo[i])
    return lenght

def updown(p1,p2,grafo): #p1 y p2 es de donde sale y quiere llegr o puntos del grafo 
    
    bajadas=dlist(grafo,p2) #Puntos del grafo que estan mas cerca de p2
    subidas=dlist(grafo,p1) #lo mismo pero con p1

    out=[] #El return
    
    db=[LA.norm(i-p2) for i in bajadas] #Distancia de las bajadas entre dos aristas
    dbo=[[db[i],i] for i in range(0,len(db))] #Distancia de las subidas entre dos aristas y su indice, 1er arista
    dbo.sort() #CUAL ES EL CRITERIO PARA ORDENAR ? 

    ds=[LA.norm(i-p1) for i in subidas]
    dso=[[ds[i],i] for i in range(0,len(ds))] 
    dso.sort()    

    ilb=[dbo[i][1] for i in range(0,len(db))] # Me va a tirar los indices de los 3 primeros que estan mas cerca de la bjada
    ils=[dso[i][1] for i in range(0,len(db))] # Lo mismo pero para la subida

    recorrido=[] #Que es recorrido ?
    lenght=0 #Que es lenght ?

    for i in range(0,len(ilb)): #Recorro los indices que me quedo en ilb
        for j in range(0,len(ils)): #Recorro los indices que me quedo en ils
            m=ils[j] 
            n=ilb[i]
            ps=subidas[m]
            pb=bajadas[n]            
            if (n==m) and (LA.norm(grafo[n+1]-pb)) <= (LA.norm(grafo[m+1]-ps)): #Si se sube y baja en el mismo tramo
                out.append([ps,pb])
                lenght=LA.norm(pb-ps)
                recorrido.append(lenght)
            elif ilb[i]>ils[j]:
                out.append([ps,pb])    
                lenght=LA.norm(ps-grafo[m+1])+nodelenght(m+1,n+1,grafo)-LA.norm(grafo[n+1]-pb)
                recorrido.append(lenght)
            lenght=0
    return tuple([out,recorrido])

def walkdistance(ps,pb,pi,pf):
    """ walkdistance toma 4 vectores y les toma la norma del taxista, agarra vectores no coordenadas """
    c1=int(abs(ps[0]-pi[0])+abs(ps[1]-pi[1]))
    c2=int(abs(pb[0]-pf[0])+abs(pb[1]- pf[1]))
    return [c1,c2,c1+c2]

def uds(p1,p2,grafo):
    """Decide con algun criterio cual es la mejor opcion de updown, p1 y p2 no son necesariamente puntos del grafo """
    paradas=updown(p1,p2,grafo)[0]
    dbus=updown(p1,p2,grafo)[1]
    camina=[walkdistance(i[0],i[1],p1,p2) for i in paradas]
#    a = 5 # Esta es el tiempo relativo cuando vamina y anda en cole

    if range(len(dbus) != 0):
        ddbus=[dbus[i] + (a)*camina[i][2] for i in range(len(dbus))] # a es el tiempo x cuadra
        i=ddbus.index(min(ddbus))
        return tuple([ddbus[i],a * LA.norm(p2-p1,1)] ) #el  elemento [0] es el tiempo que tarda en bondi y el [1]  caminando
    else:
        return tuple([a*LA.norm(p2-p1,1),a*LA.norm(p2-p1,1)]) #Si no hay paradas posibles que te minimizen
                                                         # anda caminando

def toptimo(p1,p2,grafo):
    """Me dice cual es el tiempo optimo de viaje"""
    return min(uds(p1,p2,grafo))
#Esta cosa me devuelve el tiempo minimo que tarda entre dos puntos 


def selector(p1,p2,gragrafofox):
    Tiempos = []
    D=[]
    for i in range(0,len(gragrafofox)):
        D =  toptimo(p1,p2,gragrafofox[i])
        Tiempos.append(D)

    tmin = min(Tiempos)
    b = Tiempos.index(tmin) #Este te devuelve el primer minimo que encuentra 
    return(b,tmin) #Retorna el num de grafo que se toma y el tiempo que tarda cuando viaja optimo



def tot0(grafo,q): # List Random tiene que ser una lista de numeros random, de 4*bach numeros random
    total = 0
    for j in range(0,bach): #El limite se puede aumentar para tener mas precision
        taux = toptimo(np.array([q[j][0],q[j][1]]),np.array([q[j][2],q[j][3]]),grafo)
        total = total + taux
    return (total)


def tot2(grafo): # Este total calcula el tiempo total sobre todos los limites en las esquinas
    total = 0
    for x1 in range(-7,32):
        for y1 in range(32,73):
            for y2 in range(32,73):
                for x2 in range(-7,32):
                    taux = toptimo(np.array([x1,y1]),np.array([x2,y2]),grafo)
                    total = total + taux
    return (total)

def tot(grafo): # Este total tira numeros random para hacer lo mismo que el de arriba
    total = 0
    for j in range(0,bach): #El limite se puede aumentar para tener mas precision
        x1 = RI(-7,31)
        x2 = RI(-7,31)
        y1 = RI(32,72)
        y2 = RI(32,72)
        taux = toptimo(np.array([x1,y1]),np.array([x2,y2]),grafo)
        total = total + taux
    return (total)


e0 = np.array([0,0])
e1 = np.array([1,0])
e2= np.array([1,1])
e3 = np.array([0,1])
e4 = np.array([-1,1])
e5= np.array([-1,0])
e6 = np.array([-1,-1])
e7 = np.array([0,-1])
e8= np.array([1,-1])
versores = np.array([e0,e1,e2,e3,e4,e5,e6,e7,e8])

def optimizador(grafo):
    grafos = []
    lista = []
#    print("El grafo original es", grafo)
    print()
    for i in range(0,9):
        for j in range(0,9):
            grafos.append(np.array( [grafo[0]+versores[j],grafo[1]+versores[i]] ) )
            lista.append( tot ( np.array([grafo[0]+versores[j],grafo[1]+versores[i]]) ) )
#    print(lista)
    tn = min(lista)
    indice = lista.index(tn)
#    print(indice)
    return(grafos[indice])

def optimizador0(grafo,q):
    grafos = []
    lista = []
#    print("El grafo original es", grafo)
    print()
    for i in range(0,9):
        for j in range(0,9):
            grafos.append(np.array([grafo[0]+versores[j],grafo[1]+versores[i]]))
            lista.append( tot0 ( np.array([grafo[0]+versores[j],grafo[1]+versores[i]]) , q ) )
#            print(G[i+j])    
#    print(lista)
    tn = min(lista)
    indice = lista.index(tn)
#    print(indice)
    return([grafos[indice],tn])
    
def optimizador2(gragrafofo):
    listorta= []
    tiempos = []
    for j in range(0,len(gragrafofo)):
        listorta.append (  optimizador ( gragrafofo[j] ) )
        tiempos.append ( tot( optimizador ( gragrafofo[j] ) ) )
    tn = min(tiempos)
    indice = tiempos.index(tn)
    
    for j in range(0,len(gragrafofo)):
        if (j == indice):
            gragrafofo[j] = listorta[j]
            
    return(gragrafofo)

def optimizador20(gragrafofox,q):
    listorta= []
    tiempos = []
    for j in range(0,len(gragrafofox)):
        listorta.append (  optimizador0 ( gragrafofox[j],q )[0] )
        tiempos.append (  optimizador0(gragrafofox[j],q)[1] )

    tn = min(tiempos)
    indice = tiempos.index(tn)
    
    for j in range(0,len(gragrafofox)):
        if (j == indice):
            gragrafofox[j] = listorta[j]
            
    return(gragrafofox)

# In[16]:





# In[41]:

"""ESto Abajo Esta Escrito para poner Animarlo con el Mathematica (Tarda mucho, voy a cambiarle la funcion tot)"""

"""grafo = np.array([[11,35],[12,70]])
print("Empezo")
print()
Datos = open("Prueba2","w")
Datos.write("Aca la configuracion inicial es [[11,35],[12,70]], tiene un bach de 100000 y le aplique 10 iteraciones")
Datos.write("\n")

Datos.write( str(grafo[0][0]) + "," + str(grafo[0][1])  + ","  + str(grafo[1][0]) + "," + str(grafo[1][1]) )
Datos.write("\n")
for j in range(0,iteracion):
    grafo = optimizador(grafo)
    Datos.write( str(grafo[0][0]) + "," + str(grafo[0][1])  + ","  + str(grafo[1][0]) + "," + str(grafo[1][1])   )
    if (j != iteracion - 1):
        Datos.write( str("\n") )

    print(time.clock())
    print("pasada" ,j+1,"De", iteracion )


print("termino")"""




