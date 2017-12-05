#!/bin/bash

## The first commands are the same as the create_fst.sh file
## neeed for prepare lab 1

set -x #echo on
set -e # on error stop

### Prepare lab ###

# sec 1-2
python3 ask1_v2.py

# sec 3 - Dimiourgia metatropea G 
fstcompile -isymbols=G.syms -osymbols=G.syms G_fst.txt G.fst

# sec 4 - Dimiourgia metatropea I
fstcompile -isymbols=G.syms -osymbols=G.syms I_fst.txt I.fst

# sec 5 - Dimiourgia apodoxea A1 gia to elliniko le3iko
fstcompile --acceptor -isymbols=G.syms A1_fst.txt A1.fst
# fstcompile -isymbols=A1.syms -osymbols=A1.syms A1_fst.txt A1.fst
# sec 6 - Metatropi tou A1 se ntetsecministiko kai elaxistopoiisi tou
fstdeterminize A1.fst A1_det.fst
fstminimize A1_det.fst A1_min.fst

# sec 7 - Ta idia vimata gia to A2
fstcompile --acceptor -isymbols=G.syms A2_fst.txt A2.fst
# fstcompile  -isymbols=A2.syms -osymbols=A2.syms A2_fst.txt A2.fst
fstdeterminize A2.fst A2_det.fst
fstminimize A2_det.fst A2_min.fst

### End of prepare lab

# sec 8 - First we find the A1 U A2 and then (A1 U A2) GI which
# we name it T fst

# closure for G,I because we want to accept a lot of letters
fstclosure G.fst G_closure.fst
fstclosure I.fst I_closure.fst

# union because we may have greek or english
fstunion G_closure.fst I_closure.fst GI.fst
fstunion A1_min.fst A2_min.fst union_A1_A2.fst


fstclosure GI.fst GI_closure.fst
fstarcsort GI_closure.fst GI_sort_closure.fst
fstarcsort union_A1_A2.fst union_A1_A2_sort.fst

fstcompose  GI_sort_closure.fst union_A1_A2_sort.fst T.fst

# sec 9
set +x
greng_lekseis=$(python3 list_of_english_words.py) # to change it
greek_lekseis=$(python3 list_of_greek_words.py)

# we create 2 lists (greeklish words) and (greek words)
IFS=' ' read -ra lista_greeklish_words <<< $greng_lekseis
IFS=' ' read -ra lista_greek_words <<< $greek_lekseis

swstes_antistoixies=0 # how many words we found correctly
lathos_antistoixies=0 # how many words we found in dic but weren't the expected
aggliki_swsti=0
aggliki=0
elliniki=0
englishwords=0 # how many of the correctly found words are english
notfound=0 # how many not found

printf "" > lathos #create file for false words


for ((t=0; t<${#lista_greek_words[@]}; t++)); do
    isenglishword=false
    findindict=false
    expected=false
    # echo $t ${lista_greeklish_words[$t]} ${lista_greek_words[$t]}

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
	    echo ${lista_greeklish_words[$t]}
	    echo ${lista_greeklish_words[$t]} >> lathos 
	    lathos_antistoixies=$((lathos_antistoixies + 1))
	fi;
    else
	echo ${lista_greeklish_words[$t]}
	notfound=$((notfound + 1))
    fi;

done
echo "Metatrapikan swsta $swstes_antistoixies lekseis ap tis 505" > results.txt
echo "Ap autes ${elliniki} einai agglikes poy eginan ellinikes" >> results.txt
echo "kai eixame ${aggliki} agglikes genika" >> results.txt
echo "Se kanena dic itan ${notfound} lekseis" >> results.txt

echo "Metatrapikan swsta $swstes_antistoixies lekseis ap tis 505"
echo "Ap autes ${elliniki} einai agglikes poy eginan ellinikes"
echo "kai eixame ${aggliki} agglikes genika"
echo "Se kanena dic itan ${notfound} lekseis"
