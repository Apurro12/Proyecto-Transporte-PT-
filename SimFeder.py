import numpy as np
from random import randint as RI
from itertools import product
import pandas as pd
import pickle

# pickle.dump(new,open("db.p", "wb"))
dataBase = pickle.load(open("db.p", "rb"))


def norm(p):
    """ Devuelve la norma euclídea de un vector p."""
    return np.linalg.norm(p)


def psp(p1, p2, q):
    """
    Dado un segmento que va de p1 a p2 y un punto q, esta funcion encuentra
    el punto sobre el segmento a menor distancia de q.

    Parameters:
    ----------
    p1, p2, q: np.array
    """
    # Esto es para manejar el caso p1 == p2
    with np.errstate(divide='raise'):
        try:
            t = np.dot((p2-p1), (q-p1))/(norm(p2-p1)**2)
        except FloatingPointError:
            t = 0

    x = p1 if t <= 0 else p2 if t > 1 else (p2-p1)*t+p1
    return x


def dlist(punto, grafo):
    """
    Función que aplica d para cada arista de un grafo.
    """

    return [psp(grafo[i], grafo[i+1], punto) for i in range(len(grafo)-1)]


def ud(p1, p2, grafo):
    """
    Devuelve una matriz donde cada fila reprensenta una posible subida y
    bajada.
    """
    # Quiero trabajar con conjuntos para evitar elementos repetidos.
    # Para ello usaré tuplas ya que los arrays no son hasheables.

    subidas, bajadas = dlist(p1, grafo), dlist(p2, grafo)
    matrix = set()

    for i, x in enumerate(subidas):
        for j, y in enumerate(bajadas):

            condition = norm(x-grafo[i]) < norm(y-grafo[i])
            if i < j or (i == j and condition):
                matrix.add((tuple(x), tuple(y)))
    # Convierto el conjunto a matriz.
    return np.array(list(matrix))


def nodelenght(i, j, grafo):
    """
    Devuelve la longitud del grafo comprendido entre los puntos i, j.
    """

    lenght = 0
    if i < j:
        for i in range(i, j):
            lenght += norm(grafo[i+1]-grafo[i])

    return lenght


def travelenght(ps, pb, grafo):
    """
    Calcula la distancia viajada entre los puntos ps, pb sobre el grafo.
    """

    ps, pb = np.array(ps), np.array(pb)

    insu = [i for i, x in enumerate(dlist(ps, grafo)) if (x == ps).all()]
    inba = [i for i, x in enumerate(dlist(pb, grafo)) if (x == pb).all()]

    dist = lambda i, j, grafo: norm(ps - grafo[i+1]) - norm(pb - grafo[j+1]) +\
        nodelenght(i+1, j+1, grafo)

    lenght = []
    for i, j in product(insu, inba):
        if i <= j and dist(i, j, grafo) >= 0:
            lenght.append(dist(i, j, grafo))
    if not lenght: return None
    else: return min(lenght)


def walkdistance(pi, pf, ps, pb):
    """
    Se define la c-distancia entre p1 y p2 como abs(p1[0]-p2[0])+abs(p1[1]-\
                                                                     p2[1]).
    Esta función devuelve una lista cuya primera componente es la c-distancia
    de pi-ps y la segunda componente es la distancia pf-pb.
    """

    return [abs(ps[0]-pi[0]) + abs(ps[1]-pi[1]),
            abs(pb[0]-pf[0]) + abs(pb[1] - pf[1])]


def heaviside(p, grafo):
    """
    Devuelve 1 si p esta sobre el grafo 0 en otro caso.
    """
    A = [round(norm(i-p),2) for i in dlist(p, grafo)]
    x = 1 if 0 in A else 0
    return x


# Forma cheta (que no me sirve) de definirse la heaviside usando funciones \
# lambda
# heaviside = lambda x: 0.5 if x == 0 else 0 if x < 0 else 1

def solapamiento_local(p, info=False, data=dataBase):
    """
    Calcula el solapamiento en un dado punto p asumiendo una base de datos.
    """

    lineas = []

    for linea in data:

        if heaviside(p, data[linea]): lineas.append(linea)

    if info == False: return len(lineas)
    else: return lineas


def score(pi, pf, ps, pb, grafo, k=4):
    if travelenght(ps, pb, grafo) != None:
        score = travelenght(ps, pb, grafo)+k*sum(walkdistance(pi, pf, ps, pb))
    else: score = 999

    return int(score)

def time_travel(ps,pb,grafo):
    p = lambda i: 0.5*(grafo[i]+grafo[i+1])

    for p in enriquecer(grafo):
        grafo = np.array(enriquecer(grafo))
        z = np.array([solapamiento_local(p(i)) for i in range(len(grafo)-1)])
    return z

def uds(pi, pf, dic, k1=10, k2=4):
    """
    Devuelve una tabla de la información de la simulación.
    k1 total dispuesto a caminar
    k2 el weigth factor de score.
    """

    etiquetas = ('pi', 'pf', 'ps', 'pb', 'wd_s','wd_b','Linea', "score")
    table = pd.DataFrame(columns=etiquetas)
    row = 0

    for linea, grafo in dic.items():
        for ps, pb in ud(pi, pf, grafo):

            wd_u, wd_d = np.round(walkdistance(pi, pf, ps, pb),1)

            if wd_u < k1 and wd_d < (k1-wd_u):
                sc = score(pi, pf, ps, pb, grafo, k2)
                ps, pb = np.round(ps,2), np.round(pb,1)
                table.loc[row] = pi, pf, ps, pb, wd_u, wd_d, linea, sc
                row += 1
    return table.sort_values('score').reset_index(drop=True)


def pointGen():
    """
    Genera un punto al azar.
    """

    x, y = RI(-7, 32), RI(32, 72)
    return (x, y)


def personGen(x):
    """Crea puntos inciiales y finales con una distancia mayor a x"""

    pi, pf = pointGen(), pointGen()
    while abs(pi[0]-pf[0]) + abs(pi[1]-pf[1]) <= x:
        pi, pf = pointGen(), pointGen()
    return pi,pf


poblacion = lambda n,x: [personGen(x) for i in range(n)]

dfs = []

for pi,pf in poblacion(10,10):
    dfs.append(uds(pi,pf,dataBase)[:4])

dfs = pd.concat(dfs, axis=0)


