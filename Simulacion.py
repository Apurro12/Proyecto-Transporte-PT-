import numpy as np
from numpy import linalg as LA
import random

def d(p1,p2,q):
    """Dado un segmento que va de p1 a p2 y un punto q, esta funcion \n encuentra el punto sobre el segmento a menor distancia de q. Los argumentos \n son p1, p2, q que son np.arrays y devuelve un np.array."""
    t=np.dot(p2-p1,(q-p1))/(LA.norm(p2-p1)**2)
    if t<0:
        x=p1
    elif t>1:
        x=p2
    else:
        x=(p2-p1)*t+p1
    return x


p1=np.array([2,60])
p2=np.array([1,50])
grafo=np.array([[7,60],[7,44],[1,44],[1,60]])

def dlist(grafo,punto):
    """Retorna una lista con la funcion d aplicada entre puntos sucesivos de un grafo y punto"""
    return [d(grafo[i],grafo[i+1],punto) for i in range(0,len(grafo)-1)]  



def nodelenght(i,j,grafo):
    """Mide la longitud de las aristas comprendidas entre los nodos i y j"""
    lenght=0
    if i<j:
        for i in range(i,j):
            lenght+=LA.norm(grafo[i+1]-grafo[i])
    return lenght



def updown(p1,p2,grafo):  
    """Dado un punto inicial p1 y un punto final p2 y un grafo, esta funcion devuelve una tupla cuyo primer elemento es una lista con todas las distancias a las paradas de p2 y para cada una de ellas las distancias a p1. El segundo elemento de la tupla es la longitud del recorrido del micro para cada uno de los trayectos calculados en la lista."""
    # posibles bajadas y subidas
    bajadas=dlist(grafo,p2)
    subidas=dlist(grafo,p1)
    #el return
    out=[]
    #distancias bajadas y subidas ordenadas por proximidad y con la informacion del indice.
    db=[LA.norm(i-p2) for i in bajadas]
    dbo=[[db[i],i] for i in range(0,len(db))]
    dbo.sort()
    ds=[LA.norm(i-p1) for i in subidas]
    dbs=[[ds[i],i] for i in range(0,len(ds))]
    dbs.sort()    
    # index list bajada --- index list subida
    ilb=[dbo[i][1] for i in range(0,len(db))] #Hago que me tire todos los indices de subida y bajada para que no halla error de compilacion
    ils=[dbs[i][1] for i in range(0,len(ds))] #Cuando tengo grafos de tamaño mas chico que 4 aristas
    #guardo la distancia de recorrida entre subida y bajada
    recorrido=[]
    lenght=0
    #construyo out
    for i in range(0,len(ilb)):
        for j in range(0,len(ils)):
            m=ils[j]
            n=ilb[i]
            ps=subidas[m]
            pb=bajadas[n]          
            if n==m and LA.norm(grafo[n+1]-p2)<=LA.norm(grafo[m+1]-p1):
                out.append([ps,pb])
                lenght=LA.norm(pb-ps)
                recorrido.append(lenght)
            elif ilb[i]>ils[j]:
                out.append([ps,pb])    
                lenght=LA.norm(ps-grafo[m+1])+nodelenght(m+1,n+1,grafo)-LA.norm(grafo[n+1]-pb)
                recorrido.append(lenght)
            lenght=0
    return tuple([out,recorrido])
    
#uds=updownsmart
def uds(p1,p2,grafo):
    """Decide con algun criterio cual es la mejor opcion de updown, p1 y p2 no son necesariamente puntos del grafo """
    paradas=updown(p1,p2,grafo)[0]
    dbus=updown(p1,p2,grafo)[1]
    camina=[walkdistance(i[0],i[1],p1,p2) for i in paradas]
    
    def cond(i):
        return camina[i][2] >= LA.norm(p2-p1,1) """camina[i][0]>6 or camina[i][1]>6 or camina[i][2] >= 0.75*LA.norm(p2-p1) """
    
    if LA.norm(p2-p1)<=6:
        return (print("Voy caminando"))
    else:
        for i in range(len(camina)-1,-1,-1):
            #filtro 1
            if cond(i):
                del camina[i]
                del paradas[i]
                del dbus[i]
    if len(camina)==0:
        return print("Este micro no me sirve.")
    elif len(camina)==1:
        return tuple([paradas[0],dbus[0],dbus[0]+camina[0][2]])
    else:
        ddbus=[dbus[i]+camina[i][2] for i in range(len(dbus))] #El factor que multiplica a camina es la velocidad   
        i=ddbus.index(min(ddbus))
        return tuple([paradas[i],dbus[i],ddbus[i]])
        
                
#A esta funcion le tengo que armar un gragrafofo que es un vector de grafo como los parametros que estan definidos abajo
#p1=np.array([0,60])
#p2=np.array([11,61])
#q = np.array([2,50])
#grafo=np.array([[0,60],[10,60]])
#grafo2=np.array([[0,60],[11,60]])
#gragrafofo = np.array([grafo,grafo2])

def selector(p1,p2,gragrafofo):
    Distances = []
    D=[]
    for i in range(0,len(gragrafofo)):
        D= uds(p1,p2,gragrafofo[i])[2]
        Distances.append(D)
    
    a = Distances.index(min(Distances))
    print(a)
    return(gragrafofo[a],uds(p1,p2,gragrafofo[a])[2])      w9o          
                

        
        
def read(pi,pf,grafo):
    """Arroja en pantalla informacion de la simulacion."""
    if type(uds(pi,pf,grafo))==tuple:
        ps=uds(pi,pf,grafo)[0][0]
        pb=uds(pi,pf,grafo)[0][1]
        minlen=uds(pi,pf,grafo)[1]
        uwalk=walkdistance(ps,pb,pi,pf)[0]
        dwalk=walkdistance(ps,pb,pi,pf)[1]
        return print("\n\nCamino " +str(uwalk) +" cuadras hacia la parada.\nSubio en " +str(int(ps[0])) +" y " +str(int(ps[1]))  +" y bajo en "+str(int(pb[0]))+" y "+str(int(pb[1]))  +".\nCamino al bajar " +str(dwalk)+ " cuadras hasta su destino. \nRecorrio "+str(minlen)+" cuadras en micro.\n\n")
    else:
        return uds(pi,pf,grafo)
        
#mas adelante hay que complejizar esta funcion para ponerle puntos de interes.
def pgenerator():
    x=list(range(-5,32))
    y=list(range(32,73))
    def rand(x):
        return random.choice(x)
    return [np.array([rand(x),rand(y)])for i in [1,2]]

#mas adelante hay que complejizar la funcion para que tenga en cuenta las diagonales (hay que usar grafo)
def walkdistance(ps,pb,pi,pf):
	""" walkdistance toma 4 vectores y les toma la norma del taxista, agarra vectores no coordenadas """
    c1=int(abs(ps[0]-pi[0])+abs(ps[1]-pi[1]))
    c2=int(abs(pb[0]-pf[0])+abs(pb[1]- pf[1]))
    return [c1,c2,c1+c2]

def indexconv(lista):
    out=[]
    index=0
    for i in lista:
        if i==True:
            out.append(index)
        index+=1
    return out

def travelenght(pi,pf,grafo):
    """Dada una parada inicial, una final  y un grafo, esta funcion calcula las posibles longitudes del recorrido entre esos puntos por el micro y devuelve una lista ordenada con esos valores. Si existe un unico valor posible retorna un numero."""
    #aca pi es parada inicial (en la cual sube) y pf es parada final (en la cual baja). Es decir pi y pf son puntos en alguna/s arista/s del grafo. 
    if np.all(pi==pf)==True:
        return 0
    else:
        i1=indexconv([LA.norm(i-pi)==0 for i in dlist(grafo,pi)])
        i2=indexconv([LA.norm(i-pf)==0 for i in dlist(grafo,pf)])
        op=[]
        lenght=0
        for j in i2:
            for i in i1:
                if i<=j:
                    lenght+=LA.norm(pi-grafo[i+1])+nodelenght(i+1,j+1,grafo)-LA.norm(grafo[j+1]-pf)
                    if lenght>=0:
                        i1.remove(i)
                        op.append(lenght)
            lenght=0
        if len(op)==1:
            return op[0]
        else:
            return op.sort()



