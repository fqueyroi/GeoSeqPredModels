# -*- coding: utf-8 -*-
""" Base class for the There-and-Back model
"""

import PredModel
from collections import Counter

class ThereAndBackModel(PredModel.PredModel):


	def __init__(self, max_return, alphabet):
		"""
		Parameters:
		-----------
		max_return: int > 0
			The model will compute the probability to return to symbols from
			i-1 to i-max_return step.
		"""
		super(ThereAndBackModel, self).__init__(1, alphabet)
		self.return_counts = [] ## order - 1 -> symbol -> number of returns
		self.max_return = max_return
		for i in range(self.max_return):
			self.return_counts.append(Counter())

	def learn(self, seq):
		super(ThereAndBackModel, self).learn(seq)
		## update return probabilities
		if len(seq) > 2:
			for i in range(2,len(seq)):
				for j in range(self.max_return):
					if i - j - 2 >= 0 and seq[i - j - 2] == seq[i]:
						self.return_counts[j][seq[i - 1]] += 1

	def probability(self, symbol, context = []):
		context_node = self.tree
		if len(context) > 0 :
			context_node = self.tree.longestPrefix(context)
		if context_node is None:
			return 0.
		tot_count = context_node.totalCount() + 0.
		current_p = context_node[symbol] / tot_count
		for j in range(self.max_return):
			if len(context) <= j + 1:
				break
			prev_sym = context[- (j + 2)]
			prob_return = self.return_counts[j][context[-1]] / tot_count
			current_p = (1. - prob_return) * current_p
			if prev_sym == symbol:
				current_p += prob_return
		return current_p


	def __str__(self):
		return "ThereAndBack("+str(self.max_return)+")"

	def size(self):
		no_zero_return = 0
		for i in range(self.max_return):
			for k, c in self.return_counts[i].iteritems():
				if c > 0:
					no_zero_return += 1
		return self.tree.numberOfEntries() + no_zero_return

	def print_return_probs(self):
		for i in range(self.max_return):
			print "Back "+str(i)+ " : "
			for k, c in self.return_counts[i].iteritems():
				if c > 0:
					tot_count = self.tree.longestPrefix([k]).totalCount() + 0.
					print k + " : "+str(round(c / tot_count,2))

# sequences = [['a','b','a'],['a','b','a'],['a','b','a'],['a','b','d'],['d','b','a'],\
# 			['d','b','a'],['d','b','c'],['d','b','c'], \
# 			['c','b','c'],['c','b','c'],['c','b','c']]
# nsequences = []
# for s in sequences:
# 	ns = [s[0]]
# 	ns.append('d')
# 	ns.extend(s[1:])
# 	nsequences.append(ns)
#
# sequences = nsequences
# print sequences
# alphabet = ['a','b','c','d']
#
# tab = ThereAndBackModel(2,alphabet)
# for seq in sequences:
# 	tab.learn(seq)
#
# print tab.tree
# print tab.return_counts
# print tab.size()
#
# sum_p = 0.
# for n in alphabet:
# 	context =  ['c','c','b']
# 	p = tab.probability(n,context)
# 	sum_p += p
# 	print n + " | " + ','.join(context) + " : " + str(tab.probability(n,context))
# print "Sum = "+str(sum_p)
