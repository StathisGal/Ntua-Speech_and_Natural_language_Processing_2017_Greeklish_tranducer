import sys
import os


file = open("test_greng.txt", "r")
lekseis = file.read()
lekseis = lekseis.split()
for i in range(0,len(lekseis)):
               print(lekseis[i])
