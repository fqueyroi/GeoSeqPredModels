
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
import HONModel
import CategoriesModel
import CategoriesAndSymbolModel

import EvalFunctions

sys.path.append(''.join([os.path.dirname(__file__), '/../..', '/data/generators/']))
import CategoriesAndSymbolBasedGenerator

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
			result_func.update({'model': name, 'context': context,
				'size' : model.size(),'score_1': str(round(func1 * 100., 2)),
				'score_2': str(round(func2 * 100., 2))})
			result.append(result_func)
	return result

### PARAMETERS
### (Should list all variables for the experiments)
context_lengths = [1,2,3]
# a_size = [100, 700, 2000]				#Alphabet size
# a_size = [446]						#Airports alphabet size
a_size = [3684]							#Taxis alphabet size		Memory Error
# a_size = [9230]						#Ports alphabet size
# cat_ratio = [0.01,0.1,0.3,0.6]		#Numbers of categories
# cat_ratio = [0.1]						#Airports categories
cat_ratio = [0.01]						#Taxis categories
# cat_ratio = [0.02]						#Ports categories
stop_prob = 0.1							#Probability to stop a sequence
alpha = [0.1, 0.05]						#Transitions randomness
testing_ratio = 0.1						#Sequence separation ratio
repeat = 20

result = []

values = list(itertools.product(a_size, cat_ratio,alpha))

for i in values:
	print "Alphabet size : "+ str(i[0]) + ", Categories ratio : "+ str(i[1])+ ", Alpha : "+ str(i[2])
	for j in range(repeat):
		base = collections.OrderedDict()
		base['model'] = None
		base['alphabet_size'] = i[0]
		base['nb_symbols'] = None
		base['stop_prob'] = stop_prob
		base['context'] = None
		base['cat_ratio'] = i[1]
		base['alpha'] = i[2]
		base['size']    = None
		base['score_1'] = None
		base['score_2'] = None

		## Generate datasets
		gen = CategoriesAndSymbolBasedGenerator.CategoriesAndSymbolBasedGenerator(alphabet_size=i[0], categories_size=int(round(i[1]*i[0])),
																				  stop_prob=stop_prob, alpha=i[2])
		categories = gen.locations
		locations = gen.locations.keys()
		print "Nb Cats : " + str(int(round(i[1]*i[0])))

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

		func_table = {
			1: (PPMCModel.PPMCModel, [alphabet], "PPMC"),
			2: (ThereAndBackModel.ThereAndBackModel, [alphabet], "There And Back"),
			3: (HONModel.HONModel, [alphabet], "HON"),
			4: (FixOrderModel.FixOrderModel, [alphabet], "Fix Order"),
			5: (CategoriesModel.CategoriesModel, [alphabet, categories], "Categories"),
			6: (CategoriesAndSymbolModel.CategoriesAndSymbolModel, [alphabet, categories], "Categories and Symbol")
		}

		result.append(learning(func_table, base, context_lengths, training, testing))

##Write result in a file
path_seq_file = sys.path[0] + '/RES_CatAndSymbols_Generator.csv'
with open(path_seq_file, 'w') as seq_file:
	csv_writer = csv.DictWriter(seq_file, base.keys())
	csv_writer.writeheader()
	for i in result:
		for j in i:
			csv_writer.writerow(j)




