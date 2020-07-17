'''
Main program to run tests on geographical sequences on Lloyds_maritime data set
'''
## TODO: write specific code for import methods for each dataset

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
import LoadAirportsData

def learning(func_table, base, context_lengths, training, testing):
	'''
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
			result_func.update({'model': name, 'context': context, 'size' : model.size(),'score_1': str(round(func1 * 100., 2)), 'score_2': str(round(func2 * 100., 2))})
			result.append(result_func)
	return result


### PARAMETERS
### (Should list all variables for the experiments)
context_lengths = [1,2,3]
testing_ratio = 0.1

result = []

## for Geo models
# TODO: Use search procedure to automatically find the best gamma value
## (findBestSpreadGeo)
gamma = 0.0000001
dist_fun = GeoFixOrderModel.Dists[GeoFixOrderModel.DistCalc.HAVERSINE]

### Load Dataset
sequences = []
locations = []

sequences = LoadAirportsData.getSequences()
sequences = DataModUtils.removeRepetitions(sequences)
locations = LoadAirportsData.getLocations()
categories = LoadAirportsData.getCategories()
sequences = DataModUtils.filterSequences(sequences, categories)


print "Nb Seqs : " + str(len(sequences))

### Create Training/Testing subsets
training, test_contexts, testing = [], [], []
training, testing = DataModUtils.sampleSequences(sequences, testing_ratio)
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

## Init variables of GeoFixOrderModel
max_d = GeoFixOrderModel.getMaxDistance(locations, dist_fun)
sum_d = GeoFixOrderModel.sumDensities(alphabet, locations, gamma, max_d, dist_fun)

func_table = {
	1: (PPMCModel.PPMCModel, [alphabet], "PPMC"),
	2: (ThereAndBackModel.ThereAndBackModel, [alphabet], "There And Back"),
	3: (HONModel.HONModel, [alphabet], "HON"),
	4: (FixOrderModel.FixOrderModel, [alphabet], "Fix Order"),
	5: (CategoriesModel.CategoriesModel, [alphabet, categories], "Categories"),
	6: (CategoriesAndSymbolModel.CategoriesAndSymbolModel, [alphabet, categories], "Categories and Symbol"),
	7: (GeoFixOrderModel.GeoFixOrderModel, [alphabet, locations, gamma, dist_fun, max_d, sum_d, False],
				"GeoFix Order")
}

base = collections.OrderedDict()
base['model'] = None
base['alphabet_size'] = len(alphabet)
base['context'] = None
base['categories_size'] = len(categories)
base['gamma'] = gamma
base['size'] = None
base['score_1'] = None
base['score_2'] = None


result.append(learning(func_table, base, context_lengths, training, testing))

##Write result in a file
path_seq_file = sys.path[0] + '/RES_Airports_Model.csv'
with open(path_seq_file, 'w') as seq_file:
	csv_writer = csv.DictWriter(seq_file, base.keys())
	csv_writer.writeheader()
	for i in result:
		for j in i:
			csv_writer.writerow(j)

