import sys
import os
import string
from math import log

file = open("el_caps_noaccent.dict", "r",encoding='utf8')
greek_leksiko = file.read()
greek_leksiko = greek_leksiko.split()
file.close()

file = open("en_caps_noaccent.dict", "r",encoding='utf8')
english_leksiko = file.read()
english_leksiko = english_leksiko.split()
file.close()

file = open("train_wr.txt", "r",encoding='utf8')
wrong_spelling = file.read()
wrong_spelling = wrong_spelling.split()
file.close()

file = open("train_co.txt", "r",encoding='utf8')
correct_spelling = file.read()
correct_spelling = correct_spelling.split()
file.close()

Greek_Alphabet = ['Α','Β','Γ','Δ','Ε','Ζ','Η','Θ','Ι','Κ','Λ','Μ','Ν','Ξ','Ο','Π','Ρ','Σ','Τ','Υ','Φ','Χ','Ψ','Ω']
English_Alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

insertion_count = 0
deletion_count = 0
replace_count = 0
reorder_count = 0


for i in range(0,len(correct_spelling)):
    if(correct_spelling[i] == wrong_spelling[i]):	#an einai idies oi lekseis sunexizw
        continue;
    correct_letters = list( correct_spelling[i] )
    wrong_letters = list( wrong_spelling[i] )
    j=0
    flag=0

    while ((correct_letters or wrong_letters) and flag<2):
        if(len(correct_letters)==0 and len(wrong_letters) !=0):
            insertion_count +=1
            break
        if(len(wrong_letters)==0 and len(correct_letters) !=0):
            deletion_count += 1
            break
        if((correct_letters[j]==wrong_letters[j])):
            correct_letters.pop(0)
            wrong_letters.pop(0)
        elif(len(correct_letters)>1 and len(wrong_letters)>1):
            if(correct_letters[0]==wrong_letters[1] and correct_letters[1]==wrong_letters[0]):
                flag +=1
                reorder_count+= 1
                correct_letters.pop(0)
                correct_letters.pop(0)
                wrong_letters.pop(0)
                wrong_letters.pop(0)
            elif(correct_letters[0]==wrong_letters[1] and correct_letters[1] != wrong_letters[0]): #insertion
                flag +=1
                insertion_count += 1
                correct_letters.pop(0)
                wrong_letters.pop(0)
                wrong_letters.pop(0)
            elif(correct_letters[1]==wrong_letters[0]):
                flag +=1
                deletion_count += 1                    
                correct_letters.pop(0)
                correct_letters.pop(0)
                wrong_letters.pop(0)
            elif(correct_letters[1]==wrong_letters[1]):
                flag +=1
                replace_count += 1
                correct_letters.pop(0)
                wrong_letters.pop(0)
            else: # in case 2 cosecuative mistakes
                if(len(wrong_letters)>2):
                    if(correct_letters[1]==wrong_letters[2]):
                        flag +=1
                        replace_count += 1
                        correct_letters.pop(0)
                        wrong_letters.pop(0)
                        wrong_letters.pop(0)
                    elif(correct_letters[2] == wrong_letters[1]):
                        flag +=1
                        replace_count += 1
                        correct_letters.pop(0)
                        correct_letters.pop(0)
                        wrong_letters.pop(0)
                    else:
                        replace_count += 1
                        correct_letters.pop(0)
                        wrong_letters.pop(0)
                else:
                    flag +=2
                    replace_count += 2


        elif(len(correct_letters)==1 and len(wrong_letters) > 1):
            if(correct_letters[0]==wrong_letters[1]):
                insertion_count += 1
                correct_letters.pop(0)
                wrong_letters.pop(0)
                wrong_letters.pop(0)
            else:
                replace_count += 1
                break
        elif(len(correct_letters) > 1 and len(wrong_letters) == 1):
            if(correct_letters[1] == wrong_letters[0]):
                deletion_count += 1
                correct_letters.pop(0)
                correct_letters.pop(0)
                wrong_letters.pop(0)
            else:
                replace_count += 1
                break
        else:
            replace_count += 1
            break

sum = insertion_count + deletion_count + replace_count + reorder_count
pos_insert= insertion_count/sum
pos_delete= deletion_count/sum
pos_replace=replace_count/sum
pos_reorder=reorder_count/sum

print("Insert:",pos_insert,"\nDelete:",pos_delete,"\nReplace:",pos_replace,"\nReorder:",pos_reorder)

file = open('I_fst.txt','w')

# file.write('0 0 eps eps\n')

eisagwgi = -log((pos_insert))
diagrafi = -log((pos_delete))
antikatastasi = -log((pos_replace))
reorder= -log((pos_reorder))

for i in range(0,len(Greek_Alphabet)):
    arg = [str(0),' ',str(1),' ',Greek_Alphabet[i],' ',Greek_Alphabet[i],' ',str(0),'\n']
    arg = ''.join(arg)
    file.write(arg)

file.write('1\n')

# for i in range(0,len(Greek_Alphabet)):
#     arg = [str(0),' ',str(i),' ',Greek_Alphabet[i],' ',Greek_Alphabet[i],' ',str(0),'\n']
#     arg = ''.join(arg)
#     file.write(arg)

# file.write('0\n')
# for i in range(1,len(Greek_Alphabet)):
#     arg = [str(i),' ',str(0),' ','eps eps','\n']
#     arg = ''.join(arg)
#     file.write(arg)

file.close()

file = open('E_fst.txt','w')

# file.write('0 0 eps eps\n')

# go to self with 0 weight
for i in range(0,len(Greek_Alphabet)):
    arg = [str(0),' ',str(1),' ',Greek_Alphabet[i],' ',Greek_Alphabet[i],' ',str(0),'\n']
    arg = ''.join(arg)
    file.write(arg)

# insert letter
for i in range(0,len(Greek_Alphabet)):
    arg = ['0 1 eps ',Greek_Alphabet[i],' ',str(eisagwgi),'\n']
    arg = ''.join(arg)
    file.write(arg)

# delete letter
for i in range(0,len(Greek_Alphabet)):
    arg = ['0 1 ',Greek_Alphabet[i],' eps ',str(diagrafi),'\n']
    arg = ''.join(arg)
    file.write(arg)

# replace letter
for i in range(0,len(Greek_Alphabet)):
    for j in range(0,len(Greek_Alphabet)):
        if( Greek_Alphabet[i] != Greek_Alphabet[j]):
            arg = ['0 1 ',Greek_Alphabet[i],' ',Greek_Alphabet[j],' ',str(antikatastasi),'\n']
            arg = ''.join(arg)
            file.write(arg)

# reorder letter

for i in range(0,len(Greek_Alphabet)):
    arg = ['0 ',str(i+2),' ',Greek_Alphabet[i],' eps ',str(reorder),'\n']
    arg = ''.join(arg)
    file.write(arg)

for i in range(0,len(Greek_Alphabet)):
    for j in range(0,len(Greek_Alphabet)):
        if( i != j):
            arg = [str(i+2),' ',str(i+26),' ',Greek_Alphabet[j],' ',Greek_Alphabet[j],' 0\n']
            arg = ''.join(arg)
            file.write(arg)
            arg = [str(i+26),' ',str(1),' eps ',Greek_Alphabet[i],' 0\n']
            arg = ''.join(arg)
            file.write(arg)
file.write('1\n')


# for i in range(0,len(Greek_Alphabet)):
#     arg = ['0 1 eps ',Greek_Alphabet[i],' ',str(eisagwgi),'\n']
#     arg = ''.join(arg)
#     file.write(arg)

# arg = '1 0 eps eps\n'
# file.write(arg)

# for i in range(0,len(Greek_Alphabet)):
#     arg = ['0 2 ',Greek_Alphabet[i],' eps ',str(diagrafi),'\n']
#     arg = ''.join(arg)
#     file.write(arg)

# arg = '2 0 eps eps\n'
# file.write(arg)

# for i in range(0,len(Greek_Alphabet)):
#     arg = ['0 3 ',Greek_Alphabet[i],' eps ',str(antikatastasi),'\n']
#     arg = ''.join(arg)
#     file.write(arg)
# for i in range(0,len(Greek_Alphabet)):
#     arg = ['3 0',' eps ',Greek_Alphabet[i],' 0\n']
#     arg = ''.join(arg)
#     file.write(arg)

# for i in range(0,len(Greek_Alphabet)):
#     arg = ['0 ',str(i+4),' ',Greek_Alphabet[i],' eps ',str(reorder),'\n']
#     arg = ''.join(arg)
#     file.write(arg)

# for i in range(0,len(Greek_Alphabet)):
#     for j in range(0,len(Greek_Alphabet)):
#         if( i != j):
#             arg = [str(i+4),' ',str(i+4+27),' ',Greek_Alphabet[j],' ',Greek_Alphabet[j],' 0\n']
#             arg = ''.join(arg)
#             file.write(arg)
#         arg = [str(i+4+27),' ',str(i+4),' eps ',Greek_Alphabet[i],' 0\n']
#         arg = ''.join(arg)
#         file.write(arg)
#         arg = [str(i+4),' 0 eps eps\n']
# file.write('0\n')

file.close()


file=open('L.syms','w')
file.write('eps'+ ' ' + '0' + '\n')
for i in range(0,26):
    file.write(English_Alphabet[i] + ' '+ str(i+1) + '\n' )
for i in range(0,24):
    file.write(Greek_Alphabet[i]+ ' ' + str(i+27) + '\n' )	
for i in range(0,10): 
    file.write(str(i) + ' ' + str(i+51) +'\n')
for i in range(0,len(greek_leksiko)):
    file.write(greek_leksiko[i] + ' ' + str(i+61) + '\n')
file.close()               

