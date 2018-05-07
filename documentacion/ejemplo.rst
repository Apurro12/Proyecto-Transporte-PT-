Funciones 
===============
Acá vamos a explicar todas las funciones echas en el archivo, simulacion.py que esta en el Github
 
d(p1,p2,q)
----------------
d(p1,p2,q) devuelve la coordenada del punto mas cercano del segmento p1-p2 al punto q,
devuelve un punto sobre el segmento p1-p2
 
Sus argumentos son :
 
 * p1,p2 y q, arrays de numpy, ej q = np.array([3,4])
 
 
dlist(grafo,q)
----------------
dlist devuelve un vector de los puntos mas cercanos
entre todas las aristas consecutivas del grafo, al punto q

Sus argumentos son :
 
 * q, array de numpy, ej q = np.array([3,4])
 * grafo, vector que contiene vectores de numpy, ej grafo = np.array([[0,0][1,1][3,4]])

si aplicamos dlist(grafo,q) al ejemplo anterior nos va a tirar dos vectores,
uno por cada vertice que tenga el grafo


nodelenght(i,j,grafo)
----------------------
Dame dos vertices y un grafo, y te va a tirar la distancia que hay mientras vas del vertice i al j
si pasa que i >= j retorna identicamente el numero cero, (El primer vertice le corresponde i=0)

El return es o un entero o un float


updown(p1,p2,grafo):
----------------------
updown te va a agarrar un punto inicial p1, un final p2, y un grafo 


Se va a construir dos listas con todas las distancias mas cercanas entre todas las aristas a p1 y p2, estos son las listas subidas/bajadas

Una vez que para cada arista tiene el punto mas cercano a p1/p2, se va a calcular la distancia de todos estos puntos a p1 y p2, estas son las listas db (Distancia bajada) y ds (distancia subida)

me creo ahora vectores que en la primera componen tengan los elementos de db (distancia al punto de la arista) y en la segunda el indice del primer vertice de esa arista dbo/dbs, la segunda componente de estos vectores van a ir desde cero hasta la longitud del grafo  

Ahora estos vectores dbo/dbs me los voy a ordenar de forma tal que sean creciente en la distancia a la parada, osea que valla creciendo la primer componente de estos vectores, ejemplo:
[[1,2][2,0][3,1]]
recordar que la primer componente es la distancia a la parada mas cercana

Ahora me voy a armar otros dos vectores que donde me de los indices(2da componente) de los vectores dbo y dbs, por ejemplo anterior me daria
[2,0,1], estos vectores se llaman ils/ils (Index List subida/bajada)

Todas subidas/bajadas/db/ds/dbo/dbs/ils/ilb tienen la misma longitud, que es la del numero de aristas del grafo

Ahora hace un doble bucle de i desde 0 a len(ilb) y j desde 0 a len(ils)
Ahora recorre todas las combinaciones de subidas/bajadas y tengo dos posibilidades

 * Si subida y bajada esta en la misma arista se pregunta si la bajada esta mas cerca de la ultima arista que la subida (significa que se pregunta si subio y recorrio en la direccion del colectivo para bajarse, no alrevez), si esto se cumple

  #. Le append a out un vector de vectores que tiene los puntos de subida/bajada
  #. Le append a recorrido la longitud del viaje en colectivo por haberse subido/bajado ahí

 * Luego se pregunta si la 1er arista donde esta la bajada es mas grande que la arista de subida, si es asi

  #. Calcula la distancia entre esos puntos, usando nodelenght 
  #. Le append a out un vector de vectores que tiene los puntos de subida/bajada
  #. Le append a recorrido la longitud del viaje en colectivo por haberse subido/bajado ahí

Una vez que hace esto para todos los pares de posibles subidas y bajadas, me devuelve Una Tupla donde el 1er elemento es out y el segundo el recorrido.
Ej = [[[0,0],[10,10]],[20]],[[[4,5],[13,18]],[50]] , Esto significa que se subio en [0,0], se bajo en [10,10] y recorrio 20 cuadras en bondi, sin importar la cantidad de aristas o dobladas que alla echo el colectivo, y la otra posibilidad es que se subio en [4,5], se bajo en [13,18] y recorrio 50 cuadras en bondi, el siguiente paso es distinguir cual de todas estas opciones es la mejor

En caso de que no se cumpla ninguna de las condiciones anteriores (Como puede ser si tengo solo 2 aristas), devuelve una tupla vacia [], si el vector tiene por lo menos 3 aristas, ya me va a devoler algo


walkdistance(ps,pb,pi,pf):
----------------------------
tanto ps/pb/pi/pf son vectores arrays de numpy, ej ps = np.array([1,2])
pi/pf son los puntos de donde la persona inicia/finaliza su recorrido
ps/pb son los puntos en donde la persona se suba/baja al bondi

Lo que va a hacer es agarrar y calcularse la norma del taxista para los vectores CC1 = ps-pi y  CC2 = pb - pf que las llama c1 y c2
entonces me va a devolver una tupla con los tres valores [c1,c2,c1+c2]


uds(p1,p2,grafo):
-------------------
Se crea una matriz paradas = updown(p1,p2,grafo)[0] , que es un vector que dados p1 y p2 te dice todas las posibles combinaciones de subidas y bajadas, tal que se baje despues de donde se suba (o en el mismo punto) 
ej = [ [[S1x,S1y],[B1x,B1y]],[ [S2x,S2y],[B2x,B2y]] ] donde S/B son las coordenadas x/y el primer/segundo par de subidas/bajadas

se crea dbus = paradas(p1,p2,grafo)[1] que es la distancia que recorrio en bondi, entre cuando se sube en el 1er par de subidas/bajadas de paradas y luego el segundo elemento es cuando se sube/baja en el 2do par que aparece en paradas, etc; ej [1,4,5,1,2,3]

se crea el vector camina que me dice las distancias desde donde sale a donde se sube y de donde se baja a donde llega 











