'''
Main program to run tests on models using generated data
'''
import sys, os

import DataModUtils
import SeqStats

sys.path.append(''.join([os.path.dirname(__file__), '/..', '/models/']))

import PPMCModel
import FixOrderModel
import ThereAndBackModel
import GeoFixOrderModel
import HONModel
import CategoriesModel
import CategoriesAndSymbolModel

sys.path.append(''.join([os.path.dirname(__file__), '/..', '/data/generators/']))
import LocationBasedGenerator
import CategoriesBasedGenerator
import CategoriesAndSymbolBasedGenerator


choices = ["Location","Categories", "CategoriesSymb"]
generator = choices[2]

### PARAMETERS
### (Should list all variables for the experiments)
min_k = 1 ## minimum context length
max_k = 1 ## maximum context length
len_test = 2

## Generate datasets
if generator == "Location":
	gamma =  0.01
	dist_fun = GeoFixOrderModel.Dists[GeoFixOrderModel.DistCalc.EUCLIDIAN]
	gen = LocationBasedGenerator.LocationBasedGenerator(alphabet_size = 100, stop_prob = 0.1,gamma = gamma)
	locations = gen.locations
elif generator == "Categories":
	gen = CategoriesBasedGenerator.CategoriesBasedGenerator(alphabet_size = 100, categories_size=70, stop_prob = 0.1, alpha = 0.1)
	categories = gen.locations
	locations = gen.locations.keys()
elif generator == "CategoriesSymb":
	gen =CategoriesAndSymbolBasedGenerator.CategoriesAndSymbolBasedGenerator(alphabet_size=100, categories_size=70, stop_prob=0.1, alpha=0.1)
	categories = gen.locations
	locations = gen.locations.keys()


sequences =  gen.generate(400)
sequences = DataModUtils.removeRepetitions(sequences)

print "Nb Seqs : "+str(len(sequences))

### Get the unique list of symbols found in sequences
alphabet = SeqStats.symbols(sequences)
print "Nb Symbols : "+str(len(alphabet))

### Create Training/Testing subsets
training, test_contexts, testing = [], [], []
training, testing = DataModUtils.cutEndOfSequences(sequences, len_test)
test_contexts = training

### Set functions use to compare models
def averageProbNextKSymbols(model, test_contexts, test_seqs, k):
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

if generator == "Location":
	## Init variables of GeoFixOrderModel
	max_d = GeoFixOrderModel.getMaxDistance(locations, dist_fun)
	sum_d = GeoFixOrderModel.sumDensities(alphabet, locations, gamma, max_d, dist_fun)

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

	if generator == "Location":
		geo = GeoFixOrderModel.GeoFixOrderModel(i, alphabet, locations, gamma,
				dist_fun, max_d, sum_d,False)
		for seq in training:
			geo.learn(seq)

		geo_zp = GeoFixOrderModel.GeoFixOrderModel(i, alphabet, locations, gamma,
				dist_fun, max_d, sum_d,True)
		for seq in training:
			geo_zp.learn(seq)
	elif generator == "Categories" or generator == "CategoriesSymb":
		cat = CategoriesModel.CategoriesModel(i, alphabet, categories)
		for seq in training:
			cat.learn(seq)

		catS = CategoriesAndSymbolModel.CategoriesAndSymbolModel(i, alphabet, categories)
		for seq in training:
			catS.learn(seq)


	probs_ppmc = averageProbNextKSymbols(ppmc, test_contexts, testing, len_test)
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

	if generator == "Location":
		probs_geo = averageProbNextKSymbols(geo, test_contexts, testing, len_test)
		print str(geo)
		print "	probs : "+ SeqStats.str_probs(probs_geo)
		print "	size  : " + str(geo.size())

		probs_geo_zp = averageProbNextKSymbols(geo_zp, test_contexts, testing, len_test)
		print str(geo_zp)+' ZERO PRO'
		print "	probs : "+ SeqStats.str_probs(probs_geo_zp)
		print "	size  : " + str(geo_zp.size())

	elif generator == "Categories" or generator == "CategoriesSymb":
		probs_cat = averageProbNextKSymbols(cat, test_contexts, testing, len_test)
		print str(cat)
		print "	probs : " + SeqStats.str_probs(probs_cat)
		print "	size  : " + str(cat.size())

		probs_catS = averageProbNextKSymbols(catS, test_contexts, testing, len_test)
		print str(catS)
		print "	probs : " + SeqStats.str_probs(probs_catS)
		print "	size  : " + str(catS.size())

	print
