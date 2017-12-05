import sys
import os
import string
import fileinput

greng_test = []
tmp = (sys.argv[1])
greng_test.append(tmp)

file=open('GR_fst.txt','w')
word_buffer = []
final_states = []
state_count = 0
# file.write('0 0 eps \n')
for i in range(0,1):#len(greng_test)/5):
	word_buffer = greng_test[i]
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

