#### NOT WORKING ATM
## TODO Fix the tests for Text datasets

import random
import sys, os
sys.path.append(''.join([os.path.dirname(__file__), '/..', '/models/']))

import PPMCModel
import FixOrderModel
import HONModel

import ReadWriteUtils

file_path = ''.join([os.path.dirname(__file__), '/..', '/data/LargeCalgaryCorpus/book1'])

# sequences = ReadWriteUtils.readTextByLines(file_path)
sequence = ReadWriteUtils.readText(file_path)

training, testing = ReadWriteUtils.cutText(sequence, 0.5)
alphabet = ReadWriteUtils.symbols([sequence])

print "Nb Symbols : "+str(len(alphabet))
print len(training) + len(testing)

def averageProbNextKSymbols(model, test_seq, k, nb_test):
	res = [0 for i in range(k)]
	for i in range(nb_test):
		start_i = random.randint(model.maxContextLength, len(test_seq) - k)
		correct_vals = test_seq[start_i:start_i+k]
		context = test_seq[start_i - model.maxContextLength: start_i]
		probs = model.probabilites(correct_vals,context)
		p_temp = 1.
		for j in range(len(probs)):
			p_temp *= probs[j]
			res[j] += p_temp / (nb_test + 0.)
	return res

nb_test = 100

for i in range(1, 6):
	ppmc = PPMCModel.PPMCModel(i, alphabet)
	#for seq in training:
	ppmc.learn(training)

	hon = HONModel.HONModel(i, alphabet)
	# for seq in training:
	hon.learn(training)
	hon.prune()

	fix = FixOrderModel.FixOrderModel(i, alphabet)
	# for seq in training:
	fix.learn(training)


	probs_ppmc = averageProbNextKSymbols(ppmc, testing, 3, nb_test)
	probs_fix  = averageProbNextKSymbols(fix,  testing, 3, nb_test)
	probs_hon  = averageProbNextKSymbols(hon,  testing, 3, nb_test)

	logloss_ppmc = ppmc.averageLogLoss(testing,[])
	# logloss_hon = hon.averageLogLoss(testing,[])
	# logloss_fix = fix .averageLogLoss(testing,[])

	print str(ppmc)
	print "	probs : "+ ReadWriteUtils.str_probs(probs_ppmc)
	print "	size  : " + str(ppmc.size())
	print "	logloss : "+str(logloss_ppmc)

	print str(fix)
	print "	probs : "+ ReadWriteUtils.str_probs(probs_fix)
	print "	size  : " + str(fix.size())
	# print "	logloss : "+str(logloss_fix)

	print str(hon)+" PRUNED"
	print "	probs : "+ ReadWriteUtils.str_probs(probs_hon)
	print "	size  : " + str(hon.size())
	# print "	logloss : "+str(logloss_hon)

	print
