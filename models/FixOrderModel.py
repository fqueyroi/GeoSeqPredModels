# -*- coding: utf-8 -*-
""" Base class for Fixed order prediction model
"""

import PredModel

class FixOrderModel(PredModel.PredModel):
	""" Model of order-k for Sequence prediction
	Count the number of occurences of sequences of
	length less than k
	"""

	def __init__(self, maxContextLength, alphabet, use_lprefix = True):
		'''
		Parameters:
		-----------
		use_lprefix: bool
			If a given context was not seen during training, use the
			longest prefix encountered instead.
			Should always be True (?) but here for testing purposes.
		'''
		super(FixOrderModel, self).__init__(maxContextLength, alphabet)
		self.use_lprefix = use_lprefix

	def __str__(self):
		return "Fixed-Order Model("+str(self.maxContextLength)+")"

	def learn(self, seq):
		super(FixOrderModel, self).learn(seq)

	def probability(self, symbol, context):
		context_node = self.tree
		if self.use_lprefix:
			context_node = self.tree.longestPrefix(context)
		else:
			if len(context) > 0 :
				len_c = min(len(context), self.maxContextLength)
				## Take the last len_c char of the given context
				ncontext = context[len(context) - len_c:]
				context_node = self.tree.getNode(ncontext)

		if context_node is not None:
			tot_count_n = context_node.totalCount() + 0.
			return context_node[symbol] / tot_count_n
			# ### ESSAI POUR EVITER ZERO Proba
			# nb_next_sym = context_node.numberNextSymbols()
			# tot_count_n = context_node.totalCount() + 0.
			# if context_node[symbol] == 0 :
			# 	return 1. / tot_sym
			# else :
			# 	return ((tot_sym - nb_next_sym) / tot_sym) * (context_node[symbol] / tot_count_n)
			###
		# return 1. / tot_sym
		return 0.

	def randomSymbol(self, context = []):
		import random
		context_node = self.tree
		if self.use_lprefix:
			context_node = self.tree.longestPrefix(context)
		else:
			if len(context) > 0 :
				len_c = min(len(context), self.maxContextLength)
				## Take the last len_c char of the given context
				ncontext = context[len(context) - len_c:]
				context_node = self.tree.getNode(ncontext)

		if context_node is not None:
			u = random.random()
			tot_count_n = context_node.totalCount() + 0.
			cum_p = 0.
			for s,c in context_node.counts.iteritems():
				cum_p += c / tot_count_n
				if cum_p >= u:
					return s
		return ''

# seq = 'abracadabra'
# alphabet = set(seq)
#
# model = FixOrderModel(3,alphabet,True)
# model.learn(seq)
#
# print seq
# print
#
# print "Tree : "
# print model.tree
#
# context = ['d','r','a']
#
# for n in alphabet:
# 	ncontext = context[:]#
# 	print n + " | " + ','.join(ncontext) + " : " + str(model.probability(n,ncontext))
