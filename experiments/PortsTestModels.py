import random
import sys, os
sys.path.append(''.join([os.path.dirname(__file__), '/..', '/models/']))

import PPMCModel
import FixOrderModel
import ThereAndBackModel
import GeoFixOrderModel
import HONModel

import ReadWriteUtils

len_test = 3

## TODO: write specific code for import methods for each dataset ?
## TODO: write to output simple statistics on loaded sequences
##       ie number, min/max/mean length, distribution of length etc.

file_path = ''.join([os.path.dirname(__file__), '/..', '/data/Lloyds_maritime/apr2009_oct2009/portseq_apr2009_oct2009.csv'])
place_file_path = ''.join([os.path.dirname(__file__), '/..', '/data/Lloyds_maritime/table_places.csv'])
locations = ReadWriteUtils.readLocations(place_file_path,4,6,7)

sequences = ReadWriteUtils.readFile(file_path, True, ' ')
#sequences = ReadWriteUtils.removeRepetitions(sequences)
training, testing = ReadWriteUtils.cutEachSequences(sequences, len_test)
test_contexts = training

print "Nb Seqs : "+str(len(sequences))

alphabet = ReadWriteUtils.symbols(sequences)
print "Nb Symbols : "+str(len(alphabet))

loc_temp = dict()
for a in alphabet:
	if a in locations.keys():
		loc_temp[a] = locations[a]
locations = loc_temp
print "Nb Locations :"+str(len(locations.keys()))

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


## TODO: write prog to output results in a file
for i in range(1,3):
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

	geo = GeoFixOrderModel.GeoFixOrderModel(i, alphabet, locations, 0.01)
	for seq in training:
		geo.learn(seq)

	probs_ppmc = averageProbNextKSymbols(ppmc, test_contexts, testing, 3)
	print str(ppmc)
	print "	probs : "+ ReadWriteUtils.str_probs(probs_ppmc)
	print "	size  : " + str(ppmc.size())

	probs_tab = averageProbNextKSymbols(tab, test_contexts, testing, len_test)
	print str(tab)
	print "	probs : "+ ReadWriteUtils.str_probs(probs_tab)
	print "	size  : " + str(tab.size())

	probs_fix = averageProbNextKSymbols(fix, test_contexts, testing, len_test)
	print str(fix)
	print "	probs : "+ ReadWriteUtils.str_probs(probs_fix)
	print "	size  : " + str(fix.size())

	probs_hon = averageProbNextKSymbols(hon, test_contexts, testing, len_test)
	print str(hon)+" PRUNED"
	print "	probs : "+ ReadWriteUtils.str_probs(probs_hon)
	print "	size  : " + str(hon.size())

	probs_geo = averageProbNextKSymbols(geo, test_contexts, testing, len_test)
	print str(geo)
	print "	probs : "+ ReadWriteUtils.str_probs(probs_geo)
	print "	size  : " + str(geo.size())

	print
