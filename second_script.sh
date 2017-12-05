#!/bin/bash

set -x
### ORTHOGRAFOS ###
python3 train_orthografo.py
python3 create_L.py

# create L fst
fstcompile --isymbols=L.syms --osymbols=L.syms L_fst.txt L.fst
fstdeterminize L.fst L_det.fst
fstminimize L_det.fst L_min.fst

# Create S1 fst
fstcompile --isymbols=L.syms --osymbols=L.syms I_fst.txt I.fst
fstcompile --isymbols=L.syms --osymbols=L.syms E_fst.txt E.fst
fstclosure I.fst I_star.fst
fstconcat I_star.fst E.fst I_E.fst
fstconcat I_E.fst I_star.fst S1.fst

# Create S2 fst
fstconcat S1.fst E.fst S1_I_E.fst
fstconcat S1_I_E.fst I_star.fst S2.fst

# Create S1_L
fstminimize --allow_nondet=true S1.fst S1.fst
fstarcsort --sort_type=olabel S1.fst S1.fst
fstcompose S1.fst L_min.fst S1_L.fst

# Create S2_L
fstminimize --allow_nondet=true S2.fst S2.fst
fstarcsort --sort_type=olabel S2.fst S2.fst
fstcompose S2.fst L_min.fst S2_L.fst

correct_lekseis=$(python3 list_of_correct_words.py)
wrong_lekseis=$(python3 list_of_wrong_words.py)
IFS=' ' read -ra lista_correct_words <<< $correct_lekseis
IFS=' ' read -ra lista_wrong_words <<< $wrong_lekseis



swstes_antistoixies_S1=0
swstes_antistoixies_S2=0
lathos_lekseis=0
for ((t=0; t<${#lista_correct_words[@]}; t++)); do

    # echo $t ${lista_wrong_words[$t]} ${lista_correct_words[$t]}
    if [[  ${lista_correct_words[$t]} == ${lista_wrong_words[$t]} ]]; then
       continue;
    fi;
    lathos_lekseis=$((lathos_lekseis+1))
    python3 correct_to_fst.py ${lista_correct_words[$t]}
    python3 wrong_to_fst.py ${lista_wrong_words[$t]} 

    fstcompile --acceptor --isymbols=L.syms --osymbols=L.syms correct_fst.txt correct.fst
    fstcompile --acceptor --isymbols=L.syms --osymbols=L.syms wrong_fst.txt wrong.fst

    fstrmepsilon correct.fst correct.fst
    fstrmepsilon wrong.fst wrong.fst
    
    fstcompose  wrong.fst S1_L.fst wrong_L1.fst

    fstshortestpath wrong_L1.fst shortestS1.fst
    fstproject --project_output=true shortestS1.fst solution_S1_output.fst
    fstrmepsilon solution_S1_output.fst solution_S1_output_cl.fst
    fstintersect solution_S1_output_cl.fst  correct.fst inter.fst
    fstprint --isymbols=L.syms --osymbols=L.syms solution_S1_output_cl.fst
    fstprint --isymbols=L.syms --osymbols=L.syms inter.fst inter.txt
    if [ $(stat -c%s "inter.txt") != 0 ] ; then
    	swstes_antistoixies_S1=$((swstes_antistoixies_S1 + 1))
    	echo "Exoyme antistoixia ${lista_wrong_words[$t]}"
    fi;
    
    # fstcompose wrong.fst S2_L.fst wrong_L2.fst

    # fstshortestpath wrong_L2.fst shortestS2.fst 
    # fstproject --project_output=true shortestS2.fst solution_S2_output.fst
    # fstrmepsilon solution_S2_output.fst solution_S2_output_cl.fst
    # fstintersect solution_S2_output_cl.fst  correct.fst inter2.fst
    # fstprint --isymbols=L.syms --osymbols=L.syms inter2.fst inter2.txt
    # if [ $(stat -c%s "inter.txt") != 0 ] ; then
    # 	swstes_antistoixies_S1=$((swstes_antistoixies_S1 + 1))
    # 	echo "Exoyme antistoixia ${lista_wrong_words[$t]}"
    # fi;


done
echo "Exw $swstes_antistoixies_S1 antistoixies me to S1"
# echo "kai $swstes_antistoixies_S2 antistoixies me to S2"
echo "apo tis $lathos_lekseis lathos lekseis"

