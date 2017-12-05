import sys
import os
import string
from math import log
def isGreek(s):
    try:
        s.encode('ascii')
    except UnicodeEncodeError:
        return True
    else:
        return False

file = open("el_caps_noaccent.dict", "r",encoding='utf8')
greek_leksiko = file.read()
greek_leksiko = greek_leksiko.split()
file.close()

file = open("en_caps_noaccent.dict", "r",encoding='utf8')
english_leksiko = file.read()
english_leksiko = english_leksiko.split()
file.close()

file = open("train_gr.txt", "r",encoding='utf8')
greek = file.read()
greek = greek.split()
file.close()

file = open("train_greng.txt", "r")
greeklish = file.read() # read from greeklish file
greeklish = greeklish.split()
file.close()

lekseis_len = len(greeklish)
greek_lekseis = []
idio_mikos_greek = []
idio_mikos_greeklish = []
different_mikos_greek_1_letter = []
different_mikos_greeklish_1_letter = []
more_greek = []
more_greeklish = []
English_Alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
Greek_Alphabet = ['Α','Β','Γ','Δ','Ε','Ζ','Η','Θ','Ι','Κ','Λ','Μ','Ν','Ξ','Ο','Π','Ρ','Σ','Τ','Υ','Φ','Χ','Ψ','Ω']


for i in range(0, lekseis_len):
    if (isGreek(greek[i])):
        greek_lekseis.append(greek[i])
        if (len(greek[i]) == len(greeklish[i])):
            idio_mikos_greek.append(greek[i])
            idio_mikos_greeklish.append(greeklish[i])
        elif(abs(len(greek[i])- len(greeklish[i]))==1):
            different_mikos_greek_1_letter.append(greek[i])
            different_mikos_greeklish_1_letter.append(greeklish[i])
        else:
            more_greek.append(greek[i])
            more_greeklish.append(greeklish[i])
    else:
        continue

grammata_greek = list(idio_mikos_greek[0])
grammata_english = list(idio_mikos_greeklish[0])
print( grammata_greek)

varoi_grammatwn = {(grammata_greek[0],grammata_english[0]) : 1}
antistixies_grammatwn = [(grammata_english[0],grammata_greek[0])]

for i in range(1, len(grammata_english)):
    temp = varoi_grammatwn.get((grammata_greek[i],grammata_english[i]), "None")
    if(temp == "None"):
        varoi_grammatwn[(grammata_greek[i],grammata_english[i])] = 1
        antistixies_grammatwn.append((grammata_english[i],grammata_greek[i]))
    else:
        varoi_grammatwn[(grammata_greek[i],grammata_english[i])] += 1

for i in range(1, len(idio_mikos_greek)):
    grammata_greek = list(idio_mikos_greek[i])
    grammata_english = list(idio_mikos_greeklish[i])
    
    for j in range(0,len(grammata_english)):
        temp =varoi_grammatwn.get((grammata_greek[j], grammata_english[j]), "None")       
        if(temp == "None"):
            varoi_grammatwn[(grammata_greek[j],grammata_english[j])] = 1
            antistixies_grammatwn.append((grammata_english[j],grammata_greek[j]))
        else:
            varoi_grammatwn[(grammata_greek[j],grammata_english[j])] += 1

fores_1 = 0
fores_reverse = 0
for i in range(0,len(different_mikos_greeklish_1_letter)):
    grammata_greek = list(different_mikos_greek_1_letter[i])
    grammata_english = list(different_mikos_greeklish_1_letter[i])
    if(len(grammata_greek) > len(grammata_english)):
        max_varos_word = 0
        max_varos_word_reverse = 0
        case = -1
        case_reverse = 1
        for j in range(0, len(grammata_english)): # j is the number of letters of cases
            varos_word = 0
            step = 0;
            for l in range(0,len(grammata_english)): # l is for any case we want to search and find Weight
                if( l == j):
                    step +=1
                    temp = varoi_grammatwn.get(((grammata_greek[j]+grammata_greek[j+1]),grammata_english[j]),"None")
                    if (temp == "None"):
                        continue
                    else:
                        varos_word += temp
                else:
                    temp = varoi_grammatwn.get((grammata_greek[l+step],grammata_english[l]),"None")
                    if (temp == "None"):
                        continue
                    else:
                        varos_word += temp
            if (varos_word > max_varos_word):
                max_varos_word = varos_word
                case = j
                

        grammata_english.reverse()
        grammata_greek.reverse()

        for j in range(0, len(grammata_english)): # j is the number of letters of cases
            varos_word = 0
            step = 0;

            for l in range(0,len(grammata_english)): # l is for any case we want to search and find Weight
                if( l == j):
                    step +=1
                    temp = varoi_grammatwn.get((grammata_greek[j]+grammata_greek[j+1],(grammata_english[j])),"None")
                    if (temp == "None"):
                        continue
                    else:
                        varos_word += temp
                else:
                    temp = varoi_grammatwn.get((grammata_greek[l+step],grammata_english[l]),"None")
                    if (temp == "None"):
                        continue
                    else:
                        varos_word += temp
            if (varos_word > max_varos_word_reverse):
                max_varos_word_reverse = varos_word
                case_reverse = j

        if ( max_varos_word >= max_varos_word_reverse):
            grammata_english.reverse()
            grammata_greek.reverse()
        else:
            print(grammata_english, grammata_greek)
            case = case_reverse
            

        step = 0
        for l in range(0,len(grammata_english)): # l is for any case we want to search and find Weight
                if( l == case):
                    step +=1
                    temp = varoi_grammatwn.get(((grammata_greek[l]+grammata_greek[l+1]),(grammata_english[l])),"None")
                    if (temp == "None"):

                        insert = (grammata_greek[l]+grammata_greek[l+1])
                        varoi_grammatwn[(insert),(grammata_english[l])]= 1
                        antistixies_grammatwn.append(((grammata_english[l]),insert))
                    else:
                        varoi_grammatwn[(grammata_greek[l]+grammata_greek[l+1]),(grammata_english[l])] += 1
                else:
                    temp = varoi_grammatwn.get(((grammata_greek[l+step],grammata_english[l])),"None")
                    if (temp == "None"):
                        antistixies_grammatwn.append((grammata_english[l],grammata_greek[l]))
                        varoi_grammatwn[grammata_greek[l+step],(grammata_english[l])]= 1
                    else:
                        varoi_grammatwn[grammata_greek[l+step],(grammata_english[l])] += 1
     
    else:
        max_varos_word = 0
        max_varos_word_reverse = 0
        case = -1
        case_reverse = 1
        for j in range(0, len(grammata_greek)): # j is the number of letters of cases
            varos_word = 0
            step = 0;
            for l in range(0,len(grammata_greek)): # l is for any case we want to search and find Weight
                if( l == j):
                    step +=1
                    temp = varoi_grammatwn.get((grammata_greek[j],(grammata_english[j]+grammata_english[j+1])),"None")
                    if (temp == "None"):
                        continue
                    else:
                        varos_word += temp
                else:
                    temp = varoi_grammatwn.get((grammata_greek[l],grammata_english[l+step]),"None")
                    if (temp == "None"):
                        continue
                    else:
                        varos_word += temp
            if (varos_word > max_varos_word):
                max_varos_word = varos_word
                case = j
                

        grammata_english.reverse()
        grammata_greek.reverse()

        for j in range(0, len(grammata_greek)): # j is the number of letters of cases
            varos_word = 0
            step = 0;

            for l in range(0,len(grammata_greek)): # l is for any case we want to search and find Weight
                if( l == j):
                    step +=1
                    temp = varoi_grammatwn.get((grammata_greek[j],(grammata_english[j]+grammata_english[j+1])),"None")
                    if (temp == "None"):
                        continue
                    else:
                        varos_word += temp
                else:
                    temp = varoi_grammatwn.get((grammata_greek[l],grammata_english[l+step]),"None")
                    if (temp == "None"):
                        continue
                    else:
                        varos_word += temp
            if (varos_word > max_varos_word_reverse):
                max_varos_word_reverse = varos_word
                case_reverse = j

        if ( max_varos_word >= max_varos_word_reverse):
            grammata_english.reverse()
            grammata_greek.reverse()
        else:
            print (grammata_english, grammata_greek)
            case =  case_reverse
            fores_reverse +=1
            
        step = 0
        for l in range(0,len(grammata_greek)): # l is for any case we want to search and find Weight
                if( l == case):
                    step +=1
                    temp = varoi_grammatwn.get((grammata_greek[l],(grammata_english[l]+grammata_english[l+1])),"None")
                    if (temp == "None"):
                        insert = (grammata_english[l]+grammata_english[l+1])
                        varoi_grammatwn[grammata_greek[l],insert]= 1
                        antistixies_grammatwn.append(((insert),(grammata_greek[l])))
                    else:
                        varoi_grammatwn[grammata_greek[l],(grammata_english[l]+grammata_english[l+1])] += 1
                else:
                    temp = varoi_grammatwn.get((grammata_greek[l],grammata_english[l+step]),"None")
                    if (temp == "None"):
                        print("Episis perierga pragmata ", (grammata_english[l],grammata_greek[l]))
                        antistixies_grammatwn.append((grammata_english[l],grammata_greek[l]))
                        varoi_grammatwn[grammata_greek[l],(grammata_english[l+step])]= 1
                    else:
                        varoi_grammatwn[grammata_greek[l],(grammata_english[l+step])] += 1

print(varoi_grammatwn)                                # varoi grammatwn == { ellinixa_grammata, agglika_grammata} : varos
print(antistixies_grammatwn)                          # antistoixies grammatwn = [(agglika_grammata, ellinika grammata)]

#Create G.syms containing all letter both greek and english


# file=open('G.syms','w')
# file.write('eps 0'+'\n')
# counter = 0
# for i in range(len(antistixies_grammatwn)):
#     arg = [str(antistixies_grammatwn[i][0]),' ',str(counter+1)]
#     counter = counter+1
#     arg = ''.join(arg)
#     file.write(arg+'\n')
#     arg = [str(antistixies_grammatwn[i][1]),' ',str(counter+1)]
#     counter = counter + 1
#     arg = ''.join(arg)
#     file.write(arg+'\n')
# file.write(''.join(['Q',' ',str(len(antistixies_grammatwn)),'\n'])) # we forgot Q

file=open('G.syms','w')
file.write('eps'+ ' ' + '0' + '\n')
for i in range(0,26):
	file.write(English_Alphabet[i] + ' '+ str(i+1) + '\n' )
for i in range(0,24):
	file.write(Greek_Alphabet[i]+ ' ' + str(i+27) + '\n' )	
for i in range(0,10):
	file.write(str(i) + ' ' + str(i+51) +'\n')

file.close()



#Create G FST

file = open('G_fst.txt','w')
arith=0
for j in range(0,len(antistixies_grammatwn)):
    # vriskw varos
    try:
        weight = -log(varoi_grammatwn[(antistixies_grammatwn[j][1],antistixies_grammatwn[j][0])]/63)
    except KeyError:
        weight = -log(0.001)   #varoi_grammatwn[(antistixies_grammatwn[i][0],antistixies_grammatwn[i][1])]
    aristero = list(antistixies_grammatwn[j][0])
    deksia = list(antistixies_grammatwn[j][1])
    print(len(aristero),len(deksia),j)
    if(len(aristero)==2 and len(deksia)==1):
        print("diplo aristera", aristero,j)
        arg = ['0',' ',str(arith),' ',aristero[0],' ','eps',' ',str(weight),'\n']
        arg=''.join(arg)
        file.write(arg)
        arg = [str(arith),' ',str(arith+1),' ',aristero[1],' ',antistixies_grammatwn[j][1],' ',str(weight),'\n']
        arg=''.join(arg)
        file.write(arg)
        arith+=2
    elif(len(aristero)==1 and len(deksia)==2):
        print("diplo deksia", deksia,j)
        arg = ['0',' ',str(arith),' ',antistixies_grammatwn[j][0],' ',deksia[0],' ',str(weight),'\n']
        arg=''.join(arg)
        file.write(arg)
        arg = [str(arith),' ',str(arith+1),' ','eps',' ',deksia[1],' ',str(weight),'\n']
        arg=''.join(arg)
        file.write(arg)
        arith+=2
    else:
        arg = ['0',' ',str(arith),' ',antistixies_grammatwn[j][0],' ',antistixies_grammatwn[j][1],' ',str(weight),'\n']
        arg=''.join(arg)
        file.write(arg)
        arith+=1

        
for i in range(0,arith-1):
    try:
        weight = -log(varoi_grammatwn[(antistixies_grammatwn[j][1],antistixies_grammatwn[j][0])]/63)
    except KeyError:
        weight = -log(0.001)   #varoi_grammatwn[(antistixies_grammatwn[i][0],antistixies_grammatwn[i][1])]
    arg = [str(i+1),' ',str(weight),'\n']
    arg = ''.join(arg)
    file.write(arg)
file.close()

#Create I fst
file = open('I_fst.txt','w')
for i in range(0,len(English_Alphabet)):
    arg = [str(0),' ',str(i+1),' ',English_Alphabet[i],' ',English_Alphabet[i],' ',str(-log(0.0001)),'\n']
    arg = ''.join(arg)
    file.write(arg)
for i in range(0,len(English_Alphabet)):
	arg = [str(i+1),' ',str(-log(0.0001)),'\n']
	arg = ''.join(arg)
	file.write(arg)
file.close()

#time to create the Greek FSA yeahhhhh
file = open('A1_fst.txt','w')
word_buffer = []
final_states = []
state_count = 0
file.write('0 0 eps\n')
for i in range(0,len(greek_leksiko)):
	word_buffer = greek_leksiko[i]
	char_seq = list(word_buffer)
	if(len(char_seq) == 1):
		arg = ['0',' ',str(state_count+1),' ',char_seq[0],'\n']
		arg = ''.join(arg)
		file.write(arg)
		state_count += len(char_seq)
		final_states.append(str(state_count))
	else:
		arg = ['0',' ',str(state_count+1),' ',char_seq[0],'\n']
		arg = ''.join(arg)
		file.write(arg)
		for j in range(1,len(char_seq)):
			arg = [str(j + state_count),' ',str(j+1 + state_count),' ',char_seq[j],'\n']
			arg = ''.join(arg)
			file.write(arg)
		state_count += len(char_seq)
		final_states.append(str(state_count))
for i in range(0,len(final_states)):
	arg = [final_states[i],'\n']
	arg = ''.join(arg)
	file.write(arg)
file.close()

file=open('A2_fst.txt','w')
word_buffer = []
final_states = []
state_count = 0
file.write('0 0 eps\n')
for i in range(0,len(english_leksiko)):
	word_buffer = english_leksiko[i]
	char_seq = list(word_buffer)
	if(len(char_seq) == 1):
		arg = ['0',' ',str(state_count+1),' ',char_seq[0],'\n']
		arg = ''.join(arg)
		file.write(arg)
		state_count += len(char_seq)
		final_states.append(str(state_count))
	else:
		arg = ['0',' ',str(state_count+1),' ',char_seq[0],'\n']
		arg = ''.join(arg)
		file.write(arg)
		for j in range(1,len(char_seq)):
			arg = [str(j + state_count),' ',str(j+1 + state_count),' ',char_seq[j],'\n']
			arg = ''.join(arg)
			file.write(arg)
		state_count += len(char_seq)
		final_states.append(str(state_count))
for i in range(0,len(final_states)):
	arg = [final_states[i],'\n']
	arg = ''.join(arg)
	file.write(arg)
file.close()



