import sys
import os
import string
import fileinput

greng_test = []
tmp = (sys.argv[1])
greng_test.append(tmp)

file=open('correct_fst.txt','w')
arg = ['0 1 ',tmp,'\n']
arg = ''.join(arg)
file.write(arg)
file.write('1')
file.close()

