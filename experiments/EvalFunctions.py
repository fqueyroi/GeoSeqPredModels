'''
Contains procedures used to test the prediction models
'''
## TODO: Create one using the distance between prediction and real location
## TODO: Use these function in experiments scripts

import random
################################################################################
def averageProbNextSymbol(model, test_seqs):
	'''
	Return the average probability to correctly predicting the next symbol
	starting at a random point in each test sequence using the previous
	symbols as context.
	Return:
	-------
		res: float
	'''
	res = 0.
	order = model.maxContextLength
	for i in range(len(test_seqs)):
		seq = test_seqs[i]
		if len(seq)>=2:
			symbol = seq[-1]
			context = seq[:-1]
			if order >= len(seq):
				t_seq = random.randint(order,len(seq)-1)
				symbol = seq[t_seq]
				context = seq[:t_seq]
			prob = model.probability(symbol,context)
			res += prob / (len(test_seqs) + 0.)
	return res

################################################################################
def averageProbAllSymbols(model, test_seqs):
	'''
	Return the average probability to correctly predicting the all symbols
	in each test sequence
	Return:
	-------
		res: float
	'''
	res = 0.
	order = model.maxContextLength
	for i in range(len(test_seqs)):
		seq = test_seqs[i]
		for j in range(len(seq)):
			context = []
			if j > 1:
				context = seq[:j]
			prob = model.probability(seq[j],context)
			res += prob / (len(seq) + 0.)
	return res / (len(test_seqs) + 0.)


################################################################################
def averageProbNextKSymbols(model, test_contexts, test_seqs, k):
	'''
	Return the average probabilities to correctly predicting the first k symbols
	of each test sequence using the corresponding test_contexts' sequence
	as context.
	Return:
	-------
		res: list of k float
	'''
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
