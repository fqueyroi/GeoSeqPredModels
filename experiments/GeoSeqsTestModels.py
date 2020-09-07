'''
Main program to run tests on geographical sequences
'''
import sys, os
import csv
import collections

import DataModUtils
import SeqStats
import EvalFunctions

sys.path.append(''.join([os.path.dirname(__file__), '/..', '/models/']))

import PPMCModel
import FixOrderModel
import ThereAndBackModel
import GeoFixOrderModel
import CategoriesModel
import HONModel
import CategoriesAndSymbolModel

sys.path.append(''.join([os.path.dirname(__file__), '/..', '/data/']))
import LoadLlyodsData
import LoadAirportsData
import LoadPortoTaxisData

#########################################
#########################################
## Define the dataset for the experiments
# dataset = "Maritime"
dataset = "Taxis"
# dataset = "Airports"
#########################################
#########################################

def eval_models(func_table, base, context_lengths, training, testing):
	'''
	Evaluate models described in 'func_table' on the given
	training and testing set for the given context_lengths
	adding the results to the information in 'base'

	Parameters:
	-----------
	func_table:
		table with the models
	base:
		dictionary with all test informations by model

	:return: completed dictionary
	'''
	result = []

	for k, v in func_table.iteritems():
		##Get informations and train each model
		func, args, name = func_table[k]
		for context in context_lengths:
			model = func(context, *args)
			for seq in training:
				model.learn(seq)
			if name == "HON":
				model.prune()

			func1 = EvalFunctions.averageProbNextSymbol(model, testing)
			func2 = EvalFunctions.averageProbAllSymbols(model, testing)

			print str(model)
			print "	probs averageProbNextSymbol: " + str(round(func1 * 100., 2))
			print "	probs averageProbAllSymbols: " + str(round(func2 * 100., 2))

			result_func = base.copy()
			result_func.update({'model': name, 'context': context,
				'size' : model.size(), 'score_next': str(round(func1 * 100., 2)),
				'score_all': str(round(func2 * 100., 2))})
			result.append(result_func)
	return result

### PARAMETERS
### (Should list all variables for the experiments)
context_lengths = [1,2,3]
testing_ratio = 0.1

### Load Dataset
sequences = []
locations = {}
categories = {}

if dataset == "Airports" :
	sequences  = LoadAirportsData.getSequences()
	locations  = LoadAirportsData.getLocations()
	categories = LoadAirportsData.getCategories()
if dataset == "Taxis" :
	sequences  = LoadPortoTaxisData.getSequences()
	locations  = LoadPortoTaxisData.getLocations()
	categories = LoadPortoTaxisData.getCategories()
if dataset == "Maritime" :
	sequences  = LoadLlyodsData.getSequences()
	locations  = LoadLlyodsData.getLocations()
	categories = LoadLlyodsData.getCategories()

sequences = DataModUtils.removeRepetitions(sequences)
sequences = DataModUtils.filterSequences(sequences, categories)

print "Nb Seqs : " + str(len(sequences))

### Create Training/Testing subsets
training, testing = [], []
training, testing = DataModUtils.sampleSequences(sequences, testing_ratio)

### Get the unique list of symbols found in sequences
alphabet = SeqStats.symbols(sequences)
alphabet = DataModUtils.filterAlphabet(alphabet, categories)
print "Nb Symbols : " + str(len(alphabet))
nb_cat = len(set(categories.values()))
print "Nb Categories : " + str(nb_cat)

### Filter locations (to match alphabet)
loc_temp = dict()
for a in alphabet:
	if a in locations.keys():
		loc_temp[a] = locations[a]
locations = loc_temp
print "Nb Locations :" + str(len(locations.keys()))

base = collections.OrderedDict()
base['model'] = None
base['alphabet_size'] = len(alphabet)
base['context'] = None
base['categories_size'] = nb_cat
base['gamma'] = None
base['size'] = None
base['score_next'] = None
base['score_all'] = None

## Run the experiments on the various models
result = []

func_table = {
	1: (ThereAndBackModel.ThereAndBackModel, [alphabet], "There And Back"),
}
result.append(eval_models(func_table, base, [1], training, testing))

func_table = {
	1: (PPMCModel.PPMCModel, [alphabet], "PPMC"),
	2: (HONModel.HONModel, [alphabet], "HON"),
	3: (FixOrderModel.FixOrderModel, [alphabet], "Fix Order"),
	4: (CategoriesModel.CategoriesModel, [alphabet, categories], "Categories"),
	5: (CategoriesAndSymbolModel.CategoriesAndSymbolModel, [alphabet, categories], "Categories and Symbol")
}
result.append(eval_models(func_table, base, context_lengths, training, testing))

## for Geo models
# TODO: Use search procedure to automatically find the best gamma value
gammas = [10**(-i) for i in range(6,11)]		#Preference for close locations

## Init variables of GeoFixOrderModel
dist_fun = GeoFixOrderModel.Dists[GeoFixOrderModel.DistCalc.HAVERSINE]
max_d = GeoFixOrderModel.getMaxDistance(locations, dist_fun)

for g in gammas:
	base['gamma'] = g
	sum_d = GeoFixOrderModel.sumDensities(alphabet, locations, g, max_d, dist_fun)
	func_table = {
		7: (GeoFixOrderModel.GeoFixOrderModel,
		[alphabet, locations, g, dist_fun, max_d, sum_d, False],
		"GeoFix Order")
	}
	result.append(eval_models(func_table, base, context_lengths, training, testing))

##Write result in a file
path_seq_file = sys.path[0] + '/RES_'+dataset+'.csv'
with open(path_seq_file, 'w') as seq_file:
	csv_writer = csv.DictWriter(seq_file, base.keys())
	csv_writer.writeheader()
	for i in result:
		for j in i:
			csv_writer.writerow(j)
