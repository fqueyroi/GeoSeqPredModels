import ReadWriteUtils
import PPMCModel
import FixOrderModel
import ShmiloviciModel
import PrunePPMCModel
import HONModel
import random


file_path = "/home/queyroi-f/cs/HighOrderNetworks/data/LargeCalgaryCorpus/book1"

# sequences = ReadWriteUtils.readTextByLines(file_path)
sequence = ReadWriteUtils.readText(file_path)


# training, testing = ReadWriteUtils.cutEachSequences(sequences,3)
# # test_contexts = training
# training, test_contexts, testing = ReadWriteUtils.sampleAndCutSequences(sequences, 3, 1000)

training, testing = ReadWriteUtils.cutText(sequence, 0.5)
alphabet = ReadWriteUtils.symbols([sequence])

# alphabet = ['a','c','g','t']
# training = list(''.join(['aaacgt' for i in range(30)]))
# testing = list(''.join(['aactg' for i in range(40)]))

print "Nb Symbols : "+str(len(alphabet))
print len(training) + len(testing)

# def averageProbNextKSymbols(model, test_contexts, test_seqs, k):
# 	res = [0 for i in range(k)]
# 	order = model.maxContextLength
# 	for i in range(len(test_seqs)):
# 		train_seq = test_contexts[i]
# 		test_seq  = test_seqs[i]
# 		context = train_seq[:]
# 		if len(train_seq) > order:
# 			context = train_seq[-order:]
# 		# print "Test : "+str(test_seq)+" context : "+str(context)
# 		probs = model.probabilites(test_seq,context)
# 		# print "Probs = "+str(probs)
# 		p_temp = 1.
# 		for j in range(len(test_seq)):
# 			p_temp *= probs[j]
# 			res[j] += p_temp / (len(test_seqs) + 0.)
# 	return res

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

# def averageProbNextKSymbols(model, test_seq, k, nb_test):
# 	res = [0 for i in range(k)]
# 	for i in range(nb_test):
# 		start_i = random.randint(model.maxContextLength, len(test_seq) - k)
# 		correct_vals = test_seq[start_i:start_i+k]
# 		context = test_seq[start_i - model.maxContextLength: start_i]
# 		for j in range(len(correct_vals)):
# 			rand_a = model.randomSymbol(context)
# 			if rand_a == correct_vals[j] :
# 				res[j] += 1. / (nb_test + 0.)
# 			context = context[1:]
# 			context.append(rand_a)
# 	return res

nb_test = 1000

for i in range(1, 8):
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

	# prune = PrunePPMCModel.PrunePPMCModel(i,alphabet)
	# prune.learn(training)
	# prune.prune()

	# probs_ppmc = averageProbNextKSymbols(ppmc, testing, 3, nb_test)
	# probs_fix  = averageProbNextKSymbols(fix,  testing, 3, nb_test)
	# probs_hon  = averageProbNextKSymbols(hon,  testing, 3, nb_test)
	# probs_prune =  averageProbNextKSymbols(hon,  testing, 3, nb_test)

	logloss_ppmc = ppmc.averageLogLoss(testing,[])
	# logloss_prune = prune.averageLogLoss(testing,[])
	logloss_hon = hon.averageLogLoss(testing,[])
	logloss_fix = fix .averageLogLoss(testing,[])



	# probs_ppmc = averageProbNextKSymbols(ppmc, training, testing, 3)
	# probs_fix = averageProbNextKSymbols(fix, training, testing, 3)
	# probs_hon = averageProbNextKSymbols(hon, training, testing, 3)

	print str(ppmc)
	# print "	probs : "+ ReadWriteUtils.str_probs(probs_ppmc)
	print "	size  : " + str(ppmc.size())
	print "	logloss : "+str(logloss_ppmc)

	# print str(prune)
	# # print "	probs : "+ ReadWriteUtils.str_probs(probs_prune)
	# print "	size  : " + str(prune.size())
	# print "	logloss : "+str(logloss_prune)

	print str(fix)
	# print "	probs : "+ ReadWriteUtils.str_probs(probs_fix)
	print "	size  : " + str(fix.size())
	print "	logloss : "+str(logloss_fix)
	#
	print str(hon)+" PRUNED"
	# print "	probs : "+ ReadWriteUtils.str_probs(probs_hon)
	print "	size  : " + str(hon.size())
	print "	logloss : "+str(logloss_hon)

	print
