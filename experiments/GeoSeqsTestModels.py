'''
Main program to run tests on geographical sequences
'''
## TODO: write specific code for import methods for each dataset ?

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
import LoadPortoTaxisData
import LoadLlyodsData

### PARAMETERS
### (Should list all variables for the experiments)
len_test = 3
dataset = 'PortoTaxis'
# dataset = 'Ports'
min_k = 1  ## minimum context length
max_k = 3  ## maximum context length

## for Geo models
## TODO: Search procedure to automatically find the best gamma value ?
gamma = 0.0000001
dist_fun = GeoFixOrderModel.Dists[GeoFixOrderModel.DistCalc.HAVERSINE]

### Load Dataset
sequences = []
locations = []
if dataset == 'PortoTaxis':
    dist_fun = GeoFixOrderModel.Dists[GeoFixOrderModel.DistCalc.EUCLIDIAN]
    sequences = LoadPortoTaxisData.getSequences(False, 0)
    sequences = DataModUtils.removeRepetitions(sequences)
    categories = LoadPortoTaxisData.getCategories()
    locations = LoadPortoTaxisData.getLocations()
if dataset == 'Ports':
    sequences = LoadLlyodsData.getSequences()
    sequences = DataModUtils.removeRepetitions(sequences)
    locations = LoadLlyodsData.getLocations()
    categories = LoadLlyodsData.getCategories()
    sequences = LoadLlyodsData.filterSequences(sequences, categories)

print "Nb Seqs : " + str(len(sequences))

### Create Training/Testing subsets
training, test_contexts, testing = [], [], []
if dataset == 'PortoTaxis':
    training, testing = DataModUtils.cutEndOfSequences(sequences, len_test)
    test_contexts = training
if dataset == 'Ports':
    training, testing = DataModUtils.cutEndOfSequences(sequences, len_test)
    test_contexts = training
## TODO: perform test not only on the last symbol in training sequence
## 		instead split all sequences into to set at random (training and testing)
##		and compute the prediction score by an average on the proba of
##		symbols in each seq of sequences after the first k symbols (context)

### Get the unique list of symbols found in sequences
alphabet = SeqStats.symbols(sequences)
if dataset == 'Ports':
    alphabet = LoadLlyodsData.filterAlphabet(alphabet, categories)

print "Nb Symbols : " + str(len(alphabet))

### Filter locations (to match alphabet)
loc_temp = dict()
for a in alphabet:
    if a in locations.keys():
        loc_temp[a] = locations[a]
locations = loc_temp
print "Nb Locations :" + str(len(locations.keys()))


### Set functions use to compare models
def averageProbNextKSymbols(model, test_contexts, test_seqs, k):
    ## TODO: create file with evaluation functions including this one
    ## TODO: Test one using the distance between prediction and real location
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
