import sys
import os
import string

file = open("el_caps_noaccent.dict", "r",encoding='utf8')
greek_leksiko = file.read()
greek_leksiko = greek_leksiko.split()
file.close()

Greek_Alphabet = ['Α','Β','Γ','Δ','Ε','Ζ','Η','Θ','Ι','Κ','Λ','Μ','Ν','Ξ','Ο','Π','Ρ','Σ','Τ','Υ','Φ','Χ','Ψ','Ω']

file = open("L_fst.txt","w")
word_buffer = []
final_states = []
state_count = 0
file.write('0 0 eps eps\n')

for i in range (0,len(greek_leksiko)):
    word_buffer = greek_leksiko[i]
    char_seq = list(word_buffer)
    if(len(char_seq) == 1):
        arg = ['0',' ',str(state_count+1),' ',char_seq[0],' ',char_seq[0],'\n']
        arg = ''.join(arg)
        file.write(arg)
        state_count += len(char_seq)
        final_states.append(str(state_count))
    else:
        arg = ['0',' ',str(state_count+1),' ',char_seq[0],' ','eps','\n']
        arg = ''.join(arg)
        file.write(arg)
        for j in range(1,len(char_seq)):
            if(j==len(char_seq)-1):
                arg = [str(j + state_count),' ',str(j+1 + state_count),' ',char_seq[j],' ',word_buffer,'\n']
            else:
                arg = [str(j + state_count),' ',str(j+1 + state_count),' ',char_seq[j],' ','eps','\n']
            arg = ''.join(arg)
            file.write(arg)
        state_count += len(char_seq)
        final_states.append(str(state_count))
for i in range(0,len(final_states)):
    arg = [final_states[i],'\n']
    arg = ''.join(arg)
    file.write(arg)
file.close()

