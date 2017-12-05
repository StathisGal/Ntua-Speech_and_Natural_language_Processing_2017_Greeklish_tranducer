#!/bin/bash

set -e # on error stop

greng_lekseis=$(python3 list_of_english_words.py) # to change it
greek_lekseis=$(python3 list_of_greek_words.py)
# echo $greng_lekseis

# we create 2 lists (greeklish words) and (greek words)
IFS=' ' read -ra lista_greeklish_words <<< $greng_lekseis
IFS=' ' read -ra lista_greek_words <<< $greek_lekseis


swstes_antistoixies=0 # how many words we found correctly
swstes_antistoixies_orth=0 # how many words we found correctly
lathos_antistoixies=0 # how many words we found in dic but weren't the expected
aggliki_swsti=0
aggliki=0
elliniki=0
englishwords=0 # how many of the correctly found words are english
notfound=0 # how many not found

printf "" > lathos #create file for false words


# for ((t=0; t<${#lista_greek_words[@]}; t++)); do
 for ((t=9; t<10; t++)); do
    isenglishword=false
    findindict=false
    expected=false
    echo $t ${lista_greeklish_words[$t]} ${lista_greek_words[$t]}

    # at first we need to create the W.fst --> Greeklish word, GR.fst--> Greek word
    python3 greng_word_to_fst.py ${lista_greeklish_words[$t]}
    python3 greek_word_to_fst.py ${lista_greek_words[$t]}
    fstcompile --acceptor --isymbols=G.syms --osymbols=G.syms  GRENG_fst.txt W.fst
    fstcompile --acceptor --isymbols=G.syms --osymbols=G.syms  GR_fst.txt GR.fst

    #find possible words
    fstarcsort --sort_type=olabel W.fst W_sort.fst
    fstcompose  W_sort.fst T.fst  possible_words.fst
    fstrmepsilon possible_words.fst possible_words.fst
    fstprint --isymbols=G.syms --osymbols=G.syms possible_words.fst foundindict.txt
    if [ $(stat -c%s "foundindict.txt") != 0 ] ; then # means that we found any possible word in both dicts
	#find most possible word and rm epsilon
	fstshortestpath possible_words.fst epilogi.fst
	fstcompose epilogi.fst A1_min.fst isgreek.fst
	fstprint --isymbols=G.syms --osymbols=G.syms isgreek.fst isgreek.txt
	if [ $(stat -c%s "isgreek.txt") != 0 ] ; then
	    # echo "elliniki"
	    elliniki=$((elliniki + 1))
	else # we use else because we know that we found something
	    aggliki=$((aggliki + 1))
	fi;
	
	# check if we found the correct word
	fstproject --project_output=true epilogi.fst swstes_output.fst 
	fstintersect swstes_output.fst  GR.fst expected.fst
	fstprint --isymbols=G.syms --osymbols=G.syms expected.fst expected.txt
	if [ $(stat -c%s "expected.txt") != 0 ] ; then
	    swstes_antistoixies=$((swstes_antistoixies + 1))
	    expected=true
	else
	    set -x
	    fstprint --isymbols=L.syms --osymbols=L.syms swstes_output.fst
	    fstcompose  swstes_output.fst S1_L.fst wrong_L1.fst

	    fstshortestpath --nshortest=2 wrong_L1.fst shortestS1.fst
	    fstprint --isymbols=L.syms --osymbols=L.syms shortestS1.fst

	    fstproject --project_output=true shortestS1.fst solution_S1_output.fst
	    fstrmepsilon solution_S1_output.fst solution_S1_output_cl.fst
	    fstintersect solution_S1_output_cl.fst  correct.fst inter.fst
	    fstprint --isymbols=L.syms --osymbols=L.syms solution_S1_output_cl.fst
	    fstprint --isymbols=L.syms --osymbols=L.syms inter.fst inter.txt
	    if [ $(stat -c%s "inter.txt") != 0 ] ; then
	    	swstes_antistoixies_orth=$((swstes_antistoixies_orth + 1))
	    	echo "Exoyme antistoixia"
	    fi;
	    set +x

	fi;
    else
	echo ${lista_greeklish_words[$t]}
	notfound=$((notfound + 1))
    fi;

done
# echo "Metatrapikan swsta $swstes_antistoixies lekseis ap tis 505" > results.txt
# echo "Ap autes ${elliniki} einai agglikes poy eginan ellinikes" >> results.txt
# echo "kai eixame ${aggliki} agglikes genika" >> results.txt
# echo "Se kanena dic itan ${notfound} lekseis" >> results.txt

echo "Metatrapikan swsta $swstes_antistoixies lekseis ap tis 505"
echo "Ap autes ${elliniki} einai agglikes poy eginan ellinikes"
echo "kai eixame ${aggliki} agglikes genika"
echo "Se kanena dic itan ${notfound} lekseis"
