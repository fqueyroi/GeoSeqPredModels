
import sys, os
import itertools
import collections
sys.path.append(''.join([os.path.dirname(__file__), '/..']))
import DataModUtils
import SeqStats
import csv

sys.path.append(''.join([os.path.dirname(__file__), '/../..', '/models/']))
import PPMCModel
import FixOrderModel
import ThereAndBackModel
import GeoFixOrderModel
import HONModel
import EvalFunctions

sys.path.append(''.join([os.path.dirname(__file__), '/../..', '/data/generators/']))
import LocationBasedGenerator


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

			# print str(model)
			# print "	probs averageProbNextSymbol: " + str(round(func1 * 100., 2))
			# print "	probs averageProbAllSymbols: " + str(round(func2 * 100., 2))

			result_func = base.copy()
			result_func.update({'model': name, 'context': context, 'size' : model.size(), 'score_1': str(round(func1 * 100., 2)), 'score_2': str(round(func2 * 100., 2))})
			result.append(result_func)
	return result


### PARAMETERS
### (Should list all variables for the experiments)
context_lengths = [1,2]
# a_size = [100, 700, 2000]					#Alphabet size
# a_size = [446]							#Airports alphabet size
a_size = [3684]								#Taxis alphabet size
# a_size = [9230]							#Ports alphabet size
gamma = [10**(-i) for i in range(4)]		#Preference for far locations
stop_prob = 0.1								#Probability to stop a sequence
testing_ratio = 0.1							#Sequence separation ratio
repeat = 20

result = []

values = list(itertools.product(a_size, gamma))

for i in values:
	print "Alphabet size : "+ str(i[0]) + ", Gamma : "+ str(i[1])
	for j in range(repeat):
		base = collections.OrderedDict()
		base['model'] = None
		base['alphabet_size'] = i[0]
		base['nb_symbols'] = None
		base['stop_prob'] = stop_prob
		base['gamma'] = i[1]
		base['size']    = None
		base['context'] = None
		base['score_1'] = None
		base['score_2'] = None

		## Generate datasets
		dist_fun = GeoFixOrderModel.Dists[GeoFixOrderModel.DistCalc.EUCLIDIAN]
		gen = LocationBasedGenerator.LocationBasedGenerator(alphabet_size=i[0], stop_prob=stop_prob, gamma=i[1])
		locations = gen.locations

		# sequences = gen.generate(1000)
		# sequences = gen.generate(2751486)			#Airports
		sequences = gen.generate(4297)  			#Taxis
		# sequences = gen.generate(4298)			#Ports

		sequences = DataModUtils.removeRepetitions(sequences)

		# print "Nb Seqs : " + str(len(sequences))

		### Get the unique list of symbols found in sequences
		alphabet = SeqStats.symbols(sequences)
		# print "Nb Symbols : " + str(len(alphabet))
		base.update({'nb_symbols': len(alphabet)})

		### Create Training/Testing subsets
		training, test_contexts, testing = [], [], []
		training, testing = DataModUtils.sampleSequences(sequences, testing_ratio)
		test_contexts = training

		max_d = GeoFixOrderModel.getMaxDistance(locations, dist_fun)
		sum_d = GeoFixOrderModel.sumDensities(alphabet, locations, i[1], max_d, dist_fun)

		func_table = {
			1: (PPMCModel.PPMCModel, [alphabet], "PPMC"),
			2: (ThereAndBackModel.ThereAndBackModel, [alphabet], "There And Back"),
			3: (HONModel.HONModel, [alphabet], "HON"),
			4: (FixOrderModel.FixOrderModel, [alphabet], "Fix Order"),
			5: (GeoFixOrderModel.GeoFixOrderModel, [alphabet, locations, i[1], dist_fun, max_d, sum_d, False],
					"GeoFix Order")
		}

		result.append(learning(func_table, base, context_lengths, training, testing))



##Write result in a file
path_seq_file = sys.path[0] + '/RES_Location_Generator.csv'
with open(path_seq_file, 'w') as seq_file:
	csv_writer = csv.DictWriter(seq_file, base.keys())
	csv_writer.writeheader()
	for i in result:
		for j in i:
			csv_writer.writerow(j)




