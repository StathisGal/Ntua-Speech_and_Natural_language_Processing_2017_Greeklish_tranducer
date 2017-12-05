import sys
import os


file = open("test_co.txt", "r")
lekseis = file.read()
lekseis = lekseis.split()
for i in range(0,len(lekseis)):
               print(lekseis[i])
