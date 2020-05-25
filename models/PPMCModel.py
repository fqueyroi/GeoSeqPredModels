# -*- coding: utf-8 -*-
""" Main class for PPM-C Model
see https://github.com/bob-carpenter/java-arithcode
"""

import PredModel

class PPMCModel(PredModel.PredModel):
	"""Main class for PPM-C."""

	def __init__(self, maxContextLength, alphabet):
		super(PPMCModel, self).__init__(maxContextLength, alphabet)
		self.nbOfSymbols = len(alphabet)

	def __str__(self):
		return "PPMC-Model("+str(self.maxContextLength)+")"

	def learn(self, seq):
		super(PPMCModel, self).learn(seq)

	def probability(self, symbol, context):
		## Get the longest prefix in the suffix tree
		## that we encountered in learning
		context_node = self.tree.longestPrefix(context)

		## Start computing probability estimate
		excluded = []
		escaped = True
		prob = 1.

		## Recursive computation of probability estimate
		while escaped :
			count_sym = context_node[symbol]
			tot_count = context_node.totalCount(excluded)
			nb_next_sym = context_node.numberNextSymbols()

			if nb_next_sym == 0:
				## The path was never followed by another symbol in the
				## training. The escaped probability should be 1 (to check)
				escaped = True
				continue

			if count_sym > 0 :
				## The symbol was found after the current path therefore
				## the 'non-escaped' probability is computed
				escaped = False;
				prob *= count_sym / (tot_count + nb_next_sym)
			else:
				## The symbol was not found after the current path therefore
				## the 'non-escaped' probability is computed
				escaped = True
				if context_node.depth == 0:
					## means the symbol was never seen during the training
					## the default probability is uniform among the number of
					## possible symbol not already excluded
					# print "	Not escaped Not found : " + str(1. / (self.nbOfSymbols - len(excluded)))
					escaped = False
					prob *= 1. / (self.nbOfSymbols - len(excluded))
				else :
					## the symbol was never seen after the sequence
					## given by context_node therefore the escaped probability
					## is computed
					prob *=  nb_next_sym / (tot_count + nb_next_sym)

				## Include possible existing symbols in the excluded list
				for k in context_node.counts.keys():
					if k not in excluded:
						excluded.append(k)

			## If escaped we reduced the context by removing the first symbol
			## i.e. we take the parent of the current context_node as
			## the new context_node
			context_node = context_node.parent

		return prob

# seq = 'abracadabra'
# alphabet = ['a','b','r','c','d']
# model = PPMCModel(2,alphabet)
# model.learn(seq)
#
# print model.tree
#
# context = ['r','a']
# for n in alphabet:
# 	ncontext = context[:]#
# 	print n + " | " + ','.join(ncontext) + " : " + str(model.probability(n,ncontext))
