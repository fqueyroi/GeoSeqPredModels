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

	def __init__(self, maxContextLength, alphabet, use_lprefix = True, valid_prefix = False):
		'''
		Parameters:
		-----------
		use_lprefix: bool
			If a given context was not seen during training, use the
			longest prefix encountered instead.
			Should always be True (?) but here for testing purposes.
		valid_prefix: bool
			Whether or not prefixes of a valid node should be valid
			If True, the valid nodes correspond to the final rules
			after network rewiring in Xu et al. (2017)
		'''
		self.maxContextLength = maxContextLength
		self.alphabet = alphabet
		self.tree = HONSuffixTree.HONSuffixNode('', None, 0)  ## root node
		self.use_lprefix = use_lprefix
		self.valid_prefix = valid_prefix

	def __str__(self):
		return "HON-Model("+str(self.maxContextLength)+")"

	def size(self):
		return self.tree.numberOfEntries()

	def learn(self, seq):
		super(HONModel, self).learn(seq)

	def probabilityForSymbol(self, node, symbol):
		tot_count_n = node.totalCount() + 0.
		return node[symbol] / tot_count_n

	def divergence(self, node, suffix_node):
		'''
		Compute the KL-divergence between the distribution of
		node.counts and suffix_node.counts where suffix_node
		is a suffix (parent) of node i.e. the similarity between the
		distribution
		'''
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
		'''
		Compute the threshold for the divergence with next-symbol distribution
		of 'node'
		'''
		import math
		tot_count_n = node.totalCount() + 0.
		return node.depth / math.log(tot_count_n + 1., 2)

	def prune(self):
		'''
		Filter the nodes in the suffix tree that are redundant i.e. there have
		suffix node with a similar distribution.
		'''
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
			if self.valid_prefix:
				self.setValid(valid)
			else:
				valid.is_rule = True
			return

		for k, c in current.children.iteritems():
			div = self.divergence(c, current)
			if div > self.divergenceThreshold(c):
				self.recurPruning(c, c)
			else:
				self.recurPruning(valid, c)

	def setValid(self, node):
		node.is_rule = True
		if node.depth > 1:
			path = node.getSymbolPath()
			prev_node = node.getRoot().getNode(path[:-1])
			self.setValid(prev_node)

	def probability(self, symbol, context):
		context_node = self.tree
		## TODO: test the effect of use_lprefix
		if self.use_lprefix:
			context_node = self.tree.longestPrefix(context)
		else:
			if len(context) > 0 :
				len_c = min(len(context), self.maxContextLength)
				## Take the last len_c char of the given context
				ncontext = context[len(context) - len_c:]
				context_node = self.tree.getNode(ncontext)

		if context_node is not None:
			return self.probabilityForSymbol(context_node, symbol)
		else:
			## TODO: For consistency (sum prob = 1) maybe we should
			## add uniform probability on alphabet if the context was never seen ?
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
# alphabet = ['a','b','r','c','d']
#
# model = HONModel(3,alphabet,True,False)
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
