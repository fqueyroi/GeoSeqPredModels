'''
Main program to run tests on geographical sequences on Lloyds_maritime data set
'''
## TODO: write specific code for import methods for each dataset

import sys, os

import DataModUtils
import SeqStats

sys.path.append(''.join([os.path.dirname(__file__), '/..', '/models/']))

import PPMCModel
import FixOrderModel
import ThereAndBackModel
import CategoriesModel
import HONModel
import CategoriesAndSymbolModel

sys.path.append(''.join([os.path.dirname(__file__), '/..', '/data/']))
import LoadAirportsData

### PARAMETERS
### (Should list all variables for the experiments)
len_test = 3
min_k = 1  ## minimum context length
max_k = 3  ## maximum context length


### Load Dataset
sequences = []

sequences = LoadAirportsData.getSequences()
sequences = DataModUtils.removeRepetitions(sequences)
categories = LoadAirportsData.getCategories()
sequences = DataModUtils.filterSequences(sequences, categories)

print "Nb Seqs : " + str(len(sequences))

### Create Training/Testing subsets
training, test_contexts, testing = [], [], []
training, testing = DataModUtils.cutEndOfSequences(sequences, len_test)
test_contexts = training


### Get the unique list of symbols found in sequences
alphabet = SeqStats.symbols(sequences)
alphabet = DataModUtils.filterAlphabet(alphabet, categories)

print "Nb Symbols : " + str(len(alphabet))

# TODO: test with functions in file EvalFunctions
### Set functions use to compare models
def averageProbNextKSymbols(model, test_contexts, test_seqs, k):

    res = [0 for i in range(k)]
    order = model.maxContextLength
    for i in range(len(test_seqs)):
        t_seq = test_seqs[i][:min(k, len(test_seqs[i]))]
        probs = model.probabilites(t_seq, test_contexts[i])
        # print "Probs = "+str(probs)
        p_temp = 1.
        for j in range(len(t_seq)):
            p_temp *= probs[j]
            res[j] += p_temp / (len(test_seqs) + 0.)
    return res


## TODO: output results in a file
for i in range(min_k, max_k + 1):
    ppmc = PPMCModel.PPMCModel(i, alphabet)
    for seq in training:
        ppmc.learn(seq)

    tab = ThereAndBackModel.ThereAndBackModel(i, alphabet)
    for seq in training:
        tab.learn(seq)

    hon = HONModel.HONModel(i, alphabet)
    for seq in training:
        hon.learn(seq)
    hon.prune()

    fix = FixOrderModel.FixOrderModel(i, alphabet)
    for seq in training:
        fix.learn(seq)

    cat = CategoriesModel.CategoriesModel(i, alphabet, categories)
    for seq in training:
        cat.learn(seq)

    catS = CategoriesAndSymbolModel.CategoriesAndSymbolModel(i, alphabet, categories)
    for seq in training:
        catS.learn(seq)

    probs_ppmc = averageProbNextKSymbols(ppmc, test_contexts, testing, len_test)
    print str(ppmc)
    print "	probs : " + SeqStats.str_probs(probs_ppmc)
    print "	size  : " + str(ppmc.size())

    probs_tab = averageProbNextKSymbols(tab, test_contexts, testing, len_test)
    print str(tab)
    print "	probs : " + SeqStats.str_probs(probs_tab)
    print "	size  : " + str(tab.size())

    probs_fix = averageProbNextKSymbols(fix, test_contexts, testing, len_test)
    print str(fix)
    print "	probs : " + SeqStats.str_probs(probs_fix)
    print "	size  : " + str(fix.size())

    probs_hon = averageProbNextKSymbols(hon, test_contexts, testing, len_test)
    print str(hon) + " PRUNED"
    print "	probs : " + SeqStats.str_probs(probs_hon)
    print "	size  : " + str(hon.size())


    probs_cat = averageProbNextKSymbols(cat, test_contexts, testing, len_test)
    print str(cat)
    print "	probs : " + SeqStats.str_probs(probs_cat)
    print "	size  : " + str(cat.size())

    probs_catS = averageProbNextKSymbols(catS, test_contexts, testing, len_test)
    print str(catS)
    print "	probs : " + SeqStats.str_probs(probs_catS)
    print "	size  : " + str(catS.size())

    print
