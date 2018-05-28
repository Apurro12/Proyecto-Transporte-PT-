from random import randint as RI
import time
import numpy as np

print("Empezo")
time.clock()
LR = open("LR","w")


for j in range(0,100000):

    x1 = RI(-7,31)
    x2 = RI(-7,31)
    y1 = RI(32,72)
    y2 = RI(32,72)	
    LR.write(str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2) )
    LR.write( "\n" )

print(time.clock())
