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
import GeoFixOrderModel
import CategoriesModel
import HONModel

sys.path.append(''.join([os.path.dirname(__file__), '/..', '/data/']))
import LoadLlyodsData

### PARAMETERS
### (Should list all variables for the experiments)
len_test = 3
min_k = 1  ## minimum context length
max_k = 3  ## maximum context length

## for Geo models
# TODO: Use search procedure to automatically find the best gamma value
## (findBestSpreadGeo)
gamma = 0.0000001
dist_fun = GeoFixOrderModel.Dists[GeoFixOrderModel.DistCalc.HAVERSINE]

### Load Dataset
sequences = []
locations = []

sequences = LoadLlyodsData.getSequences()
sequences = DataModUtils.removeRepetitions(sequences)
locations = LoadLlyodsData.getLocations()
categories = LoadLlyodsData.getCategories()
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

### Filter locations (to match alphabet)
loc_temp = dict()
for a in alphabet:
    if a in locations.keys():
        loc_temp[a] = locations[a]
locations = loc_temp
print "Nb Locations :" + str(len(locations.keys()))

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


## Init variables of GeoFixOrderModel
max_d = GeoFixOrderModel.getMaxDistance(locations, dist_fun)
sum_d = GeoFixOrderModel.sumDensities(alphabet, locations, gamma, max_d, dist_fun)

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

    geo = GeoFixOrderModel.GeoFixOrderModel(i, alphabet, locations, gamma,
                                            dist_fun, max_d, sum_d, False)
    for seq in training:
        geo.learn(seq)

    geo_zp = GeoFixOrderModel.GeoFixOrderModel(i, alphabet, locations, gamma,
                                               dist_fun, max_d, sum_d, True)
    for seq in training:
        geo_zp.learn(seq)


    cat = CategoriesModel.CategoriesModel(i, alphabet, categories)
    for seq in training:
        cat.learn(seq)

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

    probs_geo = averageProbNextKSymbols(geo, test_contexts, testing, len_test)
    print str(geo)
    print "	probs : " + SeqStats.str_probs(probs_geo)
    print "	size  : " + str(geo.size())

    probs_geo_zp = averageProbNextKSymbols(geo_zp, test_contexts, testing, len_test)
    print str(geo_zp)+' ZERO PROB'
    print "	probs : "+ SeqStats.str_probs(probs_geo_zp)
    print "	size  : " + str(geo_zp.size())

    probs_cat = averageProbNextKSymbols(cat, test_contexts, testing, len_test)
    print str(cat)
    print "	probs : " + SeqStats.str_probs(probs_cat)
    print "	size  : " + str(cat.size())

    print
