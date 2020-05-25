import ReadWriteUtils
import PPMCModel
import FixOrderModel
import ShmiloviciModel
import ThereAndBackModel
import GeoFixOrderModel
import HONModel

import random

len_test = 3

file_path = "/home/queyroi-f/cs/HighOrderNetworks/data/Lloyds_maritime/apr2009_oct2009/portseq_apr2009_oct2009.csv"
# file_path = "/home/queyroi-f/cs/HighOrderNetworks/dev/VOM_algorithms/NonArithmeticPPMC/generators/test_return.csv"
place_file_path = "/home/queyroi-f/cs/HighOrderNetworks/data/Lloyds_maritime/table_places.csv"
locations = ReadWriteUtils.readLocations(place_file_path,4,6,7)

sequences = ReadWriteUtils.readFile(file_path, True, ' ')
#sequences = ReadWriteUtils.removeRepetitions(sequences)
training, testing = ReadWriteUtils.cutEachSequences(sequences, len_test)
test_contexts = training

# file_path = "/home/queyroi-f/cs/HighOrderNetworks/data/airports/2011Q1_SEQ.csv"
# sequences = ReadWriteUtils.readFile(file_path, True, ',')
#
# tsequences = []
# for s in sequences:
# 	if len(s) > 2:
# 		tsequences.append(s)
# sequences, tt =  ReadWriteUtils.sampleSequences(tsequences, 0.75)
# training, test_contexts, testing = ReadWriteUtils.sampleAndCutSequences(sequences, len_test, 0.5)

print "Nb Seqs : "+str(len(sequences))
# distr_seq = dict()
# for s in sequences:
# 	if len(s) not in distr_seq.keys():
# 		distr_seq[len(s)] = 0
# 	distr_seq[len(s)] += 1
# print "Distr : "+str(distr_seq)
#
# size_train = 0
# tot_nb_sym = 0
# for s in sequences :
# 	tot_nb_sym += len(s)
# for t in training:
# 	if len(t) > 0:
# 		size_train += 1
# print "Tot Nb Sym : " + str(tot_nb_sym)
# print "Size training : " +str(size_train)
# print "Size test_contexts : " +str(len(test_contexts))
# print "Size testing : " +str(len(testing))

alphabet = ReadWriteUtils.symbols(sequences)
print "Nb Symbols : "+str(len(alphabet))
loc_temp = dict()
for a in alphabet:
	if a in locations.keys():
		loc_temp[a] = locations[a]
locations = loc_temp
print "Nb Locations :"+str(len(locations.keys()))


# def averageProbNextKSymbols(model, test_contexts, test_seqs, k):
# 	res = [0 for i in range(k)]
# 	for i in range(len(test_seqs)):
# 		test_seq = test_seqs[i]
# 		start_i = random.randint(model.maxContextLength, len(test_seq) - k)
# 		correct_vals = test_seq[start_i:start_i+k]
# 		context = test_seq[start_i - model.maxContextLength: start_i]
# 		probs = model.probabilites(correct_vals,context)
# 		p_temp = 1.,
# 		for j in range(len(probs)):
# 			p_temp *= probs[j]
# 			res[j] += p_temp / (len(test_seqs) + 0.)
# 	return res


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

# def averageProbNextKSymbols(model, test_contexts, test_seqs, k, nb_test = 500):
# 	res = [0 for i in range(k)]
# 	order = model.maxContextLength
# 	for i in range(len(test_seqs)):
# 		correct_vals = test_seqs[i]
# 		# print str(correct_vals)
# 		for k in range(nb_test):
# 			context = test_contexts[i][:]
# 			# if len(test_contexts) > order:
# 			# 	context = test_contexts[-order:]
# 			for j in range(len(correct_vals)):
# 				rand_a = model.randomSymbol(context)
# 				# print "	-> "+ str(rand_a)
# 				if rand_a == correct_vals[j] :
# 					res[j] += 1. / (len(test_seqs) * nb_test + 0.)
# 				context = context[1:]
# 				context.append(rand_a)
# 	return res

for i in range(1,3):
	# ppmc = PPMCModel.PPMCModel(i, alphabet)
	# for seq in training:
	# 	ppmc.learn(seq)

	# tab = ThereAndBackModel.ThereAndBackModel(i, alphabet)
	# for seq in training:
	# 	tab.learn(seq)
	#
	# hon = HONModel.HONModel(i, alphabet)
	# for seq in training:
	# 	hon.learn(seq)
	# hon.prune()
	#
	fix = FixOrderModel.FixOrderModel(i, alphabet)
	for seq in training:
		fix.learn(seq)

	geo = GeoFixOrderModel.GeoFixOrderModel(i, alphabet, locations, 10000)
	for seq in training:
		geo.learn(seq)

	# probs_ppmc = averageProbNextKSymbols(ppmc, test_contexts, testing, 3)
	# print str(ppmc)
	# print "	probs : "+ ReadWriteUtils.str_probs(probs_ppmc)
	# print "	size  : " + str(ppmc.size())

	# probs_tab = averageProbNextKSymbols(tab, test_contexts, testing, len_test)
	# print str(tab)
	# print "	probs : "+ ReadWriteUtils.str_probs(probs_tab)
	# print "	size  : " + str(tab.size())
	# # print tab.print_return_probs()
	#
	probs_fix = averageProbNextKSymbols(fix, test_contexts, testing, len_test)
	print str(fix)
	print "	probs : "+ ReadWriteUtils.str_probs(probs_fix)
	print "	size  : " + str(fix.size())
	#
	#
	# probs_hon = averageProbNextKSymbols(hon, test_contexts, testing, len_test)
	# print str(hon)+" PRUNED"
	# print "	probs : "+ ReadWriteUtils.str_probs(probs_hon)
	# print "	size  : " + str(hon.size())

	probs_geo = averageProbNextKSymbols(geo, test_contexts, testing, len_test)
	print str(geo)
	print "	probs : "+ ReadWriteUtils.str_probs(probs_geo)
	print "	size  : " + str(geo.size())

	print
