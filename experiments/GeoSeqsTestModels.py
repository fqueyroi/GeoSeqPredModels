'''
Main program to run tests on geographical sequences
'''
## TODO: write specific code for import methods for each dataset ?
## TODO: write to output simple statistics on loaded sequences
##       ie number, min/max/mean length, distribution of length etc.

import sys, os

import DataModUtils
import SeqStats

sys.path.append(''.join([os.path.dirname(__file__), '/..', '/models/']))

import PPMCModel
import FixOrderModel
import ThereAndBackModel
import GeoFixOrderModel
import HONModel

sys.path.append(''.join([os.path.dirname(__file__), '/..', '/data/']))
import LoadPortoTaxisData
import LoadLlyodsData

### PARAMETERS
### (Should list all variables for the experiments)
len_test = 3
# dataset = 'PortoTaxis'
dataset = 'Ports'
min_k = 1 ## minimum context length
max_k = 3 ## maximum context length

### Load Dataset
sequences = []
locations = []
if dataset == 'PortoTaxis':
	sequences = LoadPortoTaxisData.getSequences(False, 0) ## only week 0 to test
	sequences = DataModUtils.removeRepetitions(sequences)
	locations = LoadPortoTaxisData.getLocations()
if dataset == 'Ports':
	sequences = LoadLlyodsData.getSequences()
	sequences = DataModUtils.removeRepetitions(sequences)
	locations = LoadLlyodsData.getLocations()

print "Nb Seqs : "+str(len(sequences))

### Create Training/Testing subsets
training, test_contexts, testing = [], [], []
if dataset == 'PortoTaxis':
	training, testing = DataModUtils.cutEndOfSequences(sequences, len_test)
	test_contexts = training
if dataset == 'Ports':
	training, testing = DataModUtils.cutEndOfSequences(sequences, len_test)
	test_contexts = training

### Get the unique list of symbols found in sequences
alphabet = SeqStats.symbols(sequences)
print "Nb Symbols : "+str(len(alphabet))

### Filter locations (to match alphabet)
loc_temp = dict()
for a in alphabet:
	if a in locations.keys():
		loc_temp[a] = locations[a]
locations = loc_temp
print "Nb Locations :"+str(len(locations.keys()))


### Set functions use to compare models
def averageProbNextKSymbols(model, test_contexts, test_seqs, k):
	## TODO: create file with evaluation functions
	res = [0 for i in range(k)]
	order = model.maxContextLength
	for i in range(len(test_seqs)):
		t_seq = test_seqs[i][:min(k,len(test_seqs[i]))]
		probs = model.probabilites(t_seq,test_contexts[i])
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

	geo = GeoFixOrderModel.GeoFixOrderModel(i, alphabet, locations, 0.05, "haversine")
	for seq in training:
		geo.learn(seq)

	probs_ppmc = averageProbNextKSymbols(ppmc, test_contexts, testing, 3)
	print str(ppmc)
	print "	probs : "+ SeqStats.str_probs(probs_ppmc)
	print "	size  : " + str(ppmc.size())

	probs_tab = averageProbNextKSymbols(tab, test_contexts, testing, len_test)
	print str(tab)
	print "	probs : "+ SeqStats.str_probs(probs_tab)
	print "	size  : " + str(tab.size())

	probs_fix = averageProbNextKSymbols(fix, test_contexts, testing, len_test)
	print str(fix)
	print "	probs : "+ SeqStats.str_probs(probs_fix)
	print "	size  : " + str(fix.size())

	probs_hon = averageProbNextKSymbols(hon, test_contexts, testing, len_test)
	print str(hon)+" PRUNED"
	print "	probs : "+ SeqStats.str_probs(probs_hon)
	print "	size  : " + str(hon.size())

	probs_geo = averageProbNextKSymbols(geo, test_contexts, testing, len_test)
	print str(geo)
	print "	probs : "+ SeqStats.str_probs(probs_geo)
	print "	size  : " + str(geo.size())

	print
