import sys
import os


file = open("test_wr.txt", "r")
lekseis = file.read()
lekseis = lekseis.split()
for i in range(0,len(lekseis)):
               print(lekseis[i])
