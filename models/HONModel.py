# -*- coding: utf-8 -*-
""" Main class for HON Model
ref:
Xu, Jian, et al.
"Detecting anomalies in sequential data with higher-order networks."
arXiv preprint arXiv:1712.09658 (2017).
"""

import PredModel
import HONSuffixTree

class HONModel(PredModel.PredModel):
	"""Main class for HON model"""

	def __init__(self, maxContextLength, alphabet):
		self.maxContextLength = maxContextLength
		self.alphabet = alphabet
		self.tree = HONSuffixTree.HONSuffixNode('', None, 0)  ## root node with dummy symbol

	def __str__(self):
		return "HON-Model("+str(self.maxContextLength)+")"

	def size(self):
		return self.tree.numberOfRules()

	def learn(self, seq):
		super(HONModel, self).learn(seq)

	def probabilityForSymbol(self, node, symbol):
		tot_count_n = node.totalCount() + 0.
		#### ESSAI POUR EVITER ZERO Proba
		# nb_next_sym = node.numberNextSymbols()
		# tot_sym = len(self.alphabet) + 0.
		# if node[symbol] == 0 :
		# 	return 1. / tot_sym
		# else :
		# 	return ((tot_sym - nb_next_sym) / tot_sym) * (node[symbol] / tot_count_n)
		####
		return node[symbol] / tot_count_n

	def divergence(self, node, suffix_node):
		import math
		if node.depth == 0:
			return node.depth + 1.
		res = 0.
		for k in node.counts.keys():
			p_k_n = self.probabilityForSymbol(node, k)
			p_k_p = self.probabilityForSymbol(suffix_node, k)
			if p_k_n > 0:
				res += p_k_n * math.log(p_k_n / p_k_p, 2)
		return res

	def divergenceThreshold(self, node):
		import math
		tot_count_n = node.totalCount() + 0.
		return node.depth / math.log(tot_count_n + 1., 2)

	def prune(self):
		self.tree.is_rule = True
		for k, c in self.tree.children.iteritems():
			c.is_rule = True
			self.recurPruning(c, c)

	def setAllRules(self, node, value = True):
		node.is_rule = value
		for k, c in node.children.iteritems():
			self.setAllRules(c,value)

	def recurPruning(self, valid, current):
		if current.numberChildren() == 0:
			# valid.is_rule = True
			### TEST ADD REWIRING RULES
			self.setValid(valid)
			return

		for k, c in current.children.iteritems():
			# print "N : (" + ' '.join(c.getSymbolPath()) + ') d = ' + \
				# str( self.divergence(c, current)) + ' thres = ' + str(self.divergenceThreshold(c))
			div = self.divergence(c, current)
			if div > self.divergenceThreshold(c):
				self.recurPruning(c, c)
			else:
				self.recurPruning(valid, c)

	def setValid(self, node):
		node.is_rule = True
		if node.depth > 1:
			path = node.getSymbolPath()
			# print "Set valid path : " + ''.join(path[:-1])
			prev_node = node.getRoot().getNode(path[:-1])
			self.setValid(prev_node)

	def probability(self, symbol, context):
		context_node = self.tree
		ncontext = context
		## Find the largest existing prefix of ncontext in the trie
		if len(context) > 0 :
			len_c = min(len(context), self.maxContextLength)
			## Take the last len_c char of the given context
			ncontext = context[len(context) - len_c:]
			context_node = self.tree.longestPrefix(ncontext)

		# print "Probabiblity of '" + symbol + "' context : "+ str(ncontext)
		# print "Context node : " + str(context_node.getSymbolPath())
		return self.probabilityForSymbol(context_node, symbol)

	def randomSymbol(self, context = []):
		import random
		context_node = self.tree
		ncontext = context
		## Find the largest existing prefix of ncontext in the trie
		if len(context) > 0 :
			len_c = min(len(context), self.maxContextLength)
			## Take the last len_c char of the given context
			ncontext = context[len(context) - len_c:]
			context_node = self.tree.longestPrefix(ncontext)

		u = random.random()
		tot_count_n = context_node.totalCount() + 0.
		cum_p = 0.
		for s,c in context_node.counts.iteritems():
			cum_p += c / tot_count_n
			if cum_p >= u:
				return s



# seq = 'abracadabra'
# alphabet = ['a','b','r','c','d']
# model = HONModel(2,alphabet)
# model.learn(seq)
# model.prune()
#
# context = ['r','a']
#
# print model.tree
#
# for n in alphabet:
# 	ncontext = context[:]#
# 	print n + " | " + ','.join(ncontext) + " : " + str(model.probability(n,ncontext))
